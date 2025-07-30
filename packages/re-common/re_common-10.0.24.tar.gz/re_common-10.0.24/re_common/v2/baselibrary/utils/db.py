from contextlib import asynccontextmanager
from typing import AsyncGenerator, Tuple

import aiomysql
from aiomysql import Pool, Connection, Cursor, DictCursor

DB_CONFIG = {
    'host': '192.168.98.55',
    'port': 4000,
    'user': 'dataware_house_baseUser',
    'password': 'FF19AF831AEBD580B450B16BF9264200',
    'db': 'dataware_house_base',
    'charset': 'utf8mb4',
    'minsize': 16,  # 最小连接数
    'maxsize': 128,  # 最大连接数
    'autocommit': False,  # 自动提交事务
    'pool_recycle': 3600,  # 每个连接的回收时间（秒），超过此时间后连接将被关闭并重新创建，避免失效连接
    'echo': False,  # 打印SQL语句
}


@asynccontextmanager
async def get_db_pool():
    """异步数据库连接池管理工具"""
    pool: Pool = await aiomysql.create_pool(**DB_CONFIG)
    try:
        yield pool
    finally:
        pool.close()
        await pool.wait_closed()


@asynccontextmanager
async def get_session(pool: Pool) -> AsyncGenerator[Tuple[Connection, Cursor], None]:
    """获取数据库会话"""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            yield conn, cursor
