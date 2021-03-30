#! /use/bin/python3
# -*- coding:utf-8 -*-
# @Author : zander
# @Time : 2021/3/15 17:51
from vefui import VefUI
from vefui.form import Input


def main():
    app = VefUI("hello", debug=False)

    app.add(Input(key="name", label="Name"))

    @app.on_submit()
    def submit():
        name = app.get_value("name")

        # print log to app console
        app.console("Hello {}.".format(name))
        pass

    app.run()


if __name__ == "__main__":
    main()
    pass
