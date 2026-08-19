# quseit-learning-core

面向 K12 的 AI 学习技能集合，把建构主义、主动提取、间隔复习等教学法翻译成 Agent 可执行的规则。

## 技能一览

| 技能 | 版本 | 功能 | 依赖工具 |
|------|------|------|----------|
| [agent-memory-method](./agent-memory-method) | 0.10.1 | 把记忆内容转化为可提取、可复述、可间隔复习的记忆任务 | 无 |
| [agent-mistake-review](./agent-mistake-review) | 0.10.0 | 错题分析、找错因、提炼错误模式、安排复习 | 无 |
| [agent-photo-question](./agent-photo-question) | 0.12.0 | 拍照识题、先讲思路再追问、生成同类变式题 | vision_analyze |
| [agent-question-explanation](./agent-question-explanation) | 0.10.0 | AI 讲题：先定位卡点，用年级语言拆解，变式确认 | 无 |

## 适用学段

- 小学（primary）
- 初中（junior）
- 高中（senior）

## 安装方式

在 Hermes 配置中添加外部技能目录：

```yaml
skills:
  external_dirs:
    - C:/path/to/quseit-learning-core
```

或在 Hermes 桌面端通过 `skills.external_dirs` 加载本仓库。

## 许可证

全集合采用 [MIT](./LICENSE) 许可证。

- agent-memory-method: MIT (c) 2026 zhongwei
- agent-mistake-review: MIT (c) 2024 zhongwei
- agent-photo-question: MIT (c) 2024 zhongwei
- agent-question-explanation: MIT (c) 2024 zhongwei

## 贡献与反馈

欢迎提交 Issue 和 Pull Request：

- [Issue 反馈](https://github.com/QUSEIT/quseit-learning-core/issues)
- [Pull Request](https://github.com/QUSEIT/quseit-learning-core/pulls)

---
