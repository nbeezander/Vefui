#! /use/bin/python3
# -*- coding:utf-8 -*-
# @Author : zander
# @Time : 2021/2/22 15:30
from enum import Enum


class Rule:

    def __init__(self, message: str = None, trigger: str = "blur"):
        self.message = message
        self.trigger = trigger

    def json(self) -> dict:
        kv = {
            "trigger": self.trigger
        }
        if self.message is not None:
            kv['message'] = self.message
        return kv


class RequiredRule(Rule):

    def __init__(self, **options):
        super().__init__(**options)
        self.required = True

    def json(self):
        data = super().json()
        data['required'] = True
        return data


class JsType(Enum):
    number = "number"
    string = "string"


class TypeRule(Rule):

    def __init__(self, filed_type: JsType = JsType.string, **options):
        super().__init__(**options)
        self.type = filed_type

    def json(self):
        data = super().json()
        data['type'] = self.type.value
        return data


class LengthRule(Rule):

    def __init__(self, min: int, max: int):
        super().__init__()
        self.min = min
        self.max = max

    def json(self):
        data = super().json()
        data['min'] = self.min
        data['max'] = self.max
        return data


if __name__ == "__main__":
    r = TypeRule(message="xxx", filed_type=JsType.number)
    print(r.json())
    pass
