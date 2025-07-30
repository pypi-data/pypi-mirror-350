# setup.py
from setuptools import setup, find_packages

setup(
    name='add-mcp-server',         # 包名称，在 PyPI 上的名称
    version='0.1.0',                # 版本号
    packages=find_packages(),       # 自动查找包目录
    entry_points={
        'console_scripts': [
            # 定义命令行工具，用户运行 uvx your-mcp-server 时会执行 your_mcp_server.main:main
            'your-mcp-server=your_mcp_server.main:main',
        ],
    },
    install_requires=[],            # 如有依赖可以在这里添加
    author='Your Name',
    author_email='your.email@example.com',
    description='A custom MCP Server example for PyPI.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)