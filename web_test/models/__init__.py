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
    从文件中载入数据并转化为 dict 或 list
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
        '''
        通过调用cls.__name__返回MVC中的数据文档路径
        '''
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
        if self.__dict__.get('id') is None:
            # 添加id
            if len(models) > 0:
                # 不是第一条数据
                self.id = models[-1].id + 1
            else:
                # 第一条数据
                self.id = 1
            models.append(self)
        else:
            # 有id说明已经存在于数据文件中的数据
            # 那么就找到这条数据替换掉
            # 这里需要得到下标，所以使用enumerate()
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            # 看看是否找到下标
            # 如果找到就替换掉这条数据
        # __dict__包含了对象所有属性和值得字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        log("***", l)
        save(l, path)

    @classmethod
    def find_by(cls, **kwargs):
        '''
        kwargs 是只有一个元素的dict
        如：u = User.find_by(username='gua')
        查找对应的db/User.txt 是否有 username 为 gua 的值
        '''
        log('kwargs: ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k , v = key, value
        for m in cls.all():
            if v == m.__dict__[k]:
                # 和 getattr(m, k) 等价
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        '''
        '''
        log('kwargs: ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k , v = key, value
        all = cls.all()
        data = []
        for m in all:
            if v == m.__dict__[k]:
                # 和 getattr(m, k) 等价
                data.append(m)
        return data

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
