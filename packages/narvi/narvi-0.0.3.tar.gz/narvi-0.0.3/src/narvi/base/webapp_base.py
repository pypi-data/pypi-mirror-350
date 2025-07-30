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

from abc import ABC, abstractmethod
from typing import Tuple, List

import narvi.services


class WebappBase(ABC):

    @abstractmethod
    def __init__(self, webapp_services: narvi.services.WebAppServices):
        """
        Construct a webapp

        Args:
            services: a services object that the webapp can use to communicate with webapp sessions
        """
        pass

    def get_peer_constructor(self) -> Tuple[str,dict[str,str]]:
        """
        Return the name of a Javascript class and a set of parameters to
        pass when instantiating a peer object in the browser of each new session of this web app

        Returns:
            2-tuple containing the name of the javascript class and a dictionary containing parameters.

        Notes:
            the dictionary returned must be JSON serialisable

        """
        return ("",None)

    @staticmethod
    def get_metadata() -> List[Tuple[str,str,str,str]]:
        """
        Return metadata on this app

        Returns:
            a list of (name,version,description,url) tuples.  The first tuple should describe the app itself,
            subsequent tuples may describe dependencies
        """
        return None




