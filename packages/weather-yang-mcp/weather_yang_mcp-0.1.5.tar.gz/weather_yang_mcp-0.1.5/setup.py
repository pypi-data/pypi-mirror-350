from setuptools import setup, find_packages

# *****stdio模式*****
# 目录架构格式，严格按照这个项目；
# 这个setup文件可以上传到pypi上，并可以正常被uvx调用
# 应用启动：uvx time_yang_mcp --local-timezone=America/New_York
# 注意 entry_points、  install_requires要填写正确；
# pypi 有超时问题，可以多试几次，多连接几次；
# mcp包有时候会出现找不到问题，多连接几次；
#
#启动可视化测试
# cd c:\GuangHuanWork\software\LLM2025\time_yang_mcp
# npx @modelcontextprotocol/inspector uvx time_yang_mcp --local-timezone=America/New_York
# Asia/Shanghai 测试；

# 应用启动：uvx weather_yang_mcp
# 启动可视化测试
# cd c:\GuangHuanWork\software\LLM2025\weather_yang_mcp
# npx @modelcontextprotocol/inspector uvx weather_yang_mcp

setup(
    name="weather_yang_mcp",    
    version="0.1.5",
    description="A get weather tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="jokul",
    author_email="test@qq.com",
    url="https://github.com/jokulyang/mytool",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            # 定义命令行工具
            'weather_yang_mcp=weather_yang_mcp.__main__:__main__',
        ],
    },
    install_requires=[
        "mcp>=1.9.0",
        "pydantic>=2.0.0",
        "tzdata>=2023.3",
        "typing-extensions>=4.7.0",
        "httpx>=0.24.0"  # 添加 HTTP 客户端依赖
       
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  # 添加操作系统兼容性
        "Development Status :: 3 - Alpha",     # 添加开发状态
        "Intended Audience :: Developers",     # 添加目标用户群
        "Topic :: Software Development :: Libraries :: Python Modules"  # 添加主题分类
    ],
    python_requires=">=3.11",
)