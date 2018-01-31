#!usr/bin/env python3

import socket
import lucky_draw
import os

ld = lucky_draw.lucky_draw()

def route_index():
    '''
    主页
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">'\
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'\
    '<meta http-equiv="X-UA-Compatible" content="ie=edge"><title>年会抽奖'\
    '</title><style>#container{height: 100vh;width: 100vw;overflow: hidden;}'\
    '#baImage{position: fixed;top: 0px;left: 0px;right: 0px;'\
    'bottom: 0px;width: 100%;height: 100%;z-index: -10;}.btn{width: 100%;'\
    '}#btnView{position: fixed;bottom:10%;left:35%;}'\
    '#btnContinue{position: fixed;bottom:8%;left:55% '\
    ';}</style></head><body id="container"><img id="baImage" src="/index.jpg" '\
    'alt=""><div  id="btnView"  class="btn"><a href="/result"><img style="height:'\
    '80px;" src="/btn-view.png" alt=""></a></div>'\
    '<div id="btnContinue" class="btn"><a href="/draw"><img style='\
    '"height:200px;" src="/btn-draw.png" alt=""></a></div>'
    body += """
    ﻿<script>
          //定义雪花
          function CreateSnow(snowBox,src,style){
            this.snowBox = document.getElementById(snowBox);//找到容器
            this.snowStyle = Math.ceil(Math.random()*style);//雪花类型[1,2]
            this.maxLeft = this.snowBox.offsetWidth-Math.random()*5+3;//运动范围
            this.maxTop = this.snowBox.offsetHeight-Math.random()*5+3;
            this.left = this.snowBox.offsetWidth*Math.random();//起始位置
            this.top = this.snowBox.offsetHeight*Math.random();
            this.angle=1.1+0.8*Math.random();//飘落角度
            this.minAngle=1.1;
            this.maxAngle=1.9;
            this.angleDelta=0.01*Math.random();
            this.speed=1.4+Math.random();//下落速度
            this.createEle(src);//制作雪花dom   凹=放在最后，使得原型里能取到值
          };
          //雪片生成+下落
          CreateSnow.prototype = {
            createEle : function(baseSrc){//生成雪花元素
              var srcIndex = baseSrc.lastIndexOf('.'),//获取最后一个'.'
                src = baseSrc.substring(0,srcIndex)+this.snowStyle+baseSrc.substring(srcIndex,baseSrc.length);
              var image = new Image();
                image.src = src;
              this.ele = document.createElement("img");
              this.ele.setAttribute('src',src);
              this.ele.style.position="absolute";
              this.ele.style.zIndex="99";
              this.snowBox.appendChild(this.ele);
              //设置雪花尺寸
              var img = this.ele;
              image.onload = function(){
                imgW = image.width;
                img.setAttribute('width',Math.ceil(imgW*(0.1+Math.random())));
              };
            },
            move : function(){//雪花运动
              this.angleDelta=-this.angleDelta;
              this.angle+=this.angleDelta;
              this.top-=this.speed*Math.sin(this.angle*Math.PI);
              if(this.top>this.maxTop){//雪花掉出来后回到顶部
                  this.top=0;
              }
              this.ele.style.left=this.left+'px';//凹=加‘px’
              this.ele.style.top=this.top+'px';
            }
          };
          //下雪启动
          function goSnow(snowBox,src,num,style){
            var snowArr = [];
            for(var j = 0 ; j<num ; j++){
              snowArr.push(new CreateSnow(snowBox,src,style));
            }
            var makeSnowtime = setInterval(function(){
              for(var i = snowArr.length-1;i>=0;i--){//找到数组中的最新的一个
                if(snowArr[i]){
                  snowArr[i].move();
                }
              }
            },40);
          };
          //初始化加载
          window.onload = function(){
            var snowBox = 'container',//雪花容器
              src = './snow.png',//雪花图基本命名<图片名就是snow+1/2/3/4...>
              num = 28,//雪花数量
              style = 2;//图片种类数
            goSnow(snowBox,src,num,style);
          };
        </script></body></html>"""
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
    'top: 5%;left: 420px;width: 225px;}#second{top: 15%;left: 0px;'\
    'width: 240px;}#thired{top: 20%;left: 870px;width: 260px;}#second li{'\
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
    content = ld.draw()
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
    '<img style="height:60px;opacity:0.6" src="/btn-back.png" alt=""></a>'\
    '</div><div id="entryTitle"><ul>'
    if content:
        price = list(content.keys())[0]
        body += '{}等奖中奖结果：'.format({1: "一", 2: "二", 3: "三"}[price])
        body += '</ul></div><div id="entryList">'
        for i in content[price]:
            body += '<ul><li>---</li></ul>'
        body += '</div><div id="btnContinue"  class="btn"><a href="/draw">'\
        '<img style="height:200px" src="/btn-redraw.png" alt=""></a>'\
        '<a>'\
        '<img style="height:200px" src="/btn-stop.png" alt=""></a></div>'
        # 总名单
        body += '''
        <script type="text/javascript">
                    //定义一个数组变量存放几个数据，一个定时器，一个标识变量
                    var data = ['''
        for i in ld.emplist:
            body += '"' + i[0] + '",'
        body = body[:-1]
        body += '''];
        var timer = null;
        var flag = 0;
        //函数开始

        function shuffle(arr) {
            var length = arr.length,
                randomIndex,
                temp;
            while (length) {
                randomIndex = Math.floor(Math.random() * (length--));
                temp = arr[randomIndex];
                arr[randomIndex] = arr[length];
                arr[length] = temp
            }
            return arr;
        }

        function render(list) {
            var oTitle = document.getElementById("entryList")
            for (var i = 0; i < list.length; i++) {
                oTitle.children[i].innerText = list[i]
                oTitle.children[i].style.fontSize = '38px'
                oTitle.children[i].style.color = '#ff344c'
            }
        }

        function fnplay(num) {
            //var that=this;//这里指的是begin这个按钮 这里暂时不考虑这个。
            //每个开始之前关闭一下定时器，不然每次按click的时候容易加快速度，以至于整个浏览器容易奔溃
            //定义一个定时器
            timer = setInterval(function () {
                //Math.random()拿到的是0-1之前的数字，去乘数组的长度 再取整数可以拿到想要的数组下标
                //floor去取整
                //把拿到的数组的值写进去
                shuffle(data)
                render(data.slice(0, num))
                // oTitle.innerHTML=data[random];
            }, 60);
            //按开始之后，让颜色改变一下
        }
        window.onload = function () {
            fnplay(''' + str(len(content[price])) + ''')
        //开始抽奖
        var begin = document.getElementById('btnContinue').children[0];
        var stop = document.getElementById('btnContinue').children[1];
        begin.style.display = "none"
        stop.style.display = "block"

        stop.addEventListener("click", function (event) {
            event.preventDefault();
            render(['''
        # 抽奖名单
        for i in content[price]:
            body += '"' + i[0] + '",'
        body = body[:-1]
        body += '''])
        clearInterval(timer)
        begin.style.display = "block"
        stop.style.display = "none"
    }, false);
}
</script></body></html>'''
    else:
        body += '<div style="position: fixed;top:40%;left:36%;color:#ff344c;'\
        'line-height:200%;text-align: center;">抽奖已经结束！<br>'\
        '所有大奖都名花有主了哦！<br>恭喜中奖的亲们！</div></ul></div><div '\
        'id="btnContinue" class="btn"><a href="/result"><img style='\
        '"position:fixed;height:80px;bottom:10%;left:44%;" src="/btn-view.png"'\
        ' alt=""></a></div></body></html>'
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
    with open(os.path.dirname(os.path.realpath(__file__)) + os.sep + "img" + os.sep + filename, 'rb') as f:
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

def btn_stop():
    return img("btn-stop.gif")

def snow1():
    return img("snow1.png")

def snow2():
    return img("snow2.png")

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
        '/btn-stop.png': btn_stop,
        '/btn-redraw.png': btn_redraw,
        '/btn-back.png': btn_back,
        '/snow1.png':snow1,
        '/snow2.png':snow2,
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
