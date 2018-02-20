from utils import log

from routes import route_dict

import urllib
import socket


class Request():
    # 保存请求的数据
    def __init__(self):
        self.method = "GET"
        self.path = "/"
        self.query = {}
        self.body = ""

    def log(self):
        '''
        打印所有当前 request 类中的参数值
        '''
        log("Method: ", self.method)
        log("Path: ", self.path)
        log("Query: ", self.query)
        log("Body: ", self.body)

    def form(self):
        '''
        把 body 解析为一个字典并返回
        '''
        args = self.body.split("&")
        f = {}
        for arg in args:
            k, v = arg.split("=")
            f[urllib.parse.unquote(k)] = urllib.parse.unquote(v)
        return f

request = Request()

def run(host="", port=3001):
    log("服务器启动在 {0} 端口，请通过 localhost.com:{0} 访问！".format(port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            log("--- New listen ---")
            s.listen(5)
            connection, address = s.accept()
            log("请求的客户端信息: ", address)

            r = b''
            while True:
                rec = connection.recv(2048)
                r += rec
                if len(r) < 2048:
                    break
            r = r.decode("utf-8")
            log("发出的信息：\n", r)
            # GET / HTTP/1.1\r\nHost: localhost:3001\r\n
            # Connection: keep-alive...\r\n

            if len(r.split()) < 2:
                continue

            request.method = r.split()[0]
            path = r.split()[1]     # 未转化的版本，包含 path和 query
            request.body = r.split("\r\n\r\n", 1)[1]
            request.path, request.query = parsed_path(path)
            request.log()       # 打印 request 的分类信息

            # 调用路由，运行响应函数
            response = response_for_path(request.path)
            log("[服务器返回的信息]\n", response)
            connection.sendall(response)
            connection.close()

def parsed_path(raw_path):
    index = raw_path.find("?")
    if index == -1:
        return raw_path, {}
    else:
        path = raw_path.split("?", 1)[0]
        raw_query = raw_path.split("?", 1)[1]
        query = {}
        for i in raw_query.split("&"):
            k, v = i.split("=")
            query[k] = v
        return path, query

def response_for_path(path):
    r = {
        "/" : index,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)

def error(request):
    response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"\
    "<html><body><h1>404</h1><p>Not Found</p></body></html>"
    return response.encode("utf-8")

def index(request):
    # response = "HTTP/1.1\r\n200 OK\r\nContent-Type: text/html\r\n\r\n"\
    # "<html><body><h1>Index.html</h1></body></html>"
    # return response.encode("utf-8")
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    body = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>html & CSS 测试主页</title>
    </head>
    <body>
        <h1 id="top-title">《Head First HTML & CSS》代码测试页</h1>
        <a href="/login">【点击登陆】</a>
    </body>
    </html>
    """
    r = header + "\r\n" + body
    return r.encode("utf-8")

if __name__ == "__main__":
    config = dict(
        host = "",
        port = 3018,
    )
    run(**config)
