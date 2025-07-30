# Instancer

一个用于程序实例控制和管理的Python包。

## 功能特性

- 🎯 **客户端装饰器**: 通过简单的装饰器设置程序ID和服务地址
- 🖥️ **服务端管理**: 提供Web界面进行实例管理
- 📊 **实时控制**: 动态控制实例数量和状态
- 🚫 **强制退出**: 支持实时禁用和强制退出正在运行的实例
- 🔧 **简易部署**: 一键启动服务端

## 快速开始

### 安装

```bash
pip install instancer
```

### 客户端使用

```python
from instancer import instance_control

@instance_control(program_id="my_app", server_url="http://localhost:5000")
def my_application():
    print("应用程序正在运行...")
    # 您的应用逻辑
    
if __name__ == "__main__":
    my_application()
```

### 服务端部署

```bash
# 启动服务端
instancer-server --host 0.0.0.0 --port 5000

# 或者在Python中启动
python -m instancer.server
```

### 管理界面

访问 `http://localhost:5000` 打开管理界面，可以：

- 添加和配置程序ID
- 设置允许的实例数量
- 实时查看运行状态
- 禁用/启用程序

## 配置说明

### 客户端配置

- `program_id`: 程序的唯一标识符
- `server_url`: 服务端地址
- `check_interval`: 状态检查间隔（秒，默认5秒）

### 服务端配置

- `host`: 服务绑定地址（默认127.0.0.1）
- `port`: 服务端口（默认5000）
- `database_url`: 数据库连接字符串（默认SQLite）

## 许可证

MIT License
