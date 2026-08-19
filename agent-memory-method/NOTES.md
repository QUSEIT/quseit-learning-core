## 改进日志

### 2026-08-19（部署）
- 来源：https://github.com/QUSEIT/quseit-learning-core/tree/main/agent-memory-method
- 版本：0.10.0，仅含 SKILL.md
- 部署时在 frontmatter 的 `metadata.hermes` 下加了 `deployed_from` 字段记录来源

### 2026-08-19（改进 v0.10.1）
- 删除 `requires_tools` 及相关 `Public Skill Contract` 中的工具声明，改为纯对话技能
- `standalone_support` 从 `needs_user_input` 升级为 `full`
- 展开工作流：每步给出具体操作指引和数量约束（记忆块 ≤ 20字/个，复习节点 5 个固定日期等）
- 增加 2 个完整示例（古诗词 + 英语单词），含输入+输出对照
- 重写 Quality Checks 为 5 条可验证标准
- 添加"调用信号"：明确触发关键词 + 路由排除规则（→ agent-question-explanation、agent-mistake-review）
- `requires_data` 改为具体说明：纯文本粘贴 + 年级 + 截止时间（可选）+ 掌握程度（可选）
