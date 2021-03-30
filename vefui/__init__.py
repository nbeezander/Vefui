#! /use/bin/python3
# -*- coding:utf-8 -*-
# @Author : zander
# @Time : 2021/2/20 14:34
import gevent as gvt
from vefui.form import FormItem
from vefui.app import create_app, IOApp
from vefui.errors import ExistedError
from flask import render_template, request, jsonify
from pathlib import Path
from typing import Dict
from vefui import chrome as brw
from engineio.async_drivers import gevent
import sys

Components = Dict[str, FormItem]


class VefUI:

    def __init__(self, title: str,
                 workspace: Path = None,
                 debug: bool = False,
                 lang: str = "en",
                 size: tuple = (640, 720),
                 position: tuple = (320, 200),
                 lang_messages: dict = None,
                 **options):
        """

        :param title:
        :param workspace: workspace, default: run path
        :param size: window init size
        :param position: window init position
        :param debug: if not, client will be exit on websocket disconnect
        :param lang: language, default en. allow [en, zh-cn ]
        :param lang_messages: rewrite client text
        :param options:
            :param options -> label_position: left | right | top ; default: top
            :param options -> label_width: default 120
            :param options -> label_suffix: default ' : '
            :param options -> submit_text: default "Submit"
        """
        self.title = title or "UnTitled"

        self.workspace = workspace or Path(sys.argv[0]).parent
        self.chrome_path = self.workspace.joinpath("chrome")
        self.upload_path = self.workspace.joinpath("upload")
        self.app = None
        self.io = None
        self.debug = debug
        self.__components: Components = {}
        self.items = []
        self.submit_callback = None

        # browser option
        self.size = size
        self.position = position
        self.lang = lang
        self.messages = lang_messages or {}

        # form option
        self.form_options = {
            "labelPosition": options.get("label_position", "top"),
            "labelWidth": "{}px".format(options.get("label_width", 120)),
            "suffix": options.get("label_suffix", " : ")
        }

        self._form_default = {}

    def get_value(self, key: str, default=None):
        component = self.__components.get(key, None)
        if component is None:
            return default
        return component.value

    def _set_value(self, key: str, value) -> None:
        """
        set component value
        :param key:
        :param value:
        :return:
        """
        component = self.__components.get(key, None)
        if component is None:
            return
        component.value = value

    def add(self, item: FormItem):
        if item.key in self.__components:
            raise ExistedError("{} has existed.".format(item.key))
        self.__components[item.key] = item
        self.items.append(item.json())
        self._form_default[item.key] = item.default
        pass

    def on_submit(self):
        # wrap func
        def decorator(f):
            self.submit_callback = f
        return decorator

    def console(self, message, language: str = "",  event: str = "console"):
        """
        send message to client by ws.
        :param message:
        :param language: highlight language
        :param event:
        """
        self.io.send(message, language, event)

    def _index(self):
        return render_template("index.html", title=self.title, lang=self.lang)

    def _submit(self):
        try:
            if request.files:
                if not self.upload_path.exists():
                    self.upload_path.mkdir()

                for key in request.files.keys():
                    file = request.files[key]
                    path = self.upload_path.joinpath(file.filename)
                    file.save(path)
                    self._set_value(key, path)

            for key in self.__components:
                if key in request.form.keys():
                    self._set_value(key, request.form.get(key, None))
        except Exception as e:
            self.console(e.args[0])
            return {"ok": False, "error": e.args[0]}
        else:
            self.submit_callback()
            self.console("complete", event="task:complete")
            return {"ok": True}

    def _init(self):
        return jsonify({
            "form": {
                "items": self.items,
                "default": self._form_default,
                "option": self.form_options
            },
            "debug": self.debug,
            "window": {
                "width": self.size[0],
                "height": self.size[1],
                "minHeight": self.size[1],
                "minWidth": self.size[0]
            },
            "messages": self.messages,
            "lang": self.lang
        })

    def run(self, port: int = 9030, flags: str = ""):
        self.app, self.io = create_app(debug=self.debug)
        self.app.add_url_rule("/", None, self._index)
        self.app.add_url_rule("/submit", None, self._submit, methods=["POST"])
        self.app.add_url_rule("/init", None, self._init, methods=['GET'])

        run_flags = [
            "--window-position={},{}".format(*self.position),
            "--window-size={},{}".format(*self.size),
            "--new-window",
            "--user-data-dir={}".format(self.workspace.joinpath("chrome").absolute()),
            "--disable-windows10-custom-titlebar",
            "-–disable-new-menu-style",
            flags
        ]

        if self.debug:
            run_flags.append("--auto-open-devtools-for-tabs")

        brw_options = {
            "chromeFlags": run_flags,
            "mode": "chrome-app"
        }

        brw.run(options=brw_options, start_urls=['http://127.0.0.1:{}'.format(port)])
        self.io.run(port=port)


if __name__ == "__main__":
    pass
