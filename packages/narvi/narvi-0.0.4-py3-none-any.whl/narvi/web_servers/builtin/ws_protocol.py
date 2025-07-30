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

from narvi.web_servers.common.server_utils import str2bytes, bytes2str
import base64
import hashlib


class WSProtocol(object):

    WS_CONT = 0x0
    WS_TEXT = 0x1
    WS_BINARY = 0x2
    WS_CLOSE = 0x8
    WS_PING = 0x9
    WS_PONG = 0xA

    @staticmethod
    def create_hash(key1):
        h = hashlib.sha1(str2bytes(key1) + str2bytes('258EAFA5-E914-47DA-95CA-C5AB0DC85B11'))
        return bytes2str(base64.b64encode(h.digest()))

    @staticmethod
    def read_http_request(sock):
        request_content = sock.recv(1024)
        lines = str(request_content,"utf-8").split("\n")
        lines = list(map(lambda line: line.strip("\n\r"), lines))
        words = lines[0].split()
        if len(words) < 2:
            return None
        method = words[0]
        resource_or_code = words[1]
        headers = {}
        for line in lines[1:]:
            if line != "":
                keyval = line.split(":")
                headers[keyval[0].strip()] = keyval[1].strip()
        content = None
        return (method, headers, resource_or_code, content)

    @staticmethod
    def write_http_header_request(sock, headers, resource):
        msg = "GET %s HTTP/1.1\r\n" % (resource)
        for key in headers:
            msg += key + ": " + headers[key] + "\r\n"
        msg += "\r\n"
        sock.send(str2bytes(msg))

    @staticmethod
    def write_http_header_response(sock, headers, code, msg):
        msg = "HTTP/1.1 %d %s\r\n" % (code, msg)
        for key in headers:
            msg += key + ": " + headers[key] + "\r\n"
        msg += "\r\n"
        sock.sendall(str2bytes(msg))

    @staticmethod
    def recv(sock, count):
        try:
            result = bytes()
            sz = count
            while sz:
                message = sock.recv(sz)
                if message == b'':
                    return None
                result = result + message
                sz -= len(message)
            return result
        except:
            return None

    @staticmethod
    def decode_ws(sock):
        data = WSProtocol.recv(sock, 2)
        if data == b'' or data == None:
            return None
        opcode = data[0] & 0x0F
        length = data[1] & ~0x80
        masked = data[1] & 0x80
        lenbytes = 0
        if length == 126:
            lenbytes = 2
        elif length == 127:
            lenbytes = 8

        if lenbytes > 0:
            length = 0
            lendata = WSProtocol.recv(sock, lenbytes)
            for i in range(0, lenbytes):
                length = (length * 256) + lendata[i]
        msg = bytearray(b'')
        if not masked:
            msg += WSProtocol.recv(sock, length)
        else:
            maskdata = WSProtocol.recv(sock, 4)
            msgdata = WSProtocol.recv(sock, length)

            for i in range(0, length):
                msg.append(msgdata[i] ^ maskdata[i % 4])
        if opcode == WSProtocol.WS_TEXT:
            msg = str(msg,"utf-8")
        else:
            msg = bytes(msg)
        return (opcode, msg)

    @staticmethod
    def encode_ws(sock, msg, opcode=None):
        if opcode is None:
            opcode = WSProtocol.WS_BINARY if isinstance(msg,bytes) else WSProtocol.WS_TEXT

        if isinstance(msg,bytes):
            msgbytes = msg
        else:
            msgbytes = msg.encode("utf-8")
        data = bytearray(b'')
        data.append(opcode | 0x80)
        length = len(msgbytes)
        if length < 126:
            data.append(len(msgbytes))
            lenbytes = 0
        elif length < 65536:
            data.append(126)
            lenbytes = 2
        else:
            data.append(127)
            lenbytes = 8
        if lenbytes > 0:
            for i in range(0, lenbytes):
                data.append((length >> 8 * (lenbytes - (i + 1))) & 0xFF)
        data += msgbytes
        sock.sendall(data)

    @staticmethod
    def handshake_request(sock, path="/vk"):
        headers = {}
        headers["Sec-WebSocket-Key"] = "SnwISUf0T7ttFQE1RqpDOw=="
        headers["Sec-WebSocket-Version"] = "13"
        headers["Upgrade"] = "websocket"
        headers["Cache-Control"] = "no-cache"
        WSProtocol.write_http_header_request(sock, headers, path)
        return WSProtocol.read_http_request(sock)

    @staticmethod
    def handshake_response(sock, valid_resources=None):
        (method, headers, resource, content) = WSProtocol.read_http_request(sock)
        if valid_resources and resource not in valid_resources:
            WSProtocol.write_http_header_response(sock, {}, 404, "Not Found")
            return None
        hs_headers = WSProtocol.complete_handshake(sock, headers)
        return (hs_headers, resource)

    @staticmethod
    def complete_handshake(sock, headers):
        digest = WSProtocol.create_hash(
            headers.get('Sec-WebSocket-Key', headers.get('Sec-Websocket-Key', None)))
        hs_headers = {}
        hs_headers["Upgrade"] = "WebSocket"
        hs_headers["Connection"] = "Upgrade"
        hs_headers["Sec-WebSocket-Accept"] = digest
        WSProtocol.write_http_header_response(sock, hs_headers, 101, "Switching Protocols")
        return hs_headers

    def __init__(self):
        pass

    def sendmessage(self, sock, message):
        WSProtocol.encode_ws(sock, message)

    def recievemessage(self, sock):
        m = WSProtocol.decode_ws(sock)
        if m == None:
            return m
        return m[1]


