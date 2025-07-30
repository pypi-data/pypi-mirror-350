#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据模型 - 定义数据库表结构
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Program(db.Model):
    """程序配置表"""
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    max_instances = db.Column(db.Integer, default=1, nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联实例
    instances = db.relationship('Instance', backref='program', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Program {self.program_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'program_id': self.program_id,
            'name': self.name,
            'description': self.description,
            'max_instances': self.max_instances,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'current_instances': self.instances.filter_by(status='running').count()
        }


class Instance(db.Model):
    """实例表"""
    __tablename__ = 'instances'
    
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    program_id = db.Column(db.String(100), db.ForeignKey('programs.program_id'), nullable=False)
    process_id = db.Column(db.Integer, nullable=False)
    hostname = db.Column(db.String(200))
    status = db.Column(db.String(20), default='running', nullable=False)  # running, stopped, terminated
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_heartbeat = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Instance {self.instance_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'instance_id': self.instance_id,
            'program_id': self.program_id,
            'process_id': self.process_id,
            'hostname': self.hostname,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None
        }
    
    def update_heartbeat(self):
        """更新心跳时间"""
        self.last_heartbeat = datetime.utcnow()
        db.session.commit()


def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 创建默认程序配置（如果不存在）
        if not Program.query.filter_by(program_id='demo').first():
            demo_program = Program(
                program_id='demo',
                name='演示程序',
                description='这是一个演示程序配置',
                max_instances=1,
                enabled=True
            )
            db.session.add(demo_program)
            db.session.commit()
            print("✅ 创建了默认演示程序配置")
