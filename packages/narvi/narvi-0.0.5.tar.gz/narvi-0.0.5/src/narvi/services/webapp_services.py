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

from typing import Union, Callable, Any


class WebAppServicesException(Exception):

    def __init__(self, msg):
        self.__init__(msg)

"""
Defines a set of services that can be called by a web application.  When a web application is instantiated by narvi,
a services object is passed into the constructor.
"""

class WebAppServices:

    def __init__(self, webapp, namespace, service_id):
        self.app = webapp
        self.namespace = namespace
        self.service_id = service_id

    def create_request_service(self, app_name, handler_pattern,
                               handler: Callable[[dict[str, str],dict[str, str],dict[str, str], bytes], tuple[int, bytes, str, dict[str, str]]],
                               request_method:str="GET", session_id:str=None) -> (str,str):
        """
        Create a request service and return a URL to it

        Args:
            app_name:
            handler_pattern:
            callback: A function called when a user requests the service.  The callback is passed path parameters, request parameters, a dictionary containing HTTP headers from the request and the request body
                and should return a 4-tuple with components (response_code, binary_content, mime_type, response-headers)
            request_method: the method eg "GET", "PUT"
            session_id: the session id, if known
        Returns:
            a (handler-id, URL) (relative to the app) that points to the created service endpoint
        """
        return self.app.create_request_service(app_name, handler_pattern, request_method, handler, session_id)

    def remove_request_service(self, handler_id) -> None:
        """
        Remove a request handler

        Args:
            handler_id:
        """
        return self.app.remove_request_service(handler_id)

    def send(self, msg:Union[str,bytes], for_session_id:str=None, except_session_id:str=None):
        """
        Send a message to the client peer (javascript) instance running in one or more client sessions

        Args:
            msg: str or bytes to send
            for_session_id: if specified, send to only this session
            except_session_id: if specified, send to all sessions except this one

        Notes:
            If both for_session_id and except_session_id are provided, except_session_id is ignored
        """
        self.app.send_webapp_message(msg, for_session_id=for_session_id, except_session_id=except_session_id)

    def add_message_listener(self, callback:Callable[[Union[str,bytes],str],None]):
        """
        Register a callback which is invoked when a message from a client peer (javascript) instance is received

        Args:
            callback: a function to call when a message is received, passing in the message content and originating session id
        """
        return self.app.add_message_listener(callback)

    def add_session_open_listener(self, callback:Callable[[str,str,dict[str,str],dict[str,str]],None]):
        """
        Register a callback which is invoked when a session is opened

        Args:
            callback: a function to call when the event occurs, passing in the application name, session id, query parameters and the request headers
        """
        return self.app.add_session_open_listener(callback)

    def add_session_close_listener(self, callback:Callable[[str],None]):
        """
        Register a callback which is invoked when a session is closed

        Args:
            callback: a function to call when the event occurs, passing in the session id
        """
        return self.app.add_session_close_listener(callback)

    def set_admin_listener(self, callback:Callable[[],dict[str,Any]]):
        """
        Register a callback which is invoked to retrieve admin status of the app

        Args:
            callback: a function to call, accepting no arguments, and returning a JSON-serialisable object

        Notes: the callback will be called outside the app's execution thread, and must be thread safe
        """
        return self.app.set_admin_listener(callback)

    def add_app_close_listener(self, callback:Callable[[],None]):
        """
        Register a callback which is invoked when the application instance is about to be closed

        Args:
            callback: a function to call when the event occurs, accepting no arguments
        """
        return self.app.add_app_close_listener(callback)

    def get_service_id(self):
        """
        Gets the service id associated with this instance of the web app

        Returns:
            string containing the service id
        """
        return self.service_id


