#!/bin/bash
# 三层架构演示 - 快速启动脚本

set -e

echo ""
echo "============================================================"
echo "  🏗️  三层架构演示 - 快速启动"
echo "============================================================"
echo ""

DEMO_DIR="$HOME/.claude/three-tier-demo"
cd "$DEMO_DIR"

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker Desktop"
    exit 1
fi

echo "✅ Docker 已运行"

# 创建数据目录
mkdir -p data/{minio,postgres,etcd,milvus-minio,milvus}
echo "✅ 数据目录已创建"

# 停止旧容器
echo ""
echo "🛑 停止旧容器..."
docker-compose down 2>/dev/null || true

# 启动所有服务
echo ""
echo "🚀 启动服务..."
docker-compose up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo ""
echo "📊 服务状态："
echo ""

# MinIO
if curl -s http://localhost:9000/minio/health/live > /dev/null 2>&1; then
    echo "✅ MinIO: http://localhost:9000 (API)"
    echo "   控制台: http://localhost:9001"
    echo "   用户名: minioadmin"
    echo "   密码: minioadmin123"
else
    echo "⏳ MinIO: 启动中..."
fi

# PostgreSQL
if docker exec demo-postgres pg_isready -U demo_user > /dev/null 2>&1; then
    echo "✅ PostgreSQL: localhost:5432"
else
    echo "⏳ PostgreSQL: 启动中..."
fi

# Milvus
if docker exec demo-milvus curl -s http://localhost:19530 > /dev/null 2>&1; then
    echo "✅ Milvus: localhost:19530"
else
    echo "⏳ Milvus: 启动中..."
fi

# API 服务
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API 服务: http://localhost:8000"
    echo "   文档: http://localhost:8000/docs"
else
    echo "⏳ API 服务: 启动中..."
fi

echo ""
echo "============================================================"
echo "  📖 快速测试"
echo "============================================================"
echo ""
echo "1. 健康检查:"
echo "   curl http://localhost:8000/health"
echo ""
echo "2. 保存消息:"
echo '   curl -X POST http://localhost:8000/messages -H "Content-Type: application/json" -d '"'"'{"content": "测试消息"}'"'"
echo ""
echo "3. 搜索消息:"
echo '   curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -d '"'"'{"query": "测试"}'"'"
echo ""
echo "4. 查看 API 文档:"
echo "   open http://localhost:8000/docs"
echo ""
echo "============================================================"
echo "  📚 完整文档"
echo "============================================================"
echo ""
echo "查看 README.md 了解详细使用方法:"
echo "   cat $DEMO_DIR/README.md"
echo ""
echo "============================================================"
echo "  🛠️  管理命令"
echo "============================================================"
echo ""
echo "查看日志:"
echo "   docker-compose logs -f demo-app"
echo ""
echo "停止所有服务:"
echo "   docker-compose down"
echo ""
echo "重启服务:"
echo "   docker-compose restart"
echo ""
echo "============================================================"
echo ""
