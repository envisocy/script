from jst.apis.base_services import BaseService
from jst.config import Config
import configure

def run(mode="shops.query", msg=False, file_name="jst_private", sandbox=False, **kwargs):
	env = {
		'sandbox': sandbox, # 是否为沙盒环境
        'partner_id': configure.echo(file_name)["config"]["partner_id"],
		'partner_key': configure.echo(file_name)["config"]["partner_key"],
		'token': configure.echo(file_name)["config"]["token"],
		'taobao_appkey': configure.echo(file_name)["config"]["taobao_appkey"],
		'taobao_secret': configure.echo(file_name)["config"]["taobao_secret"],
	}
	params = {
        'shop_id': '10127848',
        'modified_begin': '2018-04-18 00:00:00',
        'modified_end': '2018-04-19 00:00:00',
        'page_size': 10,
        'page_index': 1,
        # 'so_ids': ['111902591572215654']
    }
	if msg:
		print("mode:<{}>\nfile_name:<{}>\nmsg:<{}>\nsandbox:<{}>\nkwargs:<{}>".format(mode, file_name, msg, sandbox, kwargs))
	params.update(kwargs)
	cfg = Config(**env)     # 配置参数
	service = BaseService(cfg, msg)      # 运行服务
	return service.run(mode, params)
