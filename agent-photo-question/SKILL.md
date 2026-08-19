---
name: "agent-photo-question"
description: "把拍照题目转成先识题、再讲思路、最后追问确认的学习过程，而不是只给答案。 Workflow: agent_photo_question.run."
version: "0.12.0"
author: zhongwei
license: MIT
platforms: [windows, linux, macos]
last_updated: "2026-08-18"
metadata:
  hermes:
    tags: ["education", "primary", "junior", "senior", "综合", "AI 讲题", "图片识题", "拍照答疑", "课后作业"]
    source: hermes-edu-skills
    workflow: "agent_photo_question.run"
    category: "learning-core"
    stages: ["primary", "junior", "senior"]
    subjects: ["综合"]
    abilities: ["AI 讲题", "图片识题"]
    scenarios: ["拍照答疑", "课后作业"]
    quality_tier: "curated"
    standalone_support: "requires_tools"
    public_release: "recommended"
    export_mode: "installable"
    release_channel: "recommended"
    requires_tools: ["vision_analyze"]
    requires_data: ["题目图片或用户转写的题干", "学生年级", "学科"]
    feedback_channel: "https://github.com/hezkvectory/hermes-edu-skills/issues"
---

# 拍照答疑 Skill

把拍照题目转成先识题、再讲思路、最后追问确认的学习过程，而不是只给答案。

## 这个 Skill 解决什么问题 / Problem

把拍照题目转成先识题、再讲思路、最后追问确认的学习过程，而不是只给答案。

## 最适合 / Best For

- 学生或家长拍题求讲解
- 题干较长、需要拆条件的题
- 需要生成同类题巩固的场景

## 不适合 / Not For

- 考试作弊或实时替考
- 图片严重模糊且用户无法补充题干

## 使用前请准备 / Inputs

- 题目图片或完整题干
- 年级/学段
- 学科
- 学生卡住的位置（可参考下方引导采集）

## 卡点采集引导 / Stuck Point Elicitation

如果用户只说"不会"，请按以下顺序追问：

1. **"这道题读完，你最先想到的是什么？"**（激活前测，了解直觉反应）
2. **"是题目读不懂，还是知道什么意思但不知道怎么做？"**（诊断卡点类型）
3. **"你之前做过类似的题吗？"**（调用相关已学知识，建立联系）

若用户无法描述卡点，技能仍可继续——以"完整讲解"模式工作，不强制采集卡点信息。

## 推荐工作流 / Recommended Workflow

```
用户发图
  ↓
vision_analyze 识别题干
  ↓
[置信度 < 0.7？] → 是 → 标注不确定内容，请用户确认后继续
  ↓
[有选项？] → 是 → 选项反推验证（见下方说明）
  ↓
  └─ [反推与识别矛盾？] → 是 → 前置澄清关键结构/条件 → 等待用户确认
  ↓
按年级讲解深度（见下方分级参考）讲解
  ↓
追问确认（见追问协议）
  ↓
给出同类变式题（需满足质量约束）
  ↓
变式题附完整解答，供用户自行核对
```

### 选项反推验证（新增）

当题目包含选项（如选择题、判断题）时，在讲解前必须执行**选项反推验证**：

1. **提取选项关键数值**：从选项中识别起止值、转折点、比例等关键物理/数学参数
2. **反推可能结构**：根据选项数值反推可能的系统参数（如滑轮组绳子股数 n、初始重力、末态重力等）
3. **交叉比对**：将反推结果与 vision_analyze 的结构识别结果进行比对
   - **一致** → confidence += 0.2，继续讲解
   - **矛盾** → 触发前置澄清（见追问协议），请用户确认关键结构细节，等待确认后再讲解

**适用题型：** 物理力学题（滑轮组、杠杆、电路）、几何题（相似三角形比例）、函数题（参数图像）等结构依赖性强的题目。

**示例：**
- 选项起点为 2G，推导需 n=1；但识别为动滑轮 n=2 → 矛盾 → 澄清："选项 B 的起点是 2G，这与我的推导有矛盾，请确认：C 是直接挂在绳子上，还是挂在动滑轮下面？"

## 输出格式 / Output Format

### 结构化输出 Schema

```json
{
  "recognition": {
    "stem": "题目原文（识别到的完整题干）",
    "conditions": ["条件1", "条件2"],
    "question": "求解目标",
    "confidence": 0.93,
    "uncertain_parts": ["部分手写体识别存疑"],
    "needs_user_confirm": true
  },
  "grade_context": {
    "grade": "五年级",
    "explanation_depth": "小学4-6年级",
    "style": "半抽象，可引入符号"
  },
  "solution": {
    "method": "所用方法/公式",
    "steps": [
      {"step": 1, "action": "描述动作", "why": "这一步为什么要这样做"},
      {"step": 2, "action": "描述动作", "why": "这一步为什么要这样做"}
    ],
    "common_mistakes": ["易错点1", "易错点2"]
  },
  "follow_up": {
    "triggered": true,
    "question": "你觉得下一步该怎么做？",
    "user_response": null,
    "attempts": 0
  },
  "variation": {
    "stem": "变式题题干",
    "answer": "变式题完整解答",
    "difficulty": "标准",
    "knowledge_point_match": "与原题同属XX知识点"
  }
}
```

### 追问确认协议 / Follow-up Protocol

#### 前置澄清（讲解前触发）

**触发条件（满足任一即触发）：**
1. vision_analyze 置信度 < 0.8
2. 有选项且**选项反推与识别结果矛盾**
3. 关键结构细节模糊（如滑轮类型、绳子走法、电路连接方式）

**澄清方式：**
- 描述矛盾点："我看到 X，但选项 Y 暗示 Z，请帮我确认：..."
- 要求用户确认关键结构细节（如"是有动滑轮还是只有定滑轮？"）
- **必须等待用户确认后，才能进入讲解阶段**

#### 后置确认（讲解后触发）

- **触发时机：** 讲解完成后，主动发起
- **形式：** 开放式问题（如"你觉得下一步该怎么做？"）
- **用户回答正确：** 肯定并过渡到变式题
- **用户回答错误（≤3次）：** 给出提示而非直接纠正，等待再次尝试
- **连续 3 次错误：** 给出完整答案，说明"卡在第 X 步"，不指责用户
- **无用户反馈：** 超时后自动过渡到变式题，注明"用户未回应追问"

## 变式题质量约束 / Variation Quality Rules

生成变式题时必须同时满足：

- ✅ 与原题属于**同一知识点**（引用同一定理/公式）
- ✅ 答案**可独立验证**（非开放性问题）
- ✅ 难度波动不超过 ±1 级（基础↔标准↔提高）
- ✅ 附**完整解答**，供用户自行核对

若无法满足以上约束，**不得输出变式题**，改为："这道题已掌握，建议通过同类型作业题自行练习。"

## 年级讲解深度参考 / Grade Explanation Depth

| 年级段 | 讲解风格 | 示例语言 |
|--------|---------|---------|
| 小学1-3年级 | 具象类比，图形化 | "就像把苹果分成两堆，左边有3个，右边有2个…" |
| 小学4-6年级 | 半抽象，可引入符号 | "我们用□代替未知数，先把已知的数填进去…" |
| 初中7-9年级 | 符号化，完整格式 | "设 x 为…，根据题意列方程：…" |
| 高中 | 数学语言，逻辑严格 | "由已知条件可得…，根据定理一，有…" |

## 质量检查 / Quality Checks

**通用检查：**
- 不得只输出答案
- 识别不确定时必须标注（`uncertain_parts`）
- 讲解风格必须匹配年级段（见上方分级参考）
- 避免诱导未成年人消费或泄露隐私
- 变式题必须通过质量约束检查后方可输出

**选项反推检查（新增）：**
- [ ] 有选项时，已提取关键数值（起止值、转折点、比例等）
- [ ] 已反推可能的系统参数（如 n 值、初始重力、末态重力）
- [ ] 反推结果与 vision_analyze 识别结果已交叉比对
- [ ] 若矛盾，已触发前置澄清并等待用户确认
- [ ] 确认后，讲解使用的是用户确认的正确结构

**前置澄清检查（新增）：**
- [ ] 触发条件满足时（置信度 < 0.8 或矛盾或结构模糊），已发起澄清
- [ ] 澄清等待用户响应，未强行讲解
- [ ] 讲解使用的结构参数与用户确认的一致

## 没有平台工具时 / Standalone Fallback

| 场景 | 处理方式 |
|------|---------|
| `vision_analyze` 不可用 | 请用户手动输入题干，技能转为纯文字讲解模式 |
| 识别置信度 < 0.7 | 标注不确定内容，请用户确认后再继续 |
| 图片严重模糊 | 引导用户换角度重拍，或切换为手动输入题干 |
| 无练习工具 | 由 Agent 生成变式题，但必须通过质量约束检查 |

## 示例提示 / Example Prompts

- 我把数学题文字贴给你，请按五年级水平讲解。
- 这道物理题我卡在受力分析，帮我拆条件。
- 帮我看看这道题，我完全不知道从哪下手。

## 适用场景 / When To Use

当学习者、家长、老师、学校或教育应用开发者需要处理以下场景时，可以使用这个 Skill。

最适合的场景：
- 拍照答疑
- 课后作业

适用角色：
- 学习者
- 家长

## 调用信号 / Invocation Signals

意图：
- `agent_photo_question`
- `learning_core`
- `拍照答疑`
- `课后作业`

示例表达：
- 开始拍照答疑 Skill
- 帮我做拍照答疑
- 根据当前上下文执行拍照答疑 Skill

## 公开 Skill 契约 / Public Skill Contract

- Workflow: `agent_photo_question.run`
- Category: `learning-core`
- Stages: `primary`, `junior`, `senior`
- Subjects: `综合`
- Abilities: `AI 讲题`, `图片识题`
- Quality Tier: `curated`
- Standalone Support: `requires_tools`
- Public Release: `recommended`
- Requires Tools: `vision_analyze`
- Requires Data: `题目图片或用户转写的题干`, `学生年级`, `学科`
- Export Mode: `installable`
- Release Channel: `recommended`

## 参数化使用 / Parameters

这个 Skill 不再把年级、册别、单元、知识点和难度拆成大量独立 Skill。请在调用时通过参数或自然语言补充这些信息。

- Grades: `一年级`~`高三`（共12个年级）
- Semesters: `上册`, `下册`, `必修一`, `必修二`, `选择性必修`
- Scenarios: `拍照答疑`, `课后作业`
- Difficulties: `基础`, `标准`, `提高`
- Parameterized Dimensions: `grade`, `semester`, `unit`, `lesson`, `knowledgePointCodes`, `scenario`, `difficulty`

## 独立 Hermes 使用方式 / Standalone Hermes Usage

这个 Skill 可以通过 Hermes 的 `skills.external_dirs` 作为外部 Skill 加载。

如果你有自己的工具、记忆、课程数据或 workflow runner，可以把它们与本 Skill 组合使用。如果没有外部工具，也可以直接使用上面的说明来引导对话，生成有用的学习或教学反馈。
