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

class resultDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Reliability Result Output',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            
        sendCommand("import resultfunc")
        sendCommand("reload(resultfunc)")

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        GroupBox_1 = FXGroupBox(p=self, text='ODB file selection', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        l = FXLabel(p=GroupBox_1, text='Please Select the FIRST ODB File in the Folder', opts=JUSTIFY_LEFT)
        l.setFont( getAFXFont(FONT_BOLD) )
        fileHandler = ODBDBFileHandler(form, 'fileName', 'All files (*)')
        fileTextHf = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        AFXTextField(p=fileTextHf, ncols=40, labelText='File name:', tgt=form.fileNameKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
        GroupBox_3 = FXGroupBox(p=self, text='Position to Output', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXCheckButton(p=GroupBox_3, text='Find Max Value in the model', tgt=form.MaxindexKw, sel=0)
        self.setname = AFXTextField(p=GroupBox_3, ncols=12, labelText='SET Name:', tgt=form.setnameKw, sel=0)
        GroupBox_2 = FXGroupBox(p=self, text='Output Variable', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXCheckButton(p=GroupBox_2, text='Fatigue Damage', tgt=form.fatiguedamageKw, sel=0)
        FXCheckButton(p=GroupBox_2, text='Creep Damage', tgt=form.creepdamageKw, sel=0)
        FXCheckButton(p=GroupBox_2, text='Total Damage', tgt=form.totaldamageKw, sel=0)
        GroupBox_4 = FXGroupBox(p=GroupBox_2, text='Other Variables', opts=FRAME_GROOVE)
        HFrame_2 = FXHorizontalFrame(p=GroupBox_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        self.variablename = AFXTextField(p=HFrame_2, ncols=12, labelText='Variables Name:', tgt=form.othervaraibleKw, sel=0)
        m = FXLabel(p=HFrame_2, text='(Separated by commas)', opts=JUSTIFY_LEFT)
        HFrame_1 = FXHorizontalFrame(p=GroupBox_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        self.step = AFXTextField(p=HFrame_1, ncols=12, labelText='Step:', tgt=form.stepKw, sel=0)
        self.frame = AFXTextField(p=HFrame_1, ncols=12, labelText='Frame:', tgt=form.frameKw, sel=0)

###########################################################################
# Class definition
###########################################################################

class ODBDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, ODBDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.odb')
       fileDb.create()
       fileDb.showModal()
