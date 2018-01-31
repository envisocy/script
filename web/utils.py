import time


def log(*args, **kwargs):
    # 在代码中使用 log() 替代 print() 作为后端终端的信息输出函数
    # time.time() 返回 Unix time
    # 返回str格式化时间 time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(int(time.time())))
    dt = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(int(time.time())))
    print(dt, *args, **kwargs)
