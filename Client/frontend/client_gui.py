from tkinter import *
from typing import List

from PIL import ImageTk, Image
from Client.Controller.Controller import Controller
import os

from Emoji import *
from Utilities import Misc


class Room:
    """
    This clas is responsible for creating the Gui for our chat.
    in particular - LOGIN window & Chat room window
    """

    def __init__(self):
        # This is the chat window, it will be hidden for new users until they join the room.
        self.chat_window = Tk()
        # imgs abs paths:
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        parent_path = Misc.resource_path(relative_path='frontend')
        self.images_path = parent_path + "/imgs/"
        # TXT BOXES:
        self.chat_box = None  # TODO: find better solution
        self.names_box = None
        self.files_box = None
        self.txt_name = None
        self.client_msg = None
        # char room window
        # create background:
        self.generate_background(name="Template.png", window=self.chat_window)
        self.chat_window_textbox_builder()
        # controller:
        self.controller = Controller(("127.0.0.1", 12345), self.chat_box, self.names_box, self.files_box)
        self.chat_window_button_builder()
        self.chat_window.withdraw()
        # login window
        self.chat_login = Toplevel()
        self.chat_login.protocol("WM_DELETE_WINDOW", self.chat_window.destroy)  # terminates program
        self.chat_login_builder()

        self.chat_window.mainloop()

    def default_text(self, event):
        """
        This method makes the text go vrom vrom disppaer when pressing the box ( it only occurs once for some reason)
        :param event:
        :return:
        """
        name = self.txt_name.get()
        msg = self.client_msg.get()
        if name == "Username":
            self.txt_name.delete(0, END)
        if msg == "Type message here...":
            self.client_msg.delete(0, END)

    def chat_login_builder(self):
        """
        This method creates the login window
        :return:
        """
        self.chat_login.title("Login")
        self.chat_login.resizable(width=FALSE, height=FALSE)
        self.chat_login.configure(width=450, height=500)
        # create background:
        self.generate_background(name="Login.png", window=self.chat_login)

        # name label & entry:
        self.txt_name = Entry(self.chat_login, font=("Helvetica", 13))
        self.txt_name.insert(0, "Username")
        self.txt_name.place(relheight=0.0580, relwidth=0.3850, relx=0.308, rely=0.4885)
        # Appearing and reappearing text:
        self.txt_name.bind("<FocusIn>", self.default_text)
        self.txt_name.bind("<FocusOut>", self.default_text)
        # connect button:
        # TODO: find better solution
        connect = Button(self.chat_login, text="Connect", borderwidth=0, font=("Helvetica", 13),
                         command=lambda: self.controller.connect(self.chat_login,
                                                                 self.chat_window,
                                                                 self.txt_name,
                                                                 self.chat_box,
                                                                 self.files_box,
                                                                 self.names_box))
        connect.place(relheight=0.0580, relwidth=0.3850, relx=0.308, rely=0.6080)

    def chat_window_textbox_builder(self):
        """
        This method creates the text boxes.
        :return:
        """
        # chat_box:
        """
        This is the chat box where messages appear after sending 
        """
        self.chat_box = Text(self.chat_window, font=("Helvetica", 14), bg="#17202A",
                             fg="#EAECEE")
        self.chat_box.config(state=DISABLED)
        self.chat_box.place(relheight=0.7030, relwidth=0.6980, relx=0.0080, rely=0.1480)
        self.scrollbar(0.972, self.chat_box)

        # client box:
        """
        This is the list box where all the clients will appear
        """
        self.names_box = Listbox(self.chat_window, font=("Helvetica", 14), bg="#17202A",
                                 fg="#EAECEE", selectmode=SINGLE)
        l2 = Label(self.chat_window, font=("Helvetica", 14), text="People:", bg="#17202A",
                   fg="#EAECEE", borderwidth=0, anchor='w')
        l2.place(relheight=0.030, relwidth=0.2450, relx=0.723, rely=0.1480)
        self.names_box.insert(0, "\n")
        self.names_box.insert(1, "Everyone")
        self.names_box.place(relheight=0.3465, relwidth=0.2680, relx=0.723, rely=0.1480)
        self.scrollbar(0.92, self.names_box)

        # files BOX:
        """
        This is the list box where the files of the server will appear
        """

        self.files_box = Listbox(self.chat_window, font=("Helvetica", 14), bg="#17202A",
                                 fg="#EAECEE")
        l1 = Label(self.chat_window, font=("Helvetica", 14), text="Files:", bg="#17202A",
                   fg="#EAECEE", borderwidth=0, anchor='w')
        l1.place(relheight=0.030, relwidth=0.2450, relx=0.723, rely=0.5)
        self.files_box.insert(0, "\n")
        self.files_box.place(relheight=0.3465, relwidth=0.2680, relx=0.723, rely=0.5)
        self.scrollbar(0.92, self.files_box)

    def chat_window_button_builder(self):
        """
        This method creates all the other widgets inside the chat room
        :return:
        """
        self.chat_window.title("Walk2Talk")
        self.chat_window.resizable(width=FALSE, height=FALSE)
        self.chat_window.configure(width=700, height=600)

        # Client msg box:
        """
        This is the Entry for the client to send messages on.
        """
        self.client_msg = Entry(self.chat_window, font=("Helvetica", 13))
        self.client_msg.insert(0, "Type message here...")
        self.client_msg.place(relheight=0.0450, relwidth=0.6915, relx=0.014, rely=0.9480)
        self.client_msg.bind("<FocusIn>", self.default_text)
        self.client_msg.bind("<FocusOut>", self.default_text)

        # emoji box:
        """
        This is the Optionmenu for the client to choose emojis from
        """
        value_inside = StringVar(self.chat_window)
        options_list = [HAPPY, LAUGH, WINK, SMILE, LOVE, SMIRK, OOF, KISS, ANGRY, CRY, CORONA]
        value_inside.set("Emojis")
        question_menu = OptionMenu(self.chat_window, value_inside, *options_list,
                                   command=lambda event: self.controller.send_emoji(msg=self.client_msg,
                                                                                    Emoji=value_inside.get()))
        question_menu.place(relheight=0.0450, relwidth=0.135, relx=0.8580, rely=0.9480)

        # msg_details:
        """
        This is an updating text box that will display the person you're talking to and which chat is it (private/broadcast)
        """
        msg_details = Text(self.chat_window, font=("Helvetica", 13))
        msg_details.insert('1.0', "To: Everyone")
        msg_details.config(state=DISABLED)
        msg_details.place(relheight=0.0450, relwidth=0.6915, relx=0.014, rely=0.8983)
        self.names_box.bind("<<ListboxSelect>>", lambda event: self.controller.update_send_to(event, msg_details))

        # send msg button:
        """
        This is the send message button which sends the message the client wrote inside the entry
        """
        # TODO: make receiver viable
        send_msg = Button(self.chat_window, text="Send", borderwidth=0, fg='navy', font=("Helvetica", 13),
                          command=lambda: self.controller.send_msg(chat_box=self.chat_box, msg_box=self.client_msg,
                                                                   names_box=self.names_box,
                                                                   msg_details=msg_details))
        send_msg.place(relheight=0.0450, relwidth=0.135, relx=0.7210, rely=0.9480)

        # Download Button:
        """
        This is the Download button, it will send the file to our client
        """
        download = Button(self.chat_window, text="Download", borderwidth=0, fg='navy', font=("Helvetica", 13),
                          command=self.controller.download)
        download.place(relheight=0.0450, relwidth=0.270, relx=0.7210, rely=0.8983)

        # disconnect button:
        """
        This is the exit button
        """
        exit_chat = Button(self.chat_window, text="Exit", borderwidth=0, fg='navy', font=("Helvetica", 13),
                           command=lambda: self.controller.exit_chat(self.chat_login, self.chat_window))
        exit_chat.place(relheight=0.0440, relwidth=0.065, relx=0.0075, rely=0.0073)

        # clear chat button:
        """
        This button clears the chat box messages 
        """
        clear_chat = Button(self.chat_window, text="Clear Chat", borderwidth=0, fg='navy', font=("Helvetica", 13),
                            command=lambda: self.controller.clear_chat(self.chat_box))
        clear_chat.place(relheight=0.03, relwidth=0.12, relx=0.0075, rely=0.06)

        # get clients button:
        """
        This button shows the clients in the server
        """
        get_clients = Button(self.chat_window, text="Show Connected", borderwidth=0, fg='navy', font=("Helvetica", 13),
                             command=lambda: self.controller.get_clients())
        get_clients.place(relheight=0.0440, relwidth=0.2650, relx=0.7255, rely=0.002)

        # get files button
        """
        This button shows the files in the server
        """
        get_files = Button(self.chat_window, text="Show Files", borderwidth=0, fg='navy', font=("Helvetica", 13),
                           command=self.controller.get_files)
        get_files.place(relheight=0.0440, relwidth=0.2650, relx=0.7255, rely=0.0485)

    def scrollbar(self, x: float, txt):
        """
        This method creates the scroll bar for the chat boxes
        :param x: representing float number for locating the bar
        :param txt: a text box to place the scroll bar on
        :return:
        """
        scrollbar = Scrollbar(txt, cursor='dot', orient=VERTICAL)
        scrollbar.place(relheight=1, relx=x)
        txt.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=txt.yview)

    def generate_background(self, name: str, window):
        # TODO: make this resizable
        """
        This method generates the background for our chat box,
        :return:
        """
        # Background load:
        template = Image.open(self.images_path + name)
        img = ImageTk.PhotoImage(template)
        bg = Label(window, image=img)
        bg.image = img
        bg.pack(side='top', fill='both', expand='yes')


if __name__ == '__main__':
    Room()
