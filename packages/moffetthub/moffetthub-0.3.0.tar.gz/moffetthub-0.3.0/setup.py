from setuptools import setup, find_packages

setup(
    name="moffetthub",  # 包名
    version="0.3.0",  # 版本号
    packages=find_packages(),  # 自动发现包
    include_package_data=True,  # 包含非代码文件
    install_requires=[
        "requests>=2.31.0",
        "tqdm>=4.66.0",
        "click>=8.1.0",
        "rich>=13.0.0",
    ],  # 依赖包
    extras_require={
        "dev": [
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "moffetthub-cli=moffetthub_cli.main:main",  # 命令行入口
        ],
    },
    author="Alinshans",
    author_email="alinshans@gmail.com",
    description="A CLI tool for querying and downloading files from MoffettHub.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="cli, model-hub",
)
