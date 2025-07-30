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

from narvi.core.service import Service


class NarviServer:

    def __init__(self, host: str = "localhost", port: int = 8999, web_server_type: str = "tornado",
                 base_path: str = "/narvi", admin_path=None):
        """
        Constructs a Narvi app server

        Args:
            host: hostname to run server, for example "localhost" or "0.0.0.0"
            port: port number for the servier, for example, 8080
            web_server_type: either "tornado" (recommended) or "builtin"
            base_path: the base url for all narvi URLs, should start with a leading "/"
            admin_path: path to listen at for admin requests
        """
        self.service = Service(host=host, port=port, base_path=base_path,
                               web_server_type=web_server_type,
                               admin_path=admin_path)
        self.logger = logging.getLogger("NaviServer")

    def register_service(self, namespace, app_service_name, app_cls_name, app_parameters={},
                         fixed_service_id=None, shared_service=True, service_id_validator=lambda service_id:True):
        """
        Register an application service backend.  Websocket connections can be made to this service at URL

        base_path + /$namespace/$app_service_name/$service_id/connect

        Args:
            namespace: a string identifying a namespace within which the app will be registered.  The namespace may be used as a security context.
            app_service_name: the name of the app
            app_cls_name: the resource path and name of the class implementing the web app name, eg foo.bar.foobar.FooBar
            app_parameters: a set of parameters passed to the app constructor
            fixed_service_id:  assign this parameter to the service id if this application service uses a fixed service id
            shared_service: whether the service allows multiple connections to the same service instance
            service_id_validator: a callable which validates the service id
        """
        return self.service.register_service(namespace=namespace, app_service_name=app_service_name, app_cls_name=app_cls_name,
                                             app_parameters=app_parameters, fixed_service_id=fixed_service_id,
                                             shared_service=shared_service, service_id_validator=service_id_validator)

    def register_app(self, app_name, application_service, app_parameters={},
                     resource_roots={}, service_chooser_app_name=None):
        """
        Register a web application frontend.  The application can be loaded from the following URL

        base_path + /$namespace/$app_service_name/$service_id/index.html
            or
        base_path + /$namespace/$app_service_name/index.html

        Args:
            app_name: the name of the app
            application_service: the name of the backend application service this frontend will connect to
            app_parameters: parameters to pass to the web application when constructed
            resource_roots: a dictionary mapping from a URL (relative to the application URL) to a filesystem path
                            eg { "images/icon.png": "/full/path/to/images/icon.png" }
                            or { ("images","*.png"): "/full/path/to/images" }
                            both of these definitions will load URL images/icon.png from /full/path/to/images/icon.png
                            but the second definition will load all png images files from that folder
            service_chooser_app_name: the name of an app to redirect to if the service id is not provided by a connecting client
        """
        self.service.register_app(app_name, application_service=application_service,
                                  app_parameters=app_parameters,
                                  resource_roots=resource_roots,
                                  service_chooser_app_name=service_chooser_app_name)

    def print_services(self):
        messages = self.service.get_summary()
        for msg in messages:
            print(msg)

    def run(self, callback):
        self.service.run(callback)

    def close(self):
        self.service.close()


