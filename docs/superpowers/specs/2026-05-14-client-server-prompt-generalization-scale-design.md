# 客户端生成与服务端校验泛化扩样实验设计
日期：2026-05-14

## 1. 背景

当前仓库已经具备一套真实可执行的客户端到服务端泛化验证链路：

- 客户端从自然语言输入生成 `processed_prompt_text`
- 服务端对 `processed_prompt_text` 执行场景识别、槽位提取、JSON Schema 校验与语义校验
- 现有基础实验覆盖 3 个业务场景、24 条样本，重点验证同义改写与语序扰动下的链路稳定性

最近一次基础泛化回归已经验证了这 24 条样本在当前 prompt 与 `slot.json` 条件下可全部通过。因此，下一步不再是确认链路是否可用，而是提升样本量，继续验证泛化能力，重点观察：

1. 客户端对更广泛自然语言表达的提取与生成是否稳定
2. 服务端对客户端生成 prompt 的放行与拦截是否稳定
3. 不同类型扰动下，问题主要集中在客户端还是服务端

## 2. 目标

- 在当前 3 个真实业务场景上，将泛化实验从 24 条扩展到 270 条
- 同时覆盖 3 类泛化维度：
  - 词面改写
  - 结构扰动
  - 值域替换
- 将结果按实验条件归档，便于后续按场景、按扰动类型、按失败环节复盘
- 保持实验样本“应当通过”的判断边界清晰，避免因为样本定义不严导致分析失真

覆盖场景固定为：

- `subscribe_incident`
- `private_line_complaint`
- `energy_saving`

## 3. 非目标

- 不在本轮引入新的业务场景
- 不在本轮覆盖明确非法值、对抗输入或跨场景混淆输入
- 不在本轮直接修改业务代码、prompt 或 `slot.json`
- 不把实验样本与业务 UT 混在一起提交
- 不追求一次性穷举所有表达方式，而是优先建立有分层、有统计意义的扩样基线

## 4. 设计原则

- 先分层，再混合。避免一次把多种扰动揉在一起，导致失败原因不可定位。
- 先验证表达泛化，再验证值域泛化，最后验证组合泛化。
- 样本设计优先保证“语义等价且应当通过”的判断明确。
- 结果记录必须保留客户端与服务端两个阶段的输入输出证据。
- manifest 与结果文件不能平铺，必须按实验条件组织目录。

## 5. 方案选择

本轮考虑 3 种扩样方式：

### 方案 A：分层扩样，逐层放量

先拆为三组实验：

- `lexical_structure`
- `value_substitution`
- `hybrid_generalization`

每组独立建 manifest、独立执行、独立统计。

优点：

- 失败原因最容易定位
- 可直接区分“表达问题”和“值域问题”
- 便于后续只重跑某一组

缺点：

- manifest 与结果目录会更多
- 前期样本组织成本略高

### 方案 B：一次性混合扩样

将三类扰动混成一批大样本，统一执行。

优点：

- 跑数最快
- 能快速得到总体通过率

缺点：

- 可解释性差
- 一旦失败，很难判断是词面、结构还是值域导致

### 方案 C：按场景逐个扩样

先深挖 `subscribe_incident`，再扩其他场景。

优点：

- 风险最低
- 适合先聚焦最敏感场景

缺点：

- 三个场景的横向结论出来慢
- 不利于快速形成统一统计口径

### 选型结论

采用方案 A：分层扩样，逐层放量。

原因：

- 当前诉求不是单纯“多跑一些”，而是要继续验证泛化能力，并能看清问题落点
- 现有链路已经稳定，下一阶段核心是拿到更高解释力的实验结果
- 分层设计最利于后续决定是继续调 prompt、调 `slot.json`，还是补客户端提取策略

## 6. 总体规模设计

总规模定为 270 条：

- 3 个场景
- 3 组实验
- 每个场景每组 30 条

公式：

`3 场景 x 3 组实验 x 30 条 = 270 条`

## 7. 三组实验定义

### 7.1 lexical_structure

目的：只验证表达形式变化，不改变核心槽位值。

每个场景 30 条，拆为 3 个子桶：

- `lexical` 10 条
- `reorder` 10 条
- `noise` 10 条

其中：

- `lexical`：同义改写、口语化、书面化、祈使句与陈述句切换
- `reorder`：槽位换位、前后倒装、先结果后条件、跨分句重排
- `noise`：插入礼貌语、解释性短语、无害修饰语，但不引入新约束

### 7.2 value_substitution

目的：固定句式骨架，验证值域替换后的客户端提取与服务端校验。

每个场景 30 条，拆为 3 个子桶：

- `core_value_swap` 10 条
- `alias_or_surface_form` 10 条
- `weak_anchor` 10 条

其中：

- `core_value_swap`：替换主要业务值，例如告警名、区域名、资源标识等
- `alias_or_surface_form`：中英混写、缩写、不同表述方式
- `weak_anchor`：时间、范围、量纲等弱锚定表达替换

说明：

- `weak_anchor` 仅用于“当前业务允许弱锚定表达”的槽位
- 如果某场景某槽位不适合弱锚定，则该子桶可改为其他表层值域替换，但仍需保持 10 条规模

### 7.3 hybrid_generalization

目的：同时验证表达变化与值域替换叠加时的稳定性。

每个场景 30 条，拆为 3 个子桶：

- `lexical_value` 10 条
- `reorder_value` 10 条
- `noise_value` 10 条

要求：

- 每条样本至少同时包含一种表达层扰动和一种值域层扰动
- 不引入跨场景意图，不制造本应失败的非法样本

## 8. 各场景扩样侧重点

### 8.1 subscribe_incident

重点验证：

- 告警名或故障名的泛化，例如英文标识符、缩写风格、不同表述顺序
- 优先级的中英表达与位置变化
- 可选订阅条件在“有值”和“无值”两种情况下的稳定性
- `DataPart` 及其表层表达变化

额外要求：

- 合法样本不能因为可选条件缺失而被定义为失败
- 合法样本如果填写了可选条件，则填写内容应与场景意图一致

### 8.2 private_line_complaint

重点验证：

- 资源 ID、故障现象、故障时间、故障流水号在不同句位中的提取稳定性
- “投诉诊断 / 根因分析 / 定位原因 / 输出修复建议”等表达变化
- 任务上下文与结果要求前后调换后的稳定性

### 8.3 energy_saving

重点验证：

- 区域、节能目标、速率保障目标、制式、频点、时段等槽位的多表达形式
- 目标与约束交错表达时的稳定性
- “体验无损 / 不影响用户体验 / 业务不掉速”等近义表达

## 9. 样本组织规则

### 9.1 分桶原则

每个场景每组固定 30 条，每个子桶固定 10 条，避免样本分布失衡。

### 9.2 case id 规则

统一命名为：

`<scenario>_<group>_<bucket>_<seq>`

例如：

- `subscribe_incident_lexical_structure_lexical_01`
- `private_line_complaint_value_substitution_core_value_swap_07`
- `energy_saving_hybrid_generalization_noise_value_10`

### 9.3 样本约束

所有样本必须满足：

1. 场景意图明确且唯一
2. 属于“应当通过”的合法输入
3. 扰动类型与所属分桶一致
4. 不新增会改变业务决策的新约束

## 10. manifest 与目录设计

### 10.1 manifest 目录

按实验条件建目录，不平铺：

- `docs/superpowers/analysis/client_to_server_generalization/manifests/scale_270/`

本轮至少包含 3 份 manifest：

- `all_scenarios_lexical_structure_20260514.json`
- `all_scenarios_value_substitution_20260514.json`
- `all_scenarios_hybrid_generalization_20260514.json`

### 10.2 结果目录

沿用现有结果归档风格，在 `all_scenarios` 下按实验组区分：

- `.../all_scenarios/lexical_structure/...`
- `.../all_scenarios/value_substitution/...`
- `.../all_scenarios/hybrid_generalization/...`

建议完整层级为：

`docs/superpowers/analysis/client_to_server_generalization/all_scenarios/<group>/<provider>__<model>/<prompt_tag>/<run_id>/`

### 10.3 结果文件

每批结果目录至少包含：

- `manifest.json`
- `result_detail.json`
- `result_summary.json`
- `notes.md`

其中：

- `manifest.json`：记录本次实验条件与样本清单
- `result_detail.json`：记录逐条样本明细
- `result_summary.json`：记录统计汇总
- `notes.md`：记录人工观察、异常样本、可疑波动

## 11. 执行链路

每条样本统一走以下链路：

1. 将 `raw_input` 输入客户端
2. 客户端执行场景识别、槽位提取与 prompt 生成
3. 记录客户端输出，包括场景、槽位与 `processed_prompt_text`
4. 将客户端输出的 `processed_prompt_text` 送入服务端校验
5. 记录服务端最终校验结果，以及失败阶段与失败码

本轮实验重点不是只拿到最终通过率，而是保留足够的中间证据，能够回答：

- 客户端是否识别错场景
- 客户端是否提取错槽位
- 客户端是否在生成 prompt 时丢失语义
- 服务端是否对合法 prompt 误拦截

## 12. 通过标准与统计口径

### 12.1 单条样本通过标准

单条样本通过需同时满足：

1. 客户端成功生成 prompt
2. 客户端识别出的场景等于预期场景
3. 客户端关键槽位与样本预期一致
4. 服务端成功通过校验

### 12.2 汇总统计口径

至少输出以下维度：

- overall pass rate
- per-scenario pass rate
- per-group pass rate
- per-bucket pass rate
- client failure count
- server failure count
- failure inventory

其中 `failure inventory` 需要区分：

- 客户端失败
- 服务端失败
- 失败对应的场景、实验组、子桶、case id

## 13. 推荐执行顺序

推荐严格按以下顺序实施：

1. 先补 3 份 manifest，不改业务代码
2. 先跑 `lexical_structure`
3. 再跑 `value_substitution`
4. 最后跑 `hybrid_generalization`
5. 汇总结论后，再决定是否需要优化 prompt 或 `slot.json`

这样做的价值是：

- 如果第一组就出现明显问题，可以先在表达层定位
- 如果前两组稳定、第三组掉点，则更可能是组合复杂度问题
- 便于控制真实 LLM 跑数成本与排障成本

## 14. 风险与限制

- 270 条真实运行会增加执行时间与模型调用成本
- 部分结果仍受 LLM 非确定性影响，必要时需要重复运行确认稳定性
- 不同 `slot.json` 版本、prompt 版本、模型版本会影响可比性，因此结果必须严格按实验条件归档
- 若某些值域替换超出当前场景自然边界，可能引入“样本定义问题”而非“系统问题”，因此样本编写需要人工把关

## 15. 验收标准

满足以下条件即可视为本轮设计可进入实现阶段：

1. 能基于当前 3 个业务场景组织出 3 份扩样 manifest
2. 总样本规模达到 270 条，且分组、分桶规模符合设计
3. 结果目录按实验条件归档，不发生平铺覆盖
4. 结果记录可区分客户端失败与服务端失败
5. 汇总结果可按场景、按实验组、按子桶分析泛化表现
