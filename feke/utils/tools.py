import time
import datetime
from datetime import date, timedelta


# 装饰器 判断入参是否为none 有则返回原始数据
def check_none(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                return arg
        return func(*args, **kwargs)
    return wrapper


# datetime 转时间戳 13位
@check_none
def datetime_to_timestamp_in_milliseconds(d):
    """datetime 转时间戳 13位"""
    return int(time.mktime(d.timetuple()) * 1000)


# 时间戳转datetime
@check_none
def timestamp_to_datetime(timestamp):
    """时间戳转datetime"""
    return datetime.datetime.fromtimestamp(timestamp)

# date 转时间戳 13位
@check_none
def date_to_timestamp_in_milliseconds(d):
    """date 转时间戳 13位"""
    return int(time.mktime(d.timetuple()) * 1000)


# 时间戳转date
@check_none
def timestamp_to_date(timestamp):
    """时间戳转date"""
    return datetime.datetime.fromtimestamp(timestamp).date()


@check_none
def str_to_date(date_str):
    """字符串转date"""
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

@check_none
def split_dates(start_date, end_date):
    """拆分日期"""
    if start_date == end_date:
        return [start_date]
    
    cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    
    date_list = []
    while cur_date <= end_date:
        date_list.append(cur_date.strftime('%Y-%m-%d'))
        cur_date += timedelta(days=1)
    return date_list.pop() if date_list  else []


@check_none
def get_date_list(start_date, end_date):
    """获取日期列表"""
    if start_date == end_date:
        return [start_date]
    
    cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    
    date_list = []
    while cur_date <= end_date:
        date_list.append(cur_date.strftime('%Y-%m-%d'))
        cur_date += timedelta(days=1)
    return date_list


@check_none
def compute_checkin_days(start_date, end_date):
    """计算入住天数"""
    # 检查字符串是否为日期格式
    try:
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
        datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    if start_date == end_date:
        return 1
    return (datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days