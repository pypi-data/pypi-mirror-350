# clickhouse-df
请求 clickhouse集群，结果返回pandas.DataFrame/polars.DataFrame

### 安装
```shell
pip install -U clickhouse-df
```

### 示例

```python
import clickhouse_df

# 版本
print(clickhouse_df.__version__)

# 集群配置
config = dict(
    urls=["<host1>:<port>", "<host2>:<port>", ....],
    user="<user_name>", 
    password="xxxxxx", 
)

sql = "select * from <db_name>.<tb_name> where date='2024-10-23';"

# 例子1
with clickhouse_df.connect(**config):
    # 请求 polars 
    df_pl = clickhouse_df.to_polars(sql)
    # 请求 pandas
    df_pd = clickhouse_df.to_pandas(sql)

# 例子2
conn = clickhouse_df.connect(**config)
df_pl = clickhouse_df.to_polars(sql, conn)
df_pd = clickhouse_df.to_pandas(sql, conn)
conn.disconnect()