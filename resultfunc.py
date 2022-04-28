from unicodedata import name

from attr import field
from MathTools.resultClass import fieldOutput
import os
import csv
import numpy as np
from part import *
from material import *
from section import *
from optimization import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from odbAccess import *
from abaqusConstants import *

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

def scaner_file(url):
    num = 0
    file  = os.listdir(url)
    for f in file:
        if f[:3] == "job" and f[-4:] == ".odb":
            temp = int(f[3:-3])
            if num < temp:
                num = temp
    return num  


def resultfunc(fileName, Maxindex, setname, fatiguedamage, creepdamage, 
               totaldamage, othervaraible, step, frame):
    dir = "\\".join(fileName.split("\\")[:-1])
    odb_num = scaner_file(dir)
    for i in range(odb_num):
        odbfile = dir + "job%d.odb"%(i+1)
        pass
    return 0 