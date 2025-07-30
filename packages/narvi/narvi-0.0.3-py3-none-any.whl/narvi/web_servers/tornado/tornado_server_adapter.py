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

import threading
import asyncio
import uuid
import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
from ..common.server_utils import ServerUtils

server = None

class NarviWebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, app, request, **kwargs):
        super().__init__(app, request,**kwargs)
        self.path = request.path
        self.query = request.query
        self.headers = {k:v for (k,v) in request.headers.get_all()}
        self.path_parameters = {}
        self.query_parameters = {}
        self.session = None
        ServerUtils.collect_parameters(self.query, self.query_parameters)

    def check_origin(self, origin):
        self.origin = origin
        return True

    def open(self, *args):
        for (handlerpath, handler) in server.get_ws_handlers():
            if ServerUtils.match_path(handlerpath, self.path, self.path_parameters):
                ServerUtils.collect_parameters(self.query, self.query_parameters)
                def sender(msg):
                    server.event_loop.call_soon_threadsafe(lambda m: self.write_message(m,binary=isinstance(m,bytes)), msg)

                session_id = str(uuid.uuid4())
                self.session = handler(session_id, sender, self.path, self.path_parameters, self.query_parameters, self.headers)
                return
        server.logger.error("WebSocket no handler")

    def on_message(self, message):
        self.session.recv(message)

    def on_close(self):
        self.session.recv(None)

    def on_ping(self):
        pass

class NarviHttpRequestHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        return self.handle("GET")

    def put(self, *args, **kwargs):
        return self.handle("PUT")

    def post(self, *args, **kwargs):
        return self.handle("POST")

    def delete(self, *args, **kwargs):
        return self.handle("DELETE")

    def handle(self, method):
        path = self.request.path
        query = self.request.query
        headers = {k:v for (k,v) in self.request.headers.get_all()}
        request_body = self.request.body
        redirects = server.get_redirects()
        for (from_path, to_path) in redirects:
            if path == from_path:
                return self.redirect(to_path)

        for (handlermethod, handlerpath, handler) in server.get_http_handlers():
            if handlermethod.lower() != method.lower():
                continue
            path_parameters = {}
            query_parameters = {}
            if ServerUtils.match_path(handlerpath, path, path_parameters):
                ServerUtils.collect_parameters(query, query_parameters)
                try:
                    handled = handler(path, headers, path_parameters, query_parameters, request_body)
                    if handled:
                        self.send(handled)
                        return
                except Exception as ex:
                    logging.exception(ex)
                    return (500, str(ex), "text/plain", {})

        return self.send((404, None, "text/plain", {}))

    def send(self, output_tuple):
        (code, content, mimetype, custom_headers) = output_tuple
        for (name, value) in custom_headers.items():
            self.set_header(name, value)
        if mimetype:
            self.set_header("Content-Type", mimetype)
        self.set_status(code)
        self.finish(content)


class TornadoServerAdapter:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.redirects = []
        self.handlers = []
        self.handler_registry = {}
        self.ws_handlers = []
        self.default_handlers = {}
        self.logger = logging.getLogger("narvi.web_servers.tornado.tornado_server_adapter")
        global server
        server = self

    def get_ws_handlers(self):
        return self.ws_handlers

    def get_http_handlers(self):
        return self.handlers

    def get_redirects(self):
        return self.redirects

    def get_default_handlers(self):
        return self.default_handlers

    def add_redirect(self, from_path, to_path):
        self.redirects.append((from_path,to_path))

    def attach_handler(self, method, path, handler):
        handler_id = str(uuid.uuid4())
        t = (method, path, handler)
        self.handler_registry[handler_id] = t
        self.handlers.append(t)
        return handler_id

    def detach_handler(self, handler_id):
        t = self.handler_registry.get(handler_id, None)
        if t is not None:
            self.handlers.remove(t)

    def attach_ws_handler(self, path, handler):
        self.ws_handlers.append((path, handler))

    def run(self, callback):
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        self.app =  tornado.web.Application([
            (r"/(.*/connect)", NarviWebSocketHandler),
            (r"/(.*)", NarviHttpRequestHandler)],
                websocket_ping_interval=10,
                websocket_ping_timeout=30,)
        self.app.listen(self.port)

        self.logger.info('Listening on port %s ...' % self.port)

        callback()
        tornado.ioloop.IOLoop.current().start()

    def close(self):
        self.logger.info('Closing ...')
        # FIXME there should be a cleaner way
        import os
        import signal
        os.kill(os.getpid(), signal.SIGUSR1)
        # ioloop = tornado.ioloop.IOLoop.current()
        # ioloop.stop()