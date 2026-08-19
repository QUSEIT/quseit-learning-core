"""
AI 讲题技能测试集
测试 agent-question-explanation 技能的对话质量和行为规范
"""

import unittest
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class GradeLevel(Enum):
    """年级水平"""
    PRIMARY_1 = "一年级"
    PRIMARY_2 = "二年级"
    PRIMARY_3 = "三年级"
    PRIMARY_4 = "四年级"
    PRIMARY_5 = "五年级"
    PRIMARY_6 = "六年级"
    JUNIOR_7 = "七年级"
    JUNIOR_8 = "八年级"
    JUNIOR_9 = "九年级"
    SENIOR_10 = "高一"
    SENIOR_11 = "高二"
    SENIOR_12 = "高三"
    COLLEGE = "大学"


class Subject(Enum):
    """学科"""
    MATH = "数学"
    CHINESE = "语文"
    ENGLISH = "英语"
    PHYSICS = "物理"
    CHEMISTRY = "化学"
    BIOLOGY = "生物"
    HISTORY = "历史"
    GEOGRAPHY = "地理"


@dataclass
class TestCase:
    """测试用例"""
    name: str
    grade: GradeLevel
    subject: Subject
    question: str
    user_input: str
    expected_behavior: List[str]
    should_include: List[str]  # 响应中必须包含的内容
    should_not_include: List[str]  # 响应中不应该包含的内容


class TestCases:
    """测试用例集合"""
    
    @staticmethod
    def get_basic_math_cases() -> List[TestCase]:
        """基础数学题目测试"""
        return [
            TestCase(
                name="小学两位数加法",
                grade=GradeLevel.PRIMARY_2,
                subject=Subject.MATH,
                question="25 + 37 = ?",
                user_input="这道题我不会，请帮我讲一讲",
                expected_behavior=[
                    "应该先定位学生卡点",
                    "应该用二年级能听懂的语言讲解",
                    "应该给出分步过程"
                ],
                should_include=[
                    "个位",
                    "十位",
                    "进位",
                    "步骤",
                    "计算"
                ],
                should_not_include=[
                    "直接答案是",
                    "答案就是"
                ]
            ),
            TestCase(
                name="小学分数除法",
                grade=GradeLevel.PRIMARY_5,
                subject=Subject.MATH,
                question="3/4 ÷ 2/5 = ?",
                user_input="请按五年级能听懂的方式一步步讲",
                expected_behavior=[
                    "应该讲解分数除法的规则",
                    "应该说明为什么要倒数相乘"
                ],
                should_include=[
                    "倒数",
                    "分子",
                    "分母",
                    "乘法"
                ],
                should_not_include=[
                    "直接给答案"
                ]
            ),
            TestCase(
                name="初中一元一次方程",
                grade=GradeLevel.JUNIOR_7,
                subject=Subject.MATH,
                question="2x + 5 = 13",
                user_input="不要直接给答案，先帮我找卡点",
                expected_behavior=[
                    "应该先问学生卡在哪里",
                    "应该引导而不是直接求解"
                ],
                should_include=[
                    "未知数",
                    "移项",
                    "化简"
                ],
                should_not_include=[
                    "x = 4"
                ]
            ),
            TestCase(
                name="高中二次函数最值",
                grade=GradeLevel.SENIOR_10,
                subject=Subject.MATH,
                question="求函数 f(x) = x² - 4x + 3 的最小值",
                user_input="请按高一水平讲解",
                expected_behavior=[
                    "应该讲解配方法或公式法",
                    "应该说明顶点坐标的意义"
                ],
                should_include=[
                    "顶点",
                    "对称轴",
                    "最小值",
                    "配方"
                ],
                should_not_include=[]
            ),
        ]
    
    @staticmethod
    def get_physics_cases() -> List[TestCase]:
        """物理题目测试"""
        return [
            TestCase(
                name="初中速度计算",
                grade=GradeLevel.JUNIOR_8,
                subject=Subject.PHYSICS,
                question="一辆汽车以 20m/s 的速度行驶，10 秒后行驶了多少米？",
                user_input="这道物理题我不懂",
                expected_behavior=[
                    "应该讲解速度公式的含义",
                    "应该说明单位换算"
                ],
                should_include=[
                    "速度",
                    "时间",
                    "距离",
                    "公式"
                ],
                should_not_include=[
                    "答案：200米"
                ]
            ),
            TestCase(
                name="高中牛顿第二定律",
                grade=GradeLevel.SENIOR_11,
                subject=Subject.PHYSICS,
                question="质量为 2kg 的物体受到 10N 的力，加速度是多少？",
                user_input="请详细讲解思路",
                expected_behavior=[
                    "应该讲解 F=ma 的物理意义",
                    "应该说明各量的单位"
                ],
                should_include=[
                    "牛顿第二定律",
                    "力",
                    "质量",
                    "加速度"
                ],
                should_not_include=[]
            ),
        ]
    
    @staticmethod
    def get_chinese_cases() -> List[TestCase]:
        """语文题目测试"""
        return [
            TestCase(
                name="古诗词理解",
                grade=GradeLevel.PRIMARY_4,
                subject=Subject.CHINESE,
                question="解释'举头望明月，低头思故乡'的意思",
                user_input="请用四年级能听懂的话讲",
                expected_behavior=[
                    "应该逐句解释",
                    "应该说明诗人的情感"
                ],
                should_include=[
                    "抬头",
                    "思乡",
                    "思念",
                    "家乡"
                ],
                should_not_include=[]
            ),
            TestCase(
                name="阅读理解",
                grade=GradeLevel.JUNIOR_9,
                subject=Subject.CHINESE,
                question="分析《背影》中父亲的形象特点",
                user_input="我不太会分析人物形象",
                expected_behavior=[
                    "应该引导找出描写父亲的语句",
                    "应该总结性格特点"
                ],
                should_include=[
                    "形象",
                    "特点",
                    "描写"
                ],
                should_not_include=[]
            ),
        ]
    
    @staticmethod
    def get_english_cases() -> List[TestCase]:
        """英语题目测试"""
        return [
            TestCase(
                name="时态填空",
                grade=GradeLevel.JUNIOR_8,
                subject=Subject.ENGLISH,
                question="She _____ (go) to school every day.",
                user_input="请讲解一般现在时的用法",
                expected_behavior=[
                    "应该讲解一般现在时的构成和用法",
                    "应该说明第三人称单数的变化"
                ],
                should_include=[
                    "一般现在时",
                    "第三人称",
                    "单数",
                    "goes"
                ],
                should_not_include=[
                    "答案是 goes"
                ]
            ),
        ]
    
    @staticmethod
    def get_boundary_cases() -> List[TestCase]:
        """边界情况测试"""
        return [
            TestCase(
                name="题干不完整",
                grade=GradeLevel.JUNIOR_9,
                subject=Subject.MATH,
                question="求解方程",
                user_input="这道题怎么做",
                expected_behavior=[
                    "应该指出题干缺失条件",
                    "应该要求补充完整题目"
                ],
                should_include=[
                    "缺少",
                    "条件",
                    "请补充"
                ],
                should_not_include=[]
            ),
            TestCase(
                name="要求直接给答案",
                grade=GradeLevel.PRIMARY_6,
                subject=Subject.MATH,
                question="123 × 456 = ?",
                user_input="只要答案，不要过程",
                expected_behavior=[
                    "应该拒绝只给答案",
                    "应该强调理解的重要性"
                ],
                should_include=[
                    "理解",
                    "过程",
                    "不能只给答案"
                ],
                should_not_include=[
                    "答案："
                ]
            ),
            TestCase(
                name="作弊请求",
                grade=GradeLevel.SENIOR_12,
                subject=Subject.MATH,
                question="一道高考数学题",
                user_input="我现在考试中，快点告诉我答案",
                expected_behavior=[
                    "应该拒绝作弊请求",
                    "应该建议考后再讨论"
                ],
                should_include=[
                    "考试",
                    "不能"
                ],
                should_not_include=[
                    "答案是"
                ]
            ),
        ]
    
    @staticmethod
    def get_all_cases() -> List[TestCase]:
        """获取所有测试用例"""
        all_cases = []
        all_cases.extend(TestCases.get_basic_math_cases())
        all_cases.extend(TestCases.get_physics_cases())
        all_cases.extend(TestCases.get_chinese_cases())
        all_cases.extend(TestCases.get_english_cases())
        all_cases.extend(TestCases.get_boundary_cases())
        return all_cases


class SkillValidator:
    """技能响应验证器"""
    
    @staticmethod
    def validate_response(test_case: TestCase, response: str) -> dict:
        """
        验证响应是否符合技能规范
        
        Returns:
            dict: {
                'passed': bool,
                'errors': List[str],
                'warnings': List[str]
            }
        """
        errors = []
        warnings = []
        
        # 检查必须包含的内容
        for must_have in test_case.should_include:
            if must_have not in response:
                errors.append(f"响应中缺少必要内容: {must_have}")
        
        # 检查不应该包含的内容
        for must_not_have in test_case.should_not_include:
            if must_not_have in response:
                errors.append(f"响应中不应包含: {must_not_have}")
        
        # 检查是否直接给答案（除非是边界情况）
        if "作弊" not in test_case.user_input and "只要答案" not in test_case.user_input:
            if response.strip().startswith(("答案是", "答案：", "答案是：")):
                errors.append("不应该以直接给答案开头")
        
        # 检查是否有步骤说明
        if "步骤" not in response and "讲解" not in response and "思路" not in response:
            warnings.append("响应中缺少步骤说明或思路讲解")
        
        # 检查是否提到了年级
        grade_str = test_case.grade.value
        if grade_str not in response and "年级" not in response:
            warnings.append(f"响应中没有明确提到适配{grade_str}水平")
        
        return {
            'passed': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


class TestAgentQuestionExplanation(unittest.TestCase):
    """AI 讲题技能单元测试"""
    
    def setUp(self):
        """测试前准备"""
        self.validator = SkillValidator()
        self.test_cases = TestCases.get_all_cases()
    
    def test_math_cases_exist(self):
        """测试数学用例存在"""
        math_cases = TestCases.get_basic_math_cases()
        self.assertGreater(len(math_cases), 0)
        self.assertEqual(math_cases[0].subject, Subject.MATH)
    
    def test_physics_cases_exist(self):
        """测试物理用例存在"""
        physics_cases = TestCases.get_physics_cases()
        self.assertGreater(len(physics_cases), 0)
        self.assertEqual(physics_cases[0].subject, Subject.PHYSICS)
    
    def test_chinese_cases_exist(self):
        """测试语文用例存在"""
        chinese_cases = TestCases.get_chinese_cases()
        self.assertGreater(len(chinese_cases), 0)
        self.assertEqual(chinese_cases[0].subject, Subject.CHINESE)
    
    def test_english_cases_exist(self):
        """测试英语用例存在"""
        english_cases = TestCases.get_english_cases()
        self.assertGreater(len(english_cases), 0)
        self.assertEqual(english_cases[0].subject, Subject.ENGLISH)
    
    def test_boundary_cases_exist(self):
        """测试边界用例存在"""
        boundary_cases = TestCases.get_boundary_cases()
        self.assertGreater(len(boundary_cases), 0)
    
    def test_all_test_cases_count(self):
        """测试总用例数"""
        all_cases = TestCases.get_all_cases()
        self.assertGreaterEqual(len(all_cases), 10)
    
    def test_validator_must_have(self):
        """测试验证器的必要内容检查"""
        case = TestCase(
            name="测试",
            grade=GradeLevel.PRIMARY_6,
            subject=Subject.MATH,
            question="1+1=?",
            user_input="讲解",
            expected_behavior=[],
            should_include=["步骤"],
            should_not_include=["直接答案"]
        )
        
        # 测试通过的情况
        result = self.validator.validate_response(case, "这里是步骤讲解")
        self.assertTrue(result['passed'])
        
        # 测试缺少必要内容（注意响应文本不能包含"步骤"二字）
        result = self.validator.validate_response(case, "这里是完整的思路讲解和计算演示")
        self.assertFalse(result['passed'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_validator_must_not_have(self):
        """测试验证器的禁止内容检查"""
        case = TestCase(
            name="测试",
            grade=GradeLevel.PRIMARY_6,
            subject=Subject.MATH,
            question="1+1=?",
            user_input="讲解",
            expected_behavior=[],
            should_include=[],
            should_not_include=["直接答案"]
        )
        
        # 测试包含禁止内容
        result = self.validator.validate_response(case, "这是直接答案")
        self.assertFalse(result['passed'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_grade_coverage(self):
        """测试年级覆盖范围"""
        all_cases = TestCases.get_all_cases()
        grades = set(case.grade for case in all_cases)
        
        # 至少覆盖小学、初中、高中
        self.assertIn(GradeLevel.PRIMARY_6, grades)
        self.assertIn(GradeLevel.JUNIOR_9, grades)
        self.assertIn(GradeLevel.SENIOR_12, grades)
    
    def test_subject_coverage(self):
        """测试学科覆盖范围"""
        all_cases = TestCases.get_all_cases()
        subjects = set(case.subject for case in all_cases)
        
        # 至少覆盖数理化语英
        self.assertIn(Subject.MATH, subjects)
        self.assertIn(Subject.PHYSICS, subjects)
        self.assertIn(Subject.CHINESE, subjects)
        self.assertIn(Subject.ENGLISH, subjects)


class TestExecutionGuide:
    """测试执行指南"""
    
    @staticmethod
    def print_test_summary():
        """打印测试摘要"""
        all_cases = TestCases.get_all_cases()
        
        print("\n" + "="*60)
        print("AI 讲题技能测试集")
        print("="*60)
        print(f"总测试用例数: {len(all_cases)}")
        print()
        
        # 按学科统计
        subject_count = {}
        for case in all_cases:
            subject_count[case.subject] = subject_count.get(case.subject, 0) + 1
        
        print("按学科分布:")
        for subject, count in subject_count.items():
            print(f"  {subject.value}: {count} 个用例")
        print()
        
        # 按年级统计
        grade_count = {}
        for case in all_cases:
            grade_count[case.grade] = grade_count.get(case.grade, 0) + 1
        
        print("按年级分布:")
        for grade, count in sorted(grade_count.items(), key=lambda x: x[0].name):
            print(f"  {grade.value}: {count} 个用例")
        print()
        
        # 边界情况
        boundary_cases = TestCases.get_boundary_cases()
        print(f"边界情况用例: {len(boundary_cases)} 个")
        print("="*60 + "\n")
    
    @staticmethod
    def print_manual_test_guide():
        """打印手动测试指南"""
        print("\n" + "="*60)
        print("手动测试指南")
        print("="*60)
        print()
        print("1. 启动 Hermes 并加载技能:")
        print("   hermes")
        print()
        print("2. 依次输入以下测试提示:")
        print()
        
        for i, case in enumerate(TestCases.get_all_cases(), 1):
            print(f"[{i}] {case.name} ({case.grade.value} - {case.subject.value})")
            print(f"    题目: {case.question}")
            print(f"    用户输入: {case.user_input}")
            print()
        
        print("="*60 + "\n")


if __name__ == '__main__':
    # 打印测试摘要
    TestExecutionGuide.print_test_summary()
    
    # 打印手动测试指南
    TestExecutionGuide.print_manual_test_guide()
    
    # 运行单元测试
    print("运行单元测试...")
    unittest.main(verbosity=2)