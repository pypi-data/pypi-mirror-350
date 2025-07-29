# from agentcp import AgentID
from flask import Flask
import threading
import socket
import time
from .llm_agent_utils import LLMAgent
from flask import jsonify, make_response
app = Flask(__name__)
actual_port = 0
llm_app_key = ""
aid = None

@app.route('/<llm_aid>/chat/completions', methods=['POST'])  # 添加methods参数指定POST方法
async def llm_request(llm_aid):
    # 获取请求头并打印
    from flask import request
    headers = dict(request.headers)
    if request.is_json:
        body = request.get_json()
    else:
        body = request.form.to_dict()
    global aid
    auth_str = headers.get("Authorization")
    if auth_str is None or auth_str != "Bearer "+llm_app_key:
        return make_response(jsonify({"error": "Unauthorized"}), 401)
    llm_agent = LLMAgent(llm_agent=llm_aid, aid=aid)
    response = await llm_agent.chat_create(body)
    return response

def get_base_url(agentId,llm_aid):
    global aid
    aid = agentId
    global actual_port
    # 获取实际分配的端口号
    return "http://127.0.0.1:"+str(actual_port)+"/"+llm_aid

def get_llm_api_key():
    # 获取实际分配的端口号
    return llm_app_key

def __run_server():
    # 端口设为0让系统自动分配
    try:
        global actual_port,llm_app_key
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        actual_port = sock.getsockname()[1]
        sock.close()
        llm_app_key = str(int(time.time())+actual_port)
        import hashlib
        llm_app_key = hashlib.sha256(llm_app_key.encode()).hexdigest()
        app.run(host='127.0.0.1', port=actual_port, debug=False)
    except Exception as e:
        print(f"Flask服务启动失败,请检查端口占用后，重启服务")

def run_server():
    # 创建并启动子线程运行Flask服务
    server_thread = threading.Thread(target=__run_server)
    server_thread.daemon = True  # 设置为守护线程，主线程退出时会自动结束
    server_thread.start()
    # 主线程可以继续执行其他任务