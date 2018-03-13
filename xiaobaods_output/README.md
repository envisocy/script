
## 淘宝综合数据输出程式
#### 宝儿电商数据平台输出
#### 宝儿电商【数据组】
#### 程序：王志平 envisocy

> https://github.com/envisocy

> E-mail: envisocy@qq.com


### 程序更新
- Ver_12 03-13-2018 调用接口的优化，完善调用文档；
- Ver_11 01-19-2018 完成了对w模块的移植；
- Ver_10 01-11-2018 完成了对c模块的移植，调整了相关SQL的索引配置；
- Ver_09 01-10-2018 移植al模块，并测试完毕；完善现有函数的说明；
- Ver_08 01-09-2018 添加pr体系：生成及调用模块；统一加购内函数命名；
- Ver_06 01-05-2018 展示台构架，添加ps和pi模块，针对ERP店铺信息进行输出；
- Ver_05 01-04-2018 修复一些BUG；
- Ver_04 01-03-2018 xiaobaods_a_alg 使用新算法Dec开发的测试版本；
- Ver_03 12-27-2017 xiaobaods_a 对接正式版本，测试完毕；
- Ver_02 12-23-2017 重新调整框架；
- Ver_01 12-19-2017 放弃原有程式，重写输出框架；


### 调用说明

#### 载包调用范例

```
import xiaobaods_output
fun = xiaobaods_output.function()
a.run(fun="a", line_f="20", date="2018-01-01")
```

#### 参数 parameter
- fun 调用的程序类型
	- a(Default) 类目趋势：热销商品趋势分析/流量商品趋势分析
	- al 算法排序，筛选增长率高的宝贝
	- c 类目属性趋势
	- w 行业热词榜
	- ps 面板
	- pi 面板
- debug 数据输出类型
	- None(Default) Json数据形式返回
	- 1 基本的数据参数信息
	- 2 数据库信息
	- 6 内部算法专用序列
	- 7 print数据，数据格式
	- 8 返回数据，数据格式pandas.DataFrame
	- 9 输出到指定路径，数据格式CSV文件
- line_b(Default=0) 起始数据条数
- line_f(Default=20) 结束数据条数
- date(Default今天前一天有数据的日期) 选择的日期，格式"YYYY-MM-DD"
- date_range [算法专有]日期范围
- category(Default="牛仔裤") 类目
- classification(Default="款式") 分类
- attributes(Default="铅笔裤") 二级分类
- length(Default=7) 前溯日期范围，显示其他筛选的时间长度
- table(通常情况无需传参) 数据库指定
- variable(Default="热销排名") 二次筛选需求显示的变量值
- fillna(Default=0) 填充空值的替换
- path(Default为桌面) Debug=9时输出CSV文档的位置
- choice(Default="热搜核心词") [关键词]表单选择