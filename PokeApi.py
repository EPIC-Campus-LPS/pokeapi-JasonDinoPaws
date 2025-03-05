import requests
import cv2
import numpy as np
from tkinter import Tk,Canvas,Label,Entry

# A bunch of vars
path = "".join(x+"/" for x in __file__.split("/")[:-1])
root = Tk()
root.title("Pokédex")
root.config(background="#000000")
can = Canvas(root,background="#000000",highlightthickness=0)
nam = Label(can,bg="white",highlightthickness=0,font=("Arial",15,"bold"))

Left = {"Name":1,"Size":5,"R":2,"G":1,"B":0}
Entrys = []
images = []


# Creates the image from a array for each pixel mulitplyed by the size and given a color based off of the variables
def CreateImage(img):
    global root,can
    if type(img) == type(None):
        return
    
    can.delete("all")
    for r in range(len(img)):
        y1 = r*Left["Size"]
        y2 = y1+Left["Size"]
        for c in range(len(img[r])):
            x1 = c*Left["Size"]
            x2 = x1+Left["Size"]
            color = (img[r,c,Left["R"]],img[r,c,Left["G"]],img[r,c,Left["B"]])

            if img[r][c][0] != 0:
                can.create_rectangle(x1,y1,x2,y2,outline="",fill="#%02x%02x%02x" % color )
    can.config(height=len(img)*Left["Size"],width=len(img[0])*Left["Size"])
    root.update()

# checks if the link is valid for the iamge
def GetImage(link):
    if link:
        img = requests.get(link)
        if img.status_code == 200:
            img = np.asarray(bytearray(img.content), dtype="uint8")
            return cv2.imdecode(img, cv2.IMREAD_COLOR)
    return

# If a entry is unfocused a and trys to set it to a value
def Out(en,x=""):
    global images
    if x == "":
        data = en.widget.get()
        for x,ent in Entrys:
            if ent == en.widget:
                break
        else:
            return
    else:
        data = en.get()

    if x in ["R","G","B"] and data.isdigit():
        if int(data) >= 0 and int(data) < 3:
            Left[x] = int(data)
    elif x == "Size" and data.isdigit() and int(data) >= 3 and int(data) <= 12: 
        Left[x] = int(data)

    elif x == "Name":
        page = requests.get(f"https://pokeapi.co/api/v2/pokemon/{data}",json=True)

        if page.status_code == 200:
            js = page.json()

            name = js["name"]
            images = [
                GetImage(js["sprites"]["front_default"]),
                GetImage(js["sprites"]["back_default"]),
                GetImage(js["sprites"]["front_female"]),
                GetImage(js["sprites"]["back_female"]),


                GetImage(js["sprites"]["front_shiny"]),
                GetImage(js["sprites"]["back_shiny"]),
                GetImage(js["sprites"]["front_shiny_female"]),
                GetImage(js["sprites"]["back_shiny_female"]),
            ]

            nam.config(text=name)

    CreateImage(images[0])


root.bind_class("Entry", "<FocusOut>", Out)

# Places and loads in all items like the canvas and the Entrys
yp = 5
for N in Left.keys():
    ent =  Entry(root)
    Label(root,text=N).place(x=5,y=yp)
    ent.insert(0,Left[N])
    ent.place(x=5,y=yp+20)
    Entrys.append([N,ent])
    Out(ent,N)
    yp += 50

can.pack()
nam.place(x=5,y=5)

root.mainloop()