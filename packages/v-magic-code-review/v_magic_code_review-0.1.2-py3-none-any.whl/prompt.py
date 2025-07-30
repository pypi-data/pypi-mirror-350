import os
import textwrap
from collections import OrderedDict
from typing import List, Tuple


class Prompts:
    @classmethod
    def all_templates(cls) -> OrderedDict[str, str]:
        system_templates = cls._system_template()
        custom_templates = cls._custom_template()
        return OrderedDict(system_templates + custom_templates)

    @classmethod
    def list_template_names(cls) -> list[str]:
        return list(cls.all_templates().keys())

    @classmethod
    def create(
        cls,
        template_name: str,
        issue_summary: str, issue_requirements: str, issue_design: str, issue_comments: str, mr_description: str,
        mr_diff: str
    ) -> str:
        prompt_structure = cls.all_templates()[template_name]
        prompt_structure = textwrap.dedent(prompt_structure).strip()
        return prompt_structure.format(
            issue_summary=issue_summary,
            issue_requirements=issue_requirements,
            issue_design=issue_design,
            issue_comments=issue_comments,
            mr_description=mr_description,
            mr_diff=mr_diff,
        )

    @classmethod
    def _system_template(cls) -> List[Tuple[str, str]]:
        default_template = (
            'DEFAULT',
            '''
                你是一个专业的全栈开发工程师，拥有丰富的 Code Review 经验。
    
                我将提供以下信息：
                    1. <section>需求标题</section>
                    2. <section>需求说明</section>
                    3. <section>设计方案</section>
                    4. <section>代码改动描述</section>
                    5. <section>需求相关的讨论内容</section>
    
                请根据这些信息，从以下几个方面对代码改动进行严格评估，并提出具体改进建议：
                1.  **代码质量与最佳实践**
                    * 通用编码规范符合度（例如命名约定、代码风格一致性）。
                    * 是否存在冗余、不必要的复杂性或“坏味道”代码。
                    * 代码结构是否清晰、分层合理，易于理解和扩展。
                    * 函数参数和返回值是否都正确设置了类型提示 (Type Hints)。
    
                2.  **潜在 Bug 与边缘情况**
                    * 核心逻辑是否有潜在错误。
                    * 是否覆盖了所有已知的输入、状态和异常情况。
                    * 是否存在并发安全问题（若适用）。
    
                3.  **性能优化**
                    * 是否存在明显的性能瓶颈。
                    * 算法效率或资源使用方面是否有改进空间。
    
                4.  **可读性与可维护性**
                    * 代码是否易于理解和修改。
                    * 变量、函数和类命名是否清晰、表意。
                    * 关键或复杂逻辑是否有必要且恰当的注释。
                    * 模块化程度如何，是否方便后期扩展和重构。
    
                5.  **安全隐患**
                    * 是否存在潜在的安全漏洞，如输入验证不足、SQL 注入、XSS、不安全的数据处理等（根据代码类型重点评估）。
    
                ---
    
                **要求：**
    
                * **精炼具体：** 语言精炼，条理清晰，直接指出问题点和改进建议，避免泛泛而谈。
                * **仅列建议：** 只列出需要改进的地方和建议，无需提及做得好的部分。
                * **中文输出：** 结果必须以中文 Markdown 格式输出。
    
                ---
    
                **信息提供：**
    
                <section>需求标题</section>
                {issue_summary}
    
                <section>需求说明</section>
                {issue_requirements}
    
                <section>设计方案</section>
                {issue_design}
    
                <section>相关讨论</section>
                {issue_comments}
    
                <section>代码改动描述</section>
                {mr_description}
    
                <section>Code Diff</section>
                {mr_diff}
            '''
        )
        return [
            default_template
        ]

    @classmethod
    def _custom_template(cls) -> List[Tuple[str, str]]:
        custom_template_folder = os.path.expanduser('~/.local/share/v-cr/prompts')
        custom_templates = []
        for filename in os.listdir(custom_template_folder):
            template_name, ext = os.path.splitext(filename)
            if ext == '.txt':
                with open(os.path.join(custom_template_folder, filename), 'r') as f:
                    custom_templates.append((template_name, f.read()))
        return custom_templates
