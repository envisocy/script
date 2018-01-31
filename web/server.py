# 调用支援函数
from utils import log

def run(host="", port=3000):
    """
    启用服务器
    """
    log("start at", "{}:{}".format(host, port))

if __name__=='__main__':
    # 生成配置文件并且运行程序
    config = dict(
        host="",
        port=3000,
    )
    run(**config)
