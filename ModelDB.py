from imp import reload
from abaqusConstants import *
from abaqusGui import *
from abaqusGui import sendCommand
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class modelDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Material Reliability Modeling',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        
        sendCommand("import modelfunc")
        sendCommand("reload(modelfunc)")
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        frame = FXHorizontalFrame(self, 0, 0,0,0,0, 0,0,0,0)

        # Model combo
        # Since all forms will be canceled if the  model changes,
        # we do not need to register a query on the model.
        #
        self.RootComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Model:', tgt=form.modelNameKw, sel=0)
        self.RootComboBox_1.setMaxVisible(10)

        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_1.appendItem(name)
        if not form.modelNameKw.getValue() in names:
            form.modelNameKw.setValue( names[0] )
        msgCount = 368
        form.modelNameKw.setTarget(self)
        form.modelNameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_1MaterialsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )

        # Materials combo
        #
        self.ComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Material:', tgt=form.materialNameKw, sel=0)
        self.ComboBox_1.setMaxVisible(10)

        self.form = form
        GroupBox_1 = FXGroupBox(p=self, text='Distribution & Sample', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXCheckButton(p=GroupBox_1, text='Latin Hypercube Sampling', tgt=form.LHSindexKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=GroupBox_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_2 = FXGroupBox(p=HFrame_1, text='', opts=FRAME_GROOVE)
        HFrame_2 = FXHorizontalFrame(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=HFrame_2, text='Uniform', tgt=form.DistributionKw1, sel=1162)
        fileName = os.path.join(thisDir, r'icon\junyun1.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_2, text='', ic=icon)
        GroupBox_3 = FXGroupBox(p=HFrame_1, text='', opts=FRAME_GROOVE)
        HFrame_5 = FXHorizontalFrame(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=HFrame_5, text='Normal', tgt=form.DistributionKw1, sel=1163)
        fileName = os.path.join(thisDir, r'icon\normal1.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_5, text='', ic=icon)
        TabBook_3 = FXTabBook(p=self, tgt=None, sel=0,
            opts=TABBOOK_NORMAL|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_3, text='Material Parameters', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_8 = FXVerticalFrame(p=TabBook_3,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_6 = FXHorizontalFrame(p=TabItem_8, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXCheckButton(p=HFrame_6, text='Density', tgt=form.DensityindexKw, sel=0)
        FXCheckButton(p=HFrame_6, text='Elastic', tgt=form.ElasticindexKw, sel=0)
        FXCheckButton(p=HFrame_6, text='Plastic', tgt=form.PlasticindexKw, sel=0)
        FXCheckButton(p=HFrame_6, text='Creep', tgt=form.CreepindexKw, sel=0)
        TabBook_2 = FXTabBook(p=TabItem_8, tgt=None, sel=0,
            opts=TABBOOK_NORMAL|LAYOUT_FILL_X|LAYOUT_FILL_Y,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        self.Density = FXTabItem(p=TabBook_2, text='Density', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_3 = FXVerticalFrame(p=TabBook_2,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vf = FXVerticalFrame(TabItem_3, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.Densitytable = AFXTable(vf, 4, 4, 4, 4, form.DensitytableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.Densitytable.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE)
        self.Densitytable.setLeadingRows(1)
        self.Densitytable.setLeadingColumns(1)
        self.Densitytable.setColumnWidth(1, 100)
        self.Densitytable.setColumnType(1, AFXTable.FLOAT)
        self.Densitytable.setColumnWidth(2, 100)
        self.Densitytable.setColumnType(2, AFXTable.FLOAT)
        self.Densitytable.setColumnWidth(3, 100)
        self.Densitytable.setColumnType(3, AFXTable.FLOAT)
        self.Densitytable.setLeadingRowLabels('Density\tCov\tTEMP')
        self.Densitytable.setStretchableColumn( self.Densitytable.getNumColumns()-1 )
        self.Densitytable.showHorizontalGrid(True)
        self.Densitytable.showVerticalGrid(True)
        self.Elastic = FXTabItem(p=TabBook_2, text='Elastic', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_4 = FXVerticalFrame(p=TabBook_2,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vf = FXVerticalFrame(TabItem_4, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.Elastictable = AFXTable(vf, 4, 4, 4, 4, form.ElastictableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.Elastictable.setLeadingRows(1)
        self.Elastictable.setLeadingColumns(1)
        self.Elastictable.setColumnWidth(1, 100)
        self.Elastictable.setColumnType(1, AFXTable.FLOAT)
        self.Elastictable.setColumnWidth(2, 100)
        self.Elastictable.setColumnType(2, AFXTable.FLOAT)
        self.Elastictable.setColumnWidth(3, 100)
        self.Elastictable.setColumnType(3, AFXTable.FLOAT)
        self.Elastictable.setLeadingRowLabels('Young module\tCov\tTEMP')
        self.Elastictable.setStretchableColumn( self.Elastictable.getNumColumns()-1 )
        self.Elastictable.showHorizontalGrid(True)
        self.Elastictable.showVerticalGrid(True)
        self.Plastic = FXTabItem(p=TabBook_2, text='Plastic', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_5 = FXVerticalFrame(p=TabBook_2,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vf = FXVerticalFrame(TabItem_5, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.Plastictable = AFXTable(vf, 4, 10, 4, 10, form.PlastictableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.Plastictable.setLeadingRows(1)
        self.Plastictable.setLeadingColumns(1)
        self.Plastictable.setColumnWidth(1, 100)
        self.Plastictable.setColumnType(1, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(2, 100)
        self.Plastictable.setColumnType(2, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(3, 100)
        self.Plastictable.setColumnType(3, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(4, 100)
        self.Plastictable.setColumnType(4, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(5, 100)
        self.Plastictable.setColumnType(5, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(6, 100)
        self.Plastictable.setColumnType(6, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(7, 100)
        self.Plastictable.setColumnType(7, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(8, 100)
        self.Plastictable.setColumnType(8, AFXTable.FLOAT)
        self.Plastictable.setColumnWidth(9, 100)
        self.Plastictable.setColumnType(9, AFXTable.FLOAT)
        self.Plastictable.setLeadingRowLabels('Yield Stress\tC1\tGamma1\tC2\tGamma2\tC3\tGamma3\tCov\tTEMP')
        self.Plastictable.setStretchableColumn( self.Plastictable.getNumColumns()-1 )
        self.Plastictable.showHorizontalGrid(True)
        self.Plastictable.showVerticalGrid(True)
        self.Creep = FXTabItem(p=TabBook_2, text='Creep', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_6 = FXVerticalFrame(p=TabBook_2,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vf = FXVerticalFrame(TabItem_6, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.Creeptable = AFXTable(vf, 4, 6, 4, 6, form.CreeptableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.Creeptable.setLeadingRows(1)
        self.Creeptable.setLeadingColumns(1)
        self.Creeptable.setColumnWidth(1, 100)
        self.Creeptable.setColumnType(1, AFXTable.FLOAT)
        self.Creeptable.setColumnWidth(2, 100)
        self.Creeptable.setColumnType(2, AFXTable.FLOAT)
        self.Creeptable.setColumnWidth(3, 100)
        self.Creeptable.setColumnType(3, AFXTable.FLOAT)
        self.Creeptable.setColumnWidth(4, 100)
        self.Creeptable.setColumnType(4, AFXTable.FLOAT)
        self.Creeptable.setColumnWidth(5, 100)
        self.Creeptable.setColumnType(5, AFXTable.FLOAT)
        self.Creeptable.setLeadingRowLabels('Power Law Multiplier\tEq Stress Order\tTime Order\tCov\tTEMP')
        self.Creeptable.setStretchableColumn( self.Creeptable.getNumColumns()-1 )
        self.Creeptable.showHorizontalGrid(True)
        self.Creeptable.showVerticalGrid(True)
        tabItem = FXTabItem(p=TabBook_3, text='Damage Models', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_9 = FXVerticalFrame(p=TabBook_3,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        GroupBox_5 = FXGroupBox(p=TabItem_9, text='Fatigue Damage Models', opts=FRAME_GROOVE)
        HFrame_7 = FXHorizontalFrame(p=GroupBox_5, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_7 = FXGroupBox(p=HFrame_7, text='', opts=FRAME_GROOVE)
        VFrame_1 = FXVerticalFrame(p=GroupBox_7, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=VFrame_1, text='Equivalent Strain', tgt=form.FatigueKw1, sel=1164)
        fileName = os.path.join(thisDir, r'icon\ES.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=VFrame_1, text='', ic=icon)
        GroupBox_8 = FXGroupBox(p=HFrame_7, text='', opts=FRAME_GROOVE)
        VFrame_2 = FXVerticalFrame(p=GroupBox_8, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=VFrame_2, text='MGSA', tgt=form.FatigueKw1, sel=1165)
        fileName = os.path.join(thisDir, r'icon\MGSA.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=VFrame_2, text='', ic=icon)
        GroupBox_9 = FXGroupBox(p=HFrame_7, text='', opts=FRAME_GROOVE)
        VFrame_3 = FXVerticalFrame(p=GroupBox_9, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        fileName = os.path.join(thisDir, r'icon\MC.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=VFrame_3, text='', ic=icon)
        vf = FXVerticalFrame(VFrame_3, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(vf, 2, 5, 2, 5, form.FatiguetableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 100)
        table.setColumnType(1, AFXTable.FLOAT)
        table.setColumnWidth(2, 100)
        table.setColumnType(2, AFXTable.FLOAT)
        table.setColumnWidth(3, 100)
        table.setColumnType(3, AFXTable.FLOAT)
        table.setColumnWidth(4, 100)
        table.setColumnType(4, AFXTable.FLOAT)
        table.setLeadingRowLabels('sigmaf\tepsilonf\tb\tc')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)
        GroupBox_6 = FXGroupBox(p=TabItem_9, text='Creep Damage Models', opts=FRAME_GROOVE)
        HFrame_8 = FXHorizontalFrame(p=GroupBox_6, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_10 = FXGroupBox(p=HFrame_8, text='', opts=FRAME_GROOVE)
        VFrame_4 = FXVerticalFrame(p=GroupBox_10, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_9 = FXHorizontalFrame(p=VFrame_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=HFrame_9, text='TF', tgt=form.CreepmodelindexKw1, sel=1166)
        fileName = os.path.join(thisDir, r'icon\TF.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_9, text='', ic=icon)
        vf = FXVerticalFrame(VFrame_4, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.TFtable = AFXTable(vf, 2, 3, 2, 3, form.TFtableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.TFtable.setLeadingRows(1)
        self.TFtable.setLeadingColumns(1)
        self.TFtable.setColumnWidth(1, 100)
        self.TFtable.setColumnType(1, AFXTable.FLOAT)
        self.TFtable.setColumnWidth(2, 100)
        self.TFtable.setColumnType(2, AFXTable.FLOAT)
        self.TFtable.setLeadingRowLabels('k\talpha')
        self.TFtable.setStretchableColumn( self.TFtable.getNumColumns()-1 )
        self.TFtable.showHorizontalGrid(True)
        self.TFtable.showVerticalGrid(True)
        GroupBox_11 = FXGroupBox(p=HFrame_8, text='', opts=FRAME_GROOVE)
        VFrame_5 = FXVerticalFrame(p=GroupBox_11, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_10 = FXHorizontalFrame(p=VFrame_5, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=HFrame_10, text='DE', tgt=form.CreepmodelindexKw1, sel=1167)
        fileName = os.path.join(thisDir, r'icon\DE.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_10, text='', ic=icon)
        vf = FXVerticalFrame(VFrame_5, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.DEtable = AFXTable(vf, 2, 3, 2, 3, form.DEtableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.DEtable.setLeadingRows(1)
        self.DEtable.setLeadingColumns(1)
        self.DEtable.setColumnWidth(1, 100)
        self.DEtable.setColumnType(1, AFXTable.FLOAT)
        self.DEtable.setColumnWidth(2, 100)
        self.DEtable.setColumnType(2, AFXTable.FLOAT)
        self.DEtable.setLeadingRowLabels('d\tbeta')
        self.DEtable.setStretchableColumn( self.DEtable.getNumColumns()-1 )
        self.DEtable.showHorizontalGrid(True)
        self.DEtable.showVerticalGrid(True)
        GroupBox_12 = FXGroupBox(p=HFrame_8, text='', opts=FRAME_GROOVE)
        VFrame_6 = FXVerticalFrame(p=GroupBox_12, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_11 = FXHorizontalFrame(p=VFrame_6, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=HFrame_11, text='MSEDE', tgt=form.CreepmodelindexKw1, sel=1168)
        fileName = os.path.join(thisDir, r'icon\MSEDE.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_11, text='', ic=icon)
        vf = FXVerticalFrame(VFrame_6, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        self.MSEDEtable = AFXTable(vf, 2, 4, 2, 4, form.MSEDEtableKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        self.MSEDEtable.setLeadingRows(1)
        self.MSEDEtable.setLeadingColumns(1)
        self.MSEDEtable.setColumnWidth(1, 100)
        self.MSEDEtable.setColumnType(1, AFXTable.FLOAT)
        self.MSEDEtable.setColumnWidth(2, 100)
        self.MSEDEtable.setColumnType(2, AFXTable.FLOAT)
        self.MSEDEtable.setColumnWidth(3, 100)
        self.MSEDEtable.setColumnType(3, AFXTable.FLOAT)
        self.MSEDEtable.setLeadingRowLabels('phi\tn1\twcrit')
        self.MSEDEtable.setStretchableColumn( self.MSEDEtable.getNumColumns()-1 )
        self.MSEDEtable.showHorizontalGrid(True)
        self.MSEDEtable.showVerticalGrid(True)
        AFXTextField(p=self, ncols=12, labelText='Job nums:', tgt=form.JobnumKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='CPU nums:', tgt=form.CPUnumKw, sel=0)
        AFXTextField(p=self, ncols=12, labelText='Sample file saving name:', tgt=form.datafile_nameKw, sel=0)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)

        # Register a query on materials
        #
        self.currentModelName = getCurrentContext()['modelName']
        self.form.modelNameKw.setValue(self.currentModelName)
        mdb.models[self.currentModelName].materials.registerQuery(self.updateComboBox_1Materials)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentModelName].materials.unregisterQuery(self.updateComboBox_1Materials)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_1MaterialsChanged(self, sender, sel, ptr):

        self.updateComboBox_1Materials()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_1Materials(self):

        modelName = self.form.modelNameKw.getValue()

        # Update the names in the Materials combo
        #
        self.ComboBox_1.clearItems()
        names = mdb.models[modelName].materials.keys()
        names.sort()
        for name in names:
            self.ComboBox_1.appendItem(name)
        if names:
            if not self.form.materialNameKw.getValue() in names:
                self.form.materialNameKw.setValue( names[0] )
        else:
            self.form.materialNameKw.setValue('')

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def processUpdates(self):
        if self.form.DensityindexKw.getValue() == False:
            self.Density.disable()
            self.Densitytable.disable()
        else:
            self.Density.enable()
            self.Densitytable.enable()
        if self.form.ElasticindexKw.getValue() == False:
            self.Elastic.disable()
            self.Elastictable.disable()
        else:
            self.Elastic.enable()
            self.Elastictable.enable()
        if self.form.PlasticindexKw.getValue() == False:
            self.Plastic.disable()
            self.Plastictable.disable()
        else:
            self.Plastic.enable()
            self.Plastictable.enable()
        if self.form.CreepindexKw.getValue() == False:
            self.Creep.disable()
            self.Creeptable.disable()
        else:
            self.Creep.enable()
            self.Creeptable.enable()
        if self.form.CreepmodelindexKw1.getValue() == 1166:
            self.TFtable.enable()
            self.DEtable.disable()
            self.MSEDEtable.disable()
        elif self.form.CreepmodelindexKw1.getValue() == 1167:
            self.DEtable.enable()
            self.TFtable.disable()
            self.MSEDEtable.disable()
        elif self.form.CreepmodelindexKw1.getValue() == 1168:
            self.MSEDEtable.enable()
            self.TFtable.disable()
            self.DEtable.disable()
        return 0

