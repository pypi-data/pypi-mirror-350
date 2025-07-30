/* MIT License

Narvi - a simple python web application server

Copyright (C) 2022-2024 Visual Topology Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

class NarviWebappService {

    constructor(session) {
        this.session = session;
        this.message_listeners = [];
    }

    send(msg) {
        this.session.sendMessage(msg);
    }

    add_message_listener(listener) {
        this.message_listeners.push(listener);
    }

    recv(msg) {
        this.message_listeners.forEach(listener => listener(msg));
    }
}

class NarviWebsocketMessageChannel {

    constructor(ws_url) {
        this.ws = null;
        this.message_handler = null;
        this.pending_messages_in = [];
        this.pending_messages_out = [];
        const ws = new WebSocket(ws_url);
        ws.binaryType = "arraybuffer";
        this.heartbeat = null;

        if (ws) {
            ws.onopen = (event) => {
                this.ws = ws;
                for (let idx = 0; idx < this.pending_messages_out.length; idx++) {
                    this.ws.send(this.pending_messages_out[idx]);
                }
                this.pending_messages_out = [];
                this.start_heartbeat();
            }

            ws.onmessage = (msg) => {
                if (this.message_handler) {
                    this.message_handler(msg.data);
                } else {
                    this.pending_messages_in.push(msg.data);
                }
            }

            ws.onerror = (err) => {
                window.setTimeout(() => this.reconnect(),1000);
                this.stop_heartbeat();
            }

            ws.onclose = () => {
                window.setTimeout(() => this.reconnect(),1000);
                this.stop_heartbeat();
            }
        }
    }

    start_heartbeat() {
        // to keep the websocket from getting disconnected, it is helpful to send a heartbeat ""
        this.heartbeat = window.setInterval( () => {
            this.ws.send("");
        }, 10000);
    }

    stop_heartbeat() {
        if (this.heartbeat) {
            window.clearInterval(this.heartbeat);
            this.heartbeat = null;
        }
    }

    set_message_handler(message_handler) {
        this.message_handler = message_handler;
        for (let idx = 0; idx < this.pending_messages_in.length; idx++) {
            this.message_handler(this.pending_messages_in[idx]);
        }
        this.pending_messages_in = [];
    }

    reconnect() {
        alert("Connection to server lost, press OK to try to reconnect");
        location.reload();
    }

    send(msg) {
        if (this.ws) {
            this.ws.send(msg);
        } else {
            this.pending_messages_out.push(msg);
        }
    }
}

class NarviSession {

    constructor(channel, app_cls) {
        this.service = null;
        this.webapp = null;
        this.channel = channel;
        this.session_id = undefined;

        channel.set_message_handler(msg => {
             if (msg instanceof Blob) {
                 if (this.webapp) {
                     this.webapp.recv(msg);
                 } else {
                     console.warn("[NarviSession] No peer service to receive webapp_message");
                 }
             } else {
                 if (!this.webapp) {
                     const obj = JSON.parse(msg);
                     if (obj["action"] === "session_connected") {
                         this.session_id = obj["session_id"];
                         this.createApp(app_cls, obj["app_parameters"]);
                     }
                 } else {
                     this.webapp.recv(msg);
                 }
             }
        });
    }

    createApp(cls, parameters) {
        try {
            this.service = new NarviWebappService(this);
            this.webapp = new cls(this.service, parameters);
        } catch(e) {
            console.error(e);
        }
    }

    sendMessage(msg) {
        this.channel.send(msg);
    }
}


function start_narvi(app_cls) {
    const host = window.location.hostname;
    const path = window.location.pathname;
    const port = window.location.port;
    const protocol = window.location.protocol;

    const path_parts = path.split("/");
    let ws_protocol = "";
    if (protocol === "http:") {
        ws_protocol += "ws:";
    } else {
        ws_protocol += "wss:";
    }

    const path_len = path_parts.length;
    // page URL is <base>/namespace/appname/servicename/index.html
    let namespace = path_parts[path_len-4];
    let app_name = path_parts[path_len-3];
    let service = path_parts[path_len-2];
    let base_url = path_parts.slice(0,path_len-4).join("/");
    let ws_url = ws_protocol;
    ws_url += "//" + host + ":" + port;
    ws_url += base_url;
    ws_url += "/" + namespace;
    ws_url += "/" + app_name;
    ws_url += "/" + service;
    ws_url += "/connect";
    let channel = new NarviWebsocketMessageChannel(ws_url);
    return new NarviSession(channel, app_cls);
}




