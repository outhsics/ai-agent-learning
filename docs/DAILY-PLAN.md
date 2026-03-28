# 📅 每日学习计划

**目标**: 3 个月掌握 AI Agent 开发
**开始日期**: 2026-03-28
**结束日期**: 2026-06-28

---

## 🎯 Month 1: 基础学习（Week 1-4）

### Week 1: Python 高级特性 + LangChain 基础

#### Day 1 (2026-03-28) - 今天 ✅
- [x] 创建项目结构
- [x] 启动三层架构演示
- [x] 克隆 Langchain-Chatchat
- [ ] **学习任务**：
  - [ ] 阅读 Langchain-Chatchat README
  - [ ] 理解项目结构
  - [ ] 测试三层架构 API

**预计时间**: 2-3 小时

---

#### Day 2 (2026-03-29) - Python 异步编程
**学习目标**:
- [ ] async/await 基础
- [ ] asyncio 库使用
- [ ] 并发 vs 并行

**实践任务**:
```python
# 实现一个异步聊天处理器
async def process_message(message: str):
    # 1. 调用 LLM API
    # 2. 保存到数据库
    # 3. 返回响应
    pass
```

**参考**: `langchain-chatchat/server/api/*`

---

#### Day 3 (2026-03-30) - LangChain Chains
**学习目标**:
- [ ] LLMChain 基础
- [ ] Sequential Chains
- [ ] 自定义 Chain

**实践任务**:
```python
# 创建一个简单的问答链
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# TODO: 实现
```

**文档**: https://python.langchain.com/docs/chains/

---

#### Day 4 (2026-03-31) - LangChain Agents
**学习目标**:
- [ ] Agent 基础概念
- [ ] ReAct Agent
- [ ] 自定义 Tools

**实践任务**:
```python
# 创建一个搜索 Agent
from langchain.agents import initialize_agent, Tool

# TODO: 实现搜索工具
```

---

#### Day 5-7: 实战练习
**项目**: 构建一个简单的问答 Agent
- [ ] 集成 OpenAI API
- [ ] 实现对话历史
- [ ] 添加搜索工具

---

### Week 2: 向量数据库 + RAG

#### Day 8-9: Milvus 基础
**学习目标**:
- [ ] Collection 创建和管理
- [ ] 向量插入和查询
- [ ] 相似度搜索

**实践任务**:
```python
# 创建文档知识库
# 1. 文档切片
# 2. 向量化
# 3. 存储到 Milvus
# 4. 语义搜索
```

---

#### Day 10-11: RAG 基础
**学习目标**:
- [ ] RAG 原理
- [ ] LangChain RAG Chains
- [ ] Prompt 优化

**实践任务**:
```python
# 构建 RAG 系统
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Milvus

# TODO: 实现
```

---

#### Day 12-14: 三层架构实操
**项目**: 完整的文档问答系统
- [ ] MinIO 存储文档
- [ ] PostgreSQL 存储元数据
- [ ] Milvus 存储向量
- [ ] FastAPI 接口

---

### Week 3: LangGraph + 高级 Agent

#### Day 15-17: LangGraph 基础
**学习目标**:
- [ ] Graph 概念
- [ ] State 管理
- [ ] 条件边

**实践任务**:
```python
from langgraph.graph import StateGraph

# 创建一个多步推理 Agent
```

---

#### Day 18-21: Agent 编排
**项目**: 客服 Agent 系统
- [ ] 意图识别
- [ ] 多轮对话
- [ ] 工具调用

---

### Week 4: 项目实战

#### Day 22-28: 完整 RAG 应用
**项目**: 个人知识库问答系统
- [ ] 文档上传
- [ ] 向量检索
- [ ] AI 问答
- [ ] 前端界面

---

## 🎯 Month 2: Langchain-Chatchat 实战（Week 5-8）

### Week 5: 项目启动
#### Day 29-31: 环境搭建
- [ ] 本地运行项目
- [ ] 理解核心架构
- [ ] 配置国产模型

### Week 6-7: 核心功能学习
#### Day 32-45: 深入源码
- [ ] `server/api/*` - API 层
- [ ] `server/chains/*` - Chain 实现
- [ ] `server/db/*` - 数据库层
- [ ] `server/services/*` - 业务逻辑

### Week 8: 二次开发
#### Day 46-49: 功能扩展
- [ ] 添加新的 Agent 类型
- [ ] 优化检索策略
- [ ] 实现自定义工具

---

## 🎯 Month 3: 项目 + 求职（Week 9-12）

### Week 9-10: 个人项目
#### Day 50-57: 完整项目
**项目**: AI 智能客服系统
- [ ] 多模态支持（图片 + 文本）
- [ ] 知识库管理
- [ ] 对话管理
- [ ] 性能优化

### Week 11: 简历 + 面试准备
#### Day 58-61: 求职材料
- [ ] 优化简历
- [ ] 准备项目展示
- [ ] 刷 LeetCode
- [ ] 系统设计练习

### Week 12: 投递 + 面试
#### Day 62-84: 求职实战
- [ ] BOSS 直聘投递
- [ ] 技术面试准备
- [ ] 模拟面试
- [ ] Offer 谈判

---

## 📊 每日学习模板

### 日期: YYYY-MM-DD

**今日目标**:
- [ ] 学习内容
- [ ] 实践任务
- [ ] 代码提交

**学习笔记**:
```
- 关键概念:
- 代码片段:
- 遇到问题:
- 解决方案:
```

**进度**: ⏳ 进行中 | ✅ 已完成

---

## 📈 学习进度追踪

**当前进度**: Day 1 / 90 Days

**完成任务**:
- [x] 创建项目结构
- [x] 启动三层架构
- [ ] ...

**代码统计**:
- 提交次数: 0
- 代码行数: 0
- 项目数量: 0

---

## 🎖️ 里程碑

- [x] **Day 1**: 项目启动
- [ ] **Day 7**: 第一个 Agent
- [ ] **Day 14**: 三层架构项目
- [ ] **Day 28**: RAG 应用
- [ ] **Day 49**: Langchain-Chatchat 二次开发
- [ ] **Day 57**: 个人项目完成
- [ ] **Day 84**: 开始投递简历
- [ ] **Day 90**: 拿到 Offer

---

**最后更新**: 2026-03-28
**下次更新**: 每日完成学习后
