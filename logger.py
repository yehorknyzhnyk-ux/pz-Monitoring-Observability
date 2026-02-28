import os
import threading
from flask import Flask, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)
history = []

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        topic = msg.topic
        history.append({"topic": topic, "msg": payload})
        print(f"Logged: {topic} -> {payload}")
    except Exception as e:
        print(f"Error: {e}")

def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Postman_Web_Logger")
    client.on_message = on_message
    try:
        client.connect("web3", 1883, 60)
        client.subscribe("nodes/#")
        client.loop_forever()
    except Exception as e:
        print(f"MQTT Connection Error: {e}")

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Postman — MQTT Logger</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

            * { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'JetBrains Mono', monospace;
                background: #0d0d0d;
                color: #00ff88;
                min-height: 100vh;
                padding: 30px;
                overflow-x: hidden;
            }

            body::before {
                content: '';
                position: fixed;
                inset: 0;
                background: repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0,255,136,0.03) 2px,
                    rgba(0,255,136,0.03) 4px
                );
                pointer-events: none;
                z-index: 0;
            }

            .wrapper {
                position: relative;
                z-index: 1;
                max-width: 860px;
                margin: 0 auto;
            }

            .terminal-header {
                background: #111;
                border: 1px solid #00ff88;
                border-radius: 8px 8px 0 0;
                padding: 10px 16px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 0 30px rgba(0,255,136,0.15);
            }

            .dots { display: flex; gap: 6px; }
            .dot { width: 12px; height: 12px; border-radius: 50%; }
            .dot.red    { background: #ff5f57; }
            .dot.yellow { background: #febc2e; }
            .dot.green  { background: #28c840; }

            .header-title {
                flex: 1;
                text-align: center;
                font-size: 13px;
                letter-spacing: 3px;
                text-transform: uppercase;
                color: #00ff88;
            }

            .status-pill {
                font-size: 10px;
                color: #00ff88;
                border: 1px solid #00ff88;
                border-radius: 20px;
                padding: 2px 10px;
                letter-spacing: 1px;
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .blink-dot {
                width: 6px; height: 6px;
                border-radius: 50%;
                background: #00ff88;
                box-shadow: 0 0 4px #00ff88;
                animation: blink 1.5s infinite;
            }

            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.1; }
            }

            .terminal-body {
                background: #0a0a0a;
                border: 1px solid #00ff88;
                border-top: none;
                border-radius: 0 0 8px 8px;
                padding: 20px;
                box-shadow: 0 0 30px rgba(0,255,136,0.1);
            }

            .meta-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
                font-size: 11px;
                color: #333;
                letter-spacing: 1px;
            }

            .meta-bar span { color: #555; }
            #count { color: #00ff88; }

            #logs {
                display: flex;
                flex-direction: column;
                gap: 8px;
                max-height: 70vh;
                overflow-y: auto;
                scrollbar-width: thin;
                scrollbar-color: #00ff88 #111;
            }

            #logs::-webkit-scrollbar { width: 4px; }
            #logs::-webkit-scrollbar-track { background: #111; }
            #logs::-webkit-scrollbar-thumb { background: #00ff88; border-radius: 2px; }

            .entry {
                background: #111;
                border: 1px solid #1a1a1a;
                border-left: 3px solid #00ff88;
                border-radius: 0 4px 4px 0;
                padding: 10px 14px;
                display: grid;
                grid-template-columns: auto 1fr;
                gap: 8px 14px;
                align-items: start;
                animation: fadeIn 0.3s ease;
                transition: border-color 0.2s, background 0.2s;
            }

            .entry:hover {
                background: #141414;
                border-left-color: #00ffaa;
                box-shadow: 0 0 10px rgba(0,255,136,0.08);
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateX(-6px); }
                to   { opacity: 1; transform: translateX(0); }
            }

            .entry-index {
                font-size: 10px;
                color: #333;
                padding-top: 2px;
                user-select: none;
            }

            .entry-content { display: flex; flex-direction: column; gap: 4px; }

            .topic {
                font-size: 11px;
                color: #ff9100;
                letter-spacing: 1px;
                text-transform: uppercase;
            }

            .topic::before { content: 'TOPIC: '; color: #444; }

            .msg {
                font-size: 13px;
                color: #b3e5fc;
                word-break: break-word;
            }

            .msg::before { content: '> '; color: #444; }

            .empty {
                text-align: center;
                color: #222;
                font-size: 13px;
                padding: 40px 0;
                letter-spacing: 2px;
            }

            .footer {
                margin-top: 14px;
                text-align: center;
                font-size: 10px;
                color: #1f1f1f;
                letter-spacing: 2px;
            }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="terminal-header">
                <div class="dots">
                    <div class="dot red"></div>
                    <div class="dot yellow"></div>
                    <div class="dot green"></div>
                </div>
                <div class="header-title">postman // mqtt global logger</div>
                <div class="status-pill">
                    <div class="blink-dot"></div>
                    LIVE
                </div>
            </div>

            <div class="terminal-body">
                <div class="meta-bar">
                    <span>BROKER: web3:1883 &nbsp;|&nbsp; TOPIC: nodes/#</span>
                    <span>MESSAGES: <span id="count">0</span></span>
                </div>

                <div id="logs">
                    <div class="empty" id="empty">// awaiting transmissions...</div>
                </div>

                <div class="footer">ALL NODES MONITORED &nbsp;|&nbsp; AUTO-REFRESH 1s</div>
            </div>
        </div>

        <script>
            function updateLogs() {
                fetch('/history')
                    .then(r => r.json())
                    .then(data => {
                        const container = document.getElementById('logs');
                        document.getElementById('count').textContent = data.length;

                        if (data.length === 0) return;

                        const empty = document.getElementById('empty');
                        if (empty) empty.remove();

                        container.innerHTML = [...data].reverse().map((item, i) =>
                            `<div class="entry">
                                <span class="entry-index">#${data.length - i}</span>
                                <div class="entry-content">
                                    <span class="topic">${item.topic}</span>
                                    <span class="msg">${item.msg}</span>
                                </div>
                            </div>`
                        ).join('');
                    });
            }
            setInterval(updateLogs, 1000);
            updateLogs();
        </script>
    </body>
    </html>
    """

@app.route('/history')
def get_history():
    return jsonify(history)

if __name__ == '__main__':
    threading.Thread(target=start_mqtt, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)