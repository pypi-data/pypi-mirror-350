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


import socket
import threading
import logging
import uuid
from http import HTTPStatus

http_statuses = {}
for status in list(HTTPStatus):
    http_statuses[status.value] = status.phrase

from narvi.web_servers.common.server_utils import ServerUtils
from narvi.web_servers.common.server_utils import str2bytes
from .ws_protocol import WSProtocol


class WSConnection:

    logger = logging.getLogger(__name__+"[WSConnection]")

    def __init__(self, sock):
        self.sock = sock
        self.recv_callback = None
        WSConnection.logger.debug("opening web socket connection")

    def set_handler(self, cb):
        self.recv_callback = cb

    def run(self):
        while True:
            m = WSProtocol.decode_ws(self.sock)
            if m is None:
                if self.recv_callback is not None:
                    self.recv_callback(None)
                return None
            else:
                (opcode, data) = m

            if opcode == WSProtocol.WS_CLOSE:
                WSConnection.logger.debug("received CLOSE from remote")
                WSProtocol.encode_ws(self.sock, b'', opcode=WSProtocol.WS_CLOSE)
            elif opcode == WSProtocol.WS_PING:
                WSConnection.logger.debug("Responding to PING with PONG")
                WSProtocol.encode_ws(self.sock,data,opcode=WSProtocol.WS_PONG)
            elif opcode == WSProtocol.WS_PONG:
                pass
            else:
                if self.recv_callback is not None:
                    self.recv_callback(data)

    def send(self, payload):
        WSProtocol.encode_ws(self.sock, payload)


class Connection(threading.Thread):

    def __init__(self, server, client_connection, client_address):
        super().__init__()
        self.server = server
        self.client_connection = client_connection
        self.client_address = client_address
        self.logger = logging.getLogger(__name__+"[Connection]")
        self.setDaemon(True)

    def run(self):
        while True:
            try:
                request = WSProtocol.read_http_request(self.client_connection)
                if request is None:
                    break
                (method, headers, filename, request_body) = request
                response = self.handle_http(method, headers, filename, request_body)
                if response:
                    self.client_connection.sendall(response)
                else:
                    break
            except ConnectionResetError as ex:
                self.logger.exception("Handling WebSocket")
                break
        try:
            self.client_connection.close()
        except Exception as ex:
            self.logger.exception("Closing WebSocket")

    def handle_http(self, method, headers, filename, request_body):
        splits = filename.split("?")
        path = splits[0]
        query = splits[1] if len(splits) > 1 else ""
        response = None
        try:
            handled = self.server.handle(method, headers, self.client_connection, path, query,
                                         request_body)
            if handled is not None:
                (code, content, mimetype, handler_response_headers) = handled
                self.logger.info("%d %s %s" % (code, method, filename))
                if content is None:
                    content = str2bytes(http_statuses.get(code, ""))
                if mimetype is None:
                    mimetype = "text/plain"
                if isinstance(content, str):
                    content = str2bytes(content)
                content_length = len(content)
                phrase = http_statuses.get(code, "Unknown")
                response_headers = {
                    "Content-Type": f"{mimetype}",
                    "Connection": "Keep-Alive",
                    "Content-Length": f"{content_length}"
                }
                response_headers.update(handler_response_headers)
                header = f'HTTP/1.1 {code} {phrase}\r\n'
                for (k, v) in response_headers.items():
                    header += "%s: %s\r\n" % (k, v)
                header += "\r\n"
                response = header.encode() + content

        except FileNotFoundError as ex:
            self.logger.warning("%d %s %s" % (404, method, filename))
            response = 'HTTP/1.0 404 NOT FOUND\r\n'.encode()
        except Exception as ex:
            self.logger.exception(method + ":" + filename)
            self.logger.warning("%d %s %s" % (404, method, filename))
            response = 'HTTP/1.0 500 INTERNAL ERROR\r\n'.encode()
        return response

class BuiltinServer:

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.redirects = []
        self.handlers = []
        self.handler_registry = {}
        self.ws_handlers = []
        self.logger = logging.getLogger(__name__+"[BuiltinServer]")
        self.daemon = True

    def add_redirect(self, from_path, to_path):
        self.redirects.append((from_path, to_path))

    def attach_handler(self, method, path, handler):
        handler_id = str(uuid.uuid4())
        t = (method, path, handler)
        self.handler_registry[handler_id] = t
        self.handlers.append(t)
        return handler_id

    def detach_handler(self, handler_id):
        t = self.handler_registry.get(handler_id,None)
        if t is not None:
            self.handlers.remove(t)

    def attach_ws_handler(self, path, handler):
        self.ws_handlers.append((path, handler))

    def handle(self, method, headers, connection, path, query, request_body):
        for (from_path, to_path) in self.redirects:
            if path == from_path:
                return (307, "Temporary Redirect", "text/plain", {"Location": to_path})

        if method.lower() == "get":
            for (handlerpath, handler) in self.ws_handlers:
                path_parameters = {}
                query_parameters = {}
                if ServerUtils.match_path(handlerpath, path, path_parameters):
                    ServerUtils.collect_parameters(query, query_parameters)
                    WSProtocol.complete_handshake(connection, headers)
                    conn = WSConnection(connection)

                    def sender(msg):
                        conn.send(msg)

                    session_id = str(uuid.uuid4())
                    session = handler(session_id, sender, path, path_parameters, query_parameters, headers)
                    if isinstance(session,tuple):
                        return tuple
                    conn.set_handler(lambda msg: session.recv(msg))
                    conn.run()
                    return None

        for (handlermethod, handlerpath, handler) in self.handlers:
            if handlermethod.lower() != method.lower():
                continue
            path_parameters = {}
            query_parameters = {}
            if ServerUtils.match_path(handlerpath, path, path_parameters):
                ServerUtils.collect_parameters(query, query_parameters)
                try:
                    handled = handler(path, headers, path_parameters, query_parameters, request_body)
                    if handled:
                        return handled
                except Exception as ex:
                    logging.exception("handle")
                    return (500, str(ex), "text/plain", {})

        return (404, b'NOT FOUND', "text/plain", {})

    def open(self):
        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.logger.info('Listening on port %s ...' % self.port)

    def run(self, callback=None):
        self.open()
        if callback:
            callback()
        try:
            while True:
                # Wait for client connections
                client_connection, client_address = self.server_socket.accept()
                logging.info("Accepted connection from: "+str(client_address))
                client_connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                conn = Connection(self, client_connection, client_address)
                conn.start()
        finally:
            try:
                self.server_socket.close()
            except Exception as ex:
                self.logger.warning("close server socket failed", exc_info=ex)

    def close(self):
        self.logger.info('Closing ...')
        # FIXME there should be a cleaner way
        import os
        import signal
        os.kill(os.getpid(), signal.SIGUSR1)
