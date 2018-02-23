from utils import log

from routes import route_dict
from routes import route_static

import urllib.parse
import socket


class Request():
    # 保存请求的数据
    def __init__(self):
        self.method = "GET"
        self.path = "/"
        self.query = {}
        self.body = ""
        # L.4 cookies 拓展
        self.headers = {}
        self.cookies = {}

    def log(self):
        '''
        打印所有当前 request 类中的参数值
        '''
        pars = "\n".join([" > {}: {}".format(k, v) for k, v in self.
                          __dict__.items()])
        log("--- Requst Parameter ---\n" + pars)

    def form(self):
        '''
        在需要时：
        把 body 解析为一个字典并返回
        将原函数进行了修改，未完全测试通过
        '''
        args = self.body.split("&")
        f = {}
        for arg in args:
            k, v = arg.split("=")
            f[urllib.parse.unquote(k)] = urllib.parse.unquote(v)
        return f

    def add_headers(self, header):
        # 更新 headers 的同时更新 cookies
        for line in header:
            k, v = line.split(": ", 1)
            self.headers[k] = v
        # 更新 cookie
        self.cookies = {}
        cookies = self.headers.get("Cookie", "")
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

request = Request()

def run(host="", port=3001):
    log("服务器启动在 {0} 端口，请通过 localhost.com:{0} 访问！".format(port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            print("\n")
            log("--- New Listen ---")
            s.listen(5)
            connection, address = s.accept()
            log("Host message: ", address)

            r = b''
            while True:
                rec = connection.recv(2048)
                r += rec
                if len(r) < 2048:
                    break
            r = r.decode("utf-8")
            # log("发出的信息：\n", r)
            # GET / HTTP/1.1\r\nHost: localhost:3001\r\n
            # Connection: keep-alive...\r\n

            if len(r.split()) < 2:
                continue

            # 特别的，这里在每次运行，都会重新对 request 对象进行赋值覆盖
            request.method = r.split()[0]
            path = r.split()[1]     # 未转化的版本，包含 path和 query
            request.add_headers(r.split("\r\n\r\n", 1)[0].
                                          split("\r\n")[1:])
            request.body = r.split("\r\n\r\n", 1)[1]
            request.path, request.query = parsed_path(path) # 函数转化
            request.log()       # 打印 request 的分类信息

            # 调用路由，运行响应函数
            response = response_for_path(request.path)
            log("--- Retuen Response ---\n", response[:100])
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
    '/static': route_static,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)

def error(request):
    response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"\
    "<html><body><h1>404</h1><p>Not Found</p></body></html>"
    return response.encode("utf-8")


if __name__ == "__main__":
    config = dict(
        host = "",
        port = 3018,
    )
    run(**config)
