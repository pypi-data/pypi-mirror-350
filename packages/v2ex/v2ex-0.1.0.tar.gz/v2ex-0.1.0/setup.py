from setuptools import setup, find_packages

setup(
    name="v2ex",
    version="0.1.0",
    description="V2EX 热门话题终端工具",
    author="xiao.xu",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "rich",
        "prompt_toolkit",
        "requests",
        "beautifulsoup4",
        "lxml",
        "paprika",
        "markdown-it-py",
        "Pygments",
        "tabulate",
        "typing_extensions",
        "urllib3",
        "wcwidth",
        "certifi",
        "charset-normalizer",
        "idna",
        "mdurl",
        "soupsieve",
        "bs4"
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "v2ex = v2expkg.v2ex:main"
        ]
    },
    include_package_data=True,
) 