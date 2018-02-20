from utils import log

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

def route_index(request):
    '''
    主页返回
    '''
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    body = template("index.html")
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
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    if request.method == "POST":
        form = request.form()   # 将内容转化为字典
        u = User.new(form)      # ?
        if u.validate_login():
            result = "登录成功，欢迎" + u + "回来！"
        else:
            result = "用户名或密码错误！"
    else:   # get
        result = ""
    body = template("login.html")
    body = body.replace("{{result}}", result)
    r = header + "\r\n" + body
    return r.encode("utf-8")

def route_register(request):
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
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
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

route_dict = {
    "/": route_index,
    "/favicon.ico": route_favicon,
    "/login": route_login,
    "/register": route_register,
    #"/messages": route_message,
}
