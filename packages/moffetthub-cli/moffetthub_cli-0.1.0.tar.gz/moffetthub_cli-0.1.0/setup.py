from setuptools import setup, find_packages

setup(
    name="moffetthub-cli",  # 包名
    version="0.1.0",  # 版本号
    packages=find_packages(),  # 自动发现包
    include_package_data=True,  # 包含非代码文件
    install_requires=[
        "requests",
        "tqdm",
    ],  # 依赖包
    entry_points={
        "console_scripts": [
            "moffetthub-cli=moffetthub_cli.main:main",  # 命令行入口
        ],
    },
    author="orion.zou",
    author_email="guangyuan.zou@moffett.ai",
    description="A CLI tool for querying and downloading files from MoffettHub.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/moffetthub-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
