#! /use/bin/python3
# -*- coding:utf-8 -*-
# @Author : zander
# @Time : 2021/2/20 14:14
import os
import flask
from flask import Flask
from flask_socketio import SocketIO, Namespace
from dataclasses import dataclass
import json


@dataclass()
class Client:

    _sid: str = ""
    _nsp: str = ""

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, value):
        self._sid = value

    @property
    def nsp(self):
        return self._nsp

    @nsp.setter
    def nsp(self, value):
        self._nsp = value


SingletonClient: Client = Client()


class ConsoleNameSpace(Namespace):

    def __init__(self, namespace: str, debug: bool = False):
        super().__init__(namespace=namespace)
        self.debug = debug

    def on_connect(self):
        global SingletonClient
        SingletonClient.sid = flask.request.sid
        SingletonClient.nsp = flask.request.namespace

    def on_disconnect(self):
        global SingletonClient
        self.disconnect(SingletonClient.sid, SingletonClient.nsp)

    def on_test(self, data):
        print(data)

    def disconnect(self, sid, namespace=None):
        super().disconnect(sid, namespace)
        if not self.debug:
            os._exit(0)


class IOApp:

    def __init__(self, app, debug: bool = False):
        self.app = app
        socket_io = SocketIO()
        socket_io.init_app(app)
        socket_io.on_namespace(ConsoleNameSpace("/console", debug=debug))
        self.io = socket_io

    def run(self, port: int = 9030):
        self.io.run(self.app, host="127.0.0.1", port=port)

    def send(self, message, language: str = "",  event: str = "console"):
        if not isinstance(message, str):
            message = json.dumps(message)
        self.io.emit(event, {"language": language, "message": message},
                     namespace=SingletonClient.nsp, to=SingletonClient.sid)
        pass


def create_app(debug: bool = False):
    app = Flask(__name__, template_folder="web", static_folder="web/assets")

    app.config['SECRET_KEY'] = 'secret!'

    io = IOApp(app, debug=debug)

    return app, io


if __name__ == "__main__":

    pass
