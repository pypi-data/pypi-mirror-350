# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description: 随机数据封装
# @Time   : 2022-11-04 22:05
# @Author : 毛鹏
import random

import time
from faker import Faker


class RandomNumberData:
    """ 随机的数字类型测试数据 """
    faker = Faker(locale='zh_CN')

    @classmethod
    def randint(cls, **kwargs):
        """随机的范围数，传入：left，right"""
        data = kwargs.get('data')
        if data:
            left = data.get('left', 2000)
        else:
            left = 2000
        if data:
            right = data.get('left', 2500)
        else:
            right = 2500
        return random.randint(left, right)

    @classmethod
    def number_time_5(cls):
        """获取基于当前时间戳的随机五位数"""
        s = int(time.time())
        s = str(s)
        return s[5:len(s)]

    @classmethod
    def number_random_0_9(cls) -> int:
        """0-9的随机数"""
        _data = random.randint(0, 9)
        return _data

    @classmethod
    def number_random_0_5(cls) -> int:
        """0-9的随机数"""
        _data = random.randint(0, 5)
        return _data

    @classmethod
    def number_random_10_99(cls) -> int:
        """10-99的随机数"""
        _data = random.randint(10, 99)
        return _data

    @classmethod
    def number_random_100_999(cls) -> int:
        """100-999的随机数"""
        _data = random.randint(100, 999)
        return _data

    @classmethod
    def number_random_0_5000(cls) -> int:
        """0-5000的随机数"""
        _data = random.randint(0, 5000)
        return _data

    @classmethod
    def number_random_float(cls):
        """小数"""
        return random.random()

    @classmethod
    def number_random_two_float(cls):
        """随机两位小数"""
        return round(random.random(), 2)

    @classmethod
    def number_random_1000_two_float(cls):
        """1000以内的随机两位小数"""
        return cls.number_random_100_999() + round(random.random(), 2)
