from tkinter import Tk, ttk, BOTH, YES
from PIL import ImageTk
from PIL import Image
from Utilities import Misc

images_path = Misc.resource_path(relative_path='frontend') + "/imgs/"

root = Tk()
root.title("Title")


def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo  # avoid garbage collection


image = Image.open('./imgs/Login Page design.png')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = ttk.Label(root, image=photo)
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand=YES)
root.mainloop()
