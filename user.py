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
root.minsize(922, 600)
root.title('Image Quilting for Texture Synthesis')
root.configure(background="#ffffff")

ref_img = ImageTk.PhotoImage(Image.open(path+test_images[0].split('.')[0]+'.'+test_images[0].split('.')[1] ))
panel1 = Label(root, image = ref_img)
panel1.grid(row=2, pady=50, padx=50)

selected_name = test_images[0].split('.')[0]
selected_ext = test_images[0].split('.')[1]
# functions
def image_selected():
    global selected_name 
    selected_name = var.get().split('.')[0]
    global selected_ext 
    selected_ext = var.get().split('.')[1]
    img = ImageTk.PhotoImage(Image.open(path+selected_name+'.'+selected_ext))
    panel1.configure(image=img)
    panel1.image = img
    print ("selected image " + selected_name + " " + selected_ext)

def start_simulation():
    quilting(path+selected_name+'.'+selected_ext, path+'results/'+selected_name+'_result.'+selected_ext)



# file select
var = StringVar(root)
var.set(test_images[0]) # default value
w = OptionMenu(root, var, *test_images)
w.configure(width=15, height=3, font=25, bg="#000000", fg="#ffffff")
w['menu'].configure(font=25, bg="#000000", fg="#ffffff")
w.grid(row=0, column=0, padx=20, pady=20)

load_btn = Button(root, text="Load", command=image_selected, width=15, height=3, bg="#000000", fg="#ffffff", font=25) 
load_btn.grid(row=0, column=5, padx=20, pady=20)

start_btn = Button(root, text="Start", command=start_simulation, width=15, height=3, bg="#000000", fg="#ffffff", font=25) 
start_btn.grid(row=0, column=6, padx=20, pady=20)


root.mainloop()