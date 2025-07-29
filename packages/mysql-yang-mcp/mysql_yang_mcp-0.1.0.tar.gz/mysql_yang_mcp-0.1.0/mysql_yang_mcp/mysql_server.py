# mysql_stdio.py
from mcp.server.fastmcp import FastMCP
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import logging
from argparse import ArgumentParser

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 创建MCP服务器
mcp = FastMCP("MySQL Query Tool")

def parse_args():
    """解析命令行参数"""
    parser = ArgumentParser(description="MySQL查询工具")
    parser.add_argument("--mysql-host", help="MySQL服务器地址")
    parser.add_argument("--mysql-port", type=int, help="MySQL端口号")
    parser.add_argument("--mysql-user", help="MySQL用户名")
    parser.add_argument("--mysql-password", help="MySQL密码")
    parser.add_argument("--mysql-database", help="数据库名")
    return parser.parse_args()

def get_db_config():
    """从环境变量和命令行参数获取数据库配置"""
    # 加载.env文件
    load_dotenv()
    
    # 获取命令行参数
    args = parse_args()
    
    # 优先使用命令行参数，如果没有则使用环境变量
    config = {
        "host": args.mysql_host or os.getenv("MYSQL_HOST", ""),
        "port": args.mysql_port or int(os.getenv("MYSQL_PORT", "3306")),
        "user": args.mysql_user or os.getenv("MYSQL_USER", "root"),
        "password": args.mysql_password or os.getenv("MYSQL_PASSWORD", "111111"),
        "database": args.mysql_database or os.getenv("MYSQL_DATABASE", "dbgpt"),
    }
    
    if not all([config["user"], config["password"], config["database"]]):
        raise ValueError("缺少必需的数据库配置")
    
    return config

@mcp.tool()
def execute_sql(query: str) -> str:
    """执行SQL查询语句
    
    参数:
        query (str): 要执行的SQL语句，支持多条语句以分号分隔
    
    返回:
        str: 查询结果，格式化为可读的文本
    """
    config = get_db_config()
    logger.info(f"执行SQL查询: {query}")
    
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                statements = [stmt.strip() for stmt in query.split(";") if stmt.strip()]
                results = []
                
                for statement in statements:
                    try:
                        cursor.execute(statement)
                        
                        # 检查语句是否返回了结果集
                        if cursor.description:
                            columns = [desc[0] for desc in cursor.description]
                            rows = cursor.fetchall()
                            
                            # 格式化输出
                            result = [" | ".join(columns)]
                            result.append("-" * len(result[0]))
                            
                            for row in rows:
                                formatted_row = [str(val) if val is not None else "NULL" for val in row]
                                result.append(" | ".join(formatted_row))
                            
                            results.append("\n".join(result))
                        else:
                            conn.commit()  # 提交非查询语句
                            results.append(f"查询执行成功。影响行数: {cursor.rowcount}")
                    
                    except Error as stmt_error:
                        results.append(f"执行语句 '{statement}' 出错: {str(stmt_error)}")
                
                return "\n\n".join(results)
    
    except Error as e:
        error_msg = f"执行SQL '{query}' 时出错: {e}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
def get_table_structure(table_name: str) -> str:
    """获取指定表的结构信息
    
    参数:
        table_name (str): 表名
    
    返回:
        str: 表结构信息，包含字段名、类型、是否为NULL和默认值
    """
    query = f"DESCRIBE {table_name};"
    return execute_sql(query)

@mcp.tool()
def list_tables() -> str:
    """列出数据库中的所有表"""
    query = "SHOW TABLES;"
    return execute_sql(query)

@mcp.resource("db://tables")
def get_tables_resource() -> list:
    """获取数据库中的所有表名作为资源"""
    config = get_db_config()
    
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES;")
                return [row[0] for row in cursor.fetchall()]
    except Error as e:
        logger.error(f"获取表列表时出错: {e}")
        return []

@mcp.resource("db://schema/{table}")
def get_table_schema(table: str) -> dict:
    """获取指定表的模式定义作为资源"""
    config = get_db_config()
    
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                # 获取表结构
                cursor.execute(f"DESCRIBE {table};")
                columns = cursor.fetchall()
                
                schema = {
                    "table": table,
                    "columns": []
                }
                
                for col in columns:
                    schema["columns"].append({
                        "name": col[0],
                        "type": col[1],
                        "nullable": col[2] == "YES",
                        "key": col[3],
                        "default": col[4],
                        "extra": col[5]
                    })
                
                return schema
    except Error as e:
        logger.error(f"获取表 {table} 的模式时出错: {e}")
        return {"error": str(e)}

def main():
    """主函数"""
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
