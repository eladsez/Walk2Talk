"""
This is a well designed creator for labels,buttons,texts, etc
we chose to pass on it for now because had hard time integrate inside the project
"""
# # Server msg box:
# self.creator(operator="Text", text="", command=0.974, relheight=0.6530,
#              relwidth=0.6980, relx=0.0080,
#              rely=0.19)
#
# # Data BOX:
# self.creator(operator="Text", text="", command=0.92, relheight=0.6530,
#              relwidth=0.2680, relx=0.723,
#              rely=0.19)
#
# # Client msg box:
# self.creator(operator="Entry", text="", command=None, relheight=0.1050,
#              relwidth=0.6975, relx=0.01,
#              rely=0.8875)
#
# # disconnect button:
# self.creator(operator="Button", text="Exit Chat", command=Controller.disconnect, relheight=0.0570,
#              relwidth=0.1190, relx=0.0080,
#              rely=0.0075)
#
# # send msg button:
# self.creator(operator="Button", text="Send", command=Controller.send_msg, relheight=0.1050,
#              relwidth=0.135, relx=0.7180,
#              rely=0.8875)
#
# # send all button:
# self.creator(operator="Button", text="Send All", command=Controller.send_all, relheight=0.1050,
#              relwidth=0.135, relx=0.8580,
#              rely=0.8875)
#
# # get clients button:
# self.creator(operator="Button", text="Show Connected", command=Controller.get_clients, relheight=0.0570,
#              relwidth=0.2680, relx=0.7250,
#              rely=0.0075)
#
# # files / clients label:
# self.creator(operator="Label", text="Files/Connected Clients", command=None, relheight=0.0650,
#              relwidth=0.27, relx=0.723,
#              rely=0.0750)
#
# # get files button
# self.creator(operator="Button", text="Show Files", command=Controller.get_files, relheight=0.0570,
#              relwidth=0.2680, relx=0.442,
#              rely=0.0075)
#
# # clear chat button:
# self.creator(operator="Button", text="Clear Chat", command=Controller.clear_chat, relheight=0.0650,
#              relwidth=0.27, relx=0.442,
#              rely=0.0750)
#
#
# def creator(self, operator: str, text: str, command, relheight: float, relwidth: float, relx: float, rely: float):
#     """
#     This method is a creator for the objects we present in the window
#     :param operator: operator to tell the method which object to create
#     :param text: Name of the object
#     :param command: a method to operate on the button, on Text its used as a scrollbar y position
#     :param relheight: float representing height of object
#     :param relwidth: float representing width of object
#     :param relx: float representing x pos of the object
#     :param rely: float representing y pos of the object
#     :return: None
#     """
#     parts = None
#     if operator == 'Button':
#         parts = Button(self.chat_window, text=text, command=command)
#     if operator == 'Label':
#         parts = Label(self.chat_window, text=text)
#     if operator == 'Entry':
#         parts = Entry(self.chat_window)
#     if operator == 'Text':
#         parts = Text(self.chat_window, font=("Helvetica", 32))
#         parts.config(state=DISABLED)
#         # scrollbar:
#         scrollbar = Scrollbar(parts)
#         scrollbar.place(relheight=1, relx=command)
#         scrollbar.config(command=parts.yview)
#     parts.place(relheight=relheight, relwidth=relwidth, relx=relx, rely=rely)

# Import the tkinter library
