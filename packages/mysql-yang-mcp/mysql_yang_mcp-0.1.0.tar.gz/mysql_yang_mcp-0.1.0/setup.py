from setuptools import setup, find_packages

# *****stdio模式*****
# 目录架构格式，严格按照这个项目；
# 这个setup文件可以上传到pypi上，并可以正常被uvx调用
# 应用启动：uvx mysql_yang_mcp
# uvx mysql_yang_mcp --mysql-host=localhost --mysql-port=3306 --mysql-user=root --mysql-password=your_password --mysql-database=your_database
# 注意 entry_points、  install_requires要填写正确；
# pypi 有超时问题，可以多试几次，多连接几次；
# mcp包有时候会出现找不到问题，多连接几次；

setup(
    name="mysql_yang_mcp",    
    version="0.1.0",
    description="A MySQL query tool with MCP support",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="jokul",
    author_email="test@qq.com",
    url="https://github.com/jokulyang/mytool",  
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            # 定义命令行工具
            'mysql_yang_mcp=mysql_yang_mcp.__main__:__main__',
        ],
    },
    install_requires=[
        "mcp>=1.9.0",
        "pydantic>=2.0.0",
        "mysql-connector-python>=8.0.0",  # MySQL连接器
        "python-dotenv>=0.19.0",         # 环境变量管理
        "typing-extensions>=4.7.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.11",
)