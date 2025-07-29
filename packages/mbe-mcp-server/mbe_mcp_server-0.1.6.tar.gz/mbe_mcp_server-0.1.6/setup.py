from setuptools import setup, find_packages

setup(
    name="mbe_mcp_server",  # 项目名称
    version="0.1.6",  # 版本号
    description="韬略服务对外Mcp服务",  # 简要描述
    long_description=open('README.md', encoding='utf-8').read(),
    author="yanan.wya",  # 作者名字
    author_email="wya0556@qq.com",  # 作者邮箱
    url="",  # 项目
    packages=find_packages(),  # 自动发现所有包
    entry_points={
        'console_scripts': [
            # 定义命令行工具，运行 uvx mbe-mcp-server 时会执行 mbe_mcp_server.main:main
            'mbe-mcp-server=mbe_mcp_server.main:main',
        ],
    },
    install_requires=[
        "mcp",  # 所依赖的第三方库，例如 mcp 库
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)