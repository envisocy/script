### 程序更新

- Ver_04 12-23-2017 添加echo函数，完善接口；
- Ver_03 12-19-2017 修改完善数据结构，统一读写方式；
- Ver_02 11-26-2017 确定整体的框架和储存加密模式；
- Ver_01 11-21-2017 正式确定整合数据库及数据文件配置信息并统一管理；

By envisocy

### 基础框架

管理系统内所有可以连通的数据源的连接信息：

返回的信息格式为：
调用名称：Name：{
    显示别名: 'alias':
    备注信息: 'remark':
    数据源类型: 'style':
    具体参数类型： 'config':{}
    修改时间： 'date':
    }

支持的数据源类型：
数据文件：csv文档
数据库：Mysql
数据库：MongoDB (待下个版本支持)

配置信息目录：

./DatafileConfig/...

> 自动索引该目录列表下所有支持的数据文件配置信息


./DatabaseConfig/...

> 自动索引该目录列表下所有支持的数据库配置信息


### 使用框架

#### 获取库内SQL信息

'''
>>> import configure
>>> configure.sql_msg
{'localhost': {'alias': 'localhost',
  'config': {'charset': 'utf8',
   'db': 'mysql',
   'host': '127.0.0.1',
   'passwd': '123456',
   'port': 3306,
   'user': 'root'},
  'date': '2017-12-23 15:00:00',
  'remark': 'None',
  'style': 'mysql'}}
'''

#### 库内文档配置文件

'''
>>> import configure
>>> configure.config.search_dirs

['DatabaseConfig', 'DatafileConfig']
'''

#### 读取特定文件

'''
>>> import configure
>>> prp = configure.prpcrypt.prpcrypt()
>>> prp.read_file("C:\\Users\\Administrator\\Desktop\\","localhost.txt")
### 参数
#- 路径 path，默认为空
#- 文件名 filename，默认为default.txt
"There's no file exists."
'''

#### 写入特定文件

'''
>>> import configure
>>> text = "{'alias': 'localhost','config': {'charset': 'utf8','db': 'mysql',\
'host': '127.0.0.1','passwd': '123456','port': 3306,'user': 'root'},'date': \
'2017-12-23 15:00:00','remark': 'None','style': 'mysql'}"
>>> prp = configure.prpcrypt.prpcrypt()
>>> prp.write_file(text,"C:\\Users\\Administrator\\Desktop\\","localhost.txt")
### 参数
#- 文本 text
#- 路径 path，默认为空
#- 文件名 filename，默认为default.txt
'''
