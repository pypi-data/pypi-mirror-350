from setuptools import setup, find_packages
 
setup(
    name="weather_yang_mcp",  # 包名，pip install 时用这个
    version="0.1.3",
    description="A get weather tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="jokul",
    author_email="test@qq.com",
    url="https://github.com/jokulyang/mytool",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)