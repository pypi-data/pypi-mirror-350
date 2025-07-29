# v2ex

一个基于 Python 的命令行 V2EX 热门话题与回复浏览工具，支持自动补全、历史建议、键盘快捷键，终端美观显示。

## 特性
- 获取 V2EX 热门话题和今日热门
- 查看指定话题的详细内容与全部回复
- 支持命令行交互、自动补全、历史建议
- 终端美观分页显示，支持多种快捷键

## 安装

推荐使用 pip 安装（需 Python 3.7+）：

```bash
pip install v2ex
```

或从源码安装：

```bash
git clone https://github.com/taizilongxu/v2ex-shell.git
cd v2ex-shell
pip install .
```

## 使用方法

安装后，直接在终端输入：

```bash
v2ex
```

- 启动后自动显示 V2EX 热门话题
- 输入数字（如 1、2...）查看对应话题详情与回复
- 输入字母（如 a、b、c...）查看今日热门话题详情
- 输入 `hot` 刷新热门话题
- 输入 `help` 查看命令帮助
- Ctrl+C 重新输入，Ctrl+D 退出

## 依赖

主要依赖：
- rich
- prompt_toolkit
- requests
- beautifulsoup4
- lxml
- paprika

完整依赖见 requirements.txt。

## 数据结构

- `Topic`：话题对象，包含 id、title、replies、url、content、node_title、username、last_reply_user、created 等字段
- `Reply`：回复对象，包含 id、topic_id、content、username、created 等字段

## 数据来源

- 热门话题和回复数据来自 V2EX 官方 API 和网页解析，仅用于学习与交流。

## 贡献

欢迎 issue 和 PR！如有建议或 bug，欢迎反馈。

---

> 本项目仅供学习交流，严禁用于商业用途。
