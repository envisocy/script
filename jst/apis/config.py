MODE = {
	'shops.query': ["modified_begin", "modified_end",],  # 基础 - 店铺查询
	'logisticscompany.query': ["modified_begin", "modified_end",],   # 基础 - 物流公司查询
	'wms.partner.query': [], # 基础 - 分仓查询
	'auth.shop.generate.query': [], # 基础 - 获取淘宝授权地址
	'item.upload': ["shop_id", "i_id", "shop_i_id", "name", "sale_price", "enabled", "brand_name", "market_price",
	                "skus",],   # 商品 - 普通商品上传(更改库存)
	'mall.item.upload': ["c_name", "i_id", "sku_id", "name", "properties_value", "sku_code", "s_price",
	                     "market_price", "c_price", "weight", "supplier_name", "supplier_i_id",
	                     "remark", "brand", "pic", "sku_pic"],  # 商品 - 商品维护上传(商品信息)
	'sku.query': ["modified_begin", "modified_end", "sku_ids"], # 商品 - 普通商品查询
	'sku.source.query': ["shop_id", "modified_begin", "modified_end", "num_iids", "status"], # 商品 - 平台商品查询
	'skumap.query': ["modified_begin", "modified_end",],    # 商品 - 商品映射查询
	'inventory.query': ["modified_begin", "modified_end", "sku_ids"],   # 库存 - 库存查询
	'inventory.count.query': ["modified_begin", "modified_end", "io_ids", "status"],    # 库存 - 库存盘点查询
	'jst.orders.query': ["shop_id", "so_ids", "modified_begin", "modified_end", "status",],  # 订单 - 订单查询(奇门)
	'jst.orders.source.query': ["shop_id", "modified_begin", "modified_end", "so_ids", "status",], # 订单 - 订单源数据查询(奇门)
	'order.action.query': ["modified_begin", "modified_end", "so_ids"], # 订单 - 订单操作日志查询
	'logistic.query': ["shop_id", "modified_begin", "modified_end", "so_ids"], # 物流 - 发货信息查询
	'purchase.query': ["modified_begin", "modified_end", "so_ids"], # 采购 - 采购单查询
	'supplier.query': ["shop_id", "modified_begin", "modified_end",], # 采购 - 供应商查询
	'purchasein.query': ["modified_begin", "modified_end", "po_ids"], # 入库 - 采购进仓查询
	'jst.orders.out.query': ["modified_begin", "modified_end", "so_ids"],  # 出库 - 出库查询(奇门)
	'jst.orders.out.skusn.query': ["modified_begin", "modified_end", "so_ids"],    # 出库 - 出库唯一码查询(奇门)
	'purchaseout.query': ["modified_begin", "modified_end",],    # 出库 - 采购退货查询
	'jst.refund.query': ["modified_begin", "modified_end", "so_ids", "shop_buyer_ids"], # 售后API - 退货退款查询(奇门)
	'aftersale.received.query': ["modified_begin", "modified_end", "so_ids", "o_ids"],  # 售后API - 实际收货查询
	'worklog.query': ["modified_begin", "modified_end",],   # 操作日志 - 操作查询
	'other.inout.query': ["modified_begin", "modified_end", "so_ids"],  # 其他出入库API - 其他出入库查询
	'allocate.query': ["modified_begin", "modified_end"],   # 调拨API - 调拨单查询
}

for i in MODE.values():
	i.extend(["page_index", "page_size",])