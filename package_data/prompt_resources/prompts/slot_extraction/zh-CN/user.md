根据下方提供的 slot schema 和模板，从归一化输入中提取 slot 值。

## 执行顺序
1. 先判断候选内容是否属于“用户明确要求写入任务”的约束。
2. 若候选内容只是背景、示例、模板说明、风格要求或元任务说明，则不提取。
3. 若候选内容处于否定或排除语义（如“不要/不是/非/排除”）中，则不提取为正向值。
4. 若输入中出现显式字段锚点，优先按字段锚点后的内容映射到对应 slot。
5. 显式字段锚点可以表现为 slot 名称本身，或与 slot `description` 语义明确对应的字段标签，并常见于“字段名 + 为 / 是 / ： / : / 包括 / 包含”等结构，以及分段式、列表式字段标签。
6. 对显式字段锚点后的值，即使它与场景默认语义或模板固定文案重复，也不要省略。
7. 仅将与 slot `description` / `value_constraint` 明确对应的内容归入该 slot。
8. 对同一 slot 的多个明确并列约束，尽量完整保留。
9. 拿不准时返回 `null`，不要猜测或补全默认值。

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
