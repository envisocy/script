from utils import log

from models.todo import Todo
from models.user import User
from routes import current_user

def template(name):
    path = "/templates/" + name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def response_with_header(headers, code=200, desc="Test OK"):
    header = "HTTP/1.1 {} {}\r\n".format(code, desc)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header

def redirect(url):
    '''
    302: 重定向
    '''
    headers = {
        "Location": url,
    }
    r = response_with_header(headers, 302, "Redirect OK") + '\r\n'
    return r.encode('utf-8')

def index(request):
    '''
    todo 首页
    '''
    headers = {
        "Content": "text/html"
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        log("***** 未登录 跳转")
        return redirect('/')
    todo_list = Todo.find_all(user_id=u.id)
    todo_html = ''.join(['<h3>{} : {}</h3>'.format(t.id, t.title)
                         for t in todo_list])
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_header(headers)
    r = headers + "\r\n" + body
    return r.encode(encoding="utf-8")

def edit(request):
    pass

def add(request):
    '''
    处理POST后 todo 的路由函数
    '''
    headers = {
        "Content": "text/html",
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == "POST":
        '''
        Body:
        'title=aaa'
        -> {'title': 'aaa'}
        '''
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()    # 任务完成
    return redirect('/todo')

def update(request):
    pass

def delete_todo(request):
    pass

route_dict = {
    '/todo': index,
    '/todo/add': add,
}
