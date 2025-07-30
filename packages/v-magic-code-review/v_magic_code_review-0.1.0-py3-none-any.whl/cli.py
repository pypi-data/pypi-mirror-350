import argparse
import logging
import os
import textwrap
import tomllib
from urllib.parse import urlparse, parse_qs

import bs4
import gitlab
import pyperclip
from atlassian import Confluence, Jira
from gemini_webapi import GeminiClient
from gemini_webapi.constants import Model
from markdownify import MarkdownConverter
from rich.console import Console
from rich.markdown import Markdown
from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

from config import GitlabConfig, JiraConfig, JiraField, ConfluenceConfig, GeminiConfig
from util import call_async_func, remove_blank_lines, first_element, num_tokens_from_text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GitlabService:
    def __init__(self):
        gl = gitlab.Gitlab(GitlabConfig.HOST, private_token=GitlabConfig.TOKEN)
        gl_project = gl.projects.get(GitlabConfig.PROJECT_ID)

        self.gl = gl
        self.gl_project = gl_project

    def get_mr(self, mr_id):
        return self.gl_project.mergerequests.get(mr_id)

    def find_mr_by_jira_key(self, jira_key):
        merge_requests = self.gl_project.mergerequests.list(state='opened', iterator=True)
        for mr in merge_requests:
            if jira_key in mr.title:
                return mr
        return None

    def get_plain_diff_from_mr(self, mr):
        changes = mr.changes()

        full_plain_diff = []  # List to store all formatted diffs

        for change in changes.get('changes', []):
            old_path = change.get('old_path')
            new_path = change.get('new_path')
            diff_content = change.get('diff')
            new_file = change.get('new_file')
            renamed_file = change.get('renamed_file')
            deleted_file = change.get('deleted_file')

            # Skip files based on an extension or path
            if (
                any(old_path.endswith(ext) for ext in GitlabConfig.DIFF_EXCLUDE_EXT)
                or any(old_path.startswith(path) for path in GitlabConfig.DIFF_EXCLUDE_PATH)
            ):
                continue
            # Skip files based on an extension or path
            if (
                any(new_path.endswith(ext) for ext in GitlabConfig.DIFF_EXCLUDE_EXT)
                or any(new_path.startswith(path) for path in GitlabConfig.DIFF_EXCLUDE_PATH)
            ):
                continue
            # Skip empty diffs
            if not diff_content:
                continue

            diff_git_line = f"diff --git a/{old_path} b/{new_path}"
            full_plain_diff.append(diff_git_line)

            # Handle file mode changes, new files, deleted files, and renamed files
            if new_file:
                full_plain_diff.append("new file mode 100644")  # Assuming typical file mode
                full_plain_diff.append("--- /dev/null")
                full_plain_diff.append(f"+++ b/{new_path}")
            elif deleted_file:
                full_plain_diff.append(f"--- a/{old_path}")
                full_plain_diff.append("+++ /dev/null")
            elif renamed_file:
                full_plain_diff.append(f"rename from {old_path}")
                full_plain_diff.append(f"rename to {new_path}")
                full_plain_diff.append(f"--- a/{old_path}")
                full_plain_diff.append(f"+++ b/{new_path}")
            else:
                full_plain_diff.append(f"--- a/{old_path}")
                full_plain_diff.append(f"+++ b/{new_path}")
            full_plain_diff.append(diff_content)
        return "\n".join(full_plain_diff)

    def add_comments(self, mr, body):
        mr.notes.create({'body': body})


class JiraService:
    def __init__(self):
        self.jira = Jira(
            url=JiraConfig.HOST,
            token=JiraConfig.TOKEN,
        )

    def get_client(self) -> Jira:
        return self.jira

    def get_issue(self, issue_key: str) -> dict:
        return self.jira.issue(issue_key)

    def get_issue_comments(self, issue: dict) -> str:
        original_comments = issue['fields'][JiraField.COMMENT]['comments']
        text_comments = []
        for comment in original_comments:
            author_section = '{} {}：\n'.format(comment['created'], comment['author']['displayName'])
            body_section = remove_blank_lines(comment['body'])
            text_comments.append(author_section + body_section)
            logging.info('get issue comment, author: %s, body: %s', author_section, body_section.splitlines()[1])
        return '\n'.join(text_comments)

    def get_issue_requirements(self, issue: dict, confluence_service: 'ConfluenceService') -> str:
        description = issue['fields'][JiraField.DESCRIPTION]
        if description.startswith('https://'):
            logging.info("get requirements from confluence: %s", description)

            wiki_url = description
            page = confluence_service.get_page_by_url(wiki_url)
            requirements = confluence_service.get_requirements(page, issue['key'])
        else:
            logging.info('get requirements from description: %s', description)
            requirements = description
        return requirements

    def get_issue_design(self, issue: dict, confluence_service: 'ConfluenceService') -> str:
        remote_links = self.jira.get_issue_remote_links(issue['key'])
        issue_designs = []
        for remote_link in remote_links:
            application = remote_link['application']
            if not application or application['type'] != 'com.atlassian.confluence':
                continue
            url = remote_link['object']['url']
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            page_id = first_element(params.get('pageId') or [])
            page = confluence_service.get_page_by_id(page_id)
            space = page['_expandable']['space']
            if space != '/rest/api/space/ORI':
                continue
            logging.info('get design from confluence, title: %s, url: %s', page['title'], url)
            issue_designs.append(confluence_service.get_page_markdown(page))
        return '\n\n'.join(issue_designs)


class ConfluenceService:
    def __init__(self):
        self.confluence = Confluence(
            url=ConfluenceConfig.HOST,
            token=ConfluenceConfig.TOKEN,
            cloud=False
        )

    def get_page_by_url(self, url):
        return self.get_page_by_id(url.split('/pages/')[1].split('/')[0])

    def get_page_by_id(self, page_id):
        return self.confluence.get_page_by_id(page_id=page_id, expand='body.storage')

    def get_page_markdown(self, page):
        soup = bs4.BeautifulSoup(page['body']['storage']['value'], "lxml")
        return MarkdownConverter().convert_soup(soup)

    def get_requirements(self, page, jira_key):
        bs_content = bs4.BeautifulSoup(page['body']['storage']['value'], "lxml")

        reference_row = self.get_reference_row(bs_content, jira_key)
        requirements = reference_row.get_text(separator='\n', strip=True)
        return requirements

    def get_reference_row(self, bs_content, jira_key):
        for table in bs_content.find_all('table'):
            for row in table.find_all('tr'):
                for cell in row.find_all(['td', 'th']):
                    if jira_key in cell.get_text(strip=True):
                        return row
        return None


class GeminiService:
    def __init__(self):
        self.gemini_client = GeminiClient(
            secure_1psid=GeminiConfig.COOKIE_SECURE_1PSID,
            secure_1psidts=GeminiConfig.COOKIE_SECURE_1PSIDTS,
        )
        call_async_func(self.gemini_client.init, timeout=600, auto_refresh=False)

    def do_code_quality_analysis(self, prompt) -> str:
        resp = call_async_func(
            self.gemini_client.generate_content,
            prompt=prompt,
            model=Model.G_2_5_PRO,
        )
        return resp.text


class Prompts:
    @staticmethod
    def create(
        issue_summary: str, issue_requirements: str, issue_design: str, issue_comments: str, mr_description: str,
        mr_diff: str
    ) -> str:
        prompt_structure = """
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
        """
        prompt_structure = textwrap.dedent(prompt_structure).strip()
        return prompt_structure.format(
            issue_summary=issue_summary,
            issue_requirements=issue_requirements,
            issue_design=issue_design,
            issue_comments=issue_comments,
            mr_description=mr_description,
            mr_diff=mr_diff,
        )


def code_review(jira_key: str, mr_id: int, only_code: bool, copy_prompt: bool) -> None:
    logging.info('get jira issue ...')

    jira_service = JiraService()
    jira_issue = jira_service.get_issue(jira_key)
    assert jira_issue is not None, f"jira issue not found: {jira_key}"

    logging.info('jira issue link: %s', jira_issue['self'])
    logging.info('jira issue summary: %s', jira_issue['fields'][JiraField.SUMMARY])

    gitlab_service = GitlabService()
    if mr_id is not None:
        mr = gitlab_service.get_mr(mr_id)
    else:
        mr = gitlab_service.find_mr_by_jira_key(jira_key)
    assert mr is not None, f"merge request not found with jira key: {jira_key}"

    logging.info('merge request link: %s', mr.web_url)
    logging.info('merge request title: %s', mr.title)

    if only_code:
        issue_requirements = '无'
        issue_design = '无'
        issue_comments = '无'
    else:
        confluence_service = ConfluenceService()
        issue_requirements = jira_service.get_issue_requirements(jira_issue, confluence_service)
        logging.info('✨ issue requirements length: %s', len(issue_requirements))

        issue_design = jira_service.get_issue_design(jira_issue, confluence_service)
        logging.info('✨ issue design length: %s', len(issue_design))

        issue_comments = jira_service.get_issue_comments(jira_issue)
        logging.info('✨ issue comments length: %s', len(issue_comments))

    mr_diff = gitlab_service.get_plain_diff_from_mr(mr)
    logging.info('✨ code  diff length: %s', len(mr_diff))

    prompt = Prompts.create(
        issue_summary=jira_issue['fields'][JiraField.SUMMARY],
        issue_requirements=issue_requirements,
        issue_design=issue_design,
        issue_comments=issue_comments,
        mr_description=mr.description,
        mr_diff=mr_diff
    )
    logging.info('✨ prompt length: %s, tokens num: %s', len(prompt), num_tokens_from_text(prompt))

    if copy_prompt:
        pyperclip.copy(prompt)
        print("✅ {}".format(colored('Prompt 已复制到剪贴板', 'green', attrs=['bold'])))
        return

    gemini_service = GeminiService()
    with yaspin(Spinners.clock, text="Waiting for Gemini's response, usually takes about 2 minutes", timer=True) as sp:
        analysis_result = gemini_service.do_code_quality_analysis(prompt)

    Console().print(Markdown(analysis_result, code_theme='rrt'))

    print()

    selected = input(
        "✨ {}{}/{}， 或者{}/{}\n👉 ".format(
            colored('是否添加到 MR Comments？', 'yellow', attrs=['bold']),
            colored('添加(Y)', 'green', attrs=['bold']),
            colored('放弃(Q)', 'red', attrs=['bold']),
            colored('复制(C)', 'magenta', attrs=['bold']),
            colored('保存(S)', 'blue', attrs=['bold'])
        )
    )
    if selected.lower() == 'y':
        gitlab_service.add_comments(mr, analysis_result)
        print("✅ {}".format(colored('已添加到 MR', 'green', attrs=['bold'])))
    elif selected.lower() == 'c':
        pyperclip.copy(analysis_result)
        print("✅ 已复制到剪贴板")
    elif selected.lower() == 's':
        file_path = os.path.expanduser('~/Downloads/magic_code_review_{}.md'.format(jira_key))
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(analysis_result)
        print("✅ 已保存到 {}".format(file_path))
    else:
        print("👋 Bye!")


def print_version_text() -> None:
    """Reads and show the version from pyproject.toml."""
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        name = data["project"]["name"]
        version = data["project"]["version"]
        print("{} {}".format(
            colored(name, color='green', attrs=['bold']),
            colored('v' + version, color='red', attrs=['bold'])
        ))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Magic Code Review')
    parser.add_argument('jira_key', type=str, nargs='?', metavar="JIRA_KEY", help='jira issue key')
    parser.add_argument('-m', '--mr-id', type=int, help='merge request id')
    parser.add_argument('-o', '--only-code', action='store_true', help='only review code diff')
    parser.add_argument('-c', '--copy-prompt', action='store_true', help='copy prompt to clipboard')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--version', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    logging.info('args: %s', args)

    if args.version:
        print_version_text()
        return

    if args.jira_key:
        code_review(args.jira_key, args.mr_id, args.only_code, args.copy_prompt)


if __name__ == "__main__":
    main()
