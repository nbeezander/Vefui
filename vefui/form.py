#! /use/bin/python3
# -*- coding:utf-8 -*-
# @Author : zander
# @Time : 2021/2/20 14:59
from vefui.rules import Rule, RequiredRule, TypeRule, JsType, LengthRule
from typing import List, Any, Union, Tuple

Rules = List[Rule]
SwitchType = Union[Tuple[bool, bool], Tuple[str, str], Tuple[int, int], Tuple[float, float]]


class FormItem:

    def __init__(self, component: str,
                 key: str, disabled: bool = False,
                 required: bool = True, label: str = None,
                 desc: str = None,
                 default: Any = None,
                 rules: Rules = None, auto_rules: bool = True):
        """

        :param component:
        :param key:
        :param disabled:
        :param required:
        :param label:
        :param desc:
        :param default:
        :param rules:
        :param auto_rules: auto create validate rule
        """
        self.component = component
        self.key = key
        self.required = required
        self.label = label or self.key.title()
        self.desc = desc or self.key
        self.default = default
        self.rules = rules or []
        self._value = None
        self.disabled = disabled
        self.auto_rules = auto_rules
        if required and auto_rules:
            self.add_rule(RequiredRule())
        pass

    @property
    def value(self):
        return self.formatted_value()

    @value.setter
    def value(self, value):
        self._value = value

    def formatted_value(self):
        return self._value

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def json(self):
        return {
            "component": self.component,
            "key": self.key,
            "disabled": self.disabled,
            "required": self.required,
            "label": self.label,
            "desc": self.desc,
            "default": self.default,
            "rules": [r.json() for r in self.rules]
        }
    # next version
    # def add_event_listener(self, event: str, func):
    #     pass
    #
    # def remove_event_listener(self, event: str, func):
    #     pass


class Input(FormItem):

    def __init__(self, key: str,
                 is_number: bool = False,
                 min_length: int = 0,
                 max_length: int = None,
                 trim: bool = False, **options):
        super(Input, self).__init__("input", key=key, **options)
        self.is_number = is_number
        self.min_length = min_length
        self.max_length = max_length
        self.trim = trim
        if self.auto_rules:
            if self.is_number:
                self.add_rule(TypeRule(JsType.number))
            if self.min_length > 0 or self.max_length is not None:
                self.add_rule(LengthRule(self.min_length, self.max_length))
                pass

    def json(self):
        data = super().json()
        if self.is_number:
            data['isNumber'] = self.is_number
        if self.trim:
            data['trim'] = self.trim
        if self.min_length:
            data['minLength'] = self.min_length
        if self.max_length:
            data['maxLength'] = self.max_length
        return data

    def formatted_value(self):
        if self.is_number:
            return int(self._value)
        return self._value


class Textarea(Input):

    def __init__(self, key: str, rows: int = 3, **options):
        super().__init__("textarea", key=key, **options)
        self.rows = rows

    def json(self):
        data = super().json()
        data['rows'] = self.rows


class Upload(FormItem):

    def __init__(self, key: str, accept: str = "*", drag: bool = True,
                 select_text: str = "select file",
                 drag_text: str = "drag here",
                 **options):
        """

        :param key:
        :param drag: drag model, default True
        :param accept: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
        """
        super().__init__("upload", key=key, **options)
        self.accept = accept
        self.drag = drag
        self.select_text = select_text
        self.drag_text = drag_text

    def json(self):
        data = super().json()
        data['accept'] = self.accept
        data['drag'] = self.drag
        data['selectText'] = self.select_text
        data['dragText'] = self.drag_text
        return data


class Option:

    def __init__(self, key, label=None):
        self.key = key
        self.label = label or key

    def json(self):
        return {
            "key": self.key,
            "label": self.label
        }


Options = Union[List[Option], List]


class Select(FormItem):

    def __init__(self, key: str, options: Options, multi: bool = False, **kwargs):
        super().__init__("select", key=key, **kwargs)
        self.multi = multi
        self.options = [
            option if isinstance(option, Option) else Option(option)
            for option in options
        ]

    def json(self):
        data = super().json()
        data['multi'] = self.multi
        data['options'] = [
            option.json()
            for option in self.options
        ]
        return data


class Date(FormItem):

    def __init__(self, key: str, date_format: str = "YYYY-MM-DD"):
        super(Date, self).__init__("date", key)
        self.format = date_format

    def json(self):
        data = super().json()
        data['format'] = self.format
        return data


class DateTime(FormItem):

    def __init__(self, key: str, date_format: str = "YYYY-MM-DD HH:mm:ss"):
        super(DateTime, self).__init__("datetime", key)
        self.format = date_format

    def json(self):
        data = super().json()
        data['format'] = self.format
        return data


class Slider(FormItem):

    def __init__(self, key: str,
                 min_number: Union[float, int] = 0,
                 max_number: Union[float, int] = 100,
                 step: Union[float, int] = 1,
                 range: bool = False,
                 tooltip: bool = True,
                 gap: bool = False,
                 marks: dict = None,
                 **options
                 ):
        super().__init__("slider", key, **options)
        self.min = min_number
        self.max = max_number
        self.step = step
        self.tooltip = tooltip
        self.gap = gap
        self.marks = marks
        self.range = range
        if isinstance(self.min, int) and isinstance(self.max, int):
            self.in_type = int
        else:
            self.in_type = float

    def json(self):
        data = super().json()
        data['min'] = self.min
        data['max'] = self.max
        data['step'] = self.step
        if not self.tooltip:
            data['tooltip'] = self.tooltip
        if self.gap:
            data['gap'] = self.gap
        if self.marks is not None:
            data['marks'] = self.marks
        if self.range:
            data['range'] = self.range
        return data

    def formatted_value(self):
        if self._value is None:
            return 0
        if self.range:
            return tuple(map(self.in_type, self._value.split(",")))
        else:
            return self.in_type(self._value)


class Switch(FormItem):

    def __init__(self, key: str,
                 value: SwitchType = (True, False),
                 color: Tuple[str, str] = ("#13ce66", "#ff4949"),
                 text: Tuple[str, str] = None,
                 show_text: bool = False,
                 **options):
        """

        :param key:
        :param value:
        :param color:
        :param options:
        """
        super().__init__("switch", key=key, **options)

        self.active_value, self.inactive_value = value
        self.active_color, self.inactive_color = color
        if text is None:
            self.active_text, self.inactive_text = str(self.active_value), str(self.inactive_value)
        else:
            self.active_text, self.inactive_text = text
        self.show_text = show_text
        self.in_type = type(self.active_value)
        if self.default is None:
            self.default = self.active_value

    def json(self):
        data = super().json()
        data['activeColor'] = self.active_color
        data['inactiveColor'] = self.inactive_color
        data['activeValue'] = self.active_value
        data['inactiveValue'] = self.inactive_value
        if self.show_text:
            data['showText'] = True
            data['activeText'] = self.active_text
            data['inactiveText'] = self.inactive_text
        return data

    def formatted_value(self):
        if self._value in ['true', 'True']:
            return True
        elif self._value in ['false', 'False']:
            return False
        return self.in_type(self._value)


if __name__ == "__main__":

    pass
