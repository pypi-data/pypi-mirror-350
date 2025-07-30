import akshare as ak
import pandas as pd
from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')


def us_stock():
    # 输入参数
    symbol = input("请输入股票代码（all:全量(时间很长),特定代码:106.TTE）：")
    start_date = input("请输入开始日期（格式：YYYYMMDD）：")
    end_date = input("请输入结束日期（格式：YYYYMMDD）：")
    fq = input("请输入复权信息（前复权:qfq,不复权:bfq,后复权:hfq）：")
    k_line_period = input("请输入k线周期（日线:daily,周线:weekly,月线:monthly）：")
    db_name = "us_stock_" + fq + "_" + k_line_period
    if fq == 'bfq':
        fq = ''
    if symbol != 'all':
        # 获取股票历史数据
        stock_us_hist_df = ak.stock_us_hist(symbol=symbol,
                                            period=k_line_period,
                                            start_date=start_date,
                                            end_date=end_date,
                                            adjust=fq)
        # 保存数据到 CSV 文件
        stock_us_hist_df.to_csv(f"{symbol}_historical_data.csv", index=False)
        print(f"数据已保存到 {symbol}_historical_data.csv")
    else:
        stock_us_spot_em_df = ak.stock_us_spot_em()
        stock_us_spot_em_df = stock_us_spot_em_df.rename(columns={
            "序号": "index",
            "代码": "symbol",
            "名称": "name",
            "涨跌额": "change_price",
            "涨跌幅": "chg",
            "开盘价": "open",
            "最高价": "high",
            "最低价": "low",
            "最新价": "now_price",
            "昨收价": "last_price",
            "总市值": "total_mv",
            "市盈率": "pe",
            "成交量": "volume",
            "成交额": "amount",
            "振幅": "pct_chg",
            "换手率": "exchange"
        })
        stock_us_spot_em_df = stock_us_spot_em_df.sort_values(by=['amount'], ascending=False)
        stock_us_spot_em_df = stock_us_spot_em_df.fillna(0)
        stock_us_spot_em_df = stock_us_spot_em_df.loc[stock_us_spot_em_df['total_mv'] != 0]

        k_line_result = pd.DataFrame()

        for stock_us_one in stock_us_spot_em_df.itertuples():
            try:
                # 获取股票历史数据
                stock_us_hist_df = ak.stock_us_hist(symbol=stock_us_one.symbol,
                                                    period=k_line_period,
                                                    start_date=start_date,
                                                    end_date=end_date,
                                                    adjust=fq)
                stock_us_hist_df = stock_us_hist_df.rename(columns={
                    "日期": "date",
                    "涨跌额": "change_price",
                    "涨跌幅": "chg",
                    "开盘": "open",
                    "最高": "high",
                    "最低": "low",
                    "收盘": "close",
                    "成交量": "volume",
                    "成交额": "amount",
                    "振幅": "pct_chg",
                    "换手率": "exchange"
                })

                k_line_result = pd.concat([stock_us_hist_df, k_line_result])
                stock_us_hist_df['_id'] = stock_us_one.symbol + '_' + stock_us_hist_df['date']
                stock_us_hist_df['symbol'] = stock_us_one.symbol
                stock_us_hist_df['name'] = stock_us_one.name
                mongodb_util.insert_mongo(stock_us_hist_df, db_name)
                print(f"同步k线数据到: {stock_us_one.name}")
            except BaseException as e:
                print(f"同步数据发生异常: {stock_us_one.name}, {e}")

        # 保存数据到 CSV 文件
        k_line_result.to_csv(f"{symbol}_historical_data.csv", index=False)
        print(f"数据已保存到 {symbol}_historical_data.csv")


if __name__ == "__main__":
    us_stock()
