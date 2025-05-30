
import requests
import json

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# 天气查询
def get_weather(province, city):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
    }
    with open('token_json/token.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    url = f"https://cn.apihz.cn/api/tianqi/tqyb.php?id={config['id']}&key={config['key']}&sheng={province}&place={city}"
    res = requests.get(url=url, headers=header)
    res = res.json()
    place = res['place']
    weather = res['weather1']
    temperature = res['temperature']
    data = {
        'place': place,
        'weather': weather,
        'temperature': str(temperature) + " ℃"
    }
    return data

@app.route('/')
def main_page():       # 主页
    default_province = "北京市"
    default_city = "北京"
    weather_data = get_weather(default_province, default_city)
    return render_template('index.html',  weather_data=weather_data)
    # return render_template('index.html')

@app.route("/post_weather",  methods=['POST'])
def weather_post():
    data = request.json
    header = request.headers["User-Agent"]
    cookie = request.headers["Cookie"]
    if "Mozilla/5.0" not in header:
        msg = "浏览器头错误"
    elif "mengta123" not in cookie:
        msg = "cookie错误"
    else:
        msg = "成功"
    province = data['province']
    city = data['city']
    data = get_weather(province, city)
    data = {
        "msg" : msg,
        "data" : data
    }
    return jsonify(data)

@app.route("/get_weather",  methods=['GET'])
def weather_get():
    header = request.headers["User-Agent"]
    cookie = request.headers["Cookie"]
    print(header,cookie)
    if "Mozilla/5.0" not in header:
        msg = "浏览器头错误"
    elif "mengta123" not in cookie:
        msg = "cookie错误"
    else:
        msg = "成功"
    province = request.args.get('province')
    city = request.args.get('city')
    data = get_weather(province, city)
    data = {
        "msg" : msg,
        "data" : data
    }
    return jsonify(data)



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)