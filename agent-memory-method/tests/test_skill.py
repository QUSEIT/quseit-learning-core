"""
Tests for agent-memory-method skill (learning-core).

This skill is a pure-dialogue skill: it has no scripts, only SKILL.md.
Tests validate:
1. SKILL.md loads without errors and has valid frontmatter
2. requires_tools is absent (no external tool dependencies)
3. All required content sections are present
4. Quality Checks are specific and verifiable (not vague)
5. Workflow steps are expanded with concrete constraints
6. Examples include both input AND expected output
7. Invocation Signals include trigger keywords AND exclusion rules
8. Input/output constraints are satisfied (memory block size, review nodes, etc.)
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

import yaml

# Resolve SKILL.md path relative to this file
SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_frontmatter() -> dict:
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Strip markdown body, parse YAML frontmatter only
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found in SKILL.md")
    return yaml.safe_load(match.group(1))


def load_full_content() -> str:
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Test: Frontmatter structure
# ---------------------------------------------------------------------------


class FrontmatterTest(unittest.TestCase):
    def test_skill_file_exists(self):
        self.assertTrue(SKILL_PATH.exists(), f"SKILL.md not found at {SKILL_PATH}")

    def test_frontmatter_loads(self):
        fm = load_frontmatter()
        self.assertIsInstance(fm, dict)
        self.assertIn("name", fm)
        self.assertIn("metadata", fm)

    def test_name_correct(self):
        fm = load_frontmatter()
        self.assertEqual(fm["name"], "agent-memory-method")

    def test_category_is_learning_core(self):
        fm = load_frontmatter()
        self.assertEqual(fm["metadata"]["hermes"]["category"], "learning-core")

    def test_standalone_support_is_full(self):
        fm = load_frontmatter()
        self.assertEqual(fm["metadata"]["hermes"]["standalone_support"], "full")

    def test_no_requires_tools(self):
        """requires_tools must be absent or empty — this is a pure dialogue skill."""
        fm = load_frontmatter()
        requires_tools = fm.get("metadata", {}).get("hermes", {}).get("requires_tools", None)
        self.assertIsNone(
            requires_tools,
            f"requires_tools should not be declared, got: {requires_tools}",
        )

    def test_source_declared(self):
        fm = load_frontmatter()
        self.assertEqual(
            fm["metadata"]["hermes"]["source"],
            "hermes-edu-skills",
        )

    def test_deployed_from_is_github_url(self):
        fm = load_frontmatter()
        url = fm["metadata"]["hermes"].get("deployed_from", "")
        self.assertTrue(
            url.startswith("https://github.com/"),
            f"deployed_from should be a GitHub URL, got: {url}",
        )

    def test_version_format(self):
        fm = load_frontmatter()
        version = fm.get("version", "")
        # Must be semver-like: X.Y.Z
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")

    def test_stages_cover_all_three(self):
        fm = load_frontmatter()
        stages = fm["metadata"]["hermes"].get("stages", [])
        self.assertIn("primary", stages)
        self.assertIn("junior", stages)
        self.assertIn("senior", stages)

    def test_abilities_contains_memory(self):
        fm = load_frontmatter()
        abilities = fm["metadata"]["hermes"].get("abilities", [])
        self.assertIn("记忆", abilities)


# ---------------------------------------------------------------------------
# Test: Required sections present
# ---------------------------------------------------------------------------


class ContentSectionsTest(unittest.TestCase):
    def setUp(self):
        self.content = load_full_content()

    def _section_exists(self, name: str) -> bool:
        return f"## {name}" in self.content or f"## {name.lower()}" in self.content.lower()

    def test_problem_section_exists(self):
        self.assertTrue(self._section_exists("解决什么问题"))

    def test_best_for_section_exists(self):
        self.assertTrue(self._section_exists("最适合"))

    def test_not_for_section_exists(self):
        self.assertTrue(self._section_exists("不适合"))

    def test_inputs_section_exists(self):
        self.assertTrue(self._section_exists("使用前请准备") or self._section_exists("Inputs"))

    def test_workflow_section_exists(self):
        self.assertTrue(
            self._section_exists("推荐工作流") or self._section_exists("Workflow"),
        )

    def test_output_format_section_exists(self):
        self.assertTrue(
            self._section_exists("输出格式") or self._section_exists("Output Format"),
        )

    def test_quality_checks_section_exists(self):
        self.assertTrue(
            self._section_exists("质量检查")
            or self._section_exists("Quality Checks")
            or self._section_exists("成功标准"),
        )

    def test_examples_section_exists(self):
        self.assertTrue(self._section_exists("示例") or self._section_exists("Examples"))

    def test_invocation_signals_section_exists(self):
        self.assertTrue(
            self._section_exists("调用信号") or self._section_exists("Invocation Signals"),
        )

    def test_roles_section_exists(self):
        self.assertTrue(
            self._section_exists("适用角色") or self._section_exists("Roles"),
        )


# ---------------------------------------------------------------------------
# Test: Quality Checks are specific and verifiable
# ---------------------------------------------------------------------------


class QualityChecksTest(unittest.TestCase):
    def setUp(self):
        self.content = load_full_content()

    def _get_section(self, name: str) -> str:
        """Extract markdown section content by heading name."""
        pattern = re.compile(
            r"(?:^|\n)##\s*" + re.escape(name) + r".*?\n(.*?)(?=\n## |\Z)",
            re.DOTALL | re.IGNORECASE,
        )
        match = pattern.search(self.content)
        return match.group(1) if match else ""

    def test_memory_block_size_mentioned(self):
        """Workflow must specify a size limit for memory blocks."""
        section = self._get_section("推荐工作流") or self._get_section("Workflow")
        self.assertIn(
            "20",
            section,
            "Workflow should specify memory block size (≤20 chars)",
        )

    def test_review_node_count_minimum_defined(self):
        """Quality checks must state minimum number of review nodes."""
        section = (
            self._get_section("质量检查")
            or self._get_section("Quality Checks")
            or self._get_section("成功标准")
        )
        # Should mention at least 4 review nodes
        self.assertRegex(
            section,
            r"4.*?(?:节点|次|node|review|date)",
            "Quality Checks should require ≥ 4 review nodes",
        )

    def test_memory_block_count_maximum_defined(self):
        """Quality checks must cap the number of memory blocks per session."""
        section = (
            self._get_section("质量检查")
            or self._get_section("Quality Checks")
            or self._get_section("成功标准")
        )
        self.assertIn(
            "10",
            section,
            "Quality Checks should cap memory blocks at ≤ 10 per session",
        )

    def test_no_tool_dependencies_in_body(self):
        """Body text must not reference requires_tools by name."""
        # Skip frontmatter
        content = load_full_content()
        match = re.search(r"\n---\n", content)
        body = content[match.end() :] if match else content
        for tool in ["context.load", "entitlement.check", "workflow.create", "memory.write"]:
            self.assertNotIn(
                tool,
                body,
                f"Body should not mention unavailable tool '{tool}'",
            )


# ---------------------------------------------------------------------------
# Test: Workflow is expanded
# ---------------------------------------------------------------------------


class WorkflowExpansionTest(unittest.TestCase):
    def setUp(self):
        self.content = load_full_content()

    def _get_section(self, name: str) -> str:
        pattern = re.compile(
            r"(?:^|\n)##\s*" + re.escape(name) + r".*?\n(.*?)(?=\n## |\Z)",
            re.DOTALL | re.IGNORECASE,
        )
        match = pattern.search(self.content)
        return match.group(1) if match else ""

    def test_workflow_has_5_steps(self):
        section = self._get_section("推荐工作流") or self._get_section("Workflow")
        # Count step markers (numbered steps or "第X步" or "- " bullet lines)
        numbered_steps = re.findall(r"(?:第\d+步|第\d+次|\d+\.)", section)
        self.assertGreaterEqual(
            len(numbered_steps),
            5,
            f"Workflow should have 5 steps, found {len(numbered_steps)}: {numbered_steps}",
        )

    def test_workflow_mentions_block_chunking(self):
        section = self._get_section("推荐工作流") or self._get_section("Workflow")
        self.assertTrue(
            re.search(r"记忆块|记忆 chunk|chunk", section, re.IGNORECASE),
            "Workflow step 1 should mention chunking memory blocks",
        )

    def test_workflow_mentions_spaced_repetition(self):
        section = self._get_section("推荐工作流") or self._get_section("Workflow")
        self.assertTrue(
            re.search(r"间隔|spaced|复习表|节点", section, re.IGNORECASE),
            "Workflow should mention spaced repetition / review nodes",
        )

    def test_workflow_mentions_retrieval_practice(self):
        section = self._get_section("推荐工作流") or self._get_section("Workflow")
        self.assertTrue(
            re.search(r"提取|填空|问答|回忆|retrieval", section, re.IGNORECASE),
            "Workflow should mention retrieval practice (extraction questions)",
        )


# ---------------------------------------------------------------------------
# Test: Examples include input AND output
# ---------------------------------------------------------------------------


class ExamplesTest(unittest.TestCase):
    def setUp(self):
        self.content = load_full_content()

    def test_has_poetry_example(self):
        """At least one example must involve Chinese poetry or classical text."""
        self.assertRegex(
            self.content,
            r"(静夜思|古诗|诗词|文言文|背诵)",
            "Examples should include a Chinese poetry/verse example",
        )

    def test_has_word_vocabulary_example(self):
        """At least one example must involve English vocabulary."""
        self.assertRegex(
            self.content,
            r"(单词|vocabulary|word|abandon|英语)",
            "Examples should include an English vocabulary example",
        )

    def test_example_includes_output_format(self):
        """Examples should show the generated output format, not just input."""
        # Count code fences (```) — a proper example has at least 2 (input + output)
        code_fence_count = len(re.findall(r"```", self.content))
        self.assertGreaterEqual(
            code_fence_count,
            4,
            f"Examples should show both input and output (≥4 code fences), found {code_fence_count}",
        )

    def test_example_has_review_table(self):
        """Example output must include a review schedule table."""
        # A review table contains dates and review node text
        self.assertRegex(
            self.content,
            r"(第1次|第3天|第7天|间隔复习)",
            "Example output should include a spaced repetition review table",
        )


# ---------------------------------------------------------------------------
# Test: Invocation Signals completeness
# ---------------------------------------------------------------------------


class InvocationSignalsTest(unittest.TestCase):
    def setUp(self):
        self.content = load_full_content()

    def _get_section(self, name: str) -> str:
        pattern = re.compile(
            r"(?:^|\n)##\s*" + re.escape(name) + r".*?\n(.*?)(?=\n## |\Z)",
            re.DOTALL | re.IGNORECASE,
        )
        match = pattern.search(self.content)
        return match.group(1) if match else ""

    def test_trigger_keywords_exist(self):
        section = (
            self._get_section("调用信号") or self._get_section("Invocation Signals")
        )
        self.assertIn("记忆方法", section)
        self.assertIn("背诵记忆", section)

    def test_has_exclusion_rules(self):
        """Must route away from sibling skills for non-memory tasks."""
        section = (
            self._get_section("调用信号") or self._get_section("Invocation Signals")
        )
        # Should mention at least one sibling skill to route to
        self.assertTrue(
            re.search(r"agent-question-explanation|agent-mistake-review", section),
            "Invocation Signals should include exclusion rules routing to sibling skills",
        )

    def test_triggers_are_distinct_from_explanations(self):
        """Trigger keywords for memory should differ from those for explanation."""
        section = (
            self._get_section("调用信号") or self._get_section("Invocation Signals")
        )
        # Should NOT trigger on "这首诗的意思是什么" type queries
        self.assertIn(
            "意思是什么",
            section,
            "Invocation Signals should explicitly exclude comprehension queries",
        )


# ---------------------------------------------------------------------------
# Test: Input constraints respected
# ---------------------------------------------------------------------------


class InputConstraintTest(unittest.TestCase):
    def setUp(self):
        self.content = load_full_content()

    def test_requires_data_declared(self):
        """requires_data must specify at least grade + content text."""
        fm = load_frontmatter()
        requires_data = fm.get("metadata", {}).get("hermes", {}).get("requires_data", [])
        self.assertIsInstance(requires_data, list)
        self.assertGreaterEqual(len(requires_data), 2)

    def test_inputs_mentions_grade(self):
        """Inputs section must mention grade as a required field."""
        section_match = re.search(
            r"##\s*(?:使用前请准备|Inputs).*?\n(.*?)(?=\n## |\Z)",
            self.content,
            re.DOTALL,
        )
        self.assertIsNotNone(section_match)
        self.assertIn("年级", section_match.group(1))

    def test_not_for_quantifies_large_content(self):
        """Not For section should give a size threshold for '超大量'."""
        section_match = re.search(
            r"##\s*(?:不适合|Not For).*?\n(.*?)(?=\n## |\Z)",
            self.content,
            re.DOTALL,
        )
        self.assertIsNotNone(section_match)
        section_text = section_match.group(1)
        # Should mention a word/char count threshold
        self.assertRegex(
            section_text,
            r"\d+.*?(字|词|word|char)",
            "Not For should quantify what '超大量' means (e.g. >500字)",
        )


# ---------------------------------------------------------------------------
# Test: Skill self-consistency
# ---------------------------------------------------------------------------


class SelfConsistencyTest(unittest.TestCase):
    def test_description_matches_frontmatter(self):
        fm = load_frontmatter()
        content = load_full_content()
        # Description in frontmatter should appear verbatim (or nearly) in body
        desc = fm.get("description", "")
        short_desc = desc.split("。")[0]  # First sentence
        self.assertIn(
            short_desc[:10],
            content,
            "Frontmatter description should be reflected in the body text",
        )

    def test_public_contract_no_requires_tools(self):
        """Public Skill Contract section must not mention requires_tools."""
        content = load_full_content()
        contract_match = re.search(
            r"##\s*(?:公开 Skill 契约|Public Skill Contract).*?\n(.*?)(?=\n## |\Z)",
            content,
            re.DOTALL,
        )
        if contract_match:
            contract_text = contract_match.group(1)
            self.assertNotIn(
                "requires_tools",
                contract_text,
                "Public Skill Contract should not declare requires_tools",
            )

    def test_skill_size_under_limit(self):
        """SKILL.md should be < 15 KB for fast loading."""
        size_kb = SKILL_PATH.stat().st_size / 1024
        self.assertLess(
            size_kb,
            15,
            f"SKILL.md is {size_kb:.1f} KB — should be < 15 KB for fast loading",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
