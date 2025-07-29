import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
import akshare as ak


def sync_us_company_info():
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
    stock_us_spot_em_df = stock_us_spot_em_df.loc[stock_us_spot_em_df['total_mv']!=0]
    stock_us_spot_em_df.to_csv('us_stock.csv', index=False)
    return stock_us_spot_em_df


if __name__ == '__main__':
    sync_us_company_info()
