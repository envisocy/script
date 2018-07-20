import sys
import os

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

DESKTOP_DIR = ""

if not DESKTOP_DIR:
    DESKTOP_DIR = GetDesktopPath()

if "win" in sys.platform:
    DESKTOP = DESKTOP_DIR
elif "linux" in sys.platform:
    DESKTOP = "~/Downloads"

SQL_LIST = ["localhost", "xiaobaods_w"]

MODE3_PERMIT = ["牛仔裤", "休闲裤", "打底裤", "半身裙"]

MODE4_PERMIT = {
    "牛仔裤": {
        '哈伦裤': "款式",
        '阔脚裤': "款式",
        '铅笔裤': "款式",
        '连衣裤': "款式",
        '背带裤': "款式",
        '直筒': "款式",
        '灯笼裤': "款式",
        '微喇裤': "款式",
        '工装裤': "款式",
        '垮裤': "款式",
        '长裤': "裤长",
        '超短裤': "裤长",
        '短裤': "裤长",
        '五分裤': "裤长",
        '九分裤': "裤长",
        '七分裤': "裤长",
        '高腰': "腰型",
        '低腰': "腰型",
        '中腰': "腰型",
        '超薄': "厚薄",
        '薄款': "厚薄",
        '常规': "厚薄",
        '加厚': "厚薄"},
    "打底裤": {
        '薄款': "厚薄",
        '常规': "厚薄",
        '加绒': "厚薄",
        '加厚': "厚薄",
        '长裤': "裤长",
        '短裤': "裤长",
        '七分裤/九分裤': "裤长"}}
