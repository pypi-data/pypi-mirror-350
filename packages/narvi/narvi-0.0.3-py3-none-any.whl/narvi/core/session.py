# MIT License
#
# Narvi - a simple python web application server
#
# Copyright (C) 2022-2025 Visual Topology Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import logging
import json

from narvi.commands.webapp_message import WebappMessage

class Session:

    def __init__(self, app_name, app_parameters, session_id, sender, app, query_parameters, headers, close_cb=None):
        self.app_name = app_name
        self.app_parameters = app_parameters
        self.app = app
        self.query_parameters = query_parameters
        self.session_id = session_id
        self.sender = sender
        self.headers = headers
        self.close_cb = close_cb
        self.app.connect(self.app_name, self.app_parameters, self.session_id, self.query_parameters, self.headers, lambda cmd: self.dispatch(cmd))
        self.start_time = datetime.datetime.now()

    def get_id(self):
        return self.session_id

    def get_start_time(self):
        return self.start_time

    def get_app(self):
        return self.app

    def dispatch(self,cmd):
        if isinstance(cmd,WebappMessage):
            self.send(cmd.message)
        else:
            self.send(json.dumps(cmd.serialise()))

    def send(self,msg):
        self.sender(msg)

    def recv(self,msg):
        if msg is None:
            logging.getLogger("narvi").info("Closing session %s for app %s" % (self.get_id(), self.app.getName()))
            self.app.disconnect(self.get_id())
            if self.close_cb:
                self.close_cb()
        else:
            self.app.receive_session_message(self.session_id,msg)

    def close(self):
        if self.close_cb:
            self.close_cb()