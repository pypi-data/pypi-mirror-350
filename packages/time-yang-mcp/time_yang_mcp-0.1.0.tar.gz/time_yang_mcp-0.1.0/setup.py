from setuptools import setup, find_packages
 
setup(
    name="time_yang_mcp",  # 包名，pip install  
    version="0.1.0",
    description="A get time tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="jokul",
    author_email="test@qq.com",
    url="https://github.com/jokulyang/mytool",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            # 定义命令行工具，用户运行 uvx your-mcp-server 时会执行 your_mcp_server.main:main
            'time_yang_mcp=time_yang_mcp.main:main',
        ],
    },
    install_requires=[
        "mcp-core>=0.1.0",
        "pydantic>=2.0.0",
        "tzdata>=2023.3",
        "typing-extensions>=4.7.0",
        "pytest>=7.0.0",
        "black>=23.0.0",
        "mypy>=1.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.11",
)