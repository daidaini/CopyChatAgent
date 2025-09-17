#!/bin/bash

# CopyChatAgent 项目停止脚本

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$PROJECT_DIR/logs"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 停止 Backend
stop_backend() {
    log_info "停止 Backend 服务器..."

    # 从 PID 文件读取并停止
    if [ -f "$LOG_DIR/backend.pid" ]; then
        BACKEND_PID=$(cat "$LOG_DIR/backend.pid")
        if ps -p $BACKEND_PID > /dev/null; then
            kill $BACKEND_PID
            log_success "Backend 服务器已停止 (PID: $BACKEND_PID)"
        else
            log_warning "Backend 进程不存在"
        fi
        rm -f "$LOG_DIR/backend.pid"
    fi

    # 强制停止所有相关的 Python 进程
    PIDS=$(ps aux | grep "python.*app.py" | grep -v grep | awk '{print $2}' || true)
    if [ -n "$PIDS" ]; then
        log_info "发现运行中的 Backend 进程，正在停止..."
        echo "$PIDS" | xargs kill -9
        log_success "Backend 进程已强制停止"
    fi
}

# 停止端口 5000 上的进程
stop_port_5000() {
    PIDS=$(lsof -ti:5000 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        log_info "停止端口 5000 上的进程..."
        kill -9 $PIDS 2>/dev/null || true
        log_success "端口 5000 已释放"
    fi
}

# 清理日志文件
cleanup_logs() {
    if [ "$1" = "--clean" ]; then
        log_info "清理日志文件..."
        if [ -d "$LOG_DIR" ]; then
            rm -f "$LOG_DIR"/*.log
            rm -f "$LOG_DIR"/*.pid
            log_success "日志文件已清理"
        fi
    fi
}

# 显示使用信息
show_usage() {
    echo "CopyChatAgent Backend 停止脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  stop        停止 Backend 服务 (默认)"
    echo "  clean       停止 Backend 并清理日志"
    echo "  help        显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0          # 停止 Backend"
    echo "  $0 clean    # 停止 Backend 并清理日志"
}

# 主函数
main() {
    case "${1:-stop}" in
        "stop")
            log_info "停止 CopyChatAgent Backend..."
            stop_backend
            stop_port_5000
            log_success "CopyChatAgent Backend 已停止"
            ;;
        "clean")
            log_info "停止 CopyChatAgent Backend 并清理日志..."
            stop_backend
            stop_port_5000
            cleanup_logs --clean
            log_success "CopyChatAgent Backend 已停止，日志已清理"
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            log_error "未知选项: $1"
            show_usage
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"