from unicodedata import name
from MathTools.sample import sample
from MathTools.scipy.stats import norm
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

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


def modelfunc(modelName, materialName, LHSindex, Distribution, Densityindex, 
                Densitytable, Elasticindex, Elastictable, Plasticindex, Plastictable, 
                Creepindex, Creeptable, Fatigue, Fatiguetable, Creepmodelindex, 
                TFtable, DEtable, MSEDEtable, Jobnum, CPUnum, datafile_name):
# **************************************Sample****************************************************
    datafile_name += '.csv'
    namels = []
    datals = []
    if Densityindex == True : 
        Density_arr = np.zeros([len(Densitytable), Jobnum])
        for num, i in enumerate(Densitytable):
            Density_arr[:][num] = sample(Jobnum, i[0], i[1], Distribution, LHSindex)
            namels.append('Density at {}C'.format(i[2]))
        datals.append(Density_arr)
    if Elasticindex == True : 
        Elastic_arr = np.zeros([len(Elastictable), Jobnum])
        for num, i in enumerate(Elastictable):
            Elastic_arr[:][num] = sample(Jobnum, i[0], i[1], Distribution, LHSindex)
            namels.append('E at {}C'.format(i[2]))
        datals.append(Elastic_arr)
    if Plasticindex == True : 
        Plastic_arr = np.zeros([len(Plastictable), 3, Jobnum])
        for num, i in enumerate(Plastictable):
            for j in range(3):
                Plastic_arr[:][num][j] = sample(Jobnum, i[j*2+1], i[7], Distribution, LHSindex)
            namels.extend(['C1 at {}C'.format(i[8]), 
                           'C2 at {}C'.format(i[8]), 
                           'C3 at {}C'.format(i[8])])
        Plastic_arr = np.reshape(Plastic_arr, (len(Plastictable)*3, Jobnum))
        datals.append(Plastic_arr)
    if Creepindex == True : 
        Creep_arr = np.zeros([len(Creeptable), Jobnum])
        for num, i in enumerate(Creeptable):
            Creep_arr[:][num] = sample(Jobnum, i[0], i[3], Distribution, LHSindex)
            namels.append('Creep Power Law Multiplier at {}C'.format(i[4]))
        datals.append(Creep_arr)
    data = np.vstack(datals)
    data = data.T
    
    with open(datafile_name, 'wb') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(namels)
        for i in data :
            writer.writerow(i)
# ************************************************************************************************
# ******************************damage subroutine******************************************************
    myfor = "{}-{}.for".format(Fatigue, Creepmodelindex)
    with open(os.path.join(os.getcwd(), "abaqus_plugins\Reliability Analysis\data\{}".format(myfor)), 'r') as myuvarm:
                flist = myuvarm.readlines()
                flist[111] = '      Xsigma=%.4f\n' % Fatiguetable[0][0]
                flist[112] = '      Xepsilon=%.4f\n' % Fatiguetable[0][1]
                flist[113] = '      b0=%.4f\n' % Fatiguetable[0][2]
                flist[114] = '      c0=%.4f\n' % Fatiguetable[0][3]
                if Creepmodelindex == "MSEDE":
                    flist[105] = '      fai=%.4f\n' % MSEDEtable[0][0]
                    flist[106] = '      temp_n1=%.4f\n' % MSEDEtable[0][1]
                    flist[107] = '      wfcrit=%.4f\n' % MSEDEtable[0][2]
                if Creepmodelindex == "DE":
                    flist[102] = '      D=%.4f\n' % DEtable[0][0]
                    flist[103] = '      beta=%.4f\n' % DEtable[0][1]
                if Creepmodelindex == "TF":
                    flist[109] = '      TFK=%.4f\n' % TFtable[0][0]
                    flist[110] = '      TFA=-%.4f\n' % TFtable[0][1]    
    with open(myfor, 'w') as newuvarm:
        newuvarm.writelines(flist)
# ************************************************************************************************
# *************************************modelparameter*************************************************
    Density = np.array(Densitytable)
    Elastic = np.array(Elastictable)
    Plastic = np.array(Plastictable)
    Creep = np.array(Creeptable)
    Density = np.delete(Density, 1,axis=1)
    Elastic = np.delete(Elastic, 1,axis=1)
    Plastic = np.delete(Plastic, 7,axis=1)
    Creep = np.delete(Creep, 3,axis=1)
    for i in range(Jobnum):
        if Densityindex == True :
            for j, array in enumerate(Density):
                array[0] = Density_arr[j][i]
            Density = tuple(tuple(i) for i in Density)
            mdb.models[modelName].materials[materialName].Density(temperatureDependency=ON, 
                    table=(Density))
        if Elasticindex == True :
            for j, array in enumerate(Elastic):
                array[0] = Elastic_arr[j][i]
            Elastic = tuple(tuple(i) for i in Elastic)
            mdb.models[modelName].materials[materialName].Elastic(temperatureDependency=ON, 
                    table=(Elastic))
        if Plasticindex == True :
            for j, array in enumerate(Plastic):
                array[1] = Plastic_arr[j*3][i]
                array[3] = Plastic_arr[j*3+1][i]
                array[5] = Plastic_arr[j*3+2][i]
            Plastic = tuple(tuple(i) for i in Plastic)
            mdb.models[modelName].materials[materialName].Plastic(hardening=COMBINED, 
                    dataType=PARAMETERS, numBackstresses=3, temperatureDependency=ON, table=(Plastic))
        if Creepindex == True :
            for j, array in enumerate(Creep):
                array[0] = Creep_arr[j][i]
            Creep = tuple(tuple(i) for i in Creep)
            mdb.models[modelName].materials[materialName].Creep(temperatureDependency=ON, 
                    table=(Creep))
# ************************************************************************************************
# ******************************submitjob****************************************************** 
        mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF,
                explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF,
                memory=90, model=modelName, modelPrint=OFF,
                multiprocessingMode=DEFAULT, name="Job%d"%i, nodalOutputPrecision=FULL,
                numCpus=CPUnum, numDomains=20, numGPUs=0, queue=None, scratch=
                '', userSubroutine=myfor, waitHours=0, waitMinutes=0)
        # write input
        mdb.jobs["Job%d"%i].writeInput(consistencyChecking=OFF)
        # submit

        mdb.jobs["Job%d"%i].submit(consistencyChecking=OFF)
        mdb.jobs["Job%d"%i].waitForCompletion()
# # ************************************************************************************************  
    return 0
