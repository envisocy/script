from utils import log
import socket


class Request():
    def __init__(self):
        self.method = "GET"
        self.path = "/"
        self.query = {}
        self.body = ""

    def log(self):
        log("Method: ", self.method)
        log("Path: ", self.path)
        log("Query: ", self.query)
        log("Body: ", self.body)

request = Request()

def run(host="", port=3001):
    log("服务器启动")
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            log("请求的客户端信息: ", address)

            r = b''
            while True:
                rec = connection.recv(1000)
                r += rec
                if len(r) < 1000:
                    break
            r = r.decode("utf-8")
            log(r)
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
            s.sendall(response)
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
        "/" : index
    }
    # r.update(route_dict)
    response = r.get(path, error)

def error():
    response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"\
    "<html><body><h1>404</h1><p>Not Found</p></body></html>"
    return response

def index():
    response = "HTTP/1.1 200 OK\r\n\r\n"\
    "<html><body><h1>Index.html</h1></body></html>"
    return response

if __name__ == "__main__":
    run()
