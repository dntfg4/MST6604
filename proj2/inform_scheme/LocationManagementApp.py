'''Location Management Application:
        This program uses algorithms determining search and updates for mobile station movements.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/17 12:00:00 $'
__copyright__ = '2016 James Soehlke and David N. Taylor'
__license__ = 'Python'

import sys
import Tkinter
from Tree import *
from LMTreeCanvas import *

##################################################################################
#
#  Class Description: This is exception class
#
##################################################################################
class RSCError(Exception):
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def __str__(self):
        return repr(self.name)

##################################################################################
#
#  Class Description: This is the class of the labels on the GUI
#
##################################################################################
class LocationManagementLabels:
    def __init__(self, parent, col=0, row=-1):
        self.__labels = {}
        self.__col = col
        self.__row = row
        self.__parent = parent
        self.__initialize()

    ##################################################################################
    #
    #  Description: Returns the next row
    #
    ##################################################################################
    def __nextRow(self):
        self.__row += 1
        return self.__row

    ##################################################################################
    #
    #  Description: Add a header label
    #
    ##################################################################################
    def __addHeaderLabel(self):
        self.__header = Tkinter.Label(self.__parent, text = "Labels")
        self.__header.grid(column = self.__col, row = self.__nextRow(),  columnspan=2, sticky='EW')

    ##################################################################################
    #
    #  Description: Adds a label
    #
    ##################################################################################
    def __addLabel(self, labelText):
        self.__labels[labelText] = Tkinter.Label(self.__parent,text=labelText, anchor="w",fg="white", bg="blue")
        self.__labels[labelText].grid(column=self.__col, row=self.__nextRow(), columnspan=2, sticky='EW')

    ##################################################################################
    #
    #  Description: Initializes the labels
    #
    ##################################################################################
    def __initialize(self):
        self.__addHeaderLabel()
        #self.__addLabel("Algorithm Option")
        self.__addLabel("Token Ring Wait Time (Sec)")
        self.__addLabel("MS1: Move to Node")
        self.__addLabel("MS2: Move to Node")
        self.__addLabel("MS1 messages MS2")
        self.__addLabel("MS2 messages MS1")
        #self.__addLabel("MS2 Call MS1")


##################################################################################
#
#  Class Description: This is the class for GUI entry values
#
##################################################################################
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

    ##################################################################################
    #
    #  Description: returns the next row
    #
    ##################################################################################
    def __nextRow(self):
        self.__row += 1
        return self.__row

    ##################################################################################
    #
    #  Description: Adds a drop down object
    #
    ##################################################################################
    def __addDropDownEntry(self, varName, setFocus=False):
        self.__inputs[varName] = Tkinter.StringVar()
        self.__inputs[varName].set("Pointer")
        self.__entries[varName] = Tkinter.OptionMenu(self.__parent,self.__inputs[varName], 'Pointer')
        self.__entries[varName].grid(column = self.__col, row = self.__nextRow(), sticky='EW')

    ##################################################################################
    #
    #  Description: Adds a double entry
    #
    ##################################################################################
    def __addDoubleEntry(self, varName, initValue=0, setFocus=False):
        self.__inputs[varName] = Tkinter.StringVar()
        self.__inputs[varName].set(format(initValue,".2f"))
        self.__entries[varName] = Tkinter.Entry(self.__parent,textvariable=self.__inputs[varName])
        self.__entries[varName].grid(column = self.__col, row = self.__nextRow(), sticky='EW')
        if setFocus:
            self.__entries[varName].focus_set()
            self.__entries[varName].selection_range(0, Tkinter.END)

    ##################################################################################
    #
    #  Description: Adds a Int entry
    #
    ##################################################################################
    def __addIntEntry(self, varName, initValue=0, setFocus=False):
        self.__inputs[varName] = Tkinter.StringVar()
        self.__inputs[varName].set(initValue)
        self.__entries[varName] = Tkinter.Entry(self.__parent,textvariable=self.__inputs[varName])
        self.__entries[varName].grid(column = self.__col, row = self.__nextRow(), sticky='EW')
        if setFocus:
            self.__entries[varName].focus_set()
            self.__entries[varName].selection_range(0, Tkinter.END)

    ##################################################################################
    #
    #  Description: Adds a String entry
    #
    ##################################################################################
    def __addStringEntry(self, varName, initValue="", setFocus=False):
        self.__inputs[varName] = Tkinter.StringVar()
        self.__inputs[varName].set(initValue)
        self.__entries[varName] = Tkinter.Entry(self.__parent,textvariable=self.__inputs[varName])
        self.__entries[varName].grid(column = self.__col, row = self.__nextRow(), sticky='EW')
        if setFocus:
            self.__entries[varName].focus_set()
            self.__entries[varName].selection_range(0, Tkinter.END)

    ##################################################################################
    #
    #  Description: Initializes the GUI entries
    #
    ##################################################################################
    def __initialize(self):
        self.__header = Tkinter.Label(self.__parent, text = "Values", width = 20)
        self.__header.grid(column = self.__col, row = self.__nextRow(), sticky = "W")
        #self.__addDropDownEntry("algo_option", self.__setFocus)
        self.__addIntEntry("tokenwaittime", 2)
        self.__addIntEntry("ms1movetonode", 7)
        self.__addIntEntry("ms2movetonode", 18)
        self.__addStringEntry("ms1messagems2","Hello MS2")
        self.__addStringEntry("ms2messagems1","Hello MS1")
        #self.__addIntEntry("callms1fromnode", 18)

        self.__lmaButton = Tkinter.Button(self.__parent,text="Move MS1", command=self.__OnMS1MoveClick)
        self.__lmaButton.grid(column=self.__col + 1, row=1)
        self.__lmaButton.bind("<Return>", self.__OnMS1MoveClickEvt)

        self.__lmaButton = Tkinter.Button(self.__parent,text="Move MS2", command=self.__OnMS2MoveClick)
        self.__lmaButton.grid(column=self.__col + 1 , row=2)
        self.__lmaButton.bind("<Return>", self.__OnMS2MoveClickEvt)

        self.__lmaButton = Tkinter.Button(self.__parent,text="Token Ring Wait Time", command=self.__OnTokenRingWaitTimeClick)
        self.__lmaButton.grid(column=self.__col + 2, row=1)
        self.__lmaButton.bind("<Return>", self.__OnTokenRingWaitTimeClickEvt)

        # self.__lmaButton = Tkinter.Button(self.__parent,text="MS2 Call MS1", command=self.__OnCallMS1MoveClick)
        # self.__lmaButton.grid(column=self.__col, row=self.__nextRow())
        # self.__lmaButton.bind("<Return>", self.__OnCallMS1MoveClickEvt)
        
        self.__lmaButton = Tkinter.Button(self.__parent,text="MS1 messages MS2", command=self.__OnMS1MsgMS2Click)
        self.__lmaButton.grid(column=self.__col + 2, row=2)
        self.__lmaButton.bind("<Return>", self.__OnMS1MsgMS2ClickEvt)
        
        self.__lmaButton = Tkinter.Button(self.__parent,text="MS2 messages MS1", command=self.__OnMS2MsgMS1Click)
        self.__lmaButton.grid(column=self.__col+2, row=3)
        self.__lmaButton.bind("<Return>", self.__OnMS2MsgMS1ClickEvt)

        self.__resultVar = Tkinter.StringVar()
        self.__resultVar.set("")
        self.__resultLabel = Tkinter.Label(self.__parent, textvariable = self.__resultVar, width = 20)
        self.__resultLabel.grid(column = self.__col , row=self.__nextRow(), rowspan = 2,)

    ##################################################################################
    #
    #  Description: Token Ring Wait Time click event
    #
    ##################################################################################
    def __OnTokenRingWaitTimeClickEvt(self, evt):
        self.__OnTokenRingWaitTimeClick()

    ##################################################################################
    #
    #  Description: Token Ring Wait Time click
    #
    ##################################################################################
    def __OnTokenRingWaitTimeClick(self):
        self.__parent.token_ring_wait_time(int(self.__inputs["tokenwaittime"].get()))

    ##################################################################################
    #
    #  Description: Move ms1 click event
    #
    ##################################################################################
    def __OnMS1MoveClickEvt(self, evt):
        self.__OnMS1MoveClick()

    ##################################################################################
    #
    #  Description: Move ms1 click
    #
    ##################################################################################
    def __OnMS1MoveClick(self):
        self.__parent.move_ms1(int(self.__inputs["ms1movetonode"].get()), self.__inputs)

    ##################################################################################
    #
    #  Description: Move ms2 click event
    #
    ##################################################################################
    def __OnMS2MoveClickEvt(self, evt):
        self.__OnMS2MoveClick()

    ##################################################################################
    #
    #  Description: Move ms2 click
    #
    ##################################################################################
    def __OnMS2MoveClick(self):
        self.__parent.move_ms2(int(self.__inputs["ms2movetonode"].get()), self.__inputs)


    ##################################################################################
    #
    #  Description: call ms1 button evt
    #
    ##################################################################################
    def __OnCallMS1MoveClickEvt(self, evt):
        self.__OnCallMS1MoveClick()

    ##################################################################################
    #
    #  Description: call ms1 button press
    #
    ##################################################################################
    def __OnCallMS1MoveClick(self):
        self.__parent.call_ms1(self.__inputs)

    ##################################################################################
    #
    #  Description: ms1 send ms2 a message
    #
    ##################################################################################
    def __OnMS1MsgMS2ClickEvt(self, evt):
        self.__OnMS1MsgMS2Click()

    ##################################################################################
    #
    #  Description: ms1 send ms2 a message
    #
    ##################################################################################
    def __OnMS1MsgMS2Click(self):
        self.__parent.send_ms2_message(self.__inputs["ms1messagems2"].get())

    ##################################################################################
    #
    #  Description: ms2 send ms1 a message
    #
    ##################################################################################
    def __OnMS2MsgMS1ClickEvt(self, evt):
        self.__OnMS2MsgMS1Click()

    ##################################################################################
    #
    #  Description: ms2 send ms1 a message
    #
    ##################################################################################
    def __OnMS2MsgMS1Click(self):
        self.__parent.send_ms1_message(self.__inputs["ms2messagems1"].get())


##################################################################################
#
#  Class Description: This is the class for the main GUI application
#
##################################################################################
class LocationManagementApp(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.__parent = parent
        self.__tpa = None
        self.__ms1 = None
        self.__ms2 = None
        self.__canvas = None
        self.__initialize()

    ##################################################################################
    #
    #  Description: Initializes
    #
    ##################################################################################
    def __initialize(self):
        self.grid()

        self.__numLMA = Tkinter.IntVar()
        self.__numLMA.set(1)
        self.__NumLMAsOnPressEnter()

        self.reset_trees()

        self.resizable(False, False)
        self.columnconfigure(0, minsize = 250, weight=1)
        self.update()

    def clean(self):
        self.__tpa.clean()

    ##################################################################################
    #
    #  Description: Number of LMAs
    #
    ##################################################################################
    def __NumLMAsOnPressEnter(self):
        try:
            if self.__numLMA.get() > 0:
                self.__lmaNames = {}
                for i in range(self.__numLMA.get()):
                    self.__lmaNames[i] = {}
                    self.__lmaNames[i][0] = Tkinter.Label(self, text = "LMA " + str(i+1) + " Name",
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

    ##################################################################################
    #
    #  Description: adds an lma
    #
    ##################################################################################
    def ____addLMA(self):
        for i in range(self.__numLMA.get()):
            self.__lmaNames[i][0].grid_forget()
            self.__lmaNames[i][1][1].grid_forget()

        self.__labels = LocationManagementLabels(self)
        self.__lmas = []
        self.__lmaNames[i][1][0].set("")
        self.__lmas.append(LocationManagemenEntry(self, self.__lmaNames[0][1][0].get(), i+2, -1, i==0))
        self.update()

    ##################################################################################
    #
    #  Description: Resets the trees
    #
    ##################################################################################
    def reset_trees(self):
        self.__canvas = CanvasApp(self, 6, 8)
        self.__tpa = Tree(PointerAlgorithm())
        self.__ms1 = MH(1)
        self.__ms2 = MH(2)

        fill_tree(self.__tpa, self.__canvas)

        self.__ms1.add_gui(self.__canvas.add_circle(0, 0, 0, fill="white", outline="black", width=2, name="MS1"))
        self.__tpa.put_ms_into_node_name(self.__ms1, 7)
        self.__ms2.add_gui(self.__canvas.add_circle(0, 0, 0, fill="white", outline="black", width=2, name="MS2"))
        self.__tpa.put_ms_into_node_name(self.__ms2, 18)

    ##################################################################################
    #
    #  Description: Token Ring Wait Time
    #
    ##################################################################################
    def token_ring_wait_time(self, wait_time):
        self.__tpa.set_token_ring_wait_time(wait_time)

    ##################################################################################
    #
    #  Description: Moves ms1 to name
    #
    ##################################################################################
    def move_ms1(self, name, inputs):
        self.__ms1.get_gui().clear_line()
        self.__ms2.get_gui().clear_line()
        self.__tpa.find_node_and_move_ms_location_from_node(self.__ms1, name)

    ##################################################################################
    #
    #  Description: Moves ms2 to name
    #
    ##################################################################################
    def move_ms2(self, name, inputs):
        self.__ms1.get_gui().clear_line()
        self.__ms2.get_gui().clear_line()
        self.__tpa.find_node_and_move_ms_location_from_node(self.__ms2, name)

    ##################################################################################
    #
    #  Description: calls ms1
    #
    ##################################################################################
    def call_ms1(self, inputs):
        #node_name = int(inputs["callms1fromnode"].get())

        self.__ms1.get_gui().clear_line()
        self.__ms2.get_gui().clear_line()

        # if node_name != self.__ms2.get_node().get_name():
        #     self.__tpa.remove_ms_from_tree(self.__ms2, self.__ms2.get_node())
        #     self.__tpa.put_ms_into_node_name(self.__ms2, node_name)
        if self.__tpa.query_ms_location_from_node(self.__ms1, self.__ms2.get_node()) is not None:
            self.__ms1.get_gui().search_line("green")
            self.__ms2.get_gui().search_line("green")

    def send_ms1_message(self, message):
        self.__ms2.send_message(self.__ms1, message)

    def send_ms2_message(self, message):
        self.__ms1.send_message(self.__ms2, message)


if __name__ == "__main__":
    app = LocationManagementApp(None)
    app.title('Inform Scheme - Pointer Search Algorithm')
    app.mainloop()
    app.clean()
