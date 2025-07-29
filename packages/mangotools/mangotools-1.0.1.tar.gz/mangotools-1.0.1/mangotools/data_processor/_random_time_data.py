# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description:
# @Time   : 2023-03-07 8:24
# @Author : 毛鹏
import random
from datetime import date, timedelta, datetime

import time
from faker import Faker


class RandomTimeData:
    """ 随机时间类型测试数据 """
    faker = Faker(locale='zh_CN')

    @classmethod
    def time_now_ymdhms(cls) -> str:
        """当前年月日时分秒"""
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return localtime

    @classmethod
    def time_now_ymd(cls) -> str:
        """当前年月日"""
        localtime = time.strftime("%Y-%m-%d", time.localtime())
        return localtime

    @classmethod
    def get_time_for_min(cls, **kwargs) -> int:
        """获取几分钟后的时间戳 参数：data"""
        minute = kwargs.get('data')
        if minute is None:
            minute = 1
        return int(time.time() + 60 * int(minute)) * 1000

    @classmethod
    def time__random_ymdhms(cls):
        """随机年月日时分秒"""
        return cls.faker.date_time()

    @classmethod
    def time_random_ymd(cls):
        """随机年月日"""
        return cls.faker.date_this_year()

    @classmethod
    def time_random_hms(cls):
        """随机的时分秒"""
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        random_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"  # 格式化为 HH:MM:SS
        return random_time

    @classmethod
    def time_random_year(cls):
        """获取随机年份"""
        return cls.faker.year()

    @classmethod
    def time_random_month(cls):
        """获取随机月份"""
        return cls.faker.month()

    @classmethod
    def time_random_date(cls):
        """获取随机日期"""
        return cls.faker.date()

    @classmethod
    def time_now_int(cls) -> int:
        """获取当前时间戳整形"""
        return int(time.time()) * 1000

    @classmethod
    def time_today_weekday(cls):
        """今天是周几"""
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday = date.today().weekday()
        return weekdays[weekday]

    @classmethod
    def time_before_time(cls, **kwargs):
        """当今日之前的日期"""
        days = kwargs.get('data')
        if days is None:
            days = 1
        yesterday = datetime.now() - timedelta(days=int(days))
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        return yesterday_str

    @classmethod
    def time_stamp(cls, **kwargs) -> int:
        """几分钟后的时间戳"""
        minute = kwargs.get('data')
        if minute is None:
            minute = 1
        return int(time.time() + 60 * int(minute)) * 1000

    @classmethod
    def time_next_minute(cls, **kwargs) -> str:
        """几分钟后的年月日时分秒 参数：分钟"""
        minute = kwargs.get('data')
        if minute is None:
            minute = 1
        future_time = datetime.now() + timedelta(minutes=int(minute))
        return future_time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def time_future_datetime(cls):
        """未来的随机年月日时分秒"""
        return cls.faker.future_datetime()

    @classmethod
    def time_future_date(cls):
        """未来的随机年月日"""
        return cls.faker.future_date()

    @classmethod
    def time_by_type(cls, **kwargs) -> str:
        """当前年月日时分秒并返回指定格式"""
        types = str(kwargs.get('data'))
        data_type = ''
        if types is None or types == '0':
            data_type = '%Y-%m-%d %H:%M:%S'
        elif types == '1':
            data_type = '%Y-%m-%d %H:%M'
        elif types == '2':
            data_type = '%Y-%m-%d %H'
        elif types == '3':
            data_type = '%Y-%m-%d'
        elif types == '4':
            data_type = '%Y-%m'
        elif types == '5':
            data_type = '%Y'
        now_time = datetime.now().strftime(data_type)
        return now_time

    @classmethod
    def time_today_date(cls):
        """获取今日0点整时间"""
        _today = date.today().strftime("%Y-%m-%d") + " 00:00:00"
        return str(_today)

    @classmethod
    def time_after_week(cls):
        """获取一周后12点整的时间"""
        _time_after_week = (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return _time_after_week

    @classmethod
    def time_after_month(cls):
        """获取30天后的12点整时间"""
        _time_after_week = (date.today() + timedelta(days=+30)).strftime("%Y-%m-%d") + " 00:00:00"
        return _time_after_week

    @classmethod
    def time_day_reduce(cls, **kwargs) -> int:
        """获取今日日期的数字，传参可以减N"""
        types = kwargs.get('data')
        today = datetime.today()
        if types:
            return today.day - int(types)
        else:
            return today.day

    @classmethod
    def time_day_plus(cls, **kwargs) -> int:
        """获取今日日期的数字，传参可以加N"""
        types = kwargs.get('data')
        today = datetime.today()
        if types:
            return today.day + int(types)
        else:
            return today.day

    @classmethod
    def time_now_hms(cls):
        """时分秒"""
        return datetime.now().strftime("%H:%M:%S")

    @classmethod
    def time_cron_time(cls, **kwargs) -> str:
        """秒级cron表达式"""
        time_parts = kwargs.get('data').split()
        seconds = int(time_parts[0])
        minutes = int(time_parts[1])
        hours = int(time_parts[2])
        current_date = datetime.now().date()
        date_obj = datetime(year=current_date.year,
                            month=current_date.month,
                            day=current_date.day,
                            hour=hours,
                            minute=minutes,
                            second=seconds)

        time_str_result = date_obj.strftime("%H:%M:%S")
        return time_str_result

    @classmethod
    def time_next_minute_cron(cls, **kwargs):
        """按周重复的cron表达式"""
        if kwargs.get('data'):
            minutes = int(kwargs.get('data'))
        else:
            minutes = 1
        now = datetime.now() + timedelta(minutes=minutes)
        second = f"{now.second:02d}"  # 格式化为两位数
        minute = f"{now.minute:02d}"  # 格式化为两位数
        hour = f"{now.hour:02d}"  # 格式化为两位数
        day = "?"  # 日用问号表示不指定
        month = "*"  # 月用星号表示每个月
        weekday = str(date.today().weekday() + 2)
        return f"{second} {minute} {hour} {day} {month} {weekday}"


if __name__ == '__main__':
    test = RandomTimeData.time_after_week()
    print(test)
