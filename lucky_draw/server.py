#!usr/bin/env python3

import socket
import lucky_draw

ld = lucky_draw.lucky_draw()

def route_index():
    '''
    主页
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<!DOCTYPE html><head><meta charset="UTF-8"></head>'\
    '<body><h1>宝儿电商年会抽奖程序</h1><br>'\
    '<a href="/result_1">查看一等奖中奖名单</a><br>'\
    '<a href="/result_2">查看二等奖中奖名单</a><br>'\
    '<a href="/result_3">查看三等奖中奖名单</a><br>'\
    '<a href="/draw">点击抽奖</a></body>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_result_1():
    return route_result(price=1)

def route_result_2():
    return route_result(price=2)

def route_result_3():
    return route_result(price=3)

def route_result(price):
    '''
    显示页
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<!DOCTYPE html><head><meta charset="UTF-8"></head>'\
    '<body><h1>{}等奖中奖结果</h1>'.format(price)
    content = ld.result(price)
    if not content[price]:
        body += '<br>{}等奖还没有人中奖哦！'.format(price)
    else:
        body += '<br>'
        for i in content[price]:
            body += '<h3 style="display:inline-block">' + i[0] + '</h3>(<h5 style="display:inline-block">' + i[1] + '</h5>), '
    body += '<br><a href="/">返回</a></body>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_draw():
    '''
    抽奖页
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<!DOCTYPE html><head><meta charset="UTF-8"></head><h1>'
    content = ld.draw()
    if content:
        price = list(content.keys())[0]
        body += "{}等奖中奖结果：\n".format(price)
        for i in content[price]:
            body += '<h3 style="display:inline-block">' + i[0] + '</h3>(<h5 style="display:inline-block">' + i[1] + '</h5>), '
    else:
        body += '抽奖已经结束，所有大奖都名花有主了哦！恭喜中奖的亲们！'
    body += '</h1><br>'\
    '<a href="/draw">再次抽奖！</a><br>'\
    '<a href="/">返回主页面</a></body>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def error(code=404):
    '''
    根据 code 返回不同的错误相应返回
    '''
    e = {
        404: b'<HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    '''
    根据path调用相应的处理函数
    没有处理的path返回404
    '''
    r = {
        "/": route_index,
        '/result_1': route_result_1,
        '/result_2': route_result_2,
        '/result_3': route_result_3,
        '/draw': route_draw,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=2018):
    '''
    启动服务器
    '''
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            request = request.decode('utf-8')
            print(' * ip and request {}\n{}'.format(address, request))
            try:
                print(request)
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                print(' ! Error:', e)
            connection.close()

if __name__ == '__main__':
    run()
