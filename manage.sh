#!/bin/bash

# Baccarat Simulator Docker 管理脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

show_usage() {
    echo "使用方法: $0 {start|stop|restart|status|logs|build|shell}"
    echo ""
    echo "命令:"
    echo "  start   - 启动服务"
    echo "  stop    - 停止服务"
    echo "  restart - 重启服务"
    echo "  status  - 查看服务状态"
    echo "  logs    - 查看服务日志"
    echo "  build   - 重新构建镜像"
    echo "  shell   - 进入容器 shell"
}

start_service() {
    echo "启动 Baccarat Simulator..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo "✅ 服务启动成功!"
        echo "🌐 访问地址: http://localhost:9006"
        echo "📋 查看状态: $0 status"
        echo "📝 查看日志: $0 logs"
    else
        echo "❌ 服务启动失败!"
        exit 1
    fi
}

stop_service() {
    echo "停止 Baccarat Simulator..."
    docker-compose down
    echo "✅ 服务已停止"
}

restart_service() {
    echo "重启 Baccarat Simulator..."
    stop_service
    sleep 2
    start_service
}

show_status() {
    echo "=== 服务状态 ==="
    docker-compose ps
    echo ""
    echo "=== 健康检查 ==="
    curl -s -o /dev/null -w "HTTP 状态码: %{http_code}\n" http://localhost:9006 2>/dev/null || echo "服务不可访问"
}

show_logs() {
    echo "=== 最近的日志 (按 Ctrl+C 退出实时日志) ==="
    docker-compose logs --tail=50 -f
}

build_image() {
    echo "重新构建 Baccarat Simulator 镜像..."
    docker-compose build --no-cache
    
    if [ $? -eq 0 ]; then
        echo "✅ 镜像构建成功!"
        echo "💡 使用 '$0 restart' 来重启服务以应用更改"
    else
        echo "❌ 镜像构建失败!"
        exit 1
    fi
}

enter_shell() {
    echo "进入 Baccarat Simulator 容器..."
    docker-compose exec baccarat-simulator /bin/bash
}

case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    build)
        build_image
        ;;
    shell)
        enter_shell
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
