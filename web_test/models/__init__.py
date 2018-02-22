import json

from utils import log

def save(data, path):
    '''
    data 是 dict 或 list
    path 是保存文件的路径
    '''
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, "w+", encoding="utf-8") as f:
        log("save", path, s, data)
        f.write(s)

def load(path):
    '''
    从文件中载入数据病转化为 dict 或 list
    path 是保存文件的路径
    '''
    with open(path, 'r', encoding="utf-8") as f:
        s = f.read()
        log('read', s)
        return json.loads(s)

class Model(object):
    # 储存数据的基类

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = "db/{}.txt".format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        '''
        得到一个类的储存实例
        '''
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        '''
        save 函数用于把一个 Model 的实例保存到文件中
        '''
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__包含了对象所有属性和值得字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        log("***", l)
        save(l, path)

    def __repr__(self):
        '''
        魔法函数
        当调用str(o)时
        实际上调用了o.__str__()
        在没有 __str__ 的时候会调用
        __repr__
        '''
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
