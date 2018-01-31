# 调用支援函数
from utils import log
# 基础库
import socket
import urllib.parse
# 路由库
from routes import route_static
from routes import route_dict



class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body =''

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        # 这里可能存在BUG，应该解析出数据后，再unquote
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split("=")
            f[k] = v
        return f

request = Request()

def error(request, code=404):
    # 一般情况不要用数字作为字典的 key，但在 HTTP 协议中 code 似乎更方便
    e = {
        404: b"HTTP/1.1 404 NOT FOUND\r\n\r\n<html><h1>NOT FOUND</h1><p> 404 Error </p></html>"
    }
    return e.get(code, b"")

def run(host="", port=3000):
    """
    启用服务器
    """
    log("start at:", "{}:{}".format(host, port))
    # with是非常好用的方式，可以保证每次关闭都正确的释放端口
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            log("address", address)

            # 接收
            r = b''
            while True:
                rec = connection.recv(1000)
                r += rec
                if len(r) < 1000:
                    break
            r = r.decode('utf-8')
            log("raw request:\n\n", r)

            # 解码
            # GET / HTTP/1.1\r\nHost: {host}...\r\n\r\n{body}
            # 防止 chrome 发送空请求导致 split 得到空 list 导致程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]

            # 在request中保存 method, body, path, query
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n', 1)[1]
            log("method:", request.method)
            log("body:", request.body)
            response = response_for_path(path)

            # 发送响应
            connection.sendall(response)
            connection.close()

def response_for_path(path):
    # 用于把 path 和 query 分离
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log("path & query:", path, query)
    """
    根据 path 处理相应的函数，而没有的path会返回404
    这里的 r 保留象征性的路由，更多的内容通过 r.update(route_dict) 加载
    """
    r = {
        #'/static': route_static,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)

def parsed_path(path):
    # 将 a=b&c=d 生成 {"a": b, "c": d,} 的形式
    index = path.find("?")
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split("?", 1)
        args = query_string.split("&")
        query = {}
        for arg in args:
            k, v = arg.split("=")
            query[k] = v
        return path, query

if __name__=='__main__':
    # 生成配置文件并且运行程序
    config = dict(
        host="",
        port=3000,
    )
    run(**config)
