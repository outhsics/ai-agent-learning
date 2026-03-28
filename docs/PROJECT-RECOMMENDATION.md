# 🎯 AI Agent 学习项目推荐（更新版）

## 🏆 最推荐：Dify

**⭐ 134,806 stars** | https://github.com/langgenius/dify

### 为什么是 Dify？

**类似 Ruoyi 的商业级项目**：
- ✅ **生产级平台**：很多公司直接基于 Dify 做商业项目
- ✅ **可视化编排**：拖拽式 AI 应用开发（类似 Ruoyi 的低代码）
- ✅ **企业级功能**：用户权限、多租户、API 网关
- ✅ **技术栈现代**：Go + Python + React
- ✅ **中文社区**：国内大量公司在用
- ✅ **私有化部署**：支持本地部署

### 技术栈

```
后端:
├── Go (API 服务)
├── Python (AI 处理)
└── PostgreSQL + Redis

前端:
└── React + TypeScript + Ant Design

向量数据库:
└── Milvus / Qdrant / Pinecone

LLM:
├── OpenAI (GPT-4)
├── Anthropic (Claude)
├── DeepSeek
└── 通义千问 / 文心一言
```

### 核心功能

- ✅ 可视化工作流编排
- ✅ Agent 智能体开发
- ✅ 知识库管理（RAG）
- ✅ 多模型支持
- ✅ API 服务
- ✅ 用户权限管理
- ✅ 多租户支持

### 学习路径

**Week 1-2: 本地部署**
```bash
# 克隆项目
git clone https://github.com/langgenius/dify.git
cd dify

# 使用 Docker 启动
cd docker
docker-compose up -d

# 访问 http://localhost/install
```

**Week 3-4: 理解架构**
- `docker/docker-compose.yaml` - 服务架构
- `api/` - Go 后端 API
- `web/` - React 前端
- `api/core/` - Python AI 核心

**Week 5-8: 二次开发**
- 创建自定义 Agent
- 添加新的 LLM 模型
- 开发自定义工具
- 扩展 API 接口

**Week 9-12: 商业化功能**
- 多租户开发
- 权限管理
- 支付集成
- 部署优化

### 简历亮点

```markdown
## 项目经验

**Dify 二次开发 - AI Agent 平台** (2026.03 - 2026.06)
- 基于 Dify 开发企业级 AI 应用平台
- 实现可视化工作流编排
- 开发自定义 Agent 和工具
- 接入 DeepSeek、通义千问等国产模型
- 实现多租户和权限管理
- 技术栈：Go, Python, React, PostgreSQL, Milvus
```

---

## 🥈 第二推荐：FastGPT

**⭐ 27,557 stars** | https://github.com/labring/FastGPT

### 特点

- ✅ **纯国产**：文档全中文
- ✅ **可视化工作流**：拖拽式编排
- ✅ **私有化部署**：支持本地部署
- ✅ **商业使用**：很多 SaaS 公司基于它二次开发

### 技术栈

```
后端:
├── Node.js + Express
├── MongoDB
└── Milvus

前端:
└── Next.js + React

Agent:
└── 自定义工作流引擎
```

---

## 🥉 第三推荐：Langchain-Chatchat

**⭐ 37,664 stars** | https://github.com/chatchat-space/Langchain-Chatchat

### 特点

- ✅ 适合学习 LangChain
- ✅ 中文文档完善
- ⚠️ 偏学习项目，商业化程度不如 Dify

---

## 📊 项目对比

| 维度 | Dify | FastGPT | Langchain-Chatchat |
|------|------|---------|-------------------|
| **Stars** | 134,806 | 27,557 | 37,664 |
| **商业级** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **公司使用** | 非常多 | 较多 | 较少 |
| **学习难度** | 中等 | 较低 | 较低 |
| **二次开发** | 容易 | 容易 | 一般 |
| **就业价值** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 最终推荐

**学习 Dify！**

**理由**：
1. ✅ 最类似 Ruoyi 的商业级项目
2. ✅ 很多公司直接用 Dify 做项目
3. ✅ 学会了可以直接找工作
4. ✅ 社区活跃，文档完善
5. ✅ 技术栈现代（Go + Python）

---

## 📅 更新后的学习计划

### Month 1: 基础学习
- Week 1-2: Python + LangChain 基础
- Week 3-4: Dify 本地部署和架构理解

### Month 2: Dify 实战
- Week 5-6: 深入源码学习
- Week 7-8: 二次开发功能

### Month 3: 商业化 + 求职
- Week 9-10: 商业功能开发
- Week 11-12: 简历优化 + 面试准备

---

## 🚀 立即开始

```bash
# 1. 克隆 Dify
git clone https://github.com/langgenius/dify.git
cd dify/docker

# 2. 启动服务
docker-compose up -d

# 3. 访问
open http://localhost/install

# 4. 阅读文档
# https://docs.dify.ai/
```

---

**创建时间**: 2026-03-28
**更新原因**: 用户反馈 Langchain-Chatchat 不够商业级
**推荐项目**: Dify (最类似 Ruoyi 的 AI 平台)
