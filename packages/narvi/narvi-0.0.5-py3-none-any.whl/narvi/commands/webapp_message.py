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


class WebappMessage:

    def __init__(self, message, for_session_id=None, except_session_id=None, from_session_id=None):
        self.message = message
        self.for_session_id = for_session_id
        self.except_session_id = except_session_id
        self.from_session_id = from_session_id

    def get_message(self):
        return self.message

    def get_from_session_id(self):
        return self.from_session_id

    def get_for_session_id(self):
        return self.for_session_id

    def get_except_session_id(self):
        return self.except_session_id

    def __repr__(self):
        if isinstance(self.message,bytes):
            content = "Binary(%d)" % len(self.message)
        else:
            content = self.message
        return f"WebappMessage({self.for_session_id},{self.except_session_id},{self.from_session_id},{content})"