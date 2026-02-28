import os, json
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)
msgs = []
NODE = os.getenv('NODE_NAME', 'unknown')
BROKER = os.getenv('MQTT_BROKER', 'web3')

def on_message(c, u, m):
    msgs.append(m.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, NODE)
client.on_message = on_message
client.connect(BROKER, 1883)
client.subscribe(f"nodes/{NODE}")
client.loop_start()

@app.route('/')
def index():
    return f"""
    <html>
    <head>
        <title>Node {NODE}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

            * {{ box-sizing: border-box; margin: 0; padding: 0; }}

            body {{
                font-family: 'JetBrains Mono', monospace;
                background: #0d0d0d;
                color: #00ff88;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
            }}

            body::before {{
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
            }}

            .terminal {{
                position: relative;
                z-index: 1;
                background: #111;
                border: 1px solid #00ff88;
                border-radius: 8px;
                width: 480px;
                box-shadow: 0 0 30px rgba(0,255,136,0.2), 0 0 60px rgba(0,255,136,0.05);
                overflow: hidden;
            }}

            .title-bar {{
                background: #1a1a1a;
                border-bottom: 1px solid #00ff88;
                padding: 10px 16px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .dots {{ display: flex; gap: 6px; }}
            .dot {{
                width: 12px; height: 12px;
                border-radius: 50%;
            }}
            .dot.red   {{ background: #ff5f57; }}
            .dot.yellow {{ background: #febc2e; }}
            .dot.green  {{ background: #28c840; }}

            .title-text {{
                flex: 1;
                text-align: center;
                font-size: 13px;
                color: #00ff88;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}

            .status-dot {{
                width: 8px; height: 8px;
                border-radius: 50%;
                background: #00ff88;
                box-shadow: 0 0 6px #00ff88;
                animation: blink 1.5s infinite;
            }}

            @keyframes blink {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.2; }}
            }}

            .body {{ padding: 16px; }}

            .node-label {{
                font-size: 11px;
                color: #555;
                margin-bottom: 4px;
                letter-spacing: 1px;
            }}

            .node-name {{
                font-size: 20px;
                font-weight: 700;
                color: #00ff88;
                text-shadow: 0 0 8px rgba(0,255,136,0.5);
                margin-bottom: 16px;
            }}

            #m {{
                height: 220px;
                overflow-y: auto;
                border: 1px solid #1f1f1f;
                border-radius: 4px;
                padding: 10px;
                margin-bottom: 14px;
                background: #0a0a0a;
                display: flex;
                flex-direction: column;
                gap: 6px;
                scrollbar-width: thin;
                scrollbar-color: #00ff88 #111;
            }}

            #m::-webkit-scrollbar {{ width: 4px; }}
            #m::-webkit-scrollbar-track {{ background: #111; }}
            #m::-webkit-scrollbar-thumb {{ background: #00ff88; border-radius: 2px; }}

            .msg-item {{
                font-size: 12px;
                color: #00ff88;
                padding: 6px 10px;
                border-left: 2px solid #00ff88;
                background: rgba(0,255,136,0.04);
                border-radius: 0 4px 4px 0;
                word-break: break-word;
            }}

            .msg-item::before {{
                content: '> ';
                color: #555;
            }}

            .empty-msg {{
                color: #333;
                font-size: 12px;
                text-align: center;
                margin: auto;
            }}

            .input-group {{
                display: flex;
                flex-direction: column;
                gap: 8px;
            }}

            .input-wrapper {{
                display: flex;
                align-items: center;
                border: 1px solid #1f1f1f;
                border-radius: 4px;
                background: #0a0a0a;
                padding: 0 10px;
                transition: border-color 0.2s;
            }}

            .input-wrapper:focus-within {{
                border-color: #00ff88;
                box-shadow: 0 0 8px rgba(0,255,136,0.15);
            }}

            .input-prefix {{
                color: #00ff88;
                font-size: 13px;
                margin-right: 6px;
                opacity: 0.6;
            }}

            input {{
                flex: 1;
                background: transparent;
                border: none;
                outline: none;
                color: #e0e0e0;
                font-family: 'JetBrains Mono', monospace;
                font-size: 13px;
                padding: 10px 0;
                caret-color: #00ff88;
            }}

            input::placeholder {{ color: #333; }}

            button {{
                width: 100%;
                padding: 10px;
                background: transparent;
                color: #00ff88;
                border: 1px solid #00ff88;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 2px;
                cursor: pointer;
                text-transform: uppercase;
                transition: all 0.2s;
                margin-top: 4px;
            }}

            button:hover {{
                background: #00ff88;
                color: #0d0d0d;
                box-shadow: 0 0 16px rgba(0,255,136,0.4);
            }}

            button:active {{
                transform: scale(0.98);
            }}

            .footer {{
                margin-top: 14px;
                font-size: 10px;
                color: #222;
                text-align: center;
                letter-spacing: 1px;
            }}
        </style>
    </head>
    <body>
        <div class="terminal">
            <div class="title-bar">
                <div class="dots">
                    <div class="dot red"></div>
                    <div class="dot yellow"></div>
                    <div class="dot green"></div>
                </div>
                <div class="title-text">mqtt-node</div>
                <div class="status-dot"></div>
            </div>
            <div class="body">
                <div class="node-label">CONNECTED NODE</div>
                <div class="node-name">// {NODE}</div>

                <div id="m">
                    <div class="empty-msg" id="empty">no messages yet...</div>
                </div>

                <div class="input-group">
                    <div class="input-wrapper">
                        <span class="input-prefix">TO:</span>
                        <input id="t" placeholder="web1 or web2" />
                    </div>
                    <div class="input-wrapper">
                        <span class="input-prefix">$</span>
                        <input id="txt" placeholder="type message..." />
                    </div>
                    <button onclick="send()">[ transmit ]</button>
                </div>

                <div class="footer">MQTT BROKER: {BROKER} &nbsp;|&nbsp; PORT 1883</div>
            </div>
        </div>

        <script>
            function send() {{
                const t = document.getElementById('t').value;
                const txt = document.getElementById('txt').value;
                if(!t || !txt) return;
                fetch('/publish?t=' + encodeURIComponent(t) + '&m=' + encodeURIComponent(txt));
                document.getElementById('txt').value = '';
            }}

            document.getElementById('txt').addEventListener('keydown', function(e) {{
                if(e.key === 'Enter') send();
            }});

            setInterval(() => {{
                fetch('/get_messages').then(r => r.json()).then(d => {{
                    const container = document.getElementById('m');
                    const empty = document.getElementById('empty');
                    if(d.length > 0) {{
                        if(empty) empty.remove();
                        container.innerHTML = d.map(x =>
                            '<div class="msg-item">' + x + '</div>'
                        ).join('');
                        container.scrollTop = container.scrollHeight;
                    }}
                }});
            }}, 1000);
        </script>
    </body>
    </html>
    """

@app.route('/publish')
def publish():
    t, m = request.args.get('t'), request.args.get('m')
    client.publish(f"nodes/{t}", f"[{NODE}]: {m}")
    return "OK"

@app.route('/get_messages')
def get_messages():
    return jsonify(msgs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)