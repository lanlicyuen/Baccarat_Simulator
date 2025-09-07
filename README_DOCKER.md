# Baccarat Simulator - Docker 版本

这是一个容器化的百家乐模拟器，使用 Streamlit 构建的 Web 应用程序。

## 🚀 快速开始

### 启动服务
```bash
./manage.sh start
```

### 访问应用
服务启动后，在浏览器中打开：
```
http://localhost:9006
```

默认密码：`12345aB`

## 📋 管理命令

使用 `./manage.sh` 脚本来管理服务：

```bash
./manage.sh start    # 启动服务
./manage.sh stop     # 停止服务
./manage.sh restart  # 重启服务
./manage.sh status   # 查看状态
./manage.sh logs     # 查看日志
./manage.sh build    # 重新构建镜像
./manage.sh shell    # 进入容器命令行
```

## 🔧 配置

### 修改密码
编辑 `docker-compose.yml` 文件中的环境变量：
```yaml
environment:
  - ACCESS_PASSWORD=your_new_password
```

### 修改端口
编辑 `docker-compose.yml` 文件中的端口映射：
```yaml
ports:
  - "8080:8501"  # 改为8080端口
```

## 🐛 故障排除

### 检查服务状态
```bash
./manage.sh status
```

### 查看日志
```bash
./manage.sh logs
```

### 重启服务
```bash
./manage.sh restart
```

### 重新构建镜像
如果修改了代码，需要重新构建镜像：
```bash
./manage.sh build
./manage.sh restart
```

## 📁 文件结构

```
baccarat-simulator/
├── app.py              # 主应用程序
├── baccarat_core.py    # 核心逻辑
├── baccarat_sim.py     # 模拟器
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 镜像配置
├── docker-compose.yml  # Docker Compose 配置
├── manage.sh          # 管理脚本
└── README.md          # 本文档
```

## 🆘 常见问题

### 502 Bad Gateway 错误
这通常表示服务未正常启动，请检查：
1. Docker 是否正在运行
2. 端口是否被占用
3. 查看服务日志：`./manage.sh logs`

### 容器无法启动
1. 重新构建镜像：`./manage.sh build`
2. 检查 Docker 日志：`./manage.sh logs`
3. 确保有足够的磁盘空间

### 修改代码后看不到更改
1. 重新构建镜像：`./manage.sh build`
2. 重启服务：`./manage.sh restart`

## 📊 技术栈

- **前端**: Streamlit
- **后端**: Python
- **容器化**: Docker + Docker Compose
- **数据处理**: Pandas, NumPy
- **可视化**: Altair

## 🔒 安全说明

- 默认密码应该在生产环境中更改
- 建议使用反向代理（如 Nginx）来提供 HTTPS
- 考虑限制访问 IP 范围
