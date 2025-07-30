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

import logging

class WebServerFactory:

    ServerType_Tornado = "tornado"
    ServerType_Fallback = "builtin"

    @staticmethod
    def get_web_server_types():
        return [WebServerFactory.ServerType_Tornado, WebServerFactory.ServerType_Fallback]

    @staticmethod
    def create_webserver(server_type, host, port):
        logger = logging.getLogger(WebServerFactory.__class__.__name__)

        if server_type not in WebServerFactory.get_web_server_types():
            logger.error(f"requested server_type {server_type} is not one of {WebServerFactory.get_web_server_types()}")

        try:
            if server_type == WebServerFactory.ServerType_Tornado:
                from narvi.web_servers.tornado.tornado_server_adapter import TornadoServerAdapter
                return TornadoServerAdapter(host,port)
        except Exception as ex:
            # perhaps dependencies like tornado are not installed
            logger.warning(f"Error creating {server_type} web server: {ex}")

        if server_type != WebServerFactory.ServerType_Fallback:
            logger.warning(f"Unable to create {server_type} web server, defaulting to builtin web server")

        from narvi.web_servers.builtin.builtin_server import BuiltinServer
        return BuiltinServer(host, port)