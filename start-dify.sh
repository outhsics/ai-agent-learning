#!/bin/bash
# Dify 启动脚本

set -e

echo ""
echo "============================================================"
echo "  🚀 Dify 启动脚本"
echo "============================================================"
echo ""

DIFY_DIR="~/ai-agent-learning/dify/docker"
cd "$DIFY_DIR"

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker Desktop"
    exit 1
fi

echo "✅ Docker 已运行"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo ""
    echo "📝 创建 .env 文件..."
    cp .env.example .env
    echo "✅ .env 文件已创建"
fi

# 停止旧容器
echo ""
echo "🛑 停止旧容器..."
docker-compose down 2>/dev/null || true

# 启动所有服务
echo ""
echo "🚀 启动 Dify 服务..."
echo "⏳ 首次启动需要下载镜像，请耐心等待（5-10 分钟）"
echo ""

docker-compose up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "📊 服务状态："
echo ""

docker-compose ps

echo ""
echo "============================================================"
echo "  🌐 访问地址"
echo "============================================================"
echo ""
echo "Dify 主页:     http://localhost/"
echo "安装向导:     http://localhost/install"
echo "API 文档:     http://localhost/api/docs"
echo ""
echo "============================================================"
echo "  📖 下一步"
echo "============================================================"
echo ""
echo "1. 打开浏览器访问: http://localhost/install"
echo "2. 设置管理员账号"
echo "3. 配置向量数据库和 LLM 模型"
echo "4. 开始创建你的第一个 AI 应用！"
echo ""
echo "============================================================"
echo "  🛠️  管理命令"
echo "============================================================"
echo ""
echo "查看日志:"
echo "  docker-compose logs -f"
echo ""
echo "停止服务:"
echo "  docker-compose down"
echo ""
echo "重启服务:"
echo "  docker-compose restart"
echo ""
echo "============================================================"
echo ""
