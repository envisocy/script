#!usr/bin/env python
# -*- coding:utf-8 -*-

import socket

def client(host='g.cn',port=80):
    s = socket.socket()
    # import ssl
    # s = ssl.wrap_socket(socket.socket())
    s.connect((host, port))
    ip, port = s.getsockname()
    print("本机 ip 和 port: {} {}".format(ip, port))

    # 构造一个HTTP请求
    http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
    request = http_request.encode('utf-8')
    print("请求", request)
    s.send(request)

    # 接受服务器响应数据
    buffer_size = 1024
    response = b''
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    print("响应", response)
    print("响应 str 格式", response.decode('utf-8'))

def http(host='', port=2018):
    s = socket.socket()
    s.bind((host, port))
    while True:
        s.listen(5) # 监听
        connection, address = s.accept()

        buffer_size = 1024
        request = b''
        while True:
            r = connection.recv(buffer_size)
            request += r
            if len(r) < buffer_size:
                break
        print("ip and request, {}\n{}".format(address, request.decode('utf-8')))

        response = b'/HTTP/1.1 200 Anywords\r\n\r\n<h1>Hello World!</h1>'

        connection.sendall(response)
        connection.close()

def test_parsed_url():
    """
    单元测试
    """
    host = "g.cn"
    path = "/"
    test_items = [
        ('http://g.cn', ('http', host, 80, path)),
        ('http://g.cn/', ('http', host, 80, path)),
        ('http://g.cn:90', ('http', host, 90, path)),
        ('http://g.cn:90/', ('http', host, 90, path)),
        ('https://g.cn', ('https', host, 443, path)),
        ('https://g.cn:233/', ('https', host, 233, path)),
        ('https://geogle.com.cn:60/index.html', ('https', 'geogle.com.cn', 60, '/index.html'))
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e

def parsed_url(url):
    """
    解析 url 并返回 (protocol, host, port, path)
    """
    protocol = "http"
    if url[:7] == "http://":
        u = url.split("://")[1]
    elif url[:8] == "https://":
        protocol = "https"
        u = url.split("://")[1]
    else:
        u = url

    i = u.find("/")
    if i == -1:
        host = u
        path = "/"
    else:
        host = u[:i]
        path = u[i:]

    port_default = {
        "http": 80,
        "https": 443,
    }

    port = port_default[protocol]
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path
