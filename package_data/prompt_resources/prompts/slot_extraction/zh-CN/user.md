根据下方提供的 slot schema 和模板，从归一化输入中提取 slot 值。

## 执行顺序
1. 先判断候选内容是否属于“用户明确要求写入任务”的约束。
2. 若候选内容只是背景、示例、模板说明、风格要求或元任务说明，则不提取。
3. 若候选内容处于否定或排除语义（如“不要/不是/非/排除”）中，则不提取为正向值。
4. 仅将与 slot `description` / `value_constraint` 明确对应的内容归入该 slot。
5. 对同一 slot 的多个明确并列约束，尽量完整保留。
6. 拿不准时返回 `null`，不要猜测或补全默认值。

## 错误处理
- 必填 slot 无法提取：值设为 null，报告 code="missing_input"
- 可选 slot 无法提取：值设为 null，无需错误
- 值违反 value_constraint：值设为 null，报告 code="invalid_value"

## 输出示例
```json
{
  "slots": {
    "subscription_condition_incident_name": "[\"eth-los\"]",
    "subscription_condition_incident_level": "[\"critical\", \"major\"]"
  },
  "slot_errors": []
}
```

现在处理输入并返回提取结果。
