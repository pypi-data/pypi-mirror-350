#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
服务端模块 - 提供Web API和管理界面
"""

import os
import click
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from .models import db, Program, Instance, init_db


def create_app(database_url=None):
    """创建Flask应用"""
    app = Flask(__name__)

    # 配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or os.environ.get(
        'DATABASE_URL', 'sqlite:///instancer.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    init_db(app)

    # API路由
    @app.route('/api/instances/register', methods=['POST'])
    def register_instance():
        """注册实例"""
        data = request.get_json()
        program_id = data.get('program_id')
        instance_id = data.get('instance_id')
        process_id = data.get('process_id')
        hostname = data.get('hostname')

        if not all([program_id, instance_id, process_id]):
            return jsonify({'error': '缺少必要参数'}), 400

        # 检查程序是否存在且启用
        program = Program.query.filter_by(program_id=program_id).first()
        if not program:
            return jsonify({
                'allowed': False,
                'message': f'程序 {program_id} 未配置'
            })

        if not program.enabled:
            return jsonify({
                'allowed': False,
                'message': f'程序 {program_id} 已被禁用'
            })

        # 先清理过期实例（超过30秒没有心跳的实例）
        timeout = datetime.utcnow() - timedelta(seconds=30)
        expired_instances = Instance.query.filter(
            Instance.program_id == program_id,
            Instance.last_heartbeat < timeout,
            Instance.status == 'running'
        ).update({'status': 'timeout'})

        if expired_instances > 0:
            db.session.commit()
            print(f"🧹 清理了 {expired_instances} 个过期实例 (程序: {program_id})")

        # 检查当前活跃实例数量限制
        current_instances = Instance.query.filter_by(
            program_id=program_id,
            status='running'
        ).count()

        if current_instances >= program.max_instances:
            return jsonify({
                'allowed': False,
                'message': f'程序 {program_id} 已达到最大实例数量限制 ({program.max_instances})'
            })

        # 创建实例记录
        instance = Instance(
            instance_id=instance_id,
            program_id=program_id,
            process_id=process_id,
            hostname=hostname,
            status='running'
        )

        try:
            db.session.add(instance)
            db.session.commit()

            return jsonify({
                'allowed': True,
                'message': '实例注册成功'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'注册失败: {str(e)}'}), 500

    @app.route('/api/instances/unregister', methods=['POST'])
    def unregister_instance():
        """注销实例"""
        data = request.get_json()
        instance_id = data.get('instance_id')

        if not instance_id:
            return jsonify({'error': '缺少实例ID'}), 400

        instance = Instance.query.filter_by(instance_id=instance_id).first()
        if instance:
            instance.status = 'stopped'
            db.session.commit()

        return jsonify({'message': '实例注销成功'})

    @app.route('/api/instances/status', methods=['GET'])
    def check_instance_status():
        """检查实例状态"""
        program_id = request.args.get('program_id')
        instance_id = request.args.get('instance_id')

        if not all([program_id, instance_id]):
            return jsonify({'error': '缺少必要参数'}), 400

        # 定期清理过期实例（每次状态检查时）
        timeout = datetime.utcnow() - timedelta(seconds=30)
        expired_count = Instance.query.filter(
            Instance.last_heartbeat < timeout,
            Instance.status == 'running'
        ).update({'status': 'timeout'})

        if expired_count > 0:
            db.session.commit()
            print(f"🧹 状态检查时清理了 {expired_count} 个过期实例")

        # 检查程序是否启用
        program = Program.query.filter_by(program_id=program_id).first()
        if not program or not program.enabled:
            return jsonify({'allowed': False})

        # 更新实例心跳
        instance = Instance.query.filter_by(instance_id=instance_id).first()
        if instance:
            instance.update_heartbeat()

        return jsonify({'allowed': True})

    # Web界面路由
    @app.route('/')
    def index():
        """主页"""
        programs = Program.query.all()
        return render_template('index.html', programs=programs)

    @app.route('/programs/add', methods=['GET', 'POST'])
    def add_program():
        """添加程序"""
        if request.method == 'POST':
            program_id = request.form.get('program_id')
            name = request.form.get('name')
            description = request.form.get('description', '')
            max_instances = int(request.form.get('max_instances', 1))

            if not all([program_id, name]):
                flash('程序ID和名称不能为空', 'error')
                return render_template('add_program.html')

            # 检查程序ID是否已存在
            if Program.query.filter_by(program_id=program_id).first():
                flash(f'程序ID {program_id} 已存在', 'error')
                return render_template('add_program.html')

            program = Program(
                program_id=program_id,
                name=name,
                description=description,
                max_instances=max_instances
            )

            try:
                db.session.add(program)
                db.session.commit()
                flash(f'程序 {program_id} 添加成功', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'添加失败: {str(e)}', 'error')

        return render_template('add_program.html')

    @app.route('/programs/<program_id>/toggle', methods=['POST'])
    def toggle_program(program_id):
        """切换程序启用状态"""
        program = Program.query.filter_by(program_id=program_id).first_or_404()
        program.enabled = not program.enabled

        if not program.enabled:
            # 如果禁用程序，标记所有运行中的实例为终止状态
            Instance.query.filter_by(
                program_id=program_id,
                status='running'
            ).update({'status': 'terminated'})

        db.session.commit()

        status = '启用' if program.enabled else '禁用'
        flash(f'程序 {program_id} 已{status}', 'success')
        return redirect(url_for('index'))

    @app.route('/programs/<program_id>/update_instances', methods=['POST'])
    def update_max_instances(program_id):
        """更新最大实例数"""
        program = Program.query.filter_by(program_id=program_id).first_or_404()
        max_instances = int(request.form.get('max_instances', 1))

        program.max_instances = max_instances
        db.session.commit()

        flash(f'程序 {program_id} 最大实例数已更新为 {max_instances}', 'success')
        return redirect(url_for('index'))

    @app.route('/programs/<program_id>/delete', methods=['POST'])
    def delete_program(program_id):
        """删除程序"""
        program = Program.query.filter_by(program_id=program_id).first_or_404()

        # 删除程序及其所有实例记录
        db.session.delete(program)
        db.session.commit()

        return jsonify({'message': f'程序 {program_id} 已删除'})

    @app.route('/api/programs', methods=['GET'])
    def get_programs():
        """获取所有程序"""
        programs = Program.query.all()
        return jsonify([program.to_dict() for program in programs])

    @app.route('/api/instances', methods=['GET'])
    def get_instances():
        """获取所有实例"""
        # 清理过期实例（超过30秒没有心跳的实例）
        timeout = datetime.utcnow() - timedelta(seconds=30)
        Instance.query.filter(
            Instance.last_heartbeat < timeout,
            Instance.status == 'running'
        ).update({'status': 'timeout'})
        db.session.commit()

        # 只返回运行中的实例
        instances = Instance.query.filter_by(status='running').all()
        return jsonify([instance.to_dict() for instance in instances])

    @app.route('/api/instances/cleanup', methods=['POST'])
    def cleanup_instances():
        """手动清理过期实例"""
        timeout = datetime.utcnow() - timedelta(seconds=30)

        # 清理超时实例
        timeout_count = Instance.query.filter(
            Instance.last_heartbeat < timeout,
            Instance.status == 'running'
        ).update({'status': 'timeout'})

        # 删除已停止的实例记录（可选，保留历史记录）
        # deleted_count = Instance.query.filter(
        #     Instance.status.in_(['stopped', 'timeout', 'terminated'])
        # ).delete()

        db.session.commit()

        return jsonify({
            'message': f'清理完成，标记了 {timeout_count} 个超时实例',
            'timeout_instances': timeout_count
        })

    return app


@click.command()
@click.option('--host', default='127.0.0.1', help='服务绑定地址')
@click.option('--port', default=5000, help='服务端口')
@click.option('--debug', is_flag=True, help='调试模式')
@click.option('--database-url', help='数据库连接字符串')
def main(host, port, debug, database_url):
    """启动Instancer服务端"""
    app = create_app(database_url)

    print(f"🚀 Instancer服务端启动中...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"🎛️  管理界面: http://{host}:{port}")

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
