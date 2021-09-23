from tkinter import *
from tkinter import filedialog, Text
from tkinter import messagebox
from PIL import ImageTk, Image
import encryptModule
import decryptModule
import os
from pathlib import Path, PureWindowsPath

# creating window
root = Tk()
root.title('Image Encryption And Decryption')

# creating a canvas inside window
canvas = Canvas(root, height=400, width=400, bg="#263042")
canvas.pack()

# creating a frame inside canvas
frame = Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


# creating a label to show image in frame
label = Label(frame)
label.pack()

# function to select image and to show in frame


def select_image():
    global path_to_image
    path_to_image = filedialog.askopenfilename(initialdir="/",
                                               title="Open File",
                                               filetypes=(("PNGS", "*.png"), ("GIFs", "*.gif"), ("All Files", "**")))
    image = Image.open(path_to_image)
    photo = ImageTk.PhotoImage(image.resize((300, 300), Image.ANTIALIAS))

    # label = Label(frame, image=photo)
    label.configure(image=photo)
    label.image = photo
    # label.pack()


def image_encryption():
    encryptModule.encrypt_image(path_to_image)
    path = "C:/Users/himan/Desktop/B.Tech(CSE)/6th sem/Mini Project/imageEncryption_HimanshuPanwar/encrypted/encrypted_image.png"

    image = Image.open(path)
    photo = ImageTk.PhotoImage(image.resize((300, 300), Image.ANTIALIAS))

    label.configure(image=photo)
    label.image = photo
    # label.pack()

    messagebox.showinfo('Message title', 'encryption done')


def image_decryption():
    decryptModule.decrypt_image()
    path = "C:/Users/himan/Desktop/B.Tech(CSE)/6th sem/Mini Project/imageEncryption_HimanshuPanwar/decrypted/decrypted_image.png"

    image = Image.open(path)
    photo = ImageTk.PhotoImage(image.resize((300, 300), Image.ANTIALIAS))

    label.configure(image=photo)
    label.image = photo

    messagebox.showinfo('Message title', 'decryption done')


# creating buttons
openImage = Button(root, text="open image", padx=10,
                   pady=5, fg="white", bg="#263042", command=select_image)
openImage.pack(side=LEFT)

encrypt = Button(root, text="encrypt", padx=10,
                 pady=5, fg="white", bg="#263042", command=image_encryption)
encrypt.pack(side=LEFT)

decrypt = Button(root, text="decrypt", padx=10,
                 pady=5, fg="white", bg="#263042", command=image_decryption)
decrypt.pack(side=LEFT)


# running gui
root.mainloop()
