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

import urllib.parse

def str2bytes(s):
    return bytes(s, "utf-8")

def bytes2str(b):
    return str(b, "utf-8")

class ServerUtils:

    @staticmethod
    def match_path(handlerpath, path, parameters):
        handlerpathlist = handlerpath.split("/")
        pathlist = path.split("/")
        matched = ServerUtils.__match(handlerpathlist,pathlist, parameters, True)
        if not matched:
            # if the match fails, clear away any data collected on a partial match
            parameters.clear()
        return matched

    @staticmethod
    def __match(handlerpathlist,pathlist,parameters,required):
        if handlerpathlist == [] and pathlist == []:
            return True
        if len(handlerpathlist) > 0 and not required:
            # allow empty match
            parameters1 = {}
            if ServerUtils.__match(handlerpathlist[1:], pathlist, parameters1, True):
                parameters.update(parameters1)
                return True
        if handlerpathlist == [] or pathlist == []:
            return False

        matchexp = handlerpathlist[0]
        if matchexp.startswith("$$"):
            key = matchexp[2:]
            parameters[key] = pathlist[0]
            parameters1 = {}
            if ServerUtils.__match(handlerpathlist, pathlist[1:], parameters1, False):
                parameters.update(parameters1)
                if key in parameters1:
                    parameters[key] = pathlist[0]+ "/" + parameters1[key]
                return True
            else:
                return False
        elif matchexp.startswith("$"):
            key = matchexp[1:]
            parameters[key] = pathlist[0]
        else:
            if matchexp != pathlist[0]:
                return False

        return ServerUtils.__match(handlerpathlist[1:], pathlist[1:], parameters, True)


    @staticmethod
    def collect_parameters(query, parameters):
        if query != "":
            qargs = query.split("&")
            for qarg in qargs:
                argsplit = qarg.split("=")
                if len(argsplit) == 2:
                    key = urllib.parse.unquote(argsplit[0])
                    value = urllib.parse.unquote(argsplit[1])
                    parameters[key] = value


