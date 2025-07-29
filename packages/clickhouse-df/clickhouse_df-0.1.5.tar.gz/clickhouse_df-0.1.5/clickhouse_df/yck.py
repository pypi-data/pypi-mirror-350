# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/11/4 上午9:01
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""
from random import randint
from clickhouse_driver import Client
from . import dtype
from .thread_utils import ThreadLocalVariable
import pandas as pd
import polars as pl
import pyarrow as pa


_conns = ThreadLocalVariable(default_factory=lambda: [])

def connect(urls: list[str], user: str, password: str) -> Client:
    """
    连接clickhouse服务器, 支持集群
    Parameters
    ----------
    urls: List[str]
        ["host1:port1", "host2:port2", "host3:port3"...]
    user: str
        用户名
    password: str
        密码
    Returns
    -------
    client: Client
        ClickHouse 数据库连接客户端，必须是一个有效的 `clickhouse_driver.Client` 实例
    """
    i = randint(0, len(urls) - 1)
    url_ini = urls[i]
    [host, port] = url_ini.split(":")
    conn = Client(host, port=port, round_robin=True, alt_hosts=",".join(urls), user=user, password=password)
    conns = _conns.get()
    conns.append(conn)
    return conns[-1]


def to_pandas(sql, conn: Client|None=None) -> pd.DataFrame:
    """
    请求ck，返回 pandas.DataFrame
    Parameters
    ----------
    sql: str
        查询语句
    conn: Client
        ClickHouse 数据库连接客户端，必须是一个有效的 `clickhouse_driver.Client` 实例
    Returns
    -------
    pandas.DataFrame
        包含查询结果的 Pandas DataFrame。如果查询没有返回任何数据，则
        返回一个空的 DataFrame 或者 None
    """
    conn = conn if conn is not None else _conns.get()[-1]
    return conn.query_dataframe(sql)


def to_polars(sql, conn: Client|None=None) -> pl.DataFrame:
    """
    请求ck，返回 polars.DataFrame
    Parameters
    ----------
    sql: str
        查询语句
    conn: Client
        ClickHouse 数据库连接客户端，必须是一个有效的 `clickhouse_driver.Client` 实例。
    Returns
    -------
    polars.DataFrame
        包含查询结果的 Polars DataFrame。如果查询没有返回任何数据，则
        返回一个空的 DataFrame 或者 None
    """
    conn = conn if conn is not None else _conns.get()[-1]
    data, columns = conn.execute(sql, columnar=True, with_column_types=True)
    # columns = {name: dtype.infer_dtype_from_database_typename(type_) for name, type_ in columns}
    if len(data) < 1:
        columns = {name: dtype.infer_dtype_from_database_typename(type_) for name, type_ in columns}
        return pl.DataFrame(schema=columns)
    columns = {name: dtype.map_clickhouse_to_arrow(type_) for name, type_ in columns}
    # 构造 Arrow 表（逐列传递数据和类型）
    arrow_table = pa.Table.from_arrays(
        [pa.array(col, type=col_type) for col, col_type in zip(data, columns.values())],
        schema=pa.schema(columns))

    # 从 Arrow 表构造 Polars DataFrame
    return pl.from_arrow(arrow_table)
