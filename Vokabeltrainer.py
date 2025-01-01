from tkinter import *
from tkinter import ttk
import os
from PIL import Image, ImageTk
import random
from argparse import ArgumentParser

"""
parser = ArgumentParser()
parser.add_argument("vokabelkasten", type=str)
args = parser.parse_args()
vokabelkasten = args.vokabelkasten
"""
vokabelkasten="Krimi"

os.chdir("Vokabelkästen/"+vokabelkasten)

backgroundcolor = "hotpink3"#"aquamarine4"
STUFEN = 6

root = Tk()
s = ttk.Style()
s.configure('frm.TFrame', background=backgroundcolor)
root.configure(bg=backgroundcolor)
frm = ttk.Frame(root, padding=10,style="frm.TFrame")
frm.grid()
s2 = ttk.Style()
s2.configure("button.TButton",background=backgroundcolor)
list_of_lections = Text(master=frm,width=20)
list_of_lections.grid(column=4,row=0)
lektion_variable = StringVar()
lektion_to_load = ttk.Entry(frm,textvariable=lektion_variable)
lektion_to_load.grid(column=2,row=1)
img = Image.open("Vokabelkarte.png")
img = ImageTk.PhotoImage(img)

class Vokabel:
    def __init__(self):
        self.w1 = ""
        self.w2 = ""
        self.stufe = 0
    def setValues(self,w1,w2,stufe):
        self.w1 = w1
        self.w2 = w2
        self.stufe = stufe
    def getValues(self):
        return self.w1,self.w2,self.stufe

def createLection():
    def read_in():
        text = textbox.get(1.0,END)
        name = lektionsname.get(1.0,END)
        with open("Lektionen/"+name.strip()+".txt","w",encoding="utf-8") as f:
            f.write(text)
        lektionen_aktualisieren()
        window2.destroy()
    window2 = Tk()
    window2.configure(bg=backgroundcolor)
    lektionsname = Text(master=window2, width=20, height=2, wrap='word')
    lektionsname.pack()
    textbox = Text(master=window2, width=40, height=4, wrap='word')
    button = ttk.Button(window2,text="Ok",command=read_in,style="button.TButton")#.grid(column=0,row=0)
    textbox.pack()
    button.pack()
    window2.mainloop()

    
def lektionen_aktualisieren():
    list_of_lections.delete(1.0,END) 
    start = 1.0
    for file in os.listdir("Lektionen"):
        list_of_lections.insert(start,file[:-4]+"\n")

def loadLektion():
    file = "Lektionen/"+lektion_variable.get()+".txt"
    vokabelkasten = eval(open("Vokabelkasten.txt","r",encoding="utf-8").readlines()[0])
    with open(file,"r",encoding="utf-8") as f:
        for line in f:
            w1,w2 = line.strip().split("\t")
            vokabelkasten[1].append((w1,w2))
    with open("Vokabelkasten.txt","w",encoding="utf-8") as v:
        v.write(str(vokabelkasten))

def showProgress():
    windowProgress = Toplevel()
    windowProgress.configure(bg=backgroundcolor)
    display = Text(master=windowProgress, width=40, height=200, wrap='word')
    display.grid(column=0,row=0)
    vokabelkasten = eval(open("Vokabelkasten.txt","r",encoding="utf-8").readlines()[0])
    for st in sorted(vokabelkasten):
        print(st)
        display.insert(END,"Stufe "+str(st)+"\n---------------\n")
        for word1,word2 in sorted(vokabelkasten[st]):
            display.insert(END,word1+"\t"+word2+"\n")
        display.insert(END,"\n")
    ttk.Button(windowProgress,text="Ok",command=windowProgress.destroy,style="button.TButton").grid(column=0,row=1)

    
def train():
    vokabelkasten2 = {x:[] for x in range(1,STUFEN+1)}
    def welle():
        alreadywritten = eingabefeld.get(1.0,END).strip()
        eingabefeld.delete(1.0,END)
        eingabefeld.insert(1.0,alreadywritten+"ã")
    def welle2():
        alreadywritten = eingabefeld.get(1.0,END).strip()
        eingabefeld.delete(1.0,END)
        eingabefeld.insert(1.0,alreadywritten+"õ")
    def c_mit_haken():
        alreadywritten = eingabefeld.get(1.0,END).strip()
        eingabefeld.delete(1.0,END)
        eingabefeld.insert(1.0,alreadywritten+"ç")
    def check():
        eingabe = eingabefeld.get(1.0,END).strip()
        if eingabe == w2:
            w = Label(window2, 
                 compound = CENTER,
                 fg="green",
                 text="🙂\n"+w2,
                 font =("Arial", 25),
                 image=img,width=300, height=200)
            w.grid(column=1,row=1)
            if stufe < STUFEN:
                vokabelkasten2[stufe+1].append((w1,w2))
        else:
            w = Label(window2, 
                 compound = CENTER,
                 fg="red",
                 text="😕\n"+w2,
                 font =("Arial", 25),
                 image=img,width=300, height=200)
            w.grid(column=1,row=1)
            vokabelkasten2[stufe].append((w1,w2))
    def nextVoc():
        global w1,w2,stufe
        try:
            w1,w2,stufe = next(words_to_learn)
            w = Label(window2, 
                compound = CENTER,
                text=w1,
                font=("Arial", 25),
                image=img,width=600, height=200)
            w.grid(column=1,row=1)
            return w1,w2,stufe
        except StopIteration:
            window2.destroy()
            with open("Vokabelkasten.txt","w",encoding="utf-8") as f:
                f.write(str(vokabelkasten2))
            showProgress()
    vokabelkasten = eval(open("Vokabelkasten.txt","r",encoding="utf-8").readlines()[0])
    wordlist = set()
    for st in vokabelkasten:
        for word1,word2 in vokabelkasten[st]:
            wordlist.add((word1,word2,st))
    wordlist = list(wordlist)
    random.shuffle(wordlist)
    words_to_learn = iter(wordlist)
    window2 = Toplevel()
    window2.configure(bg=backgroundcolor)
    eingabefeld = Text(master=window2, width=40, height=3, wrap='word')
    eingabefeld.grid(column=1,row=2)
    nextVoc()
    ttk.Button(window2,text="Check",command=check,style="button.TButton").grid(column=1,row=3)
    ttk.Button(window2,text="Next",command=nextVoc,style="button.TButton").grid(column=0,row=3)
    ttk.Button(window2,text="ã",command=welle,style="button.TButton").grid(column=0,row=4)
    ttk.Button(window2,text="õ",command=welle2,style="button.TButton").grid(column=2,row=4)
    ttk.Button(window2,text="ç",command=c_mit_haken,style="button.TButton").grid(column=1,row=4)

def gothrough():
    def welle():
        alreadywritten = eingabefeld.get(1.0,END).strip()
        eingabefeld.delete(1.0,END)
        eingabefeld.insert(1.0,alreadywritten+"ã")
    def welle2():
        alreadywritten = eingabefeld.get(1.0,END).strip()
        eingabefeld.delete(1.0,END)
        eingabefeld.insert(1.0,alreadywritten+"õ")
    def c_mit_haken():
        alreadywritten = eingabefeld.get(1.0,END).strip()
        eingabefeld.delete(1.0,END)
        eingabefeld.insert(1.0,alreadywritten+"ç")
    def check():
        w1,w2,stufe = aktuelle_vokabel.getValues()
        eingabe = eingabefeld.get(1.0,END).strip()
        if eingabe == w2:
            w = Label(window2, 
                 compound = CENTER,
                 fg="green",
                 text="🙂\n"+w2,
                 font =("Arial", 25),
                 image=img,width=300, height=200)
            w.grid(column=1,row=1)
            #if stufe < STUFEN:
                #vokabelkasten2[stufe+1].append((w1,w2))
        else:
            w = Label(window2, 
                 compound = CENTER,
                 fg="red",
                 text="😕\n"+w2,
                 font =("Arial", 25),
                 image=img,width=300, height=200)
            w.grid(column=1,row=1)
            vokabelkasten[1].append((w1,w2))
        
    def nextVoc():
        try:
            w1,w2,stufe = next(words_to_learn)
            w = Label(window2, 
                compound = CENTER,
                text=w1,
                font=("Arial", 25),
                image=img,width=600, height=200)
            w.grid(column=1,row=1)
            #return w1,w2,stufe
            aktuelle_vokabel.setValues(w1,w2,stufe)
        except StopIteration:
            window2.destroy()
            with open("Vokabelkasten.txt","w",encoding="utf-8") as f:
                f.write(str(vokabelkasten))
            showProgress()
            
    file = "Lektionen/"+lektion_variable.get()+".txt"
    vokabelkasten = eval(open("Vokabelkasten.txt","r",encoding="utf-8").readlines()[0])
    with open(file,"r",encoding="utf-8") as f:
        for line in f:
            w1,w2 = line.strip().split("\t")
            
            vokabelkasten[1].append((w1,w2))


    #vokabelkasten2 = {x:[] for x in range(1,STUFEN+1)}
    wordlist = set()
    for st in vokabelkasten:
        for word1,word2 in vokabelkasten[st]:
            wordlist.add((word1,word2,st))
    wordlist = list(wordlist)
    random.shuffle(wordlist)
    words_to_learn = iter(wordlist)
    aktuelle_vokabel = Vokabel()
    window2 = Toplevel()
    window2.configure(bg=backgroundcolor)
    eingabefeld = Text(master=window2, width=40, height=3, wrap='word')
    eingabefeld.grid(column=1,row=2)
    nextVoc()
    ttk.Button(window2,text="Check",command=check,style="button.TButton").grid(column=1,row=3)
    ttk.Button(window2,text="Next",command=nextVoc,style="button.TButton").grid(column=0,row=3)
    ttk.Button(window2,text="ã",command=welle,style="button.TButton").grid(column=0,row=4)
    ttk.Button(window2,text="õ",command=welle2,style="button.TButton").grid(column=2,row=4)
    ttk.Button(window2,text="ç",command=c_mit_haken,style="button.TButton").grid(column=1,row=4)
    with open("Vokabelkasten.txt","w",encoding="utf-8") as v:
        v.write(str(vokabelkasten))

lektionen_aktualisieren()
ttk.Button(frm,text="Create Lection",command=createLection,style="button.TButton").grid(column=0,row=0)
ttk.Button(frm,text="Start Training",command=train,style="button.TButton").grid(column=1,row=0)
ttk.Button(frm,text="sollte wiederholt werden",command=gothrough,style="button.TButton").grid(column=2,row=0)
ttk.Button(frm,text="Lege Lektion in Vokabelkasten",command=loadLektion,style="button.TButton").grid(column=1,row=1)
ttk.Button(frm,text="Show Progress",command=showProgress,style="button.TButton").grid(column=0,row=1)
ttk.Button(frm, text="Quit", command=root.destroy,style="button.TButton").grid(column=1, row=3)
root.mainloop()
