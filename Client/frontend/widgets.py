from tkinter import Label, Tk, BOTH, YES, ttk, Frame, Entry, Scrollbar, VERTICAL, Canvas, LEFT, RIGHT
from PIL import ImageTk, Image
from scroll_frame import VerticalScrolledFrame


def resize_widget(event, image, widget_label: Label):
    new_width = event.width / widget_label.dim[0] - 4
    new_height = event.height / widget_label.dim[1] - 4
    img = image.resize((new_width, new_height))
    tk_img = ImageTk.PhotoImage(img)
    widget_label.config(image=tk_img)
    widget_label.image = img  # avoid garbage collection


class BubbleMsg(ttk.Label):

    def __init__(self, master, text='bla', sender='Me'):
        ttk.Label.__init__(self, master, text=text, compound='center')
        if sender == 'Me':
            image = Image.open('./imgs/BubbleLeft.png')
            tk_bubble_img = ImageTk.PhotoImage(image)
        else:
            image = Image.open('./imgs/BubbleRight.png')
            tk_bubble_img = ImageTk.PhotoImage(image)
        self.configure(image=tk_bubble_img)
        self.image = tk_bubble_img
        self.dim = (227, 49)
        # self.pack(fill=BOTH, expand=YES)
        # self.bind('<Configure>', lambda event: Room.resize_image(event, image.copy(), self))


class ChatBox(VerticalScrolledFrame):

    def __init__(self, parent, *args, **kw):
        VerticalScrolledFrame.__init__(parent, *args, **kw)
        self.level_index = 0
        self.canvas = Canvas(self.interior)
    # def update_box(self, sender):


def enter(frame):
    global boole, index
    if boole:
        b = BubbleMsg(frame.interior, sender='bla')
        b.place(y=0 + index)
        b.update()
        b.pack()
        b.update()
    else:
        b = BubbleMsg(frame.interior)
        b.pack()
        b.update()
        b.place(x=-30, y=30 + index)
        b.update()
    boole = not boole
    index += 30


if __name__ == '__main__':
    root = Tk()
    frame = VerticalScrolledFrame(root)
    root.config(width=800, height=500)
    boole = False
    index = 0.1
    frame.place(relx=0, rely=0, relheight=1, relwidth=1)
    root.bind('<Return>', lambda event: enter(frame))
    root.mainloop()
