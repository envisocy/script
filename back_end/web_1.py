#!usr/bin/env python

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

def test_parsed_response():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
        'Content-Type: text/html\r\n' \
        'Location: https://movie.douban.com/top250\r\n' \
        'Content-Length: 178\r\n\r\n' \
        'test body'
    response = response.encode('utf-8')
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'

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

def parsed_request(path, host):
    http_request = 'GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    request = http_request.encode('utf-8')
    return request

def response_by_socket(s, buffer_size=1024):
    response = b''
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    return response

def parsed_response(response):
    r = response.decode('utf-8')
    header, body = r.split("\r\n\r\n", 1)
    h = header.split('\r\n')
    # GET 200 ok
    status_code = int(h[0].split()[1])

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v

    return status_code, headers, body

def get(url):
    protocol, host, port, path = parsed_url(url)
    if protocol == "http":
        s = socket.socket()
    elif protocol == "https":
        import ssl
        s = ssl.wrap_socket(socket.socket())

    s.connect((host, port))

    local_ip, local_port = s.getsockname()
    print('本机 ip 和 port：{}:{}'.format(local_ip, local_port))

    s.send(parsed_request(path, host))

    response = response_by_socket(s)

    status_code, headers, body = parsed_response(response)

    print(status_code, headers, body)
    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)

    return status_code, headers, body
