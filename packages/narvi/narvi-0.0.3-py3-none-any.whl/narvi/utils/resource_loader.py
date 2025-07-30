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

from importlib import resources
from importlib import import_module
import logging

class ResourceLoader:

    logger = logging.getLogger("resource_loader")

    @staticmethod
    def split_resource_path(resource_path):
        if resource_path.startswith("/"):
            resource_path = resource_path[1:]
        comps = resource_path.split("/")
        package = ".".join(comps[:-1])
        resource = comps[-1]
        return (package,resource)

    @staticmethod
    def get_class(module_class_name):
        try:
            module_path, class_name = module_class_name.rsplit('.', 1)
            module = import_module(module_path)
            cls = getattr(module, class_name)
            return cls
        except:
            ResourceLoader.logger.exception(f"unable to get class for {module_class_name}")
            return None

