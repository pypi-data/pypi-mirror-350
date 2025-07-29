# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description: 随机数据封装
# @Time   : 2022-11-04 22:05
# @Author : 毛鹏
import random
import string
import uuid

from faker import Faker

from ..exceptions import MangoToolsError
from ..exceptions._error_msg import ERROR_MSG_0006


class RandomStringData:
    """ 随机的字符类型测试数据 """
    faker = Faker(locale='zh_CN')

    @classmethod
    def str_uuid(cls):
        """随机的UUID，长度36"""
        return str(uuid.uuid4())

    @classmethod
    def str_city(cls):
        """获取城市"""
        return cls.faker.city()

    @classmethod
    def str_country(cls):
        """获取国家"""
        return cls.faker.country()

    @classmethod
    def str_province(cls):
        """获取省份"""
        return cls.faker.province()

    @classmethod
    def str_pystr(cls):
        """生成英文的字符串"""
        return cls.faker.pystr()

    @classmethod
    def str_word(cls):
        """生成词语"""
        return cls.faker.word()

    @classmethod
    def str_text(cls):
        """生成一篇文章"""
        return cls.faker.text()

    @classmethod
    def str_random_string(cls, **kwargs):
        """随机字母数字,可传入数字获取指定位数字符串，默认为10"""
        try:
            data = kwargs.get('data')
            if data is None:
                data = 10
            length = int(data)
        except ValueError:
            raise MangoToolsError(*ERROR_MSG_0006)
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
