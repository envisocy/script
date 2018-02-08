import time

def log(*args, **kwargs):
    dt = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime(time.time()))
    print(dt, *args, **kwargs)
