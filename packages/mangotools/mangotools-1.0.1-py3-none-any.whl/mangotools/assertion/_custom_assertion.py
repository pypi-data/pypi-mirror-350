# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-01-05 18:05
# @Author : 毛鹏
from ..decorator import sync_method_callback
from ..exceptions._error_msg import ERROR_MSG_0061
from ..exceptions._exceptions import MangoToolsError
from ..models import MethodModel


class CustomAssertion:
    """自定义断言"""

    @staticmethod
    @sync_method_callback('ass', '自定义断言', 7, [
        MethodModel(f='func_str', p='请输入一个函数，在函数里面自己断言', d=True),
        MethodModel(f='func_name', p='请输入这个函数的名称', d=True), ])
    def ass_func(func_str, func_name='func'):
        """输入断言代码"""
        try:
            global_namespace = {}
            exec(func_str, global_namespace)
            return global_namespace[func_name]
        except (KeyError, SyntaxError, TypeError):
            import traceback
            traceback.print_exc()
            raise MangoToolsError(*ERROR_MSG_0061)
