from setuptools import setup, find_packages

setup(
    name="yzc",  # 包名
    version="0.2.1",  # 版本号
    author="clveryang",  # 作者名
    author_email="yangclver@gmail.com",  # 作者邮箱
    description="A simple CLI tool to print Hello, World!",  # 简短描述
    long_description=open("README.md").read(),  # 长描述（从 README.md 读取）
    long_description_content_type="text/markdown",  # 描述格式
    url="https://github.com/yourusername/yzc",  # 项目主页（可选）
    packages=find_packages(),  # 自动发现包
    entry_points={
        "console_scripts": [
            "yzc=yzc.cli:main"  # 定义命令行工具入口点
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python 版本要求
)
