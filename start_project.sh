#!/bin/bash

# CopyChatAgent 项目启动脚本
# 用于启动 Backend (Flask) 和 Frontend (Vue.js) 开发服务器

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
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

# 检查依赖
check_dependencies() {
    log_info "检查项目依赖..."

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装，请先安装 Python3"
        exit 1
    fi

    log_success "依赖检查完成"
}

# 安装 Backend 依赖
install_backend_deps() {
    log_info "安装 Backend 依赖..."
    cd "$BACKEND_DIR"

    if [ ! -d "venv" ]; then
        log_info "创建 Python 虚拟环境..."
        python3 -m venv venv
    fi

    source venv/bin/activate
    pip install -r requirements.txt
    log_success "Backend 依赖安装完成"

    cd "$PROJECT_DIR"
}

# 检查环境变量
check_env() {
    log_info "检查环境变量..."

    if [ ! -f "$BACKEND_DIR/.env" ]; then
        log_warning "Backend .env 文件不存在，复制模板..."
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        log_warning "请编辑 $BACKEND_DIR/.env 文件，设置 GLM_API_KEY"
    fi

    if ! grep -q "GLM_API_KEY=" "$BACKEND_DIR/.env"; then
        log_error "请在 $BACKEND_DIR/.env 中设置 GLM_API_KEY"
        exit 1
    fi

    log_success "环境变量检查完成"
}

# 创建日志目录
create_log_dir() {
    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR"
        log_info "创建日志目录: $LOG_DIR"
    fi
}

# 启动 Backend
start_backend() {
    log_info "启动 Backend (Flask) 服务器..."
    cd "$BACKEND_DIR"

    source venv/bin/activate
    nohup python app.py > "$LOG_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$LOG_DIR/backend.pid"

    # 等待 Backend 启动
    sleep 3

    if ps -p $BACKEND_PID > /dev/null; then
        log_success "Backend 服务器已启动 (PID: $BACKEND_PID)"
        log_info "Backend 日志: $LOG_DIR/backend.log"
        log_info "Backend 地址: http://127.0.0.1:5000"
    else
        log_error "Backend 服务器启动失败，请检查日志: $LOG_DIR/backend.log"
        exit 1
    fi

    cd "$PROJECT_DIR"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."

    # 检查 Backend
    if curl -s http://127.0.0.1:5000/health > /dev/null; then
        log_success "Backend 健康检查通过"
    else
        log_error "Backend 健康检查失败"
        return 1
    fi
}

# 显示使用信息
show_usage() {
    echo "CopyChatAgent Backend 启动脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  install     安装 Backend 依赖"
    echo "  start       启动 Backend 服务 (默认)"
    echo "  stop        停止 Backend 服务"
    echo "  restart     重启 Backend 服务"
    echo "  status      查看 Backend 状态"
    echo "  logs        查看 Backend 日志"
    echo "  help        显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 install  # 安装依赖"
    echo "  $0 start    # 启动 Backend"
    echo "  $0 stop     # 停止 Backend"
}

# 主函数
main() {
    case "${1:-start}" in
        "install")
            log_info "开始安装 CopyChatAgent Backend..."
            check_dependencies
            create_log_dir
            install_backend_deps
            check_env
            log_success "Backend 安装完成！"
            log_info "运行 '$0 start' 启动 Backend 服务"
            ;;
        "start")
            log_info "启动 CopyChatAgent Backend..."
            create_log_dir
            check_env
            start_backend
            sleep 2
            health_check
            log_success "CopyChatAgent Backend 启动完成！"
            log_info "Backend API: http://127.0.0.1:5000"
            log_info "运行 '$0 stop' 停止 Backend 服务"
            ;;
        "stop")
            log_info "停止 CopyChatAgent Backend..."
            if [ -f "$LOG_DIR/backend.pid" ]; then
                BACKEND_PID=$(cat "$LOG_DIR/backend.pid")
                if ps -p $BACKEND_PID > /dev/null; then
                    kill $BACKEND_PID
                    log_success "Backend 已停止"
                fi
                rm -f "$LOG_DIR/backend.pid"
            fi

            log_success "Backend 已停止"
            ;;
        "restart")
            log_info "重启 CopyChatAgent Backend..."
            $0 stop
            sleep 2
            $0 start
            ;;
        "status")
            log_info "Backend 状态:"
            if [ -f "$LOG_DIR/backend.pid" ]; then
                BACKEND_PID=$(cat "$LOG_DIR/backend.pid")
                if ps -p $BACKEND_PID > /dev/null; then
                    log_success "Backend 运行中 (PID: $BACKEND_PID)"
                else
                    log_error "Backend 未运行"
                fi
            else
                log_error "Backend 未运行"
            fi
            ;;
        "logs")
            log_info "Backend 日志:"
            if [ -f "$LOG_DIR/backend.log" ]; then
                log_info "Backend 日志 (最后 20 行):"
                tail -20 "$LOG_DIR/backend.log"
            fi
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