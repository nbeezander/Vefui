#! /use/bin/python3
# -*- coding:utf-8 -*-
# @Author : zander
# @Time : 2021/2/27 18:39


class ExistedError(Exception):

    def __init__(self, message: str = "object existed"):
        self.message = message
        pass


if __name__ == "__main__":
    pass
