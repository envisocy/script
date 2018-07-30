### 宝儿电商云系统标准数据写入模块

#### 信息
- 程序：数据组
- 日期：2018-07-24
- 数据库：Mysql

#### 更新文档
- Ver_0.1 Alpha 测试版本
- Ver_0.2 Alpha 四表基础功能版
- Ver_0.21 Alpha 添加属性表功能，添加检测程序
- Ver_0.22 Alpha 修复其他类目BUG
- Ver_0.23 Alpha 添加OWNED列表
- Ver_0.24 Alpha 修复流量表BUG

#### 使用文档
【暂无】

#### 所有链接组成说明
```

宝贝链接：
- https://item.taobao.com/item.htm?id={itemId}

图片链接：
- https://img.alicdn.com/bao/uploaded/{mainPicUrl}.jpg
- _48x48.jpg (可选附加尺寸)
- _80x80.jpg
- _200x200.jpg
- _800x800.jpg

店铺链接
- https:{shopUrl}

生意参谋链接前缀：
- https://sycm.taobao.com/mq/industry/rank/brand.htm?
    spm=a21ag.7749237.0.0.7d79124647cLZN{bsUrl}

1688同款货源前缀：
- https://s.1688.com/youyuan/collaboration_search.htm?
    spm=a21ag.7749237.C_items-table.5.4fe753fd9PXHa2&
    tab=sameDesign&sortType=booked&descendOrder=true&
    autoSimilarTab=true&fromTaobao=true&fromOfferId=
    {1688Url}#topoffer
```