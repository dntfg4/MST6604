import Tkinter

import AppCircle


class CanvasApp(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, tk, cols, rows):
        self.__canvas = Tkinter.Canvas(tk, width=1100, height=500, borderwidth=0, highlightthickness=0, background="white")
        self.__canvas.grid(column=0, row=rows, columnspan=cols)
        self.__initialize()
        return

    def __initialize(self):
        self.__canvas.update()

    def add_circle(self, x, y, r, **kwargs):
        return AppCircle.CanvasNode(self, x, y, r, **kwargs)

    def add_line(self, c1, c2):
        c2.add_parent_line(self.__canvas.create_line(c1.get_x(), c1.get_y(), c2.get_x(), c2.get_y(), width="2"))

    def get_height(self):
        return self.__canvas.winfo_reqheight()

    def get_width(self):
        return self.__canvas.winfo_reqwidth()

    def get_canvas(self):
        return self.__canvas




