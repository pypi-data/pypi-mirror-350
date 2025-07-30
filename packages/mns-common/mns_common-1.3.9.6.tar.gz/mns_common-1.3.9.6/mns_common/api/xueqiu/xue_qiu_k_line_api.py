import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import requests
import pandas as pd


# year 年
#  quarter 季度
# month 月度
# week 周
# day 日
def get_xue_qiu_k_line(symbol, period, cookie, end_time, hq):
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"

    params = {
        "symbol": symbol,
        "begin": end_time,
        "period": period,
        "type": hq,
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
        # 直接抛出带有明确信息的异常
        raise ValueError("调用雪球接口失败")


if __name__ == '__main__':
    number = 1
    cookies = "cookiesu=581743780372237; device_id=e315f5f93cf4d1af01436bc234312ebb; s=ci1338vttl; xq_a_token=75116a2a5439edb58d3d99533cfbc4d72e0ee819; xqat=75116a2a5439edb58d3d99533cfbc4d72e0ee819; xq_r_token=521f1781edc2a09cffdf7d59b5b3fe37c1c1f577; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0OTk0OTc1MywiY3RtIjoxNzQ4MTU5ODU3NzYwLCJjaWQiOiJkOWQwbjRBWnVwIn0.HP0CrptQ8jJjU9eJ0LhdAA_PlErW_Sp4OA5SjCyIQhKN5nTlrlovKty3IKutb5Nn_8EgeLZqrTeLKTsNIIE1uRGEppgo-Suk6_IOV1X900M47R2aBV2TX-J3rSmfyP7mAXav8CVT1pwiRU8Xr_ag3XT8WxVNQY1aOiV5JEyKeJucwvRyoa0iB4sM9j2kxcRXCF3nK9JnofsvAg-I7ySf3hCly3csj-zWQQSWeUjpmMlMS2ddLjvAHQUNbBFMTZ2BVji0ae3mURUB2jz4A6O8pZGZHuh3qDdQfeLq0i80H2AnOEqsJ246THsS7RS20HidyWWbYm3gBlRptDr1lWgsGg; u=581743780372237; Hm_lvt_1db88642e346389874251b5a1eded6e3=1746435822,1747730708,1748159904; HMACCOUNT=2CB33FC8EC07B09A; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1748159918; ssxmod_itna=QqjxRQKiTx2DgD4qbD0nYDCDpEDymxBP01kD+xQ5DODLxn+xGdqufh=z3O=DcllGdHwiYK9DDsZ4xiNDAg40iDC3md1aUr0TPz=GmnG5Gyz7AbR3Otq2Q8c51cYZO7eBpjlSgy4xAEYDQKDoxGkDiyKD0FY+Diibx0rD0eDPxDYDGbwDDyIoUxDj7gwTzOsk77eo8oDb6xhfjxDR=dDSQ8vs8Os=Y3DarY3kUxGDmKDIalKf7oDF=d3Pq0ke4i35xEnbq0OSFYG2movzUrceE0rde4FKYR1=QiqOlG4aWG4ecpxnTillebZnbVQGFzDsQRS4xDGSKHBKqxs3DqhYkCuke4CQ+YKYozoo52q5xd1E4kEmROwyY5M04aAQKD5h05NGDs0Dl0DoCs4D; ssxmod_itna2=QqjxRQKiTx2DgD4qbD0nYDCDpEDymxBP01kD+xQ5DODLxn+xGdqufh=z3O=DcllGdHwiYK4Dfi3Qe+0wxDFOihv=8B0DD/CcBOpAgn9LMTKhhSafFNwTqw64jzZ/oQMQq4dVL95j2MbxV+kj1R3inzDd47u0y0+dUbwdeLB2QA+QBj4unSq=lSq0A0LhD1xfxGMR6KPLu+bTxvmj30MbWLjxqYLcc9=ajBhTle/THgetZmeTqY7GQCa7qFTx4+IfcbdxfeFbUSI7m5ndqfBxLhOyjZidzB887ak=NR/NzFlhDkTQPSksf+WR0WNGuFSqxSFFCh5BR5iaq0bVFpxSTc3PnQ0U9RIKDN0bA02TQDezeHGhVG7Vz4QnrLi03kGg+vRU0w4p3Ti0n7Kn5CWoGUPz99Fip6GEYZi+eIdFnD75WCq0iu1AbK7AFQDNQadaG5aIDkA4Xy+7gUS5SWGEGiWGAxHg+RipnTa3B948MFWQkPG9ay8MYs4B8vYw+4ycXQQhpmHecNj9YHuooqedamM7lW4QXaFnLdSTgBlfWG2SlAwvkmjTqwKuI4LR3cys+lX/uUiw4h8mfnKhZEcaXkTA33sFo+aT2djFUm2Cr2b/ECeLiqeOCmKiYbPZUhHC9vFm48Dnz1y5azM2wBzcKc89hcKXSpR8f4MnL5RBA/KxANHjN6g4NrXv0qCK7EX0GbbDo0WOH+EC2dj4z7tYGDh5Rf3QDrYVr3YwMGWB+QCWG+Q7ofPuoOIXGBrfIeE4nhd3o4h3YKo+pD5Crd0CRYC7Kp20qMSrziDD"
    while True:
        test_df = get_xue_qiu_k_line('SZ000004', 'day', cookies, '1748246492232', 'after')
        print(number)
        number = number + 1
