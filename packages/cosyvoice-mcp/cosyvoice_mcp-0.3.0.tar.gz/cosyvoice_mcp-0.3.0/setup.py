from setuptools import setup, find_packages

setup(
    name="cosyvoice-mcp",
    version="0.3.0",  # 按需更新版本号（遵循语义化版本）
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastmcp>=2.5.1",
        "dashscope>=1.23.0",
        "pydantic>=2.11.5"
    ],
    entry_points={
        "console_scripts": [
            "cosyvoice-mcp=cosyvoice_mcp.main:main",  # 定义命令行入口
        ],
    },
    author="Marlon Chan",
    author_email="yuxian.cj@alibaba-inc.com",
    description="A MCP server for CosyVoice TTS using DashScope API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chenjin3/cosyvoice-mcp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)