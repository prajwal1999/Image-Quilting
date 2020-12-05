from tkinter import *
from os import listdir
from os.path import isfile, join
path = './dataset/synthesis/'
from quilting import quilting
from PIL import ImageTk, Image
test_images = [f for f in listdir(path) if isfile(join(path, f))]

root = Tk()
# Code to add widgets will go here...
root.geometry("1024x768")
test = Label(text="Image Quilting for Texture Synthesis")
test.pack()

# file select
var = StringVar(root)
var.set(test_images[0]) # default value
w = OptionMenu(root, var, *test_images)
w.pack()
def image_selected():
    name = var.get().split('.')[0]
    ext = var.get().split('.')[1]
    # img = ImageTk.PhotoImage(Image.open(path+name+'.'+ext))
    # panel = Label(root, image = img)
    # panel.pack(side = "bottom", fill = "both", expand = "yes")
    # print ("selected image " + name + " " + ext)
    # quilting(path+name+'.'+ext, path+'results/'+name+'_result.'+ext)
button = Button(root, text="Load", command=image_selected)
button.pack()

img = ImageTk.PhotoImage(Image.open(path+'t1.png'))
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

root.mainloop()