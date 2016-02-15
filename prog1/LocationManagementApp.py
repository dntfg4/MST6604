'''Location Management Application:
        This program uses algorithms determining search and updates for mobile station movements.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/06 12:00:00 $'
__copyright__ = 'Copyright (c) 2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

import sys
import Tkinter
from LocationManagementMisc import *

class RSCError(Exception):
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def __str__(self):
        return repr(self.name)

class LocationManagementLabels:
    def __init__(self, parent, col=0, row=-1):
        self.__labels = {}
        self.__col = col
        self.__row = row
        self.__parent = parent
        self.__initialize()

    def __nextRow(self):
        self.__row += 1
        return self.__row

    def __addHeaderLabel(self):
        self.__header = Tkinter.Label(self.__parent, text = "Labels")
        self.__header.grid(column = self.__col, row = self.__nextRow(),  columnspan=2, sticky='EW')

    def __addLabel(self, labelText):
        self.__labels[labelText] = Tkinter.Label(self.__parent,text=labelText, anchor="w",fg="white", bg="blue")
        self.__labels[labelText].grid(column=self.__col, row=self.__nextRow(), columnspan=2, sticky='EW')

    def __initialize(self):
        self.__addHeaderLabel()
        self.__addLabel("Algorithm Option")
        self.__addLabel("Tree Level")
        self.__addLabel("Leaf Node 7 CMR")
        self.__addLabel("Leaf Node 8 CMR")
        self.__addLabel("Leaf Node 9 CMR")
        self.__addLabel("Leaf Node 10 CMR")
        self.__addLabel("Leaf Node 11 CMR")
        self.__addLabel("Leaf Node 12 CMR")
        self.__addLabel("Leaf Node 13 CMR")
        self.__addLabel("Leaf Node 14 CMR")
        self.__addLabel("Leaf Node 15 CMR")
        self.__addLabel("Leaf Node 16 CMR")
        self.__addLabel("Leaf Node 17 CMR")
        self.__addLabel("Leaf Node 18 CMR")
        self.__addLabel("minS")
        self.__addLabel("maxS")
        self.__addLabel("MS1: Move to Node")

class LocationManagemenEntry:
    def __init__(self, parent, headerName, col, row, setFocus):
        self.__inputs = {}
        self.__entries = {}
        self.__col = col
        self.__row = row
        self.__setFocus = setFocus
        self.__parent = parent
        self.__headerName = "Labels"
        self.__initialize()

    def __nextRow(self):
        self.__row += 1
        return self.__row

    def __addDropDownEntry(self, varName, setFocus=False):
        self.__inputs[varName] = Tkinter.StringVar()
        self.__inputs[varName].set("Pointer")
        self.__entries[varName] = Tkinter.OptionMenu(self.__parent,self.__inputs[varName], 'Pointer','Actual','FPPointer', 'FPActual', 'RPointer', 'RActual')
        self.__entries[varName].grid(column = self.__col, row = self.__nextRow(), sticky='EW')
        #self.__entries[varName].pack()

    def __addDoubleEntry(self, varName, initValue=0, setFocus=False):
        self.__inputs[varName] = Tkinter.StringVar()
        self.__inputs[varName].set(format(initValue,".2f"))
        self.__entries[varName] = Tkinter.Entry(self.__parent,textvariable=self.__inputs[varName])
        self.__entries[varName].grid(column = self.__col, row = self.__nextRow(), sticky='EW')
        if setFocus:
            self.__entries[varName].focus_set()
            self.__entries[varName].selection_range(0, Tkinter.END)

    def __addIntEntry(self, varName, initValue=0, setFocus=False):
        self.__inputs[varName] = Tkinter.StringVar()
        self.__inputs[varName].set(initValue)
        self.__entries[varName] = Tkinter.Entry(self.__parent,textvariable=self.__inputs[varName])
        self.__entries[varName].grid(column = self.__col, row = self.__nextRow(), sticky='EW')
        if setFocus:
            self.__entries[varName].focus_set()
            self.__entries[varName].selection_range(0, Tkinter.END)

    def __initialize(self):
        self.__header = Tkinter.Label(self.__parent, text = "Values", width = 20)
        self.__header.grid(column = self.__col, row = self.__nextRow(), sticky = "W")
        self.__addDropDownEntry("algo_option", self.__setFocus)
        self.__addIntEntry("treelevel", 1)
        self.__addDoubleEntry("node7cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node8cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node9cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node10cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node11cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node12cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node13cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node14cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node15cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node16cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node17cmr", 0, self.__setFocus)
        self.__addDoubleEntry("node18cmr", 0, self.__setFocus)
        self.__addDoubleEntry("minS", .6, self.__setFocus)
        self.__addDoubleEntry("maxS", 1.2, self.__setFocus)
        self.__addIntEntry("ms1movetonode", 7)
        #self.__addIntEntry("ms2movetonode", 18)

        self.__lmaButton = Tkinter.Button(self.__parent,text="Move MS1", command=self.__OnMS1MoveClick)
        self.__lmaButton.grid(column=self.__col, row=self.__nextRow())
        self.__lmaButton.bind("<Return>", self.__OnMS1MoveClickEvt)

        self.__lmaButton = Tkinter.Button(self.__parent,text="MS2 Call MS1", command=self.__OnMS2CallMS1MoveClick)
        self.__lmaButton.grid(column=self.__col, row=self.__nextRow())
        self.__lmaButton.bind("<Return>", self.__OnMS2CallMS1MoveClickEvt)
        
        self.__lmaButton = Tkinter.Button(self.__parent,text="Reset Tree", command=self.__OnResetTreeClick)
        self.__lmaButton.grid(column=self.__col, row=self.__nextRow())
        self.__lmaButton.bind("<Return>", self.__OnResetTreeClickEvt)

        self.__resultVar = Tkinter.StringVar()
        self.__resultVar.set("")
        self.__resultLabel = Tkinter.Label(self.__parent, textvariable = self.__resultVar, width = 20)
        self.__resultLabel.grid(column = self.__col , row=self.__nextRow(), rowspan = 2,)

    def __OnMS1MoveClickEvt(self, evt):
        self.__OnMS1MoveClick()

    def __OnMS1MoveClick(self):
        self.__parent.move_ms1(int(self.__inputs["ms1movetonode"].get()), self.__inputs)

    def __OnResetTreeClickEvt(self, evt):
        self.__OnResetTreeClick()

    def __OnResetTreeClick(self):
        self.__parent.reset_trees()

    def __OnMS2CallMS1MoveClickEvt(self, evt):
        self.__OnMS2CallMS1MoveClick()

    def __OnMS2CallMS1MoveClick(self):
        self.__parent.ms2_call_ms1(self.__inputs)


class LocationManagementApp(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.__parent = parent
        self.__tpa = None
        self.__tfppa = None
        self.__tva = None
        self.__tfpva = None
        self.__trva = None
        self.__trpa = None
        self.__ms1 = None
        self.__ms2 = None
        self.__initialize()

    def __initialize(self):
        self.grid()

        self.reset_trees()

        self.__numLMA = Tkinter.IntVar()
        self.__numLMA.set(1)
        self.__NumCalcsOnPressEnter()

        self.resizable(False, False)
        self.columnconfigure(0, minsize = 250, weight=1)
        self.update()

    def __NumCalcsOnPressEnter(self):
        try:
            if self.__numLMA.get() > 0:
                self.__lmaNames = {}
                for i in range(self.__numLMA.get()):
                    self.__lmaNames[i] = {}
                    self.__lmaNames[i][0] = Tkinter.Label(self, text = "Calculator " + str(i+1) + " Name",
                                                          anchor = "w", fg = "white", bg = "blue")
                    self.__lmaNames[i][0].grid(column = 0 , row = i, columnspan = 2, sticky = 'EW')
                    self.__lmaNames[i][1] = {}
                    self.__lmaNames[i][1][0] = Tkinter.StringVar()
                    self.__lmaNames[i][1][0].set("Values")
                    self.__lmaNames[i][1][1] = Tkinter.Entry(self, textvariable = self.__lmaNames[i][1][0], width = 20)
                    self.__lmaNames[i][1][1].grid(column = 1, row = i, sticky = 'EW')

                self.____addLMA()

        except:
            self.__numLMA.set(1)

    def ____addLMA(self):
        for i in range(self.__numLMA.get()):
            self.__lmaNames[i][0].grid_forget()
            self.__lmaNames[i][1][1].grid_forget()

        self.__labels = LocationManagementLabels(self)
        self.__calcs = []
        self.__lmaNames[i][1][0].set("")
        self.__calcs.append(LocationManagemenEntry(self, self.__lmaNames[0][1][0].get(), i+2, -1, i==0))
        self.update()

    def reset_trees(self):
        self.__tpa = Tree(PointerAlgorithm())
        self.__tfppa = Tree(ForwardingPointerPAlgorithm())
        self.__tva = Tree(ValueAlgorithm())
        self.__tfpva = Tree(ForwardingPointerVAlgorithm())
        self.__trva = Tree(ReplicationValueAlgorithm())
        self.__trpa = Tree(ReplicationPointerAlgorithm())
        self.__ms1 = MS(1)
        self.__ms2 = MS(2)

        fill_tree(self.__tpa)
        fill_tree(self.__tva)
        fill_tree(self.__tfppa)
        fill_tree(self.__tfpva)
        fill_tree(self.__trva)
        fill_tree(self.__trpa)

        self.__tpa.put_ms_into_node_name(self.__ms1, 7)
        self.__tva.put_ms_into_node_name(self.__ms1, 7)
        self.__tfppa.put_ms_into_node_name(self.__ms1, 7)
        self.__tfpva.put_ms_into_node_name(self.__ms1, 7)
        self.__trpa.put_ms_into_node_name(self.__ms1, 7)
        self.__trva.put_ms_into_node_name(self.__ms1, 7)

        self.__tpa.put_ms_into_node_name(self.__ms2, 18)
        self.__tva.put_ms_into_node_name(self.__ms2, 18)
        self.__tfppa.put_ms_into_node_name(self.__ms2, 18)
        self.__tfpva.put_ms_into_node_name(self.__ms2, 18)
        self.__trpa.put_ms_into_node_name(self.__ms2, 18)
        self.__trva.put_ms_into_node_name(self.__ms2, 18)

    def update_trees(self, inputs):
        self.__trpa.get_node(7).set_lcmr(float(inputs["node7cmr"].get()))
        self.__trpa.get_node(8).set_lcmr(float(inputs["node8cmr"].get()))
        self.__trpa.get_node(9).set_lcmr(float(inputs["node9cmr"].get()))
        self.__trpa.get_node(10).set_lcmr(float(inputs["node10cmr"].get()))
        self.__trpa.get_node(11).set_lcmr(float(inputs["node11cmr"].get()))
        self.__trpa.get_node(12).set_lcmr(float(inputs["node12cmr"].get()))
        self.__trpa.get_node(13).set_lcmr(float(inputs["node13cmr"].get()))
        self.__trpa.get_node(14).set_lcmr(float(inputs["node14cmr"].get()))
        self.__trpa.get_node(15).set_lcmr(float(inputs["node15cmr"].get()))
        self.__trpa.get_node(16).set_lcmr(float(inputs["node16cmr"].get()))
        self.__trpa.get_node(17).set_lcmr(float(inputs["node17cmr"].get()))
        self.__trpa.get_node(18).set_lcmr(float(inputs["node18cmr"].get()))
        self.__trpa.get_algorithm().set_mins(float(inputs["minS"].get()))
        self.__trpa.get_algorithm().set_mins(float(inputs["maxS"].get()))
        self.__trva.get_node(7).set_lcmr(float(inputs["node7cmr"].get()))
        self.__trva.get_node(8).set_lcmr(float(inputs["node8cmr"].get()))
        self.__trva.get_node(9).set_lcmr(float(inputs["node9cmr"].get()))
        self.__trva.get_node(10).set_lcmr(float(inputs["node10cmr"].get()))
        self.__trva.get_node(11).set_lcmr(float(inputs["node11cmr"].get()))
        self.__trva.get_node(12).set_lcmr(float(inputs["node12cmr"].get()))
        self.__trva.get_node(13).set_lcmr(float(inputs["node13cmr"].get()))
        self.__trva.get_node(14).set_lcmr(float(inputs["node14cmr"].get()))
        self.__trva.get_node(15).set_lcmr(float(inputs["node15cmr"].get()))
        self.__trva.get_node(16).set_lcmr(float(inputs["node16cmr"].get()))
        self.__trva.get_node(17).set_lcmr(float(inputs["node17cmr"].get()))
        self.__trva.get_node(18).set_lcmr(float(inputs["node18cmr"].get()))
        self.__trva.get_algorithm().set_mins(float(inputs["minS"].get()))
        self.__trva.get_algorithm().set_mins(float(inputs["maxS"].get()))

    def move_ms1(self, name, inputs):
        self.update_trees(inputs)
        if inputs["algo_option"].get() == "Pointer":
            self.__tpa.find_node_and_move_ms_location_from_node(self.__ms1, name)
        elif inputs["algo_option"].get() == "Actual":
            self.__tva.find_node_and_move_ms_location_from_node(self.__ms1, name)
        elif inputs["algo_option"].get() == "FPPointer":
            self.__tfppa.get_algorithm().set_forwarding_level(int(inputs["treelevel"].get()))
            self.__tfppa.find_node_and_move_ms_location_from_node(self.__ms1, name)
        elif inputs["algo_option"].get() == "FPActual":
            self.__tfpva.find_node_and_move_ms_location_from_node(self.__ms1, name)
        elif inputs["algo_option"].get() == "RPointer":
            self.__trpa.find_node_and_move_ms_location_from_node(self.__ms1, name)
        elif inputs["algo_option"].get() == "RActual":
            self.__trva.find_node_and_move_ms_location_from_node(self.__ms1, name)

    def move_ms2(self, name, inputs):
        self.update_trees(inputs)
        if inputs["algo_option"].get() == "Pointer":
            self.__tpa.find_node_and_move_ms_location_from_node(self.__ms2, name)
        elif inputs["algo_option"].get() == "Actual":
            self.__tva.find_node_and_move_ms_location_from_node(self.__ms2, name)
        elif inputs["algo_option"].get() == "FPPointer":
            self.__tfppa.find_node_and_move_ms_location_from_node(self.__ms2, name)
        elif inputs["algo_option"].get() == "FPActual":
            self.__tfpva.find_node_and_move_ms_location_from_node(self.__ms2, name)
        elif inputs["algo_option"].get() == "RPointer":
            self.__trpa.find_node_and_move_ms_location_from_node(self.__ms2, name)
        elif inputs["algo_option"].get() == "RActual":
            self.__trva.find_node_and_move_ms_location_from_node(self.__ms2, name)

    def ms2_call_ms1(self, inputs):
        if inputs["algo_option"].get() == "Pointer":
            self.__tpa.query_ms_location_from_node(self.__ms1, self.__ms2.get_node(self.__tpa.get_algorithm().get_type()))
            self.__tpa.draw_tree(self.__ms1, self.__ms2)
        elif inputs["algo_option"].get() == "Actual":
            self.__tva.query_ms_location_from_node(self.__ms1, self.__ms2.get_node(self.__tva.get_algorithm().get_type()))
            self.__tva.draw_tree(self.__ms1, self.__ms2)
        elif inputs["algo_option"].get() == "FPPointer":
            self.__tfppa.query_ms_location_from_node(self.__ms1, self.__ms2.get_node(self.__tfppa.get_algorithm().get_type()))
            self.__tfppa.draw_tree(self.__ms1, self.__ms2)
        elif inputs["algo_option"].get() == "FPActual":
            self.__tfpva.query_ms_location_from_node(self.__ms1, self.__ms2.get_node(self.__tfpva.get_algorithm().get_type()))
            self.__tfpva.draw_tree(self.__ms1, self.__ms2)
        elif inputs["algo_option"].get() == "RPointer":
            self.__trpa.query_ms_location_from_node(self.__ms1, self.__ms2.get_node(self.__trpa.get_algorithm().get_type()))
            self.__trpa.draw_tree(self.__ms1, self.__ms2)
        elif inputs["algo_option"].get() == "RActual":
            self.__trva.query_ms_location_from_node(self.__ms1, self.__ms2.get_node(self.__trva.get_algorithm().get_type()))
            self.__trva.draw_tree(self.__ms1, self.__ms2)

if __name__ == "__main__":
    app = LocationManagementApp(None)
    app.title('Location Management')
    app.mainloop()
