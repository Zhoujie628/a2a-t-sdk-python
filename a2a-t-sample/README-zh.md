# a2a-t-sample — 示例用例集

基于 **a2a-t-sdk** 的示例用例，以用例独立目录组织。

## 目录结构

```
a2a-t-sample/
├── env.example              # 共享环境配置模板
├── requirements.txt         # 共享依赖
├── ruff.toml                # 共享 lint 配置
├── README.md / README-zh.md # 本文档
└── subscribe_incident/      # 用例：故障订阅
    ├── src/                 #   client / server / registry / common 模块
    ├── test/                #   单元测试
    └── resources/           #   用例独有 mock LLM 响应数据（zh-CN / en-US）
```

共享配置（`env.example`、`requirements.txt`、`ruff.toml`）位于容器层，各用例可复用。每个用例携带自己的 `src/`、`test/` 和 `resources/`。

## 已有用例

| 目录 | 说明 |
|------|------|
| [subscribe_incident/](subscribe_incident/) | 故障订阅用例 — 流式推送 Incident artifact（含注册中心） |

新用例直接在 `a2a-t-sample/` 下以 `subscribe_incident/` 的同级目录添加。

## 快速开始（共享）

```bash
cd a2a-t-sample
cp env.example .env
uv pip install -r requirements.txt
```

> 如果 `A2AT_LLM_API_KEY` 留空，sample 自动使用 `resources/mock_responses/` 下的 mock LLM 响应，无需真实 API 即可跑通完整流程。

## 用例：subscribe_incident（故障订阅）

最小端到端用例，演示故障订阅场景：客户端生成 prompt → 服务端校验 → 流式推送 Incident artifact。

### 启动服务（三个终端）

```bash
# 终端1：启动注册中心
uv run python -m agentcard_example.registry_main

# 终端2：启动服务端
uv run python -m server_example.server_main

# 终端3：启动客户端
uv run python -m client_example.client_main
```

客户端会持续接收 artifact，按 `Ctrl+C` 停止。

### 限制接收数量（可选）

```bash
A2AT_SAMPLE_MAX_ARTIFACTS=5 uv run python -m client_example.client_main
```

### 流程说明

| 阶段 | 谁调 SDK | SDK 做什么 | LLM 调用次数 |
|------|---------|-----------|-------------|
| 启动 | client + server | A2ATClient / A2ATServer 初始化 | 0 |
| Prompt 生成 | 客户端 | 场景识别 + slot 提取 + 模板渲染 | 2 |
| Prompt 校验 | 服务端 | 场景识别 → slot 提取 → 语义校验 | 3 |
| 流式推送 | 客户端 | normalize_event 归一化 stream 事件 | 0 |

### 关键点

- **SDK 是中间层**：client/server 不直接调 LLM，通过 A2ATClient/A2ATServer 间接调用
- **LLM 只在 prompt 阶段用**：推送 artifact 时不调 LLM
- **无协商**：客户端一次性提交完整输入，服务端校验通过直接推送
- **三层解耦**：client（发现 + 消费）→ server（注册 + 推送）→ registry（注册中心）

## 运行测试

```bash
# 运行全部用例测试
uv run pytest subscribe_incident/test/ -v
```