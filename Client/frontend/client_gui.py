from tkinter import *
from PIL import ImageTk, Image
from Client.Controller.Controller import Controller
import os
from Utilities import Misc


class Room:
    """
    This clas is responsible for creating the Gui for our chat.
    in particular - LOGIN window & Chat room window
    """

    def __init__(self):
        # This is the chat window, it will be hidden for new users until they join the room.
        self.chat_window = Tk()
        self.controller = Controller(("127.0.0.1", 12345))
        # imgs abs paths:
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        parent_path = Misc.resource_path(relative_path='frontend')
        self.images_path = parent_path + "/imgs/"
        self.chat_window_builder()
        self.chat_window.withdraw()
        # login window
        self.chat_login = Toplevel()
        self.chat_login.protocol("WM_DELETE_WINDOW", self.chat_window.destroy)  # terminates program
        self.chat_login_builder()
        # self.enter_chat()
        self.chat_window.mainloop()

    def chat_login_builder(self):
        """
        This method creates the login window
        :return:
        """
        self.chat_login.title("Login")
        self.chat_login.resizable(width=FALSE, height=FALSE)
        self.chat_login.configure(width=400, height=300)
        # name label & entry:
        name = Label(self.chat_login, text="Enter your name:", justify=CENTER)
        name.place(relheight=0.15, relx=0.1, rely=0.15)
        txt_name = Entry(self.chat_login)
        txt_name.place(relheight=0.15, relwidth=0.5, relx=0.4, rely=0.15)
        # connect button:
        connect = Button(self.chat_login, text="Connect", command=self.enter_chat)
        connect.place(relx=0.4, rely=0.55)

    def chat_window_builder(self):
        """
        This method creates the chat window, basic gui usage - buttons,labels,text boxes..
        :return:
        """
        self.chat_window.title("Walk2Talk")
        self.chat_window.resizable(width=TRUE, height=TRUE)
        self.chat_window.configure(width=700, height=600)
        # create background:
        self.generate_background()

        # chat_box:
        chat_box = Text(self.chat_window, font=("Helvetica", 14))
        chat_box.config(state=DISABLED)
        chat_box.place(relheight=0.6530, relwidth=0.6980, relx=0.0080, rely=0.19)
        self.scrollbar(0.972, chat_box)

        # Data BOX:
        data_box = Text(self.chat_window, font=("Helvetica", 14))
        data_box.config(state=DISABLED)
        data_box.place(relheight=0.6530, relwidth=0.2680, relx=0.723, rely=0.19)
        self.scrollbar(0.92, data_box)

        # Client msg box:
        client_msg = Entry(self.chat_window)
        client_msg.place(relheight=0.1050, relwidth=0.6975, relx=0.01, rely=0.8875)

        # disconnect button:
        exit_chat = Button(self.chat_window, text="Exit Chat",
                           command=lambda: self.controller.exit_chat(self.chat_login, self.chat_window))
        exit_chat.place(relheight=0.0570, relwidth=0.1190, relx=0.0080, rely=0.0075)

        # send msg button:
        send_msg = Button(self.chat_window, text="Send",
                          command=lambda: self.controller.send_msg(text_box=chat_box, msg_box=client_msg))
        send_msg.place(relheight=0.1050, relwidth=0.135, relx=0.7180, rely=0.8875)

        # send all button:
        send_msg = Button(self.chat_window, text="Send All", command=self.controller.send_all)
        send_msg.place(relheight=0.1050, relwidth=0.135, relx=0.8580, rely=0.8875)

        # get clients button:
        get_clients = Button(self.chat_window, text="Show Connected",
                             command=self.controller.get_clients)
        get_clients.place(relheight=0.0570, relwidth=0.2680, relx=0.7250, rely=0.0075)

        # files / clients label:
        data = Label(self.chat_window, text="Files/Connected Clients")
        data.place(relheight=0.0650, relwidth=0.27, relx=0.723, rely=0.0750)

        # get files button
        get_files = Button(self.chat_window, text="Show Files", command=self.controller.get_files)
        get_files.place(relheight=0.0570, relwidth=0.2680, relx=0.442, rely=0.0075)

        # clear chat button:
        clear_chat = Button(self.chat_window, text="Clear Chat",
                            command=lambda: self.controller.clear_chat(text_box=chat_box))
        clear_chat.place(relheight=0.0650, relwidth=0.27, relx=0.442, rely=0.0750)

    def scrollbar(self, x: float, txt: Text):
        """
        This method creates the scroll bar for the chat boxes
        :param x: representing float number for locating the bar
        :param txt: a text box to place the scroll bar on
        :return:
        """
        scrollbar = Scrollbar(txt)
        scrollbar.place(relheight=1, relx=x)
        scrollbar.config(command=txt.yview)

    def generate_background(self):
        # TODO: make this resizable
        """
        This method generates the background for our chat box,
        :return:
        """
        # Background load:
        template = Image.open(self.images_path + "Template.png")
        img = ImageTk.PhotoImage(template)
        bg = Label(self.chat_window, image=img)
        bg.image = img
        bg.pack(side='top', fill='both', expand='yes')

    def enter_chat(self):
        self.chat_login.withdraw()
        self.chat_window.deiconify()  # TODO: MOVE TO CONTROLLER


if __name__ == '__main__':
    Room()
