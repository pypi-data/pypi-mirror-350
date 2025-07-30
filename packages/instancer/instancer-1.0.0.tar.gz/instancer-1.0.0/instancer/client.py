#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
客户端模块 - 提供装饰器和实例控制功能
"""

import os
import sys
import time
import uuid
import threading
import signal
import requests
import psutil
from functools import wraps
from typing import Callable, Optional


class InstanceController:
    """实例控制器"""

    def __init__(self, program_id: str, server_url: str, check_interval: int = 5):
        self.program_id = program_id
        self.server_url = server_url.rstrip('/')
        self.check_interval = check_interval
        self.instance_id = str(uuid.uuid4())
        self.process_id = os.getpid()
        self.is_running = False
        self.check_thread = None
        self.force_exit_requested = False

    def register_instance(self) -> bool:
        """注册实例到服务端"""
        try:
            response = requests.post(
                f"{self.server_url}/api/instances/register",
                json={
                    "program_id": self.program_id,
                    "instance_id": self.instance_id,
                    "process_id": self.process_id,
                    "hostname": os.uname().nodename if hasattr(os, 'uname') else 'unknown'
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("allowed"):
                    print(f"✅ 实例注册成功: {self.program_id} ({self.instance_id})")
                    return True
                else:
                    print(f"❌ 实例注册被拒绝: {result.get('message', '未知原因')}")
                    return False
            else:
                print(f"❌ 注册失败: HTTP {response.status_code}")
                return False

        except requests.RequestException as e:
            print(f"❌ 连接服务端失败: {e}")
            return False

    def unregister_instance(self):
        """注销实例"""
        try:
            requests.post(
                f"{self.server_url}/api/instances/unregister",
                json={
                    "program_id": self.program_id,
                    "instance_id": self.instance_id
                },
                timeout=5
            )
        except requests.RequestException:
            pass  # 忽略注销时的网络错误

    def check_status(self):
        """检查实例状态"""
        while self.is_running:
            try:
                response = requests.get(
                    f"{self.server_url}/api/instances/status",
                    params={
                        "program_id": self.program_id,
                        "instance_id": self.instance_id
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    result = response.json()
                    if not result.get("allowed"):
                        print(f"⚠️  程序已被禁用，正在退出...")
                        self.force_exit_requested = True
                        self.force_exit()
                        break
                else:
                    print(f"⚠️  状态检查失败: HTTP {response.status_code}")

            except requests.RequestException as e:
                print(f"⚠️  状态检查网络错误: {e}")

            time.sleep(self.check_interval)

    def start_monitoring(self):
        """开始监控"""
        self.is_running = True
        self.check_thread = threading.Thread(target=self.check_status, daemon=True)
        self.check_thread.start()

    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        if self.check_thread and self.check_thread.is_alive():
            self.check_thread.join(timeout=1)

    def force_exit(self):
        """强制退出程序"""
        print(f"🚫 程序 {self.program_id} 被强制退出")
        self.force_exit_requested = True

        # 先注销实例
        self.unregister_instance()

        # 停止监控（但不等待当前线程）
        self.is_running = False

        # 使用定时器延迟强制退出，避免线程问题
        def delayed_exit():
            time.sleep(0.1)  # 短暂延迟让当前函数返回
            # 在Windows上使用不同的方法
            if os.name == 'nt':  # Windows
                try:
                    current_process = psutil.Process(self.process_id)
                    current_process.terminate()
                    time.sleep(0.5)
                    if current_process.is_running():
                        current_process.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            else:  # Unix/Linux
                try:
                    os.kill(self.process_id, signal.SIGTERM)
                except OSError:
                    pass

            # 最终强制退出
            os._exit(1)

        # 在新线程中执行强制退出
        exit_thread = threading.Thread(target=delayed_exit, daemon=True)
        exit_thread.start()


def instance_control(program_id: str, server_url: str, check_interval: int = 5):
    """
    实例控制装饰器

    Args:
        program_id: 程序唯一标识符
        server_url: 服务端地址
        check_interval: 状态检查间隔（秒）
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            controller = InstanceController(program_id, server_url, check_interval)

            # 设置信号处理器，确保异常退出时也能清理
            def signal_handler(signum, frame):
                print(f"\n⚠️  收到信号 {signum}，正在清理资源...")
                controller.stop_monitoring()
                controller.unregister_instance()
                print(f"✅ 实例已注销: {program_id}")
                sys.exit(1)

            # 注册信号处理器（如果支持的话）
            try:
                signal.signal(signal.SIGINT, signal_handler)
                signal.signal(signal.SIGTERM, signal_handler)
                if hasattr(signal, 'SIGBREAK'):  # Windows
                    signal.signal(signal.SIGBREAK, signal_handler)
            except (AttributeError, OSError):
                pass  # 某些平台可能不支持某些信号

            # 注册实例
            if not controller.register_instance():
                print("❌ 实例注册失败，程序退出")
                sys.exit(1)

            try:
                # 开始监控
                controller.start_monitoring()

                # 执行原函数
                result = func(*args, **kwargs)

                return result

            except KeyboardInterrupt:
                print("\n⚠️  收到中断信号，正在退出...")
            except SystemExit:
                # 如果是强制退出，不要捕获
                if controller.force_exit_requested:
                    raise
                print("\n⚠️  程序被强制退出")
            except Exception as e:
                print(f"❌ 程序执行出错: {e}")
                raise
            finally:
                # 只有在非强制退出时才清理资源
                if not controller.force_exit_requested:
                    controller.stop_monitoring()
                    controller.unregister_instance()
                    print(f"✅ 实例已注销: {program_id}")

        return wrapper
    return decorator
