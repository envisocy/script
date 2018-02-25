import random

from utils import log
from models.message import Message
from models.user import User

# 保存所有的messages
message_list = []
# session 可以在服务端实现过期功能
session = {}

def random_str():
    seed = "abcdefghijklmnopqrstuvwxyz1234567890~!@#$%^&*()_+-<>,.?"
    s = ""
    for i in range(16):
        random_index = random.randint(0, len(seed)-1)
        s += seed[random_index]
    return s

def template(name):
    path = 'templates/' + name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def route_static(request):
    '''
    静态资源处理函数
    该函数被引用到server.py中执行
    分离/static?file=doge.gif
    '''
    filename = request.query.get("file", "default.jpg")
    path = "static/" + filename
    with open(path, 'rb') as f:
        header = 'HTTP/1.1 201 Static OK\r\nContent-Type: image/' + filename.split(".", 1)[1] + '\r\n'
        img = header.encode("utf-8") + b'\r\n' + f.read()
        return img

def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    return username

def response_with_header(headers, code=200):
    header = "HTTP/1.1 " + str(code) + " Test OK\r\n"
    header += ''.join(['{}: {}\r\n'.format(k, v) for k,v in headers.items()])
    return header

def route_index(request):
    '''
    主页返回
    '''
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    body = template("index.html")
    body = body.replace("{{username}}", username)
    if username == "【游客】":
        body = body.replace('{{replace}}', '<a href="/login">【点击登陆】</a><a href="/register">【点击注册】</a>')
    else:
        body = body.replace('{{replace}}', '<a href="/messages">【消息测试】</a>')
    header = response_with_header(headers)
    r = header + "\r\n" + body
    return r.encode("utf-8")

def route_favicon(request):
    '''
    /favicon.ico
    '''
    with open("static/favicon.jpg", "rb") as f:
        header = b'HTTP/1.1 201 Static OK\r\nContent-Type: image/jpg\r\n'
        img = header + b'\r\n' + f.read()
        return img

def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    if request.method == "POST":
        form = request.form()   # 将body内容转化为字典
        u = User.new(form)
        if u.validate_login():
            session_id = random_str()
            session[session_id] = u.username
            headers["Set-cookie"] = "user={}".format(session_id)
            result = "登录成功，欢迎" + u.username + "回来！"
            username = u.username # 防止头部显示【游客】
        else:
            result = "用户名或密码错误！"
    else:   # get
        result = ""
    body = template("login.html")
    if username == "【游客】":
        body = body.replace("{{form}}", template("login_form.html"))
    else:
        body = body.replace("{{form}}", "<a href='/'><button>返回</button></a>")
    body = body.replace("{{result}}", result)
    body = body.replace("{{username}}", username)
    header = response_with_header(headers)
    r = header + "\r\n" + body
    return r.encode("utf-8")

def route_register(request):
    headers = {
        "Content-Type": "text/html"
    }
    if request.method == "POST":
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = "注册成功<br> <pre>{}</pre>".format(User.all())
        else:
            result = "用户名或密码长度必须大于2"
    else:
        result = ""
    body = template("register.html")
    body = body.replace('{{result}}', result)
    header = response_with_header(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_message(request):
    headers = {
        'Content': 'text/html'
    }
    username = current_user(request)
    # L.5 使用 redirect() 函数挡掉非正常请求
    if username == "【游客】":
        log("**Debug, route msg 未登录")
        return redirect("/")
    if request.method == "POST":
        form = request.form()
        msg = Message.new(form)
        message_list.append(msg)
    body = template("html_basic.html")
    megs = '<br>'.join([str(m) for m in message_list])
    body = body.replace("{{username}}", username)
    body = body.replace("{{messages}}", megs)
    header = response_with_header(headers)
    r = header + "\r\n" + body
    return r.encode(encoding="utf-8")

def redirect(url):
    '''
    服务器收到302的时候
    会在HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    '''
    headers = {
        "Location": url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意，没有 HTTP body 部分
    r = response_with_header(headers, 302) + "\r\n"
    return r.encode("utf-8")

route_dict = {
    "/": route_index,
    "/favicon.ico": route_favicon,
    "/login": route_login,
    "/register": route_register,
    "/messages": route_message,
}
