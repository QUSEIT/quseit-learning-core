# agent-photo-question 测试集

本目录包含 `agent-photo-question` 技能的自动化测试，验证 **SKILL.md 的
结构完整性、契约正确性与质量约束的落地情况**。

## 测试分层

| 层 | 覆盖内容 | 依赖 | 默认 |
|----|---------|------|------|
| **STATIC**（静态） | YAML frontmatter 合法性、工具引用、输出 JSON Schema 完整性、变式题四条质量约束、年级分级表四档、追问协议、Fallback 四场景、卡点采集三问、工作流五步闭环 | 仅 `pyyaml` | ✅ 运行 |
| **DYNAMIC**（动态） | `vision_analyze` 调用、LLM 输出是否符合 Schema | Hermes 实机会话 + 真实图片 | ⏭️ 跳过 |

## 运行

```bash
# 静态测试（离线可跑）
cd <skill_dir>/tests
python -m unittest discover -v

# 动态测试（需 Hermes 实机 + 用户提供图片路径）
RUN_DYNAMIC=1 TEST_IMAGE_PATH=<图片路径> python -m unittest discover -v

# 仅运行动态测试
RUN_DYNAMIC=1 python -m unittest test_skill.TestDynamicBehavior -v
```

> 动态测试默认跳过：它们需要真实 LLM 推理与用户上传的题目图片，
> 无法在纯 CI / 无会话环境中可靠执行。

## 测试清单（41 项静态 + 4 项动态）

- **TestFrontmatter**（14）：frontmatter 可解析、必填字段、semver、
  requires_tools 只含 Hermes 内置工具、无 `vision.ocr_question` 幽灵引用、
  调用信号含意图关键词
- **TestWorkflow**（6）：工作流图示、五步闭环、追问协议、Fallback 四场景
- **TestOutputSchema**（8）：输出格式含 JSON Schema、recognition /
  solution / follow_up / variation 四块、confidence 为 float、
  difficulty 为枚举
- **TestQualityConstraints**（8）：变式题四条质量约束、拒绝行为、
  年级分级表四行、卡点采集三问
- **TestCompleteness**（1）：全部必需章节存在
- **TestDynamicBehavior**（4，默认跳过）：vision_analyze 输出、
  Schema 合规、追问触发、变式题质量

## 维护提示

- `extract_section()` 使用 `\n\n## ` / `\n\n### ` 边界切分章节；
  新增章节时请保持 heading 独占一行、前后有空行。
- 测试与 SKILL.md 强耦合：改 SKILL.md 的章节标题 / Schema 字段时，
  同步更新本目录对应断言。
