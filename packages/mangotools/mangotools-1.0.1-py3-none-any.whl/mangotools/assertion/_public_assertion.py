# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description:
# @Time   : 2023-09-09 23:17
# @Author : 毛鹏
from assertpy import assert_that
from deepdiff import DeepDiff

from ..decorator import sync_method_callback
from ..models import MethodModel


class WhatIsItAssertion:
    """是什么"""

    @staticmethod
    @sync_method_callback('ass', '是什么', 0, [
        MethodModel(f='actual', d=True)])
    def p_is_not_none(actual):
        """不是null"""
        try:
            assert_that(actual).is_not_none()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=不是null') from e

    @staticmethod
    @sync_method_callback('ass', '是什么', 1, [
        MethodModel(f='actual', d=True)])
    def p_is_none(actual):
        """是null"""
        try:
            assert_that(actual).is_none()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=是null') from e

    @staticmethod
    @sync_method_callback('ass', '是什么', 2, [
        MethodModel(f='actual', d=True)])
    def p_is_empty(actual):
        """是空字符串"""
        try:
            assert_that(actual).is_empty()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=是空字符串') from e

    @staticmethod
    @sync_method_callback('ass', '是什么', 3, [
        MethodModel(f='actual', d=True)])
    def p_is_not_empty(actual):
        """不是空符串"""
        try:
            assert_that(actual).is_not_empty()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=不是空符串') from e

    @staticmethod
    @sync_method_callback('ass', '是什么', 4, [
        MethodModel(f='actual', d=True)])
    def p_is_false(actual):
        """是false"""
        try:
            assert_that(actual).is_false()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=是false') from e

    @staticmethod
    @sync_method_callback('ass', '是什么', 5, [
        MethodModel(f='actual', d=True)])
    def p_is_true(actual):
        """是true"""
        try:
            assert_that(actual).is_true()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=是true') from e

    @staticmethod
    @sync_method_callback('ass', '是什么', 6, [
        MethodModel(f='actual', d=True)])
    def p_is_alpha(actual):
        """是字母"""
        try:
            assert_that(actual).is_alpha()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=是字母') from e

    @staticmethod
    @sync_method_callback('ass', '是什么', 7, [
        MethodModel(f='actual', d=True)])
    def p_is_digit(actual):
        """是数字"""
        try:
            assert_that(actual).is_digit()
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期=是数字') from e


class WhatIsEqualToAssertion:
    """等于什么"""

    @staticmethod
    @sync_method_callback('ass', '等于什么', 0, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_is_equal_to(actual: str, expect: str):
        """等于expect"""
        try:
            assert_that(actual).is_equal_to(expect),
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '等于什么', 1, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_is_not_equal_to(actual: str, expect: str):
        """不等于expect"""
        try:
            assert_that(actual).is_not_equal_to(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '等于什么', 2, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_is_length(actual: str, expect: str):
        """长度等于expect"""
        try:
            assert_that(actual).is_length(int(expect))
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '等于什么', 3, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_sum_equal_expect(actual: list, expect: str):
        """长度等于expect"""
        try:
            assert_that(sum(actual)).is_equal_to(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e


class ContainAssertion:
    """包含什么"""

    @staticmethod
    @sync_method_callback('ass', '包含什么', 0, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_contains(actual: str, expect: str):
        """包含expect"""
        try:
            assert_that(actual).contains(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '包含什么', 1, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_is_equal_to_ignoring_case(actual: str, expect: str):
        """忽略大小写等于expect"""
        try:
            assert_that(actual).is_equal_to_ignoring_case(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '包含什么', 2, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_contains_ignoring_case(actual: str, expect: str):
        """包含忽略大小写expect"""
        try:
            assert_that(actual).contains_ignoring_case(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '包含什么', 3, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_contains_only(actual: str, expect: str):
        """仅包含expect"""
        try:
            assert_that(actual).contains_only(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '包含什么', 4, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_does_not_contain(actual: str, expect: str):
        """不包含expect"""
        try:
            assert_that(actual).does_not_contain(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e


class MatchingAssertion:
    """匹配什么"""

    @staticmethod
    @sync_method_callback('ass', '匹配什么', 0, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_in_dict(actual: dict, expect: dict):
        """JSON匹配"""
        filtered_actual = filter_dict(dict(actual), dict(expect))
        diff = DeepDiff(filtered_actual, expect, ignore_order=True)
        assert not diff, f'实际={actual}, 预期={expect}'

    @staticmethod
    @sync_method_callback('ass', '匹配什么', 1, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_is_in(actual: str, expect: str):
        """在expect里面"""
        try:
            assert_that(actual).is_in(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '匹配什么', 2, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_is_not_in(actual: str, expect: str):
        """不在expect里面"""
        try:
            assert_that(actual).is_not_in(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '匹配什么', 3, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_starts_with(actual: str, expect: str):
        """以expect开头"""
        try:
            assert_that(actual).starts_with(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '匹配什么', 4, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_ends_with(actual: str, expect: str):
        """以expect结尾"""
        try:
            assert_that(actual).ends_with(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '匹配什么', 5, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_matches(actual: str, expect: str):
        """正则匹配等于expect"""
        try:
            assert_that(actual).matches(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e

    @staticmethod
    @sync_method_callback('ass', '匹配什么', 6, [
        MethodModel(f='actual', d=True), MethodModel(f='expect', p='请输入断言值', d=True)])
    def p_does_not_match(actual: str, expect: str):
        """正则不匹配expect"""
        try:
            assert_that(actual).does_not_match(expect)
        except AssertionError as e:
            raise AssertionError(f'实际={actual}, 预期={expect}') from e


def filter_dict(actual: dict, expect: dict) -> dict:
    filtered = {}
    for key in expect.keys():
        if key in actual:
            if isinstance(expect[key], dict):
                filtered[key] = filter_dict(actual[key], expect[key])
            elif isinstance(expect[key], list) and isinstance(actual[key], list):
                filtered[key] = []
                for item in actual[key]:
                    if isinstance(item, dict):
                        filtered_item = filter_dict(item, expect[key][0])
                        filtered[key].append(filtered_item)
                    else:
                        filtered[key].append(item)
            else:
                filtered[key] = actual[key]
    return filtered


class PublicAssertion(WhatIsItAssertion, ContainAssertion, MatchingAssertion, WhatIsEqualToAssertion):
    pass


if __name__ == '__main__':
    PublicAssertion.p_is_equal_to('1', '2')
