import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)

import mns_common.api.proxies.liu_guan_proxy_api as liu_guan_proxy_api
from functools import lru_cache
import pandas as pd
import mns_common.utils.data_frame_util as data_frame_util
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.constant.db_name_constant as db_name_constant
import datetime

mongodb_util = MongodbUtil('27017')


@lru_cache(maxsize=None)
def query_liu_guan_proxy_ip():
    ip_proxy_pool = mongodb_util.find_all_data(db_name_constant.IP_PROXY_POOL)
    return ip_proxy_pool


def clear_proxy_ip_cache():
    query_liu_guan_proxy_ip.cache_clear()
    mongodb_util.remove_data({}, db_name_constant.IP_PROXY_POOL)


def check_valid(str_now_date, ip_proxy_pool):
    effect_time = list(ip_proxy_pool['effect_time'])[0]
    if effect_time > str_now_date:
        return True
    else:
        clear_proxy_ip_cache()
        return False


def generate_proxy_ip(minutes):
    ip_proxy_pool = mongodb_util.find_all_data(db_name_constant.IP_PROXY_POOL)
    if data_frame_util.is_not_empty(ip_proxy_pool):
        return list(ip_proxy_pool['ip'])[0]
    else:
        query = {"type": "liu_guan_proxy", }
        stock_account_info = mongodb_util.find_query_data(db_name_constant.STOCK_ACCOUNT_INFO, query)
        order_id = list(stock_account_info['password'])[0]
        secret = list(stock_account_info['account'])[0]

        now_date = datetime.datetime.now()
        time_to_add = datetime.timedelta(minutes=minutes - 1, seconds=50)
        new_date = now_date + time_to_add
        str_now_date = new_date.strftime('%Y-%m-%d %H:%M:%S')

        # 获取10分钟动态ip
        ip = liu_guan_proxy_api.get_proxy_api(order_id, secret, str(60 * minutes))

        result_dict = {"_id": ip,
                       'effect_time': str_now_date,
                       'ip': ip}
        result_df = pd.DataFrame(result_dict, index=[1])

        mongodb_util.insert_mongo(result_df, db_name_constant.IP_PROXY_POOL)

        return ip


def get_proxy_ip(str_now_date, minutes):
    ip_proxy_pool = query_liu_guan_proxy_ip()
    if data_frame_util.is_empty(ip_proxy_pool):
        return generate_proxy_ip(minutes)
    else:
        if check_valid(str_now_date, ip_proxy_pool):
            return list(ip_proxy_pool['ip'])[0]
        else:
            return generate_proxy_ip(minutes)


if __name__ == '__main__':
    while True:
        now_date = datetime.datetime.now()
        str_now_date_test = now_date.strftime('%Y-%m-%d %H:%M:%S')
        ip_test = get_proxy_ip(str_now_date_test)
        print(ip_test)
