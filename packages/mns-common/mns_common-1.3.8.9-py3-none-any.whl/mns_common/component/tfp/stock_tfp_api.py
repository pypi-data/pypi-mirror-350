import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import akshare as ak
import mns_common.utils.date_handle_util as date_handle_util
from loguru import logger
import mns_common.utils.data_frame_util as data_frame_util
from functools import lru_cache
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.constant.db_name_constant as db_name_constant

mongodb_util = MongodbUtil('27017')


def get_stock_tfp_by_day(str_day):
    stock_tfp_em_df = ak.stock_tfp_em(date_handle_util.no_slash_date(str_day))
    stock_tfp_em_df = stock_tfp_em_df.rename(
        columns={'序号': 'index',
                 '代码': 'symbol',
                 '名称': 'name',
                 '停牌时间': 'sus_begin_time',
                 '停牌截止时间': 'sus_end_time',
                 '停牌截止时间': 'sus_end_time',
                 '停牌期限': 'sus_period',
                 '停牌原因': 'sus_reason',
                 '所属市场': 'market',
                 '预计复牌时间': 'resume_time'
                 })
    return stock_tfp_em_df


# 获取停牌股票列表
@lru_cache(maxsize=None)
def get_stock_tfp_symbol_list_by_day(str_day):
    try:
        stock_tfp_em_df = get_stock_tfp_by_day(str_day)
        if data_frame_util.is_not_empty(stock_tfp_em_df):
            return list(stock_tfp_em_df['symbol'])
        else:
            return ['666666']

    except BaseException as e:
        logger.error("获取停牌信息异常:{}", e)
        return ['666666']


@lru_cache(maxsize=None)
def get_stock_tfp_symbol_from_db(str_day):
    try:
        query = {'str_day': str_day}
        stock_tfp_df = mongodb_util.find_query_data(db_name_constant.STOCK_TFP_INFO, query)
        if data_frame_util.is_not_empty(stock_tfp_df):
            return list(stock_tfp_df['symbol'])
        else:
            return ['666666']
    except BaseException as e:
        logger.error("获取停牌信息异常:{}", e)
        return ['666666']
