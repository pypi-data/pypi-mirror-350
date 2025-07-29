# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2023-11-20 9:47
# @Author : 毛鹏

from ..database import MysqlConnect
from ..decorator import sync_method_callback
from ..models import MethodModel


class SqlAssertion:
    """sql断言"""
    mysql_connect: MysqlConnect = None

    @staticmethod
    @sync_method_callback('ass', 'sql断言', 0, [
        MethodModel(f='sql', p='请输入sql语句，确保只会查出一个值', d=True),
        MethodModel(f='expect', p='期望的json', d=True), ])
    async def sql_is_equal(sql: str, expect: list[dict]):
        """值相等"""
        result = SqlAssertion.mysql_connect.condition_execute(sql)
        assert all(dict2 in result for dict2 in expect), f'实际={result}, 预期=列表个数相等'


if __name__ == '__main__':
    _sql = "SELECT id,`name`,`status` FROM `project`;"
    _expect = [{'id': 2, 'name': '1CDXP', 'status': 1}, {'id': 5, 'name': 'AIGC', 'status': 1},
               {'id': 10, 'name': 'DESK', 'status': 1}, {'id': 11, 'name': 'AIGC-SaaS', 'status': 1}]
