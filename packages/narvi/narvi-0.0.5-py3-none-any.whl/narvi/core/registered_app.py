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

import os.path
from logging import getLogger
import fnmatch
import mimetypes

class RegisteredApp:

    def __init__(self, app_name, application_service=None, app_parameters={},
                 resource_roots={}, service_chooser_app_name=""):
        self.app_name = app_name
        self.application_service = application_service
        self.app_parameters = app_parameters
        self.resource_roots = resource_roots
        self.service_chooser_app_name = service_chooser_app_name
        self.logger = getLogger(f"RegisteredApp[{self.application_service.namespace}.{self.app_name}]")

    def get_application_service(self):
        return self.application_service

    def get_application_service_name(self):
        return self.application_service.app_service_name

    def get_app_html(self):
        loaded = self.load_resource("index.html")
        if loaded is None:
            self.logger.error(f"HTML not found for app: {self.app_name}")
            return None
        (code, html_content, mimetype, headers) = loaded
        return html_content

    def get_app_parameters(self):
        return self.app_parameters

    def get_service_chooser_app_name(self):
        return self.service_chooser_app_name

    def get_resource_roots(self):
        return self.resource_roots

    def match_resource_pattern(self, resource_url, pattern, resource_root):
        resource_path = None
        if isinstance(pattern, tuple):
            prefix = pattern[0]
            pattern = pattern[1]

            if prefix[-1] != "/":
                prefix += "/"
            if resource_url.startswith(prefix):
                # strip off the prefix
                resource_url = resource_url[len(prefix):]

                if fnmatch.fnmatch(resource_url, pattern):
                    resource_path = os.path.join(resource_root,resource_url)
        else:
            if fnmatch.fnmatch(resource_url, pattern):
                resource_path = resource_root

        if resource_path is not None:
            if os.path.isfile(resource_path):
                (mimetype, encoding) = mimetypes.guess_type(resource_path)
                return (resource_path, mimetype)

        return (None,None)

    def load_resource(self, resource_url):
        for (pattern, resource_root) in self.resource_roots.items():
            resource_path, mimetype = self.match_resource_pattern(resource_url, pattern, resource_root)
            if resource_path:
                if os.path.exists(resource_path):
                    with open(resource_path, "rb") as f:
                        content = f.read()
                        return (200, content, mimetype, {})

        return None

