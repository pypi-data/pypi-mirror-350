# EasyRemote：构建下一代算力互联网络 —— 易联网（EasyNet）

<div align="center">

![EasyRemote Logo](docs/easyremote-logo.png)

[![PyPI version](https://badge.fury.io/py/easyremote.svg)](https://badge.fury.io/py/easyremote)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/easyremote)]()

> **"Torchrun for the World"**：让任意终端用户一行命令就能调动全球算力资源，执行本地代码。

**🌐 Building the Next-Generation Computing Internet - EasyNet**

[English](README.md) | 中文

</div>

---

## 🧠 从私有函数到全局算力调度引擎

**EasyRemote不仅是一个私有函数即服务平台（Private FaaS），它是我们对未来计算形态的回答：**

> 当前云计算模式以平台为中心，数据和代码必须"上云"交换资源，而我们认为——  
> **下一代算力网络应以终端为中心、以语言为接口、以函数为单元、以信任为边界**。

我们称之为：**"易联网（EasyNet）"**。

### 🎯 核心理念：代码即资源，设备即节点，执行即协作

EasyRemote是易联网的第一阶段实现，它允许你：

* **🧠 使用熟悉的Python函数结构定义任务逻辑**
* **🔒 在任意设备部署算力节点，保持隐私、性能与控制**  
* **🌐 通过轻量VPS网关，将本地函数转为全球可访问的任务接口**
* **🚀 最终像使用`torchrun`一样简单地启动任务，自动调度至最合适的资源执行**

### 💡 我们的范式转移

| 传统云计算模式 | **易联网模式** |
|------------|-------------|
| 以平台为中心 | **以终端为中心** |
| 代码必须上云 | **代码在你的设备** |
| 付费使用算力 | **贡献获得算力** |
| 供应商锁定 | **去中心化协作** |
| 冷启动延迟 | **始终温热** |

---

## 🔭 当前实现：私有函数即服务

### **快速体验：12行代码加入易联网**

```python
# 1. 启动网关节点 (任意VPS)
from easyremote import Server
Server(port=8080).start()

# 2. 贡献算力节点 (你的设备)
from easyremote import ComputeNode
node = ComputeNode("your-gateway:8080")

@node.register
def ai_inference(prompt):
    return your_local_model.generate(prompt)  # 运行在你的GPU上

node.serve()

# 3. 全球调用算力 (任何地方)
from easyremote import Client
result = Client("your-gateway:8080").execute("ai_inference", "Hello AI")
```

**🎉 你的设备已加入易联网！**

### **🆚 与传统云服务对比**

| 特性 | AWS Lambda | Google Cloud | **EasyNet节点** |
|------|------------|--------------|----------------|
| **计算位置** | 云端服务器 | 云端服务器 | **你的设备** |
| **数据隐私** | 上传到云端 | 上传到云端 | **永不离开本地** |
| **算力成本** | $200+/百万次 | $200+/百万次 | **$5网关费用** |
| **硬件限制** | 云端规格 | 云端规格 | **你的GPU/CPU** |
| **启动延迟** | 100-1000ms | 100-1000ms | **0ms (始终在线)** |

---

## 📚 完整文档指南

### 🌐 多语言文档

#### 🇨🇳 中文文档 
- **[📖 中文文档中心](docs/zh/README.md)** - 完整的中文文档导航

#### 🇺🇸 English Documentation
- **[📖 English Documentation Center](docs/en/README.md)** - Complete English documentation

### 🚀 快速开始
- **[5分钟快速开始](docs/zh/user-guide/quick-start.md)** - 最快上手方式  | [English](docs/en/user-guide/quick-start.md)
- **[安装指南](docs/zh/user-guide/installation.md)** - 详细安装说明 | [English](docs/en/user-guide/installation.md)

### 📖 用户指南
- **[API参考文档](docs/zh/user-guide/api-reference.md)** - 完整API说明 | [English](docs/en/user-guide/api-reference.md)
- **[基础使用教程](docs/zh/tutorials/basic-usage.md)** - 详细基础教程 | [English](docs/en/tutorials/basic-usage.md)
- **[高级场景教程](docs/zh/tutorials/advanced-scenarios.md)** - 复杂应用实现 | [English](docs/en/tutorials/advanced-scenarios.md)

### 🏗️ 技术深入
- **[系统架构](docs/zh/architecture/overview.md)** - 整体架构设计 | [English](docs/en/architecture/overview.md)
- **[部署指南](docs/zh/tutorials/deployment.md)** - 多环境部署方案 | [English](docs/en/tutorials/deployment.md)

### 🔬 研究资料
- **[技术白皮书](docs/zh/research/whitepaper.md)** - EasyNet理论基础 | [English](docs/en/research/whitepaper.md)
- **[研究提案](docs/zh/research/research-proposal.md)** - 学术研究计划 | [English](docs/en/research/research-proposal.md)
- **[项目介绍](docs/zh/research/pitch.md)** - 商业计划概述 | [English](docs/en/research/pitch.md)

---

## 🌟 易联网的三大突破

### **1. 🔒 隐私优先架构**
```python
@node.register
def medical_diagnosis(scan_data):
    # 医疗数据永远不离开你的HIPAA合规设备
    # 但诊断服务可被全球安全访问
    return your_private_ai_model.diagnose(scan_data)
```

### **2. 💰 经济模型重构**
- **传统云服务**：按使用付费，规模越大成本越高
- **易联网模式**：贡献算力获得积分，使用积分调用他人算力
- **网关成本**：$5/月 vs 传统云$200+/百万调用

### **3. 🚀 消费级设备参与全球AI**
```python
# 你的游戏电脑可以为全球提供AI推理服务
@node.register
def image_generation(prompt):
    return your_stable_diffusion.generate(prompt)

# 你的MacBook可以参与分布式训练
@node.register  
def gradient_computation(batch_data):
    return your_local_model.compute_gradients(batch_data)
```

---

## 🎯 三范式跳跃：通过范式革命重塑计算未来

> **"计算演进不是线性发展，而是范式跳跃"**

### **🚀 范式一：FDCN (函数驱动计算网络)**
**核心变革**: 从本地调用 → 跨节点函数调用  
**技术表现**: `@remote` 装饰器实现透明分布式执行  
**范式类比**: RPC → gRPC → **EasyRemote** (函数调用的空间解耦)

```python
# 传统本地调用
def ai_inference(data): return model.predict(data)

# EasyRemote: 跨全球网络的函数调用
@node.register  
def ai_inference(data): return model.predict(data)
result = client.execute("global_node.ai_inference", data)
```

**突破指标**: 
- API简洁度: 25+行 → **12行** (-52%)
- 启动延迟: 100-1000ms → **0ms** (-100%)
- 隐私保护: 数据上云 → **永不离开本地**

### **🧩 范式二：智能链接调度 (Intelligence-Linked Scheduling)**
**核心变革**: 从显式调度 → 自适应智能调度  
**技术表现**: 意图驱动的多目标优化调度  
**范式类比**: Kubernetes → Ray → **EasyRemote ComputePool**

```python
# 传统显式调度
client.execute("specific_node.specific_function", data)

# EasyRemote: 智能意图调度
result = await compute_pool.execute_optimized(
    task_intent="image_classification",
    requirements=TaskRequirements(accuracy=">95%", cost="<$5")
)
# 系统自动：任务分析 → 资源匹配 → 最优调度
```

**突破指标**:
- 调度效率: 人工配置 → **毫秒级自动决策**
- 资源利用率: 60% → **85%** (+42%)
- 认知负荷: 复杂配置 → **意图表达**

### **🌟 范式三：意图图执行 (Intent-Graph Execution)**
**核心变革**: 从调用函数 → 表达意图  
**技术表现**: 自然语言驱动的专家协作网络  
**范式类比**: LangChain → AutoGPT → **EasyRemote Intent Engine**

```python
# 传统函数调用思维
await compute_pool.execute_optimized(function="train_classifier", ...)

# EasyRemote: 自然语言意图表达
result = await easynet.fulfill_intent(
    "训练一个医学影像AI，准确率超过90%，成本控制在10美元以内"
)
# 系统自动：意图理解 → 任务分解 → 专家发现 → 协作执行
```

**突破指标**:
- 用户门槛: Python开发者 → **普通用户** (1000万+用户规模)
- 交互方式: 代码调用 → **自然语言**
- 协作深度: 工具调用 → **智能体协作网络**

### **🔄 范式螺旋：纵向演化路线图**
```
┌────────────────────────────────────────────────────────────┐
│                 全球算力操作系统                             │ ← 范式3：意图调度层
│    "训练医学AI" → 自动协调全球专家节点                       │   (Intent-Graph)
└────────────────────────────────────────────────────────────┘
                            ▲
┌────────────────────────────────────────────────────────────┐
│                算力共享平台                                 │ ← 范式2：自治编排层  
│    智能任务调度 + 多目标优化 + 资源池管理                      │   (Intelligence-Linked)
└────────────────────────────────────────────────────────────┘
                            ▲
┌────────────────────────────────────────────────────────────┐
│               私有函数网络                                   │ ← 范式1：函数远程层
│    @remote 装饰器 + 跨节点调用 + 负载均衡                      │   (Function-Driven)  
└────────────────────────────────────────────────────────────┘
```

**终极愿景**: 像使用`torchrun`一样简单调动全球算力
```bash
$ easynet "训练一个医学影像AI，数据在我本地，要求准确率95%+"
🤖 理解您的需求，正在协调全球医学AI专家节点...
✅ 找到stanford-medical-ai等3个专家节点，开始协作训练...
```

---

## 🔬 技术架构：去中心化 + 边缘计算

### **网络拓扑**
```
🌍 全球客户端
    ↓
☁️ 轻量网关集群 (仅路由，不计算)
    ↓
💻 个人算力节点 (实际执行)
    ↓
🔗 点对点协作网络
```

### **核心技术栈**
- **通信协议**：gRPC + Protocol Buffers
- **安全传输**：端到端加密
- **负载均衡**：智能资源感知
- **容错机制**：自动重试和恢复

---

## 🌊 加入算力革命

### **🔥 为什么易联网将改变一切**

**传统模式的局限**：
- 💸 云服务费用随规模指数增长
- 🔒 数据必须上传到第三方服务器
- ⚡ 冷启动和网络延迟限制性能
- 🏢 被大型云服务商绑定

**易联网的突破**：
- 💰 **算力共享经济**：贡献闲置资源，获得全球算力
- 🔐 **隐私by Design**：数据永远不离开你的设备
- 🚀 **边缘优先**：零延迟，最优性能
- 🌐 **去中心化**：无单点故障，无供应商锁定

### **🎯 我们的使命**

> **重新定义计算的未来**：从少数云服务商垄断算力，到每个设备都是算力网络的一部分。

### **🚀 立即加入**

```bash
# 成为易联网的早期节点
pip install easyremote

# 贡献你的算力
python -c "
from easyremote import ComputeNode
node = ComputeNode('demo.easynet.io:8080')
@node.register
def hello_world(): return 'Hello from my device!'
node.serve()
"
```

---

## 🏗️ 开发者生态

| 角色 | 贡献 | 收益 |
|------|------|------|
| **算力提供者** | 闲置GPU/CPU时间 | 算力积分/代币奖励 |
| **应用开发者** | 创新算法和应用 | 全球算力资源访问 |
| **网关运营者** | 网络基础设施 | 路由费用分成 |
| **生态建设者** | 工具和文档 | 社区治理权益 |

---

## 📞 加入社区

* **🎯 技术讨论**: [GitHub Issues](https://github.com/Qingbolan/EasyCompute/issues)
* **💬 社区交流**: [GitHub Discussions](https://github.com/Qingbolan/EasyCompute/discussions)
* **📧 商务合作**: [silan.hu@u.nus.edu](mailto:silan.hu@u.nus.edu)
* **👨‍💻 项目发起人**: [Silan Hu](https://github.com/Qingbolan) - NUS PhD Candidate

---

<div align="center">

## 🌟 "未来的软件不是部署在云上，而是运行在你的系统+易联网之上"

**🚀 Ready to join the computing revolution?**

```bash
pip install easyremote
```

**不要只把它看作分布式函数工具 —— 它是运行在旧世界轨道上，却驶向新世界终点的原型机。**

*⭐ 如果你认同这个新世界观，请给我们一个星标！*

</div>
