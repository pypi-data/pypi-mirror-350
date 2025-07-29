#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import uuid
import time
import platform
import locale
from pathlib import Path
from datetime import date
from importlib.resources import read_text

import requests
from loguru import logger
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown

from .i18n import T
from .. import __respkg__
from .plugin import event_bus
from .utils import get_safe_filename
from .libmcp import extract_call_tool
from .blocks import CodeBlocks

CONSOLE_WHITE_HTML = read_text(__respkg__, "console_white.html")
CONSOLE_CODE_HTML = read_text(__respkg__, "console_code.html")

class Task:
    MAX_ROUNDS = 16

    def __init__(self, instruction, *, system_prompt=None, settings=None, mcp=None):
        self.task_id = uuid.uuid4().hex
        self.log = logger.bind(src='task', id=self.task_id)
        self.instruction = instruction
        self.console = None
        self.llm = None
        self.runner = None
        self.max_rounds = settings.get('max_rounds', self.MAX_ROUNDS)
        self.system_prompt = system_prompt
        self.pattern = re.compile(
            r"^(`{3,4})(\w+)\s+([\w\-\.]+)\n(.*?)^\1\s*$",
            re.DOTALL | re.MULTILINE
        )
        self.settings = settings
        self.mcp = mcp
        self.start_time = None
        self.code_blocks = CodeBlocks(self.console)
        
    def save(self, path):
       if self._console.record:
           self._console.save_html(path, clear=False, code_format=CONSOLE_WHITE_HTML)

    def save_html(self, path, task):
        if 'llm' in task and isinstance(task['llm'], list) and len(task['llm']) > 0:
            if task['llm'][0]['role'] == 'system':
                task['llm'].pop(0)

        task_json = json.dumps(task, ensure_ascii=False)
        html_content = CONSOLE_CODE_HTML.replace('{{code}}', task_json)

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                self.console.print(f"[green]Task saved to {path}[/green]")
        except Exception as e:
            self.console.print_exception()
            return

    def done(self):
        instruction = self.instruction
        task = {'instruction': instruction}
        task['llm'] = self.llm.history.json()
        task['runner'] = self.runner.history
        filename = get_safe_filename(instruction, extension='.json') or f"{self.task_id}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(task, file, ensure_ascii=False, indent=4)
        except Exception as e:
            self.console.print_exception()

        filename = get_safe_filename(instruction) or f"{self.task_id}.html"
        if hasattr(self.console, 'gui'):
            # Only save new html in gui mode for now.
            self.save_html(filename, task)
        else:
            self.console.save_html(filename, clear=True, code_format=CONSOLE_WHITE_HTML)
        filename = str(Path(filename).resolve())
        self.console.print(f"[green]{T('task_saved')}: \"{filename}\"")

        if self.settings.get('share_result'):
            self.sync_to_cloud()
        
        self.llm.clear()
        self.runner.clear()
        self.task_id = None
        self.instruction = None

    def parse_reply(self, markdown):
        code_blocks = {}
        for match in self.pattern.finditer(markdown):
            _, _, name, content = match.groups()
            code_blocks[name] = content.rstrip('\n')

        if self.mcp and not code_blocks:
            # 尝试解析mcp
            json_content = extract_call_tool(markdown)
            if json_content:
                code_blocks['call_tool'] = json_content

        return code_blocks

    def process_code_reply(self, blocks, llm=None):
        event_bus('exec', blocks)
        code_block = blocks['main']
        self.box(f"\n⚡ {T('start_execute')}:", code_block, lang='python')
        result = self.runner(code_block, blocks)
        event_bus('result', result)
        result = json.dumps(result, ensure_ascii=False, indent=4)
        self.box(f"\n✅ {T('execute_result')}:\n", result, lang="json")
        status = self.console.status(f"[dim white]{T('start_feedback')}...")
        self.console.print(status)
        feed_back = f"# 最初任务\n{self.instruction}\n\n# 代码执行结果反馈\n{result}"
        feedback_response = self.llm(feed_back, name=llm)
        return feedback_response

    def process_mcp_reply(self, blocks, llm=None):
        """处理 MCP 工具调用的回复"""

        event_bus('tool_call', blocks)
        json_content = blocks['call_tool']
        self.box(f"\n⚡ {T('call_tool')}:", json_content, lang='json')

        call_tool = json.loads(json_content)
        result = self.mcp.call_tool(call_tool['name'], call_tool['arguments'])
        event_bus('result', result)
        result = json.dumps(result, ensure_ascii=False, indent=4)
        self.box(f"\n✅ {T('call_tool_result')}:\n", result, lang="json")

        status = self.console.status(f"[dim white]{T('start_feedback')}...")
        self.console.print(status)
        feed_back = f"""# MCP 调用\n\n{self.instruction}\n
# 执行结果反馈

````json
{result}
````"""
        feedback_response = self.llm(feed_back, name=llm)

        return feedback_response


    def box(self, title, content, align=None, lang=None):
        if hasattr(self.console, 'gui'):
            # Using Mocked console. Dont use Panel

            if lang == 'json':
                # Only print execute result.
                self.console.print(f"\n{title}")
                self.console.print(content)
            return

        if lang:
            content = Syntax(content, lang, line_numbers=True, word_wrap=True)
        if align:
            content = Align(content, align=align)
        
        self.console.print(Panel(content, title=title))

    def print_summary(self, detail=False):
        history = self.llm.history
        if detail:
            table = Table(title=T("Task Summary"), show_lines=True)

            table.add_column(T("Round"), justify="center", style="bold cyan", no_wrap=True)
            table.add_column(T("Time(s)"), justify="right")
            table.add_column(T("In Tokens"), justify="right")
            table.add_column(T("Out Tokens"), justify="right")
            table.add_column(T("Total Tokens"), justify="right", style="bold magenta")

            round = 1
            for row in history.get_usage():
                table.add_row(
                    str(round),
                    str(row["time"]),
                    str(row["input_tokens"]),
                    str(row["output_tokens"]),
                    str(row["total_tokens"]),
                )
                round += 1
            self._console.print("\n")
            self._console.print(table)

        summary = history.get_summary()
        summary['elapsed_time'] = time.time() - self.start_time
        summarys = "| {rounds} | {time:.3f}s/{elapsed_time:.3f}s | Tokens: {input_tokens}/{output_tokens}/{total_tokens}".format(**summary)
        event_bus.broadcast('summary', summarys)
        self.console.print(f"\n⏹ [cyan]{T('end_instruction')} {summarys}")

    def build_user_prompt(self):
        prompt = {'task': self.instruction}
        prompt['python_version'] = platform.python_version()
        prompt['platform'] = platform.platform()
        prompt['today'] = date.today().isoformat()
        prompt['locale'] = locale.getlocale()
        prompt['think_and_reply_language'] = '始终根据用户查询的语言来进行所有内部思考和回复，即用户使用什么语言，你就要用什么语言思考和回复。'
        prompt['work_dir'] = '工作目录为当前目录，默认在当前目录下创建文件'
        if getattr(self.console, 'gui', False):
            prompt['matplotlib'] = "我现在用的是 matplotlib 的 Agg 后端，请默认用 plt.savefig() 保存图片后用 runtime.display() 显示，禁止使用 plt.show()"
            #prompt['wxPython'] = "你回复的Markdown 消息中，可以用 ![图片](图片路径) 的格式引用之前创建的图片，会显示在 wx.html2 的 WebView 中"
        else:
            prompt['TERM'] = os.environ.get('TERM')
            prompt['LC_TERMINAL'] = os.environ.get('LC_TERMINAL')
        return prompt

    def run(self, instruction=None, *, llm=None, max_rounds=None):
        """
        执行自动处理循环，直到 LLM 不再返回代码消息
        """
        self.start_time = time.time()
        self.box(f"[yellow]{T('start_instruction')}", f'[red]{instruction or self.instruction}', align="center")
        if not instruction:
            prompt = self.build_user_prompt()
            event_bus('task_start', prompt)
            instruction = json.dumps(prompt, ensure_ascii=False)
            system_prompt = self.system_prompt
        else:
            system_prompt = None

        self.loop(instruction, system_prompt, llm)


    def loop(self, instruction, system_prompt=None, llm=None):
        """ Execute the task loop """
        rounds = 1
        max_rounds = self.max_rounds
        response = self.llm(instruction, system_prompt=system_prompt, name=llm)
        while response and rounds <= max_rounds:
            blocks = self.parse_reply(response)

            if 'call_tool' not in blocks and 'main' not in blocks:
                break

            if 'call_tool' in blocks:
                response = self.process_mcp_reply(blocks, llm)
            else:
                response = self.process_code_reply(blocks, llm)

            rounds += 1
            if event_bus.is_stopped():
                break
        self.print_summary()
        self.console.bell()


    def start(self, instruction):
        """ Start a new task """
        self.start_time = time.time()
        self.instruction = instruction
        self.box(f"[yellow]{T('start_instruction')}", f'[red]{instruction}', align="center")
        prompt = self.build_user_prompt()
        instruction = json.dumps(prompt, ensure_ascii=False)
        system_prompt = self.system_prompt
        self.loop(instruction, system_prompt)
        

    def chat(self, prompt):
        system_prompt = None if self.llm.history else self.system_prompt
        response, ok = self.llm(prompt, system_prompt=system_prompt)
        self.console.print(Markdown(response))

    def step(self):
        response = self.llm.get_last_message()
        if not response:
            self.console.print(f"❌ {T('no_context')}")
            return
        self.process_reply(response)

    def sync_to_cloud(self, verbose=True):
        """ Sync result
        """
        url = T('tt_share_url')

        trustoken_apikey = self.settings.get('llm', {}).get('Trustoken', {}).get('api_key')
        if not trustoken_apikey:
            trustoken_apikey = self.settings.get('llm', {}).get('trustoken', {}).get('api_key')
        if not trustoken_apikey:
            return False
        self.console.print(f"[yellow]{T('sync_to_cloud')}")
        try:
            response = requests.post(url, json={
                'apikey': trustoken_apikey,
                'author': os.getlogin(),
                'instruction': self.instruction,
                'llm': self.llm.history.json(),
                'runner': self.runner.history,
            }, verify=True, timeout=30)
        except Exception as e:
            print(e)
            return False

        status_code = response.status_code
        if status_code in (200, 201):
            if verbose:
                data = response.json()
                url = data.get('url', '')
                if url:
                    self.console.print(f"[green]{T('upload_success', url)}[/green]")
            return True

        if verbose:
            self.console.print(f"[red]{T('upload_failed', status_code)}:", response.text)
        return False