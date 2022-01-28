from tkinter import *
from PIL import ImageTk, Image
from Frontend.Controller import Controller
import os


class Room():

    def __init__(self):
        # This is the chat window, it will be hidden for new users to until they join the room.
        self.chat_window = Tk()
        # imgs abs paths:
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        parent_path = Controller.resource_path(relative_path='View')
        self.images_path = parent_path + "/imgs/"

        self.chat_window_builder()
        self.chat_window.withdraw()

        # login window
        # self.chat_login = Toplevel()
        # self.chat_login_builder()
        self.enter_chat()
        self.chat_window.mainloop()

    def chat_login_builder(self):
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
        self.chat_window.title("Walk2Talk")
        self.chat_window.resizable(width=TRUE, height=TRUE)
        self.chat_window.configure(width=700, height=600)
        # create background:
        self.generate_background()

        # server msg box:
        self.creator(operator="Text", text="", command=0.974, relheight=0.6530,
                     relwidth=0.6980, relx=0.0080,
                     rely=0.19)

        # Data BOX:
        self.creator(operator="Text", text="", command=0.92, relheight=0.6530,
                     relwidth=0.2680, relx=0.723,
                     rely=0.19)

        # client msg box:
        self.creator(operator="Entry", text="", command=None, relheight=0.1050,
                     relwidth=0.6975, relx=0.01,
                     rely=0.8875)

        # disconnect button:
        self.creator(operator="Button", text="Exit Chat", command=Controller.disconnect, relheight=0.0570,
                     relwidth=0.1190, relx=0.0080,
                     rely=0.0075)

        # send msg button:
        self.creator(operator="Button", text="Send", command=Controller.send_msg, relheight=0.1050,
                     relwidth=0.135, relx=0.7180,
                     rely=0.8875)

        # send all button:
        self.creator(operator="Button", text="Send All", command=Controller.send_all, relheight=0.1050,
                     relwidth=0.135, relx=0.8580,
                     rely=0.8875)

        # get clients button:
        self.creator(operator="Button", text="Show Connected", command=Controller.get_clients, relheight=0.0570,
                     relwidth=0.2680, relx=0.7250,
                     rely=0.0075)

        # files / clients label:
        self.creator(operator="Label", text="Files/Connected Clients", command=None, relheight=0.0650,
                     relwidth=0.27, relx=0.723,
                     rely=0.0750)

        # get files button
        self.creator(operator="Button", text="Show Files", command=Controller.get_files, relheight=0.0570,
                     relwidth=0.2680, relx=0.442,
                     rely=0.0075)

        # clear chat button:
        self.creator(operator="Button", text="Clear Chat", command=Controller.clear_chat, relheight=0.0650,
                     relwidth=0.27, relx=0.442,
                     rely=0.0750)

    def creator(self, operator: str, text: str, command, relheight: float, relwidth: float, relx: float, rely: float):
        """
        This method is a creator for the objects we present in the window
        :param operator: operator to tell the method which object to create
        :param text: Name of the object
        :param command: a method to operate on the button, on Text its used as a scrollbar y position
        :param relheight: float representing height of object
        :param relwidth: float representing width of object
        :param relx: float representing x pos of the object
        :param rely: float representing y pos of the object
        :return: None
        """
        parts = None
        if operator == "Button":
            parts = Button(self.chat_window, text=text, command=command)
        elif operator == "Label":
            parts = Label(self.chat_window, text=text)
        elif operator == "Entry":
            parts = Entry(self.chat_window)
        elif operator == "Text":
            parts = Text(self.chat_window)
            parts.config(state=DISABLED)
            # scrollbar:
            scrollbar = Scrollbar(parts)
            scrollbar.place(relheight=1, relx=command)
            scrollbar.config(command=parts.yview)
        parts.place(relheight=relheight, relwidth=relwidth, relx=relx, rely=rely)

    def generate_background(self):
        # Background load:
        template = Image.open(self.images_path + "Template.png")
        img = ImageTk.PhotoImage(template)
        bg = Label(self.chat_window, image=img)
        bg.image = img
        bg.pack(side='top', fill='both', expand='yes')

    def enter_chat(self):
        # self.chat_login.destroy()
        self.chat_window.deiconify()  # TODO: MOVE TO CONTROLLER


if __name__ == '__main__':
    Room()
"""
THIS IS OLD CREATOR: 

 # client msg box:
        client_msg = Entry(self.chat_window)
        client_msg.place(relheight=0.1050, relwidth=0.6975, relx=0.01, rely=0.8875)  # MEASURES FOR THE client msg box

        # disconnect button:
        # ELAD -> i want this command to make the client to return to the login menu again.
        exit_chat = Button(self.chat_window, text="Exit Chat",
                           command=Controller.disconnect)
        exit_chat.place(relheight=0.0570, relwidth=0.1190, relx=0.0080, rely=0.0075)

        # send msg button:
        send_msg = Button(self.chat_window, text="Send", command=Controller.send_msg)
        send_msg.place(relheight=0.1050, relwidth=0.135, relx=0.7180, rely=0.8875)

        # send all button:
        send_msg = Button(self.chat_window, text="Send All", command=Controller.send_all)
        send_msg.place(relheight=0.1050, relwidth=0.135, relx=0.8580, rely=0.8875)

        # get clients button:
        get_clients = Button(self.chat_window, text="Show Connected",
                             command=Controller.get_clients)
        get_clients.place(relheight=0.0570, relwidth=0.2680, relx=0.7250, rely=0.0075)

        # files / clients label:
        data = Label(self.chat_window, text="Files/Connected Clients")
        data.place(relheight=0.0650, relwidth=0.27, relx=0.723, rely=0.0750)

        # get files button
        get_files = Button(self.chat_window, text="Show Files", command=Controller.get_files)
        get_files.place(relheight=0.0570, relwidth=0.2680, relx=0.442, rely=0.0075)

        # clear chat button:
        clear_chat = Button(self.chat_window, text="Clear Chat", command=Controller.clear_chat)
        clear_chat.place(relheight=0.0650, relwidth=0.27, relx=0.442, rely=0.0750)
"""
