# A2A-T Sample

基于 a2a-t-sdk 的最小端到端示例，演示**流式告警订阅**场景：客户端生成 prompt → 服务端校验 → 流式推送 Incident artifact。

[English](README.md)

## 目录结构

```
a2a-t-sample/
├── src/
│   ├── agentcard_example/   # mock 注册中心（AgentCard 注册/查询）
│   ├── client_example/      # 客户端（发现 agent + 生成 prompt + 消费流）
│   ├── server_example/      # 服务端（注册 agent + 校验 prompt + 推送 artifact）
│   └── common/              # 公共模块（LLM 日志、mock、a2a 适配器等）
├── test/                    # 单元测试
├── resources/
│   └── mock_responses/      # mock LLM 响应数据（zh-CN / en-US）
├── env.example              # 环境配置模板
├── requirements.txt         # sample 依赖
└── ruff.toml                # lint 配置
```

## 快速开始

### 1. 准备环境

```bash
cd a2a-t-sample
cp env.example .env
```

编辑 `.env`，填入你的 LLM API Key：

```
A2AT_LLM_API_KEY=sk-your-real-key
```

> 如果不填 key（留空），sample 会自动使用 mock LLM 响应，无需真实 API 即可跑通完整流程。

### 2. 安装依赖

```bash
uv pip install -r requirements.txt
```

### 3. 启动服务（三个终端）

```bash
# 终端1：启动注册中心
uv run python -m agentcard_example.registry_main

# 终端2：启动服务端
uv run python -m server_example.server_main

# 终端3：启动客户端
uv run python -m client_example.client_main
```

客户端会持续接收 artifact，按 `Ctrl+C` 停止。

### 4. 限制接收数量（可选）

通过环境变量控制客户端接收多少个 artifact 后自动停止：

```bash
A2AT_SAMPLE_MAX_ARTIFACTS=5 uv run python -m client_example.client_main
```

## 时序图

```plantuml
@startuml
autonumber
skinparam maxMessageSize 150

participant "client_example" as Client
participant "server_example" as Server
participant "agentcard_example\n(mock 注册中心)" as Registry
participant "a2a-t-sdk" as SDK
participant "LLM" as LLM

== 终端1: 启动注册中心 ==
Registry -> Registry : uvicorn 监听 127.0.0.1:5001

== 终端2: 启动服务端 ==
Server -> Registry : POST /rest/v1/registry-center/agent-cards\n{name, skills, streaming:true, extensions:[Notification-T]}
Registry --> Server : 201 Created
Server -> SDK : A2ATServer(env_path)
SDK --> Server : prompt_server 就绪
Server -> Server : uvicorn 监听 127.0.0.1:8000

== 终端3: 启动客户端 ==
Client -> Registry : GET /rest/v1/registry-center/agent-cards/\nSampleOrg/A2A-T Subscribe Incident Sample
Registry --> Client : 200 {agentCards:[{url:8000}]}
Client -> SDK : A2ATClient(env_path)
SDK --> Client : prompt_client 就绪
Client -> SDK : ClientFactory.create(agent_card)
SDK --> Client : a2a_client (streaming=True)

== Prompt 生成 (客户端) ==
Client -> SDK : prompt_client.generate_task_prompt(scenario_data)
SDK -> SDK : 根据 scenario 选模板\n渲染 slot 值
SDK -> LLM : 场景识别 + slot 提取
LLM --> SDK : prompt_text (## 订阅描述...)
SDK --> Client : PromptGenerationResult(prompt_text)

== 发送请求 + Prompt 校验 (服务端) ==
Client -> Server : POST /message:stream\nHeaders: A2A-Extensions: Notification-T\nBody: SendMessageRequest(prompt_text)

Server -> SDK : prompt_server.check_task_prompt(prompt_text)
SDK -> LLM : 1. 场景识别
LLM --> SDK : {matched:true, scenario_code:"subscribe_incident"}
SDK -> LLM : 2. Slot 提取
LLM --> SDK : {slots:{订阅条件:"故障优先级为:critical..."}}
SDK -> LLM : 3. 语义校验
LLM --> SDK : {passed:true, errors:[]}
SDK --> Server : PromptComplianceResult(success=true)

== 流式推送 artifact ==
Server --> Client : StreamResponse(task: SUBMITTED)
Server --> Client : StreamResponse(status_update: WORKING)
loop 每 5 秒推送一个 Incident artifact
    Server --> Client : StreamResponse(artifact_update)\n{name:"LASER_MOD_ERR",...}
end
Server --> Client : StreamResponse(status_update: COMPLETED)
Client -> SDK : normalize_event(stream_response)
SDK --> Client : {kind:"artifact", ...}
Client -> Client : stream-completed\nevents=N artifacts=N
@enduml
```

## 流程说明

| 阶段 | 谁调 SDK | SDK 做什么 | LLM 调用次数 |
|------|---------|-----------|-------------|
| 启动 | client + server | A2ATClient / A2ATServer 初始化 | 0 |
| Prompt 生成 | 客户端 | 场景识别 + slot 提取 + 模板渲染 | 2 |
| Prompt 校验 | 服务端 | 场景识别 → slot 提取 → 语义校验 | 3 |
| 流式推送 | 客户端 | normalize_event 归一化 stream 事件 | 0 |

## Mock LLM

当 `A2AT_LLM_API_KEY` 为空时，sample 自动使用 `resources/mock_responses/` 下的预置响应数据，无需真实 API key 即可跑通完整流程。Mock 响应按语言（`zh-CN` / `en-US`）分目录，与 `.env` 中的 `A2AT_LANGUAGE` 对应。

## 关键点

- **SDK 是中间层**：client/server 不直接调 LLM，通过 SDK 的 A2ATClient/A2ATServer 间接调用
- **LLM 只在 prompt 阶段用**：推送 artifact 时不调 LLM
- **无协商**：客户端一次性提交完整输入，服务端校验通过直接推送
- **接收控制**：设 `A2AT_SAMPLE_MAX_ARTIFACTS` 限制接收数量；不设则持续接收（Ctrl+C 停）
- **三层解耦**：client（发现 + 消费）→ server（注册 + 推送）→ registry（注册中心）

## 运行测试

```bash
uv run pytest a2a-t-sample/test/ -v
```
