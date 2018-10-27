### 字段长度限定

FIELD_RULE = {
	"co_id": 10,
	"invoice_title": 20,
	"is_cod": 6,
	"l_id": 20,
	"lc_id": 12,
	"logistics_company": 12,
	"o_id": 10,
	"order_from": 20,
	"outer_pay_id": 40,
	"question_desc": 30,
	"question_type": 10,
	"receiver_address": 100,
	"receiver_city": 20,
	"receiver_district": 50,
	"receiver_mobile": 15,
	"receiver_name": 30,
	"receiver_state": 15,
	"remark": 350,
	"shop_buyer_id": 25,
	"shop_id": 8,
	"shop_name": 10,
	"shop_status": 30,
	"so_id": 18,
	"status": 16,
	"type": 4,
	"wms_co_id": 8,
	"buyer_message": 80,
	"receiver_phone": 20,
	"tag": 2,
	"i_id": 10,
	"is_gift": 6,
	"item_status": 20,
	"name": 80,
	"oi_id": 11,
	"outer_oi_id": 20,
	"raw_so_id": 20,
	"refund_id": 20,
	"refund_status": 10,
	"shop_sku_id": 20,
	"sku_id": 30,
	"buyer_account": 40,
	"seller_account": 40,
	"is_order_pay": 6,
	"pay_id": 40,
	"payment": 10,
	"io_id": 10,
	"receiver_country": 10,
	"ioi_id": 10,
	"pic": 150,
	"as_id": 10,
	"good_status": 20,
	"out_as_id": 20,
	"warehouse": 30,
	"asi_id": 10,
	"properties_value": 40,
	"item_type": 10,
	"po_id": 10,
	"purchaser_name": 10,
	"seller": 10,
	"send_address": 100,
	"supplier_id": 10,
	"tax_rate": 10,
	"term": 10,
	"poi_id": 10,
	"supplier_name": 30,
	"seller_id": 10,
	"wh_id": 5,
	"f_status": 20,
	"nick": 20,
	"shop_site": 10,
	"shop_url": 50,
	"short_name": 20,
	"operator": 20,
	"brand": 10,
	"c_id": 10,
	"category": 10,
	"color": 10,
	"pic_big": 150,
	"properties_name": 40,
	"sku_code": 20,
	"sku_type": 10,
	"supplier_i_id": 10,
	"supplier_sku_id": 10,
	"vc_name": 20,
	"weight": 8,
	"freight": 8,
	"sale_price": 12,
	"market_price": 12,
	"cost_price": 12,
}


# 需要处理的数据库名：
BUFFER_SQL_LIST = [
	"bc_attribute_granularity_sales", "bc_attribute_granularity_visitor",
	"bc_brand_granularity_sales", "bc_brand_granularity_visitor",
	"bc_owned_granularity_sales", "bc_owned_granularity_visitor",
	"bc_category_jean_length", "bc_category_jean_style", "bc_category_jean_thick",
	"bc_category_jean_waist", "bc_category_legging_length", "bc_category_legging_thick",
	"bc_searchwords_hotwords", "bc_searchwords_risewords",
]


BUFFER_CHINESE_VARIABLE = ["bc_searchwords_hotwords", "bc_searchwords_risewords",]

SPECIAL_SINGLE_REMARK_LIST = ["掌柜推荐", "送上衣", "小仙女", "送扇子", "店铺主款", "加油必胜"]