import os 
from os import path
import re
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath) 
def scaner_file (url):
    num = 0
    file  = os.listdir(url)
    for f in file:
        if f[:3] == "job" and f[-4:] == ".odb":
            temp = int(f[3:-4])
            if num < temp:
                num = temp
    return num
 
# #调用自定义函数
# scaner_file(thisDir) 
# print(thisDir)
scaner_file("\\".join(r"H:\IJF Reliability\material\CAE\ODB\job1.odb".split("\\")[:-1]))

