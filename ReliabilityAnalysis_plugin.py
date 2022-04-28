import imp
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import ModelDB, ResultDB
from  ModelDB import modelDB
from ResultDB import resultDB


###########################################################################
# Class definition
###########################################################################

class Model_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='modelfunc',
            objectName='modelfunc', registerQuery=False)
        pickedDefault = ''
        self.modelNameKw = AFXStringKeyword(self.cmd, 'modelName', True)
        self.materialNameKw = AFXStringKeyword(self.cmd, 'materialName', True)
        self.LHSindexKw = AFXBoolKeyword(self.cmd, 'LHSindex', AFXBoolKeyword.TRUE_FALSE, True, False)
        if not self.radioButtonGroups.has_key('Distribution'):
            self.DistributionKw1 = AFXIntKeyword(None, 'DistributionDummy', True)
            self.DistributionKw2 = AFXStringKeyword(self.cmd, 'Distribution', True)
            self.radioButtonGroups['Distribution'] = (self.DistributionKw1, self.DistributionKw2, {})
        self.radioButtonGroups['Distribution'][2][1162] = 'Uniform'
        if not self.radioButtonGroups.has_key('Distribution'):
            self.DistributionKw1 = AFXIntKeyword(None, 'DistributionDummy', True)
            self.DistributionKw2 = AFXStringKeyword(self.cmd, 'Distribution', True)
            self.radioButtonGroups['Distribution'] = (self.DistributionKw1, self.DistributionKw2, {})
        self.radioButtonGroups['Distribution'][2][1163] = 'Normal'
        self.DistributionKw1.setValue(1163)
        self.DensityindexKw = AFXBoolKeyword(self.cmd, 'Densityindex', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.ElasticindexKw = AFXBoolKeyword(self.cmd, 'Elasticindex', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.PlasticindexKw = AFXBoolKeyword(self.cmd, 'Plasticindex', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.CreepindexKw = AFXBoolKeyword(self.cmd, 'Creepindex', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.DensitytableKw = AFXTableKeyword(self.cmd, 'Densitytable', True)
        self.DensitytableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.DensitytableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.DensitytableKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        self.ElastictableKw = AFXTableKeyword(self.cmd, 'Elastictable', True)
        self.ElastictableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.ElastictableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.ElastictableKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw = AFXTableKeyword(self.cmd, 'Plastictable', True)
        self.PlastictableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(4, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(5, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(6, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(7, AFXTABLE_TYPE_FLOAT)
        self.PlastictableKw.setColumnType(8, AFXTABLE_TYPE_FLOAT)
        self.CreeptableKw = AFXTableKeyword(self.cmd, 'Creeptable', True)
        self.CreeptableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.CreeptableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.CreeptableKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        self.CreeptableKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)
        self.CreeptableKw.setColumnType(4, AFXTABLE_TYPE_FLOAT)
        if not self.radioButtonGroups.has_key('Fatigue'):
            self.FatigueKw1 = AFXIntKeyword(None, 'FatigueDummy', True)
            self.FatigueKw2 = AFXStringKeyword(self.cmd, 'Fatigue', True)
            self.radioButtonGroups['Fatigue'] = (self.FatigueKw1, self.FatigueKw2, {})
        self.radioButtonGroups['Fatigue'][2][1164] = 'Equivalent Strain'
        if not self.radioButtonGroups.has_key('Fatigue'):
            self.FatigueKw1 = AFXIntKeyword(None, 'FatigueDummy', True)
            self.FatigueKw2 = AFXStringKeyword(self.cmd, 'Fatigue', True)
            self.radioButtonGroups['Fatigue'] = (self.FatigueKw1, self.FatigueKw2, {})
        self.radioButtonGroups['Fatigue'][2][1165] = 'MGSA'
        self.FatiguetableKw = AFXTableKeyword(self.cmd, 'Fatiguetable', True)
        self.FatiguetableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.FatiguetableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.FatiguetableKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        self.FatiguetableKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)
        if not self.radioButtonGroups.has_key('Creepmodelindex'):
            self.CreepmodelindexKw1 = AFXIntKeyword(None, 'CreepmodelindexDummy', True)
            self.CreepmodelindexKw2 = AFXStringKeyword(self.cmd, 'Creepmodelindex', True)
            self.radioButtonGroups['Creepmodelindex'] = (self.CreepmodelindexKw1, self.CreepmodelindexKw2, {})
        self.radioButtonGroups['Creepmodelindex'][2][1166] = 'TF'
        self.TFtableKw = AFXTableKeyword(self.cmd, 'TFtable', True)
        self.TFtableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.TFtableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        if not self.radioButtonGroups.has_key('Creepmodelindex'):
            self.CreepmodelindexKw1 = AFXIntKeyword(None, 'CreepmodelindexDummy', True)
            self.CreepmodelindexKw2 = AFXStringKeyword(self.cmd, 'Creepmodelindex', True)
            self.radioButtonGroups['Creepmodelindex'] = (self.CreepmodelindexKw1, self.CreepmodelindexKw2, {})
        self.radioButtonGroups['Creepmodelindex'][2][1167] = 'DE'
        self.DEtableKw = AFXTableKeyword(self.cmd, 'DEtable', True)
        self.DEtableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.DEtableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        if not self.radioButtonGroups.has_key('Creepmodelindex'):
            self.CreepmodelindexKw1 = AFXIntKeyword(None, 'CreepmodelindexDummy', True)
            self.CreepmodelindexKw2 = AFXStringKeyword(self.cmd, 'Creepmodelindex', True)
            self.radioButtonGroups['Creepmodelindex'] = (self.CreepmodelindexKw1, self.CreepmodelindexKw2, {})
        self.radioButtonGroups['Creepmodelindex'][2][1168] = 'MSEDE'
        self.MSEDEtableKw = AFXTableKeyword(self.cmd, 'MSEDEtable', True)
        self.MSEDEtableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.MSEDEtableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        self.MSEDEtableKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        self.JobnumKw = AFXIntKeyword(self.cmd, 'Jobnum', True, 1)
        self.CPUnumKw = AFXStringKeyword(self.cmd, 'CPUnum', True, '1')
        self.datafile_nameKw = AFXStringKeyword(self.cmd, 'datafile_name', True, 'sample_data')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        reload(ModelDB)
        return modelDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

###########################################################################
# Class definition
###########################################################################

class Result_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='resultfunc',
            objectName='resultfunc', registerQuery=False)
        pickedDefault = ''
        self.fileNameKw = AFXStringKeyword(self.cmd, 'fileName', True, '')
        self.MaxindexKw = AFXBoolKeyword(self.cmd, 'Maxindex', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.setnameKw = AFXStringKeyword(self.cmd, 'setname', True, 'None')
        self.fatiguedamageKw = AFXBoolKeyword(self.cmd, 'fatiguedamage', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.creepdamageKw = AFXBoolKeyword(self.cmd, 'creepdamage', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.totaldamageKw = AFXBoolKeyword(self.cmd, 'totaldamage', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.othervaraibleKw = AFXStringKeyword(self.cmd, 'othervaraible', True, 'None')
        self.stepKw = AFXStringKeyword(self.cmd, 'step', True, 'None')
        self.frameKw = AFXStringKeyword(self.cmd, 'frame', True, 'None')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        reload(ResultDB)
        return resultDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='ReliabilityAnalysis|Model processing', 
    object=Model_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=afxCreatePNGIcon(os.path.join(thisDir, 'Icon\Sample.png')),
    kernelInitString='import modelfunc',
    applicableModules=ALL,
    version='N/A',
    author='Rogers Tian',
    description='N/A',
    helpUrl='N/A'
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='ReliabilityAnalysis|Result processing', 
    object=Result_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=afxCreatePNGIcon(os.path.join(thisDir, 'Icon\Result.png')), 
    kernelInitString='import resultfunc',
    applicableModules=ALL,
    version='N/A',
    author='Rogers Tian',
    description='N/A',
    helpUrl='N/A'
)
