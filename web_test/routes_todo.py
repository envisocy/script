from utils import log

from models.todo import Todo
from models.user import User
from routes import current_user

def template(name):
    path = "templates/" + name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def response_with_header(headers, code=200, desc="Test OK"):
    header = "HTTP/1.1 {} {}\r\n".format(code, desc)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header

def redirect(url):
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
        "Content": "text/html",
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        log("** ERROR ** 未登录 跳转")
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    todo_html = ''.join(['<h3>{0}(user_id: {1}): {2} <a href='\
                         '"/todo/edit?id={0}">编辑</a> <a href='\
                         '"/todo/delete?id={0}">删除</a></h3>'.
                         format(t.id, t.user_id, t.title, ) for t in todo_list])
    if not todo_html:
        todo_html = '<br><b3>暂无TODO记录！</b3>'
    body = template('todo_index.html')
    body = body.replace('{{username}}', u.username)
    body = body.replace('{{todos}}', todo_html)
    header = response_with_header(headers)
    r = header + "\r\n" + body
    return r.encode(encoding="utf-8")

def edit(request):
    '''
    todo 修改页面
    '''
    headers = {
        "Content": "text/html",
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        log("** ERROR ** 未登录 跳转")
        return redirect('/login')
    # 得到当前编辑的 todo 的 id
    todo_id = int(request.query.get("id", -1))
    if todo_id < 1:
        return redirect("/todo")
    t = Todo.find_by(id=todo_id)
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', t.title)
    body = body.replace('{{username}}', u.username)
    header = response_with_header(headers)
    r = header + "\r\n" + body
    return r.encode(encoding="utf-8")

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
    '''
    处理POST后 /todo/edit 的路由函数
    '''
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == "POST":
        '''
        Body:
        'title=aaa&id=1'
        '''
        form = request.form()
        todo_id = int(form.get('id', '-1'))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()    # 任务完成
    return redirect('/todo')

def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    todo_id = request.query.get("id", "-1")
    t = Todo.find_by(id=todo_id)
    if t is not None:
        t.remove()
    return redirect("/todo")

route_dict = {
    '/todo': index,
    '/todo/edit': edit,
    # POST请求，处理数据
    '/todo/add': add,
    '/todo/update': update,
    '/todo/delete': delete_todo,
}
