### 聚水潭标准接口

---
- 更新时间: 2018-04-19
- 支持: 聚水潭技术中心
- 文档: 宝儿电商-数据组-王志平
---

#### 通过导入包方式引用
```python
>>> import jst
>>> jst.run("sku.query", False, page_size=10)
{'code': 0,
 'data_count': 1038,
 'datas': [{'brand': None,
   'c_id': 1623,
   'category': '半身裙',
   'color': None,
   'cost_price': 36.0,
   'enabled': 1,
   'i_id': '阿海9959',
   'market_price': None,
   'modified': '2018-04-18 08:40:59',
   'name': '牛仔短裙;排扣对称双贴袋牛仔裙',
   'pic': 'https://img.alicdn.com/bao/uploaded/i1/2870092769/TB28SmKc9tYBeNjSspkXXbU8VXa_!!2870092769.jpg_30x30.jpg',
   'pic_big': 'https://img.alicdn.com/bao/uploaded/i1/2870092769/TB28SmKc9tYBeNjSspkXXbU8VXa_!!2870092769.jpg',
   'properties_name': None,
   'properties_value': '白色;L',
   'sale_price': None,
   'short_name': None,
   'sku_code': '0239959000603',
   'sku_id': 'AHI9959BABA0L',
   'sku_type': 'normal',
   'supplier_i_id': '9959',
   'supplier_id': 531288,
   'supplier_name': '阿海',
   'supplier_sku_id': None,
   'vc_name': '2018工厂图',
   'weight': None},
  {'brand': None,
   'c_id': 1623,
   'category': '半身裙',
   'color': None,
   'cost_price': 36.0,
   'enabled': 1,
   'i_id': '阿海9959',
   'market_price': None,
   'modified': '2018-04-18 08:40:59',
   'name': '牛仔短裙;排扣对称双贴袋牛仔裙',
   'pic': 'https://img.alicdn.com/bao/uploaded/i1/2870092769/TB28SmKc9tYBeNjSspkXXbU8VXa_!!2870092769.jpg_30x30.jpg',
   'pic_big': 'https://img.alicdn.com/bao/uploaded/i1/2870092769/TB28SmKc9tYBeNjSspkXXbU8VXa_!!2870092769.jpg',
   'properties_name': None,
   'properties_value': '白色;M',
   'sale_price': None,
   'short_name': None,
   'sku_code': '0239959000602',
   'sku_id': 'AHI9959BABA0M',
   'sku_type': 'normal',
   'supplier_i_id': '9959',
   'supplier_id': 531288,
   'supplier_name': '阿海',
   'supplier_sku_id': None,
   'vc_name': '2018工厂图',
   'weight': None}],
 'has_next': True,
 'issuccess': True,
 'msg': None,
 'page_count': 519,
 'page_index': 1,
 'page_size': 2}
```

