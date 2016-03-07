from AppCanvas import *

class CanvasNode(object):
    ##################################################################################
    #
    #  Description: Creates the class instance and initializes the vars
    #
    ##################################################################################
    def __init__(self, canvas_app, x, y, r, **kwargs):
        self.__canvas_app = canvas_app
        self.__canvas_node = None
        self.__canvas_text = None
        self.__canvas_line = None
        self.__prev_color = "white"
        self.__x = 0
        self.__y = 0
        self.__r = 0
        self.__create_circle(x, y, r, **kwargs)
        return

    def __create_circle(self, x, y, r, **kwargs):
        name = kwargs["name"]
        del kwargs["name"]
        self.__x = x
        self.__y = y
        self.__r = r
        self.__canvas_node = self.__canvas_app.get_canvas().create_oval(x-r, y-r, x+r, y+r, **kwargs)
        self.__canvas_text = self.__canvas_app.get_canvas().create_text(x, y, text = name)
        self.__canvas_app.get_canvas().update()
        return self.__canvas_node

    def add_parent_line(self, line):
        self.__canvas_line = line
        self.__canvas_app.get_canvas().tag_lower(self.__canvas_line)
        self.__canvas_app.get_canvas().tag_raise(self.__canvas_node)
        self.__canvas_app.get_canvas().tag_raise(self.__canvas_text)
        self.__canvas_app.get_canvas().update()

    def update_node(self):
        self.__canvas_app.get_canvas().itemconfig(self.__canvas_node,fill="yellow")

    def search_line(self, color="red"):
        self.__canvas_app.get_canvas().itemconfig(self.__canvas_line,fill=color)

    def clear_node(self):
        if self.__canvas_app.get_canvas().itemcget(self.__canvas_node, "fill") == "orange":
            self.__prev_color = "white"
        else:
            self.__canvas_app.get_canvas().itemconfig(self.__canvas_node,fill="white")

    def clear_line(self):
        self.__canvas_app.get_canvas().itemconfig(self.__canvas_line,fill="black")

    def token_node(self):
        self.__prev_color = self.__canvas_app.get_canvas().itemcget(self.__canvas_node, "fill")
        self.__canvas_app.get_canvas().itemconfig(self.__canvas_node,fill="orange")

    def untoken_node(self):
        self.__canvas_app.get_canvas().itemconfig(self.__canvas_node,fill=self.__prev_color)

    def message_node(self):
        self.__canvas_app.get_canvas().itemconfig(self.__canvas_node,fill="cyan")

    def unmessage_node(self):
        self.__canvas_app.get_canvas().itemconfig(self.__canvas_node,fill="white")

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_r(self):
        return self.__r

    def move(self, canvas_node):
        text = self.__canvas_app.get_canvas().itemcget(self.__canvas_text, "text")
        self.__canvas_app.get_canvas().delete(self.__canvas_line)
        self.__canvas_app.get_canvas().delete(self.__canvas_node)
        self.__canvas_app.get_canvas().delete(self.__canvas_text)
        del self.__canvas_node
        del self.__canvas_line
        del self.__canvas_text
        self.__canvas_line = None
        self.__canvas_node = None
        self.__canvas_text = None
        self.__create_circle(canvas_node.get_x(), canvas_node.get_y() + 100, canvas_node.get_r(), fill="white", outline="black", width=2, name=text)
        self.__canvas_app.add_line(canvas_node, self)
        self.__canvas_app.get_canvas().update()
