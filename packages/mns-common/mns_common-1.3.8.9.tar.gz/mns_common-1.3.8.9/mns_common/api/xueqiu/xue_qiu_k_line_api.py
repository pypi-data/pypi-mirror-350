import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from loguru import logger
import requests
import pandas as pd


# year 年
#  quarter 季度
# month 月度
# week 周
# day 日
def get_xue_qiu_k_line(symbol, period, cookie):
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"

    params = {
        "symbol": symbol,
        "begin": "1742574377493",
        "period": period,
        "type": "before",
        "count": "-120084",
        "indicator": "kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://xueqiu.com",
        "priority": "u=1, i",
        "referer": "https://xueqiu.com/S/SZ300879?md5__1038=n4%2BxgDniDQeWqxYwq0y%2BbDyG%2BYDtODuD7q%2BqRYID",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "cookie": cookie
    }
    try:
        response = requests.get(
            url=url,
            params=params,
            headers=headers
        )

        if response.status_code == 200:
            response_data = response.json()
            df = pd.DataFrame(
                data=response_data['data']['item'],
                columns=response_data['data']['column']
            )
            # 处理DataFrame列（秒级时间戳）
            df['str_day'] = pd.to_datetime(df['timestamp'], unit='ms').dt.normalize()
            df["str_day"] = df["str_day"].dt.strftime("%Y-%m-%d")
            return df
        else:
            return pd.DataFrame()
    except BaseException as e:
        logger.error("同步股票年度数据出现异常:{},{}", symbol, e)


if __name__ == '__main__':
    test_df = get_xue_qiu_k_line('SZ000001', 'year')
    print(test_df)
