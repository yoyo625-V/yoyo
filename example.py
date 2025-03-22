import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv  # 导入 load_dotenv
from gevent.pywsgi import WSGIServer
import webbrowser

# 在启动时打开浏览器
webbrowser.open_new_tab('http://127.0.0.1:5000/')


# 加载 .env 文件
load_dotenv()

# 初始化Flask应用
app = Flask(__name__)

# 设置OpenAI API密钥
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the chat API!'}), 200

if __name__ == '__main__':
    # 在启动时打开浏览器
    webbrowser.open_new_tab('http://127.0.0.1:5000/')

    server = WSGIServer(('0.0.0.0', 5000), app)
    print("Serving on http://0.0.0.0:5000/")
    server.serve_forever()