# agent-memory-method

A Hermes Agent skill for transforming content that needs to be memorized (poems, vocabulary, formulas, historical facts) into structured memory tasks — replacing mechanical repetition with active retrieval and spaced repetition.

> **记忆不是朗读次数，而是提取次数。** — The more you retrieve, the better you retain.

---

## Why this skill exists

Most memorisation attempts fail because they rely on passive re-reading:

1. Reading the same text 10 times feels like progress — it isn't.
2. There's no retrieval practice until the exam.
3. All review happens at once (cramming) instead of spaced over time.

This skill enforces three evidence-based principles:

| Principle | Effect |
|---|---|
| **Active retrieval** | Extract before review — tests beat re-reads |
| **Spaced repetition** | Review at expanding intervals — 1d / 3d / 7d / 14d / 30d |
| **Chunking** | Break content into ≤ 20-char blocks — working memory friendly |

---

## What it produces

For any input (poem / word list / formula /知识点), the skill outputs:

1. **Memory blocks** — content split into retrievable chunks
2. **Extraction questions** — 1 fill-in + 1 open question per block
3. **First-session steps** — read 3× → retrieve blind → correct → retrieve again
4. **Spaced review table** — 5 nodes with specific dates and formats
5. **Self-test** — 3 questions (1 fill-in / 1 QA / 1 T-F), tagged by block

---

## Repository layout

```
agent-memory-method/
├── README.md          ← this file
├── LICENSE            ← MIT
├── SKILL.md           ← skill definition, workflow, quality checklist
├── NOTES.md           ← improvement log
└── tests/
    └── test_skill.py  ← stdlib unittest suite (python -m unittest discover -s tests -v)
```

---

## Installation

Copy or clone this repository into your Hermes skills directory:

```text
C:\Users\<you>\AppData\Local\hermes\skills\learning-core\agent-memory-method\
```

Or via `skills.external_dirs` in your Hermes config:

```yaml
skills:
  external_dirs:
    - C:\path\to\agent-memory-method
```

Restart Hermes (or start a new session) so the skill index reloads.

No Python dependencies required — this is a **pure dialogue skill** with no scripts.

---

## Quick start

Tell Hermes what you need to memorise:

```
帮我背《春望》，五年级，下周考试。第三联总是想不起来。
```

The skill responds with a complete memory plan: blocks, extraction questions, first-session steps, a 5-node review table, and a 3-question self-test.

---

## Asking Hermes to use it

When the skill is installed, Hermes recognises prompts like:

> *用记忆方法帮我背这首古诗。*

> *这些英语单词总是记不住，帮我做记忆卡和复习计划。*

> *用艾宾浩斯曲线安排公式复习。*

Trigger keywords: `记忆方法`, `背诵记忆`, `记忆卡`, `复习计划`, `艾宾浩斯`, `间隔复习`, `背下来`, `记住`

---

## Inputs

| Field | Required | Notes |
|---|---|---|
| Content to memorise | ✅ | Paste the raw text directly |
| Grade / level | ✅ | e.g. "三年级", "高一" |
| Deadline | ❌ | e.g. "下周考试" |
| Known parts | ❌ | e.g. "一二句能背，第三联老忘" |
| Weak spots | ❌ | e.g. "单词拼写容易混" |

All fields can be provided in natural language — no structured form required.

---

## Output quality gates

Every output from this skill must satisfy all five gates:

1. **Active retrieval** — extraction questions (fill-in or QA) are present, not just the text to memorise
2. **Review nodes ≥ 4** — at least four spaced review dates are listed
3. **Steps are actionable** — each block has a read × blind-retrieve → correct → retrieve-again sequence
4. **Understand vs memorise** — the output distinguishes parts that need comprehension first from pure memorisation
5. **Block cap ≤ 10 per session** — if content exceeds 10 blocks, the skill prompts the user to split it

---

## Limitations

| Situation | Recommendation |
|---|---|
| Content > 500 characters | Split into batches |
| Completely unfamiliar material | Use `agent-question-explanation` first, then return here |
| Non-text content (images, audio, motor skills) | This skill is text-only |
| Single-session cramming | The spaced-repetition output won't help in this case |

---

## Relationship to other learning-core skills

| Skill | What it does | When to use instead |
|---|---|---|
| `agent-question-explanation` | Explain concepts, find confusion points | User asks "这首诗什么意思" or "这道题怎么做" |
| `agent-mistake-review` | Review past errors with spaced repetition | User has wrong-answer records to revisit |
| `agent-photo-question` | Solve a photographed question | User uploads an image of a problem |
| `agent-memory-method` | Build memory blocks + spaced review | User needs to memorise / retain content |

---

## Testing

```bash
python -m unittest discover -s tests -v
```

42 tests covering: frontmatter validity, section completeness, workflow expansion, example quality, invocation signal specificity, input constraint enforcement, and self-consistency.

---

## License

MIT — see [LICENSE](LICENSE).

## Author

zhongwei (via hermes-edu-skills)
