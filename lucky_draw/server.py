#!usr/bin/env python3

import socket
import lucky_draw

ld = lucky_draw.lucky_draw()

def route_index():
    '''
    主页
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">'\
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'\
    '<meta http-equiv="X-UA-Compatible" content="ie=edge"><title>年会抽奖'\
    '</title><style>#baImage{position: fixed;top: 0px;left: 0px;right: 0px;'\
    'bottom: 0px;width: 100%;height: 100%;z-index: -10;}.btn{width: 100%;'\
    '}#btnView{position: fixed;bottom:10%;left:35%;}'\
    '#btnContinue{position: fixed;bottom:8%;left:55% '\
    ';}</style></head><body><img id="baImage" src="/index.jpg" '\
    'alt=""><div  id="btnView"  class="btn"><a href="/result"><img style="height:'\
    '80px;" src="/btn-view.png" alt=""></a></div>'\
    '<div id="btnContinue" class="btn"><a href="/draw"><img style='\
    '"height:200px;" src="/btn-draw.png" alt=""></a></div></body></html>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_result():
    '''
    显示页
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">'\
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'\
    '<meta http-equiv="X-UA-Compatible" content="ie=edge"><title>宝儿电商年会'\
    '抽奖结果页</title><style>#baImage{position: fixed;top: 0px;left: 0px;'\
    'right: 0px;bottom: 0px;width: 100%;height: 100%;z-index: -10;}.btnBack{'\
    'position: fixed;top:20px;}#resultList{position: relative;margin: 0 auto;'\
    'top:250px;height: 500px;width: 1100px;}#resultList ul{position: absolute;'\
    'display: inline-block;list-style: none;padding: 0;margin: 0;}#first{'\
    'top: 0px;left: 420px;width: 225px;}#second{top: 20px;left: 0px;'\
    'width: 240px;}#thired{top: 40px;left: 870px;width: 260px;}#second li{'\
    'width: 40%;float: left;font: 25px bold;padding: 5px 0 5px 10%;color:'\
    'rgb(231, 228, 16);}#first li{width: 40%;float: left;font: 30px bold;'\
    'padding: 15px 0 15px 10%;color:rgb(231, 228, 16);}#thired li{width: 30%;'\
    'float: left;font: 20px bold;padding: 5px 0 5px 3%;color:rgb(231, 228, 16);'\
    '}</style></head><body><img id="baImage" src="/view.jpg" alt="">'\
    '<div class="btnBack" class="btn"><a href="/"><img style="height:'\
    '60px;opacity:0.6" src="/btn-back.png" alt=""></a></div><div id="resultList">'
    for price in [2, 1, 3]:
        body += '<ul id="'+ {2:"second", 1:"first", 3:"thired"}[price] +'">'
        content = ld.result(price)
        for i in content[price]:
            body += '<li>' + i[0] + '</li>'
        body += '</ul>'
    body += '</div></body></html>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_draw():
    '''
    抽奖页
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">'\
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'\
    '<meta http-equiv="X-UA-Compatible" content="ie=edge"><title>年会抽奖</title>'\
    '<style>#baImage{position: fixed;top: 0px;left: 0px;right: 0px;bottom: 0px;'\
    'width: 100%;height: 100%;z-index: -10;}.btn{width: 100%;}.btnBack{'\
    'position: fixed;top:20px;}#btnContinue{position: fixed;bottom:20px;'\
    'text-align: center;}#entryTitle{position: fixed;top: 32%;left: 25%;'\
    'text-align: center;font: 44px bold;}#entryList{position: fixed;top: 42%;'\
    'left: 30%;width: 40%;text-align: center;}#entryList ul{display: inline-block;'\
    'list-style: none;padding: 0;width: 200px;margin: 10px;}#entryList ul li{'\
    'font: 38px bold;padding: 5px 20%;color:#ff344c;min-width: 100px;}'\
    'a:hover{cursor:pointer;}</style></head><body><img id="baImage" '\
    'src="./draw.jpg" alt=""><div class="btnBack" class="btn"><a href="/">'\
    '<img style="height:60px;opacity:0.6" src="./btn-back.png" alt=""></a>'\
    '</div><div id="entryTitle"><ul>'
    content = ld.draw()
    if content:
        price = list(content.keys())[0]
        body += '{}等奖中奖结果：'.format({1: "一", 2: "二", 3: "三"}[price])
        body += '</ul></div><div id="entryList">'
        for i in content[price]:
            body += '<ul><li>' + i[0] + '</li></ul>'
        body += '</div><div id="btnContinue"  class="btn"><a href="/draw">'\
        '<img style="height:200px" src="/btn-redraw.png" alt=""></a></div>'\
        '</body></html>'
    else:
        body += '<div style="position: fixed;top:40%;left:36%;color:#ff344c;'\
        'line-height:200%;text-align: center;">抽奖已经结束！<br>'\
        '所有大奖都名花有主了哦！<br>恭喜中奖的亲们！</div></ul></div><div '\
        'id="btnContinue" class="btn"><a href="/result"><img style='\
        '"position:fixed;height:80px;bottom:10%;left:44%;" src="/btn-view.png" alt=""></a></div></body></html>'
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

def img(filename):
    with open('./img/' + filename, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img

def jpg_index():
    return img("index.jpg")

def jpg_view():
    return img("view.jpg")

def jpg_draw():
    return img("draw.jpg")

def btn_draw():
    return img("btn-draw.png")

def btn_view():
    return img("btn-view.png")

def btn_redraw():
    return img("btn-redraw.png")

def btn_back():
    return img("btn-back.png")

def response_for_path(path):
    '''
    根据path调用相应的处理函数
    没有处理的path返回404
    '''
    r = {
        "/": route_index,
        '/result': route_result,
        '/draw': route_draw,
        '/index.jpg': jpg_index,
        '/view.jpg': jpg_view,
        '/draw.jpg': jpg_draw,
        '/btn-draw.png': btn_draw,
        '/btn-view.png': btn_view,
        '/btn-redraw.png': btn_redraw,
        '/btn-back.png': btn_back,
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
