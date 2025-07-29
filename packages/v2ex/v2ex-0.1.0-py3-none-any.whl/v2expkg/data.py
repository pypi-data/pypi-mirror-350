from . import web
from . import models

from rich.panel import Panel
import os
from time import time
from rich.table import Table
from rich import box
from rich.markdown import Markdown
from rich.console import Console


class Data():
    topic_list = []
    topic_hot_list = []

    reply_list = []
    topic_index = None

    console = Console()

    def status(func):
        def with_status(self, *args, **kwargs):
            with self.console.status("[bold green] Getting info...") as status:
                start = time()
                func(self, *args, **kwargs)
                print("Time: %0.03fs" % (time() - start))
        return with_status

    def run(self, text):
        text = text.strip()
        if text == 'hot':
            self.get_home()
            self.build_home()
        elif text == 'help':
            self.console.print('[bold green]命令帮助：[/]')
            self.console.print('[yellow]hot[/]：刷新并显示 V2EX 热门话题')
            self.console.print('[yellow]数字（如 1、2...）[/]：查看对应编号的话题详情与回复')
            self.console.print('[yellow]a-z[/]：查看今日热门话题详情（输入如 a、b、c...）')
            self.console.print('[yellow]help[/]：显示本帮助信息')
            self.console.print('[yellow]Ctrl+C[/]：中断当前输入，重新输入命令')
            self.console.print('[yellow]Ctrl+D[/]：退出程序')
        elif text.isdigit():
            if self.topic_list and 0 < int(text) <= len(self.topic_list):
                self.get_replies(int(text)-1)
                self.build_reply(self.reply_list, self.topic_list[int(text)-1])
            else:
                self.console.print("The topic range from 0 to {}".format(len(self.topic_list)))
        elif not text:
            return
        elif text == len(text) * text[0]:
            self.get_hot();
            try:
                self.get_hot_replies(ord(text)-97)
                self.build_reply(self.reply_list, self.topic_hot_list[ord(text) - 97])
            except:
                self.console.print('The hot topic range from a to {}'.format(chr(ord("a") + len(self.topic_hot_list) - 1)))
        else:
            self.console.print('You entered:', text)

    def build_home(self):
        self.console.clear()
        if not self.topic_list and not self.topic_hot_list:
            self.console.print(Panel('[red]未获取到任何话题，请检查网络或稍后重试。[/]', title='提示', border_style='red'))
            return

        table = Table.grid(padding=(0, 1), pad_edge=True)
        table.add_column("index", no_wrap=True, justify="center", style="yellow")
        table.add_column("topic")
        table.add_column("replies")
        for index, topic in enumerate(self.topic_list):
            topic_table = Table.grid(padding=0, collapse_padding=True)
            topic_table.add_row('[bold blue]{}[/]'.format(topic.title))
            if topic.last_reply_user:
                topic_table.add_row('[green]{}[/] • [dim]{}[/] • {} • 最后回复来自 {}'.format(topic.node_title, topic.username, topic.created, topic.last_reply_user))
            else:
                topic_table.add_row('[green]{}[/] • [dim]{}[/] • {}'.format(topic.node_title, topic.username, topic.created))
            table.add_row(str(index+1), topic_table, topic.replies)

        hot_table = Table.grid(padding=(0, 1), pad_edge=True)
        hot_table.add_column("index", style="yellow")
        hot_table.add_column("topic", style="blue", no_wrap=False)
        for index, topic in enumerate(self.topic_hot_list):
            hot_table.add_row(str(chr(97+index)), topic.title)

        message = Table(box=box.SIMPLE, header_style="red")
        message.add_column("Tab hot", justify="center")
        message.add_column("Today hot",ratio=0.2, justify="center")
        message.add_row(table, hot_table)

        os.environ['LESS'] = '-RXF'
        with self.console.pager(styles=True):
            self.console.print(Panel(message, title="[b cyan]V2EX 热门话题", border_style="cyan"))
            from datetime import datetime
            self.console.rule("[bold green]操作提示", style="green")
            self.console.print('[yellow]输入数字（1-{}）查看对应话题[/] | [yellow]输入字母（a-{}）查看今日热门[/]'.format(len(self.topic_list), chr(96+len(self.topic_hot_list)) if self.topic_hot_list else 'z'))
            self.console.print('[yellow]输入 hot 刷新 | 输入 help 查看帮助 | Ctrl+C 重新输入 | Ctrl+D 退出[/]')
            self.console.rule(style="cyan")
            self.console.print('[dim]数据刷新时间：{}[/]'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def build_topics_table(self, title, data):
        headers = ["id", "title", "replies", "node_title", "username", "url", "created"]
        table = Table(title=title, title_style="bold", highlight=True, box=box.SIMPLE_HEAVY, header_style="bold green")

        for header in headers:
            table.add_column(header)
        for index, topic in enumerate(data):
            table.add_row(str(index), topic.title, str(topic.replies), topic.node_title, topic.username, topic.url, topic.created)

        self.console.print(table)

    def build_reply(self, data, topic):
        table = Table(box=box.SIMPLE_HEAVY, show_header=False, expand=True)
        table.add_column(style="green", width=3)
        table.add_column(style="magenta", width=15)
        table.add_column()
        table.add_column(style="cyan", width=10)

        for index, reply in enumerate(data):
            table.add_row(str(index), reply.username, reply.content, Markdown(reply.created))

        self.console.clear()
        os.environ['LESS'] = '-RXF'
        with self.console.pager(styles=True):
            sponsor_message = Table.grid(padding=(0, 1))
            sponsor_message.add_column(justify="right", style="green")
            sponsor_message.add_column(no_wrap=False, style="yellow")

            sponsor_message.add_row("title", topic.title,)
            sponsor_message.add_row("created", None,)
            sponsor_message.add_row("username", topic.username,)
            sponsor_message.add_row("url", topic.url,)

            # 获取正文内容
            content = topic.content
            if not content and hasattr(topic, 'id'):
                try:
                    content = web.get_topic_content(topic.id)
                except Exception as e:
                    content = '[获取正文失败]'

            message = Table.grid(padding=(0, 1 ))
            message.add_column()
            message.add_column(no_wrap=False)
            message.add_row(sponsor_message, Markdown(content))
            self.console.print(
                Panel(
                    message,
                    box=box.ROUNDED,
                    padding=(1, 2),
                    title="[b red]Topic",
                    border_style="bright_blue",
                ),
            )

            # self.console.rule("[bold red]Replies")
            self.console.print(table)

    @status
    def get_hot(self):
        self.topic_hot_list = web.get_hot()

    @status
    def get_hot_replies(self, index):
        if not self.topic_hot_list:
            return
        topic = self.topic_hot_list[index]
        self.reply_list = web.get_replies(topic.id)

    @status
    def get_replies(self, index):
        if not self.topic_list:
            return
        topic = self.topic_list[index]
        self.reply_list = web.get_replies(topic.id)

    @status
    def get_home(self):
        self.topic_list, self.topic_hot_list = web.get_tab('hot')


if __name__ == "__main__":
    Data().get_hot()
