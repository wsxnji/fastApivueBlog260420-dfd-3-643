#!/bin/bash

# 个人博客系统启动脚本
# 使用方法: ./start.sh [backend|frontend|all]

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "========================================="
echo "   个人博客系统 - 启动脚本"
echo "========================================="
echo ""

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法: $0 [backend|frontend|all]"
    echo ""
    echo "选项:"
    echo "  backend  - 仅启动后端服务"
    echo "  frontend - 仅启动前端服务"
    echo "  all      - 同时启动后端和前端（默认）"
    echo ""
    MODE="all"
else
    MODE="$1"
fi

# 函数：启动后端
start_backend() {
    echo "🚀 启动后端服务..."
    cd "$BACKEND_DIR"
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo "📦 虚拟环境不存在，正在创建..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 检查依赖
    if [ ! -f "venv/installed" ]; then
        echo "📦 安装后端依赖..."
        pip install -r requirements.txt
        touch venv/installed
    fi
    
    echo "✅ 后端服务启动中..."
    echo "   后端地址: http://localhost:8000"
    echo "   API文档:  http://localhost:8000/docs"
    echo ""
    
    uvicorn main:app --reload --port 8000
}

# 函数：启动前端
start_frontend() {
    echo "🚀 启动前端服务..."
    cd "$FRONTEND_DIR"
    
    # 检查 node_modules
    if [ ! -d "node_modules" ]; then
        echo "📦 前端依赖不存在，正在安装..."
        npm install
    fi
    
    echo "✅ 前端服务启动中..."
    echo "   前端地址: http://localhost:5173"
    echo ""
    
    npm run dev
}

# 根据模式启动
case "$MODE" in
    backend)
        start_backend
        ;;
    frontend)
        start_frontend
        ;;
    all)
        echo "📢 模式: 同时启动后端和前端"
        echo ""
        
        # 使用 tmux 或 screen 同时运行两个服务
        # 如果没有 tmux，提示用户手动启动
        if command -v tmux &> /dev/null; then
            echo "🎯 使用 tmux 同时启动两个服务..."
            echo ""
            
            # 创建新的 tmux 会话
            tmux new-session -d -s blog-server
            
            # 分割窗口
            tmux split-window -v -p 50
            
            # 在第一个窗口启动后端
            tmux send-keys -t blog-server:0.0 "cd $BACKEND_DIR && source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt -q && uvicorn main:app --reload --port 8000" C-m
            
            # 在第二个窗口启动前端
            tmux send-keys -t blog-server:0.1 "cd $FRONTEND_DIR && [ ! -d node_modules ] && npm install -q; npm run dev" C-m
            
            # 附加到会话
            echo "✅ 服务已在 tmux 会话中启动！"
            echo "   按 Ctrl+B 然后 D 可以分离会话"
            echo "   使用 'tmux attach -t blog-server' 重新连接"
            echo ""
            tmux attach -t blog-server
        else
            echo "⚠️  未检测到 tmux，将在两个终端窗口中分别启动"
            echo ""
            echo "📋 请手动执行以下命令："
            echo ""
            echo "终端 1 - 后端:"
            echo "  cd $BACKEND_DIR"
            echo "  source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate"
            echo "  pip install -r requirements.txt"
            echo "  uvicorn main:app --reload --port 8000"
            echo ""
            echo "终端 2 - 前端:"
            echo "  cd $FRONTEND_DIR"
            echo "  [ ! -d node_modules ] && npm install"
            echo "  npm run dev"
            echo ""
        fi
        ;;
    *)
        echo "❌ 无效参数: $MODE"
        echo "使用方法: $0 [backend|frontend|all]"
        exit 1
        ;;
esac
