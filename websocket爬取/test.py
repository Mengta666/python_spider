import websocket
import json
import  time

# 定义 WebSocket 连接时的回调函数
def on_message(ws, message):
    print("收到消息:", message)
    # 假设消息是 JSON 格式，解析并处理
    try:
        data = json.loads(message)
        print("解析后的数据:", data)
        # 在这里添加你的数据处理逻辑，例如保存到文件或数据库
    except json.JSONDecodeError:
        print("消息非 JSON 格式:", message)

def on_error(ws, error):
    print("发生错误:", error)

def on_close(ws, close_status_code, close_msg):
    print("连接关闭:", close_status_code, close_msg)

def on_open(ws):
    print("连接已建立")
    # 连接建立后，可以发送初始消息（如果需要）
    # 例如：ws.send(json.dumps({"type": "subscribe", "channel": "some_channel"}))

ws_url = "wss://push.coinmarketcap.com/ws"

while True:
    try:
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever(ping_interval=30, ping_timeout=10)  # 添加心跳包
        break  # 连接成功则退出循环
    except Exception as e:
        print("连接失败，5秒后重试:", e)
        time.sleep(5)  # 等待 5 秒后重试