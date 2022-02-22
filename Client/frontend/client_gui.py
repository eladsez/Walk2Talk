import tkinter.font
from tkinter import *
from PIL import ImageTk, Image
from Client.Controller.Controller import Controller
import os
import webbrowser
from Client.frontend.Emoji import *
from Utilities import Misc


class Room:
    """
    This clas is responsible for creating the Gui for our chat.
    in particular - LOGIN window & Chat room window
    """

    def __init__(self):
        # This is the chat window, it will be hidden for new users until they join the room.
        self.chat_window = Tk()
        # self.chat_window.configure(bg="#093545")
        # imgs abs paths:
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        parent_path = Misc.resource_path(relative_path='frontend')
        self.images_path = parent_path + "/imgs/"
        # TXT BOXES:
        self.chat_box = None  # TODO: find better solution
        self.names_box = None
        self.files_box = None
        self.username_entry = None
        self.client_msg = None
        self.password_entry = None
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
        This method makes the text go vrom vrom disappear when pressing the box ( it only occurs once for some reason)
        :param event:
        :return:
        """
        widget = event.widget
        text = widget.get()
        hint_color = '#315B6A'
        if text == "Password":
            self.password_entry.config(fg='black')
            self.password_entry.delete(0, END)
            self.password_entry.config(show="*");
            return
        elif text == '' and widget is self.password_entry:
            self.password_entry.config(fg=hint_color)
            self.password_entry.config(show="");
            self.password_entry.insert(END, 'Password')
            return
        if text == "Username":
            self.username_entry.config(fg='black')
            self.username_entry.delete(0, END)
            return
        elif text == '' and widget is self.username_entry:
            self.username_entry.config(fg=hint_color)
            self.username_entry.insert(END, 'Username')
            return
        if text == 'Type message here...':
            self.client_msg.config(fg='black')
            self.client_msg.delete(0, END)
            return
        elif text == '' and widget is self.client_msg:
            self.client_msg.config(fg=hint_color)
            self.client_msg.insert(END, 'Type message here...')
            return

    def chat_login_builder(self):
        """
        This method creates the login window
        :return:
        """
        font_box = tkinter.font.Font(family="Lexend Deca", size=10)
        font_text = tkinter.font.Font(family="Montserrat", size=11)
        self.chat_login.title("Login")
        self.chat_login.configure(width=600, height=800)
        # create background:
        self.generate_background(name="Login_temlate.png", window=self.chat_login)

        # name label & entry:
        self.username_entry = Entry(self.chat_login, font=font_box, bg="#224957", fg='#315B6A', borderwidth=0)
        self.username_entry.place(relheight=0.0580, relwidth=0.36, relx=0.32, rely=0.42)
        self.username_entry.insert(0, "Username")
        self.password_entry = Entry(self.chat_login, font=font_box, bg="#224957", fg='#315B6A', borderwidth=0)
        self.password_entry.place(relheight=0.0580, relwidth=0.36, relx=0.32, rely=0.56)
        self.password_entry.insert(0, "Password")
        # Appearing and reappearing text:
        self.username_entry.bind("<FocusIn>", self.default_text)
        self.username_entry.bind("<FocusOut>", self.default_text)
        self.password_entry.bind("<FocusIn>", self.default_text)
        self.password_entry.bind("<FocusOut>", self.default_text)

        # checkbutton_img = ImageTk.PhotoImage(Image.open((self.images_path + 'Remember me.png')))
        # Label(self.chat_login, image=checkbutton_img, borderwidth=0).\
        #     place(relx=0.1, rely=0.5)

        forgot_password = Label(self.chat_login, font=font_text, text='Forgot password?', fg='#20DF7F', bg='#093545')
        forgot_password.place(relx=0.55, rely=0.66, relheight=0.035, relwidth=0.15)
        forgot_password.bind('<Button-1>', lambda event: webbrowser.open_new_tab(
            'https://previews.123rf.com/images/channarongsds/channarongsds1806/channarongsds180600192/102871142-hand-drawing-vintage-style-middle-finger-show.jpg?fj=1'))
        # connect button:
        button_img = ImageTk.PhotoImage(Image.open(self.images_path + 'Login_btn.png'))
        login_button = Label(self.chat_login, borderwidth=0, image=button_img, bg='#093545')
        login_button.place(relx=0.3051, rely=0.727, relheight=0.1, relwidth=0.39)
        login_button.image = button_img
        login_button.bind('<Button-1>', lambda event: self.controller.connect(self.chat_login,
                                                                              self.chat_window,
                                                                              self.username_entry,
                                                                              self.chat_box,
                                                                              self.files_box,
                                                                              self.names_box))
        # Bind the Enter Key to connect the server
        self.chat_login.bind('<Return>', lambda event: self.controller.connect(self.chat_login,
                                                                               self.chat_window,
                                                                               self.username_entry,
                                                                               self.chat_box,
                                                                               self.files_box,
                                                                               self.names_box))

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
        # self.chat_window.resizable(width=FALSE, height=FALSE)
        self.chat_window.configure(width=700, height=600)

        # Client msg box:
        """
        This is the Entry for the client to send messages on.
        """
        self.client_msg = Entry(self.chat_window, font=("Helvetica", 13))
        self.client_msg.config(fg='gray')
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
        open_send = Image.open((self.images_path + 'button_send.png'))
        send_img = ImageTk.PhotoImage(open_send)
        send_msg = Button(self.chat_window, image=send_img, bg='#57D0FF', borderwidth=50,
                          command=lambda: self.controller.send_msg(chat_box=self.chat_box, msg_box=self.client_msg,
                                                                   msg_details=msg_details))
        send_msg.image = send_img
        # send_msg.bind('<Configure>', lambda event: self.resize_image(event, open_send, send_msg))
        send_msg.place(relheight=0.0460, relwidth=0.135, relx=0.7210, rely=0.9480)
        # Bind the Enter Key to send a massage
        self.chat_window.bind('<Return>', lambda event: self.controller.send_msg(chat_box=self.chat_box,
                                                                                 msg_box=self.client_msg,
                                                                                 msg_details=msg_details))

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

    @staticmethod
    def resize_image(event, template_copy, bg):
        new_width = event.width - 4
        new_height = event.height - 4
        template = template_copy.resize((new_width, new_height))
        img = ImageTk.PhotoImage(template)
        bg.config(image=img)
        bg.image = img  # avoid garbage collection

    def generate_background(self, name: str, window):
        """
        This method generates the background for our chat box,
        :return:
        """
        # Background load:
        template = Image.open(self.images_path + name)
        img = ImageTk.PhotoImage(template)
        bg = Label(window, image=img)
        bg.image = img
        bg.pack(fill=BOTH, expand=YES)
        bg.bind('<Configure>', lambda event: Room.resize_image(event, template.copy(), bg))


if __name__ == '__main__':
    Room()
