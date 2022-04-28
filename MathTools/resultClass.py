class fieldOutput(object):
    def __init__(self, odbPath, dataName, setName, step, frame):
        self._odbPath  = odbPath
        self._dataName = dataName.upper() # must be upper-case
        self._setName  = setName.upper()  # must be upper-case
        self._frame = int(frame) # must be int
        self._step = step
        self._odb = openOdb(self._odbPath, readOnly = True)
        return

    def findMaxVar(self):
        frame = self._odb.steps[self._step].frames[self._frame]
        var = frame.fieldOutputs[self._dataName]
        data = var.values
        tmp_val = data[0].data
        tmp_label = data[0].elementLabel
        for v in data:
            if v.data > tmp_val:
                tmp_val = v.data
                tmp_label = v.elementLabel
        return tmp_label, tmp_val


    def varInregion(self):
        reigon = self._odb.rootAssembly.elementSets[self._setName]
        frame = self._odb.steps[self._step].frames[self._frame]
        data = frame.fieldOutputs[self._dataName].getSubset(region=reigon).values
        dic = {}
        for v in data:
            dic.update({v.elementLabel: v.data})
        return dic