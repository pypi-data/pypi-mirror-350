# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2025/5/23 13:10
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

import clickhouse_df

urls=["192.168.0.231:19000", "192.168.0.232:19000", "192.168.0.234:19000", "192.168.0.236:19000"]
user="ro_zhangyundi"
password="qSOPgL0ojMer"

test_query = f"""
select replaceRegexpAll(order_book_id, '[^0-9]', '') as code,
       argMax(close, volume)                         as price,
       last_value(prev_close)                        as prev_close
from cquote.stock_tick_rt_distributed final
where EventDate = '2025-05-23'
and close > 0
and volume > 0
group by order_book_id
order by order_book_id;
"""


if __name__ == '__main__':
    # clickhouse_df.connect(urls, user, password)
    with clickhouse_df.connect(urls, user, password):
        df_pd = clickhouse_df.to_pandas(test_query)
        df_pl = clickhouse_df.to_polars(test_query)
        print(df_pd)
        print(df_pl)
