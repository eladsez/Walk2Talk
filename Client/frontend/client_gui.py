import tkinter.font
from tkinter import *
from PIL import ImageTk, Image
from Client.Controller.Controller import Controller
import os
import webbrowser
from Client.frontend.Emoji import *
from Utilities import Misc
from tkinter import ttk
from ttkthemes.themed_style import ThemedStyle


class Room:
    """
    This class is responsible for creating the Gui for our chat.
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
        self.username_entry = None
        self.client_msg = None
        self.password_entry = None
        # char room window
        # create background:
        self.generate_background(name="chat_template.png", window=self.chat_window)
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

    def chat_login_builder(self):
        """
        This method creates the login window
        :return:
        """
        font_box = tkinter.font.Font(family="Lexend Deca", size=10)
        font_text = tkinter.font.Font(family="Montserrat", size=11)
        self.chat_login.title("Login")
        self.chat_login.configure(width=550, height=600)
        # create background:
        self.generate_background(name="Login_temlate.png", window=self.chat_login)

        # name label & entry:
        self.username_entry = Entry(self.chat_login, font=font_box, bg="#224957", fg='#315B6A', borderwidth=0
                                    , highlightthickness=0)
        self.username_entry.place(relheight=0.06, relwidth=0.6, relx=0.2, rely=0.395)
        self.username_entry.insert(0, "Username")
        self.password_entry = Entry(self.chat_login, font=font_box, bg="#224957", fg='#315B6A', borderwidth=0
                                    , highlightthickness=0)
        self.password_entry.place(relheight=0.06, relwidth=0.6, relx=0.2, rely=0.514)
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
        forgot_password.place(relx=0.58, rely=0.611, relheight=0.035, relwidth=0.23)
        forgot_password.bind('<Button-1>', lambda event: webbrowser.open_new_tab(
            'https://previews.123rf.com/images/channarongsds/channarongsds1806/channarongsds180600192/102871142-hand-drawing-vintage-style-middle-finger-show.jpg?fj=1'))

        # connect button:
        button_img = ImageTk.PhotoImage(Image.open(self.images_path + 'Login_btn.png'))
        button_press_img = ImageTk.PhotoImage(Image.open(self.images_path + 'Login_press_btn.png'))
        login_button = Label(self.chat_login, borderwidth=0, image=button_img, bg='#093545')
        login_button.place(relx=0.1893, rely=0.69, relheight=0.09, relwidth=0.61)
        login_button.image = button_img
        login_button.image_press = button_press_img
        login_button.bind('<Button-1>', lambda event: self.controller.connect(self.chat_login,
                                                                              self.chat_window,
                                                                              self.username_entry,
                                                                              self.chat_box,
                                                                              self.files_box,
                                                                              self.names_box,
                                                                              event))
        login_button.bind('<ButtonRelease-1>', lambda event: login_button.config(image=button_img))

        # Bind the Enter Key to user name and password entry in order to connect the server
        self.username_entry.bind('<Return>', lambda event: self.controller.connect(self.chat_login,
                                                                                   self.chat_window,
                                                                                   self.username_entry,
                                                                                   self.chat_box,
                                                                                   self.files_box,
                                                                                   self.names_box))
        self.password_entry.bind('<Return>', lambda event: self.controller.connect(self.chat_login,
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
        self.chat_box = Text(self.chat_window, font=("Helvetica", 14), bg="#224957",
                             fg="#EAECEE", borderwidth=0, highlightthickness=0)
        self.chat_box.config(state=DISABLED)
        self.chat_box.place(relheight=0.54, relwidth=0.71, relx=0.022, rely=0.159)
        self.scrollbar(0.972, self.chat_box)

        # client box:
        """
        This is the list box where all the clients will appear
        """
        conn_label = Label(self.chat_window, text="Connected: ", font=("Helvetica", 14), bg="#224957", fg='white',
                           anchor='w')
        conn_label.place(relheight=0.023, relwidth=0.2, relx=0.761, rely=0.16)
        self.names_box = Listbox(self.chat_window, font=("Helvetica", 14), bg="#224957",
                                 fg="#EAECEE", selectmode=SINGLE, borderwidth=0, highlightthickness=0)
        self.names_box.insert(1, "Everyone")
        self.names_box.place(relheight=0.21, relwidth=0.22, relx=0.761, rely=0.19)
        self.scrollbar(0.92, self.names_box)

        # files BOX:
        """
        This is the list box where the files of the server will appear
        """
        files_label = Label(self.chat_window, text="Files: ", font=("Helvetica", 14), bg="#224957", fg='white',
                            anchor='w')
        files_label.place(relheight=0.023, relwidth=0.2, relx=0.761, rely=0.46)
        self.files_box = Listbox(self.chat_window, font=("Helvetica", 14), bg="#224957",
                                 fg="#EAECEE", borderwidth=0, highlightthickness=0)
        self.files_box.place(relheight=0.21, relwidth=0.22, relx=0.761, rely=0.49)
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
        self.client_msg = Entry(self.chat_window, font=("Helvetica", 13), bg='#224957', borderwidth=0
                                , highlightthickness=0)
        self.client_msg.config(fg='#315B6A')
        self.client_msg.insert(0, "Type message here...")
        self.client_msg.place(relheight=0.0450, relwidth=0.701, relx=0.025, rely=0.861)
        self.client_msg.bind("<FocusIn>", self.default_text)
        self.client_msg.bind("<FocusOut>", self.default_text)

        # Bind the Enter Key to send a massage
        self.client_msg.bind('<Return>', lambda event: self.controller.send_msg(chat_box=self.chat_box,
                                                                                msg_box=self.client_msg,
                                                                                msg_details=msg_details))

        # msg_details:
        """
        This is an updating text box that will display the person you're talking to and which chat is it (private/broadcast)
        """
        msg_details = Text(self.chat_window, font=("Helvetica", 13), bg='#224957', fg='white', borderwidth=0
                           , highlightthickness=0)
        msg_details.insert('1.0', "To: Everyone")
        msg_details.config(state=DISABLED)
        msg_details.place(relheight=0.0450, relwidth=0.701, relx=0.025, rely=0.782)
        self.names_box.bind("<<ListboxSelect>>", lambda event: self.controller.update_send_to(event, msg_details))

        # send msg button:
        """
        This is the send message button which sends the message the client wrote inside the entry
        """
        open_send = Image.open((self.images_path + 'send btn.png'))
        send_img = ImageTk.PhotoImage(open_send)
        open_send_press = Image.open((self.images_path + 'send_btn_press.png'))
        send_press_img = ImageTk.PhotoImage(open_send_press)
        send_msg = Label(self.chat_window, image=send_img, borderwidth=0, bg='#093545')
        send_msg.image = send_img
        send_msg.image_press = send_press_img
        send_msg.bind('<Button-1>', lambda event: self.controller.send_msg(chat_box=self.chat_box,
                                                                           msg_box=self.client_msg,
                                                                           msg_details=msg_details,
                                                                           event=event))
        send_msg.bind('<ButtonRelease-1>', lambda event: send_msg.config(image=send_img))
        send_msg.place(relx=0.7535, rely=0.855)

        # Download Button:
        """
        This is the Download button, it will send the file to our client
        """
        open_download = Image.open((self.images_path + 'download_btn.png'))
        download_img = ImageTk.PhotoImage(open_download)
        download = Label(self.chat_window, image=download_img, borderwidth=0, bg='#093545')
        download.image = download_img
        open_download_press = Image.open((self.images_path + 'download_btn_press.png'))
        download_press_image = ImageTk.PhotoImage(open_download_press)
        download.image_press = download_press_image
        download.bind('<Button-1>', lambda event: self.controller.download(self.files_box, event))
        download.bind('<ButtonRelease-1>', lambda event: download.config(image=download_img))
        download.place(relx=0.7535, rely=0.772)

        # disconnect button:
        """
        This is the exit button
        """
        open_exit = Image.open((self.images_path + 'exit btn.png'))
        exit_img = ImageTk.PhotoImage(open_exit)
        exit_chat = Label(self.chat_window, borderwidth=0, image=exit_img, bg='#093545')
        exit_chat.image = exit_img
        exit_chat.bind('<Button-1>', lambda event: self.controller.exit_chat(self.chat_login, self.chat_window))
        exit_chat.place(relx=0.002, rely=0.04)

        # clear chat button:
        """
        This button clears the chat box messages 
        """
        open_clear = Image.open((self.images_path + 'clear_btn.png'))
        clear_img = ImageTk.PhotoImage(open_clear)
        clear_press_open = Image.open((self.images_path + 'clear_btn_press.png'))
        clear_press_image = ImageTk.PhotoImage(clear_press_open)
        clear_chat = Label(self.chat_window, text="Clear Chat", borderwidth=0, image=clear_img, bg='#224957')
        clear_chat.image = clear_img
        clear_chat.image_press = clear_press_image
        clear_chat.bind('<Button-1>', lambda event: self.controller.clear_chat(self.chat_box, event))
        clear_chat.bind('<ButtonRelease-1>', lambda event: clear_chat.config(image=clear_img))

        clear_chat.place(relx=0.655, rely=0.642)

        # get clients button:
        """
        This button shows the clients in the server
        """
        open_get = Image.open((self.images_path + 'refresh btn.png'))
        get_img = ImageTk.PhotoImage(open_get)
        get_clients = Label(self.chat_window, borderwidth=0, image=get_img, bg='#224957')
        get_clients.image = get_img
        open_get_press = Image.open((self.images_path + 'refresh_btn_press.png'))
        get_img_press = ImageTk.PhotoImage(open_get_press)
        get_clients.image_press = get_img_press
        get_clients.bind('<Button-1>', lambda event: self.controller.get_clients(event))
        get_clients.bind('<ButtonRelease-1>', lambda event: get_clients.config(image=get_img))
        get_clients.place(relx=0.935, rely=0.35)

        # get files button
        """
        This button shows the files in the server
        """
        get_files = Label(self.chat_window, borderwidth=0, image=get_img, bg='#224957')
        get_files.image_press = get_img_press
        get_files.bind('<Button-1>', lambda event: self.controller.get_files(event))
        get_files.bind('<ButtonRelease-1>', lambda event: get_files.config(image=get_img))
        get_files.place(relx=0.935, rely=0.649)

        # emoji box:
        """
        This is the Optionmenu for the client to choose emojis from
        """
        style = ThemedStyle()
        style.configure("TMenubutton", background="#224957", borderwidth=0)
        value_inside = StringVar(self.chat_window)
        options_list = [HAPPY, LAUGH, WINK, SMILE, LOVE, SMIRK, OOF, KISS, ANGRY, CRY, CORONA]
        value_inside.set(HAPPY)
        question_menu = ttk.OptionMenu(self.chat_window, value_inside, *options_list,
                                       command=lambda event: self.controller.send_emoji(msg=self.client_msg,
                                                                                        Emoji=value_inside.get()))
        question_menu.place(relheight=0.0450, relwidth=0.05, relx=0.68, rely=0.86)
        question_menu["menu"].config(bg="#20DF7F", fg="#224957", borderwidth=0)

    def scrollbar(self, x: float, txt):
        """
        This method creates the scroll bar for the chat boxes
        :param x: representing float number for locating the bar
        :param txt: a text box to place the scroll bar on
        :return:
        """
        style = ThemedStyle()
        style.theme_use('breeze')
        style.configure("Vertical.TScrollbar", background="#224957")
        scrollbar = ttk.Scrollbar(txt, orient=VERTICAL, cursor='dot')
        scrollbar.place(relheight=1, relx=x)
        txt.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=txt.yview)

    def default_text(self, event):
        """
        This method makes the text go vrom vrom disappear when pressing the box (it only occurs once for some reason)
        :param event:
        :return:
        """
        widget = event.widget
        text = widget.get()
        hint_color = '#315B6A'
        if text == "Password":
            self.password_entry.config(fg='#20DF7F')
            self.password_entry.delete(0, END)
            self.password_entry.config(show="*")
            return
        elif text == '' and widget is self.password_entry:
            self.password_entry.config(fg=hint_color)
            self.password_entry.config(show="")
            self.password_entry.insert(END, 'Password')
            return
        if text == "Username":
            self.username_entry.config(fg='#20DF7F')
            self.username_entry.delete(0, END)
            return
        elif text == '' and widget is self.username_entry:
            self.username_entry.config(fg=hint_color)
            self.username_entry.insert(END, 'Username')
            return
        if text == 'Type message here...':
            self.client_msg.config(fg='white')
            self.client_msg.delete(0, END)
            return
        elif text == '' and widget is self.client_msg:
            self.client_msg.config(fg=hint_color)
            self.client_msg.insert(END, 'Type message here...')
            return

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
