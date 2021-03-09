from tkinter import filedialog as fd
from tkinter import *
from tkinter import ttk
import tkinter as tk
import lsb
from dct import DCT
import image_comparison_metrics as ic
import cv2
from numpy import asarray
import blowfish_algo
import bpcs
from PIL import Image, ImageTk
import os

alpha = 0.45
 
window = tk.Tk()
#TileBar
window.title("Imgae Embedder") 
window.geometry('900x700')
TAB_CONTROL = ttk.Notebook(window)
TAB1 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB1, text='Embed')
TAB2 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB2, text='Compare')
TAB3 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB3, text='Extract')
TAB_CONTROL.pack(expand=1, fill="both")

embedInputFile = ""
dataInputFile = ""
leftInputFile = ""
rihtInputFile = ""
extractInputFile = ""
compareResult = []
outFolder = ""

def openImageFileChooser():
    global embedInputFile
    embedInputFile =  fd.askopenfilename()
    
    lim=Image.open(embedInputFile)
    lim = lim.resize((100, 75), Image.ANTIALIAS)
    lphoto=ImageTk.PhotoImage(lim)
    
    emImage['image'] = ""
    inImage['image'] = lphoto
    lphoto.image = lphoto

def getSecretContent():
    # returns secret content bytes, that will be embdded into the carrier
    if contentTypeVar.get() == "Plain text":
        return inputText.get(1.0, "end-1c").encode("utf-8")
    elif contentTypeVar.get() == "File":
        f = open(secretFile, "rb")
        content = f.read()
        f.close()
        return content

    
def embedImage():
    algo = variable.get()

    inp = getSecretContent()

    out_f, out_ext = embedInputFile.split(".")
    out_f = out_f + "_"  + algo + ".png"
    fileName = os.path.basename(out_f)
    fileName = outFolder + "/" + fileName
    
    
    if(algo == "LSB"):
        lsb.encodeImage(embedInputFile, inp, fileName)
    elif(algo == "Blowfish"):
        #encrypt the input data
        inp = blowfish_algo.encrypt(inp)
        print(type(inp))
        lsb.encodeImage(embedInputFile, inp, fileName)
    elif(algo == "BPCS"):
        global alpha
        bpcs.encode(embedInputFile, inp, fileName, alpha) 
    
    elif(algo == "DCT"):
        d = DCT(embedInputFile)
        d.DCTEn(inp, fileName)
    
    lim=Image.open(embedInputFile)
    lim = lim.resize((100, 75), Image.ANTIALIAS)
    lphoto=ImageTk.PhotoImage(lim)
    
    inImage['image'] = lphoto
    lphoto.image = lphoto
    
    oim=Image.open(embedInputFile)
    oim = oim.resize((100, 75), Image.ANTIALIAS)
    ophoto=ImageTk.PhotoImage(oim)
    
    emImage['image'] = ophoto
    ophoto.image = ophoto
    
    embedStatusLbl.configure(text="Success")
    print("Embed Success")

def openLeftImageFileChooser():
    global leftInputFile
    leftInputFile =  fd.askopenfilename()
    im=Image.open(leftInputFile)
    im = im.resize((100, 75), Image.ANTIALIAS)
    photo=ImageTk.PhotoImage(im)
    
    leftImage['image'] = photo
    photo.image = photo

def openRightImageFileChooser():
    global rihtInputFile
    rihtInputFile =  fd.askopenfilename()
    im=Image.open(rihtInputFile)
    im = im.resize((100, 75), Image.ANTIALIAS)
    photo=ImageTk.PhotoImage(im)
    
    rightImage['image'] = photo
    photo.image = photo
    
def openExtractImageFileChooser():
    global extractInputFile
    extractInputFile =  fd.askopenfilename()
    outputTexArea.delete('1.0',"end")
    
    eim=Image.open(extractInputFile)
    eim = eim.resize((100, 75), Image.ANTIALIAS)
    rphoto=ImageTk.PhotoImage(eim)
    
    eImage['image'] = rphoto
    rphoto.image = rphoto
    
def compareImage():
    img1 = cv2.imread(leftInputFile)
    img2 = cv2.imread(rihtInputFile)
    
    img1A = asarray(img1)
    img2A = asarray(img2)
    rmse = ic.rmse(img1A, img2A, 4095)
    ssim = ic.ssim(img1A, img2A, 4095)
    mse = ic.mse(img1, img2)
    
    lim=Image.open(leftInputFile)
    lim = lim.resize((100, 75), Image.ANTIALIAS)
    lphoto=ImageTk.PhotoImage(lim)
    
    leftImage['image'] = lphoto
    lphoto.image = lphoto
    
    rim=Image.open(rihtInputFile)
    rim = rim.resize((100, 75), Image.ANTIALIAS)
    rphoto=ImageTk.PhotoImage(rim)
    
    rightImage['image'] = rphoto
    rphoto.image = rphoto
    
    constructTable(rmse, ssim, mse)
    print("compareClicked")
    
def constructTable(rmse, ssim, mse):
    global compareResult
    result = []
    result.append(rmse)
    result.append(ssim)
    result.append(mse)
                   
    compareResult.append(result)
    
    for i in range(len(compareResult)):
        columns = compareResult[i]
        for j in range(len(columns)):
            compareEntry = Entry(TAB2, width=20, fg='blue')
            compareEntry.grid(row=i+5, column=j)
            compareEntry.insert(END, columns[j]) 
    
    
def extractData():
    algo = extractAlgo.get()
    
    if(algo == "Blowfish" or algo == "LSB"):
        raw = lsb.decodeImage(extractInputFile)
        if(algo == "Blowfish"):
            raw = blowfish_algo.decrypt(raw)
    elif(algo == "BPCS"):
        raw = bpcs.decode(extractInputFile, "", alpha)
        
    elif(algo == "DCT"):
        d = DCT(extractInputFile)
        raw = d.DCTDe()
        
    eim=Image.open(extractInputFile)
    eim = eim.resize((100, 75), Image.ANTIALIAS)
    rphoto=ImageTk.PhotoImage(eim)
    
    rightImage['image'] = rphoto
    rphoto.image = rphoto


    if extractContentType.get() == "Plain text":
        extractStatusLbl.configure(text="Success")
        outputTexArea.delete('1.0',"end")
        outputTexArea.insert('1.0', raw)
    elif extractContentType.get() == "File":
        with open(extractToFilename, "wb") as target:
            target.write(raw)
        print(f"Succecfully extracted to: {extractToFilename}")
        
    else:
        raise AssertionError("Invalid extract content type")
        

def selectFolder():
    global outFolder
    outFolder = fd.askdirectory()
    
def onSelectAlgo(*args):
    emImage['image'] = ""


def onContentTypeChange(*args):
    if contentTypeVar.get() == "Plain text":
        selectSecretFileBtn.grid_forget()
        secretFileLabel.grid_forget()
        inputText.grid(column=1, row=2, sticky=tk.N)
        
    elif contentTypeVar.get() == "File":
        inputText.grid_forget()
        selectSecretFileBtn.grid(column=1, row=3, sticky=tk.N)
        secretFileLabel.grid(column=1, row=4, sticky=tk.N)

    else:
        raise AssertionError("Unknown selected secret content type: " + contentTypeVar.get())


def selectSecretFile():
    global secretFile
    secretFile = fd.askopenfilename()
    secretFileLabel.config(text=secretFile)
    




#Embed Section Start
#Section Header
textLbl = Label(TAB1, text="Image") 
textLbl.grid(column=0, row=0, sticky=tk.W)

textLbl = Label(TAB1, text="Secret content") 
textLbl.grid(column=1, row=0, sticky=tk.W)

textLbl = Label(TAB1, text="Algorithm") 
textLbl.grid(column=2, row=0, sticky=tk.W)

textLbl = Label(TAB1, text="OutFile") 
textLbl.grid(column=3, row=0, sticky=tk.W)
 
# Input Image File Chooser
addBtn = Button(TAB1, text='Select Image',   command=openImageFileChooser)
addBtn.grid(column=0, row=1, sticky=tk.N)

textLbl = Label(TAB2, text="Comparison Result") 
textLbl.grid(column=0, row=2, sticky=tk.W)


# Choose to embed either text or file
choices = ['Plain text', 'File']
contentTypeVar = StringVar(TAB1)
contentTypeVar.set('Plain text')

contentTypeVar.trace_add('write', onContentTypeChange)

secretContentType = OptionMenu(TAB1, contentTypeVar, *choices)
secretContentType.grid(column=1,row=1)

#Input Text Area
inputText = Text(TAB1, height=20, width=40)
inputText.grid(column=1, row=2, sticky=tk.N)

selectSecretFileBtn = Button(TAB1, text='Select secret file',   command=selectSecretFile)
# selectSecretFileBtn.grid(column=1, row=3, sticky=tk.N)

secretFileLabel = Label(TAB1, text="None selected")
# secretFileLabel.grid(column=1, row=4, sticky=tk.N)

# Select Algorithm
OPTIONS = [
"LSB",
"BPCS",
"Blowfish",
"DCT"
] #etc

variable = StringVar(TAB1)
variable.set(OPTIONS[0]) # default value

algorithmMenu = OptionMenu(TAB1, variable, *OPTIONS, command=onSelectAlgo)
algorithmMenu.grid(column=2, row=1, sticky=tk.N)

inImage = Label(TAB1)
inImage.grid(column=0, row=2)

# Folder File Chooser
addBtn = Button(TAB1, text='Select Dir',   command=selectFolder)
addBtn.grid(column=3, row=1, sticky=tk.N)

# Embed Button
addBtn = Button(TAB1, text='Embed',   command=embedImage)
addBtn.grid(column=4, row=1, sticky=tk.N)

# Success Message
embedStatusLbl = Label(TAB1, text="")
embedStatusLbl.grid(column=5, row=1, sticky=tk.N)

emImage = Label(TAB1)
emImage.grid(column=3, row=2)

#Embed Section END
 
# Left Image File Chooser
addBtn = Button(TAB2, text='Select Left Image',   command=openLeftImageFileChooser)
addBtn.grid(column=0, row=0, sticky=tk.W)
 
# Left Image File Chooser
addBtn = Button(TAB2, text='Select Left Image',   command=openRightImageFileChooser)
addBtn.grid(column=1, row=0, sticky=tk.W)

# Compare Button
addBtn = Button(TAB2, text='Compare',   command=compareImage)
addBtn.grid(column=2, row=0, sticky=tk.W)

leftImage = Label(TAB2)
leftImage.grid(column=0, row=1)

rightImage = Label(TAB2)
rightImage.grid(column=1, row=1) 

textLbl = Label(TAB2, text="Comparison Result") 
textLbl.grid(column=0, row=2, sticky=tk.W)

textLbl = Label(TAB2, text="-----------------") 
textLbl.grid(column=0, row=3, sticky=tk.W)


textLbl = Label(TAB2, text="RMSE") 
textLbl.grid(column=0, row=4, sticky=tk.W)

textLbl = Label(TAB2, text="MSE") 
textLbl.grid(column=1, row=4, sticky=tk.W)

textLbl = Label(TAB2, text="SSIM") 
textLbl.grid(column=2, row=4, sticky=tk.W)
#Compare Section End

#Extract Data Section Start
# Extract File
addBtn = Button(TAB3, text='Select File',   command=openExtractImageFileChooser)
addBtn.grid(column=0, row=0, sticky=tk.W)


extractContentType = StringVar(TAB3)
extractContentType.set(choices[0]) # default value

def onExtractContentTypeChange(*args):
    if extractContentType.get() == "File":
        outputTexArea.grid_forget()
        textLbl.grid_forget()
        extractToLabel.grid(column=0, row=2, sticky=tk.NW)
        extractToSelectBtn.grid(column=0, row=3, sticky=tk.NW)

    elif extractContentType.get() == "Plain text":
        extractToLabel.grid_forget()
        extractToSelectBtn.grid_forget()
        outputTexArea.grid(column=0, row=3, sticky=tk.N)
        textLbl.grid(column=0, row=2, sticky=tk.W)


extractTypeMenu = OptionMenu(TAB3, extractContentType, *choices, command=onExtractContentTypeChange)
extractTypeMenu.grid(column=0, row=1, sticky=tk.NW)

extractToLabel = Label(TAB3, text="Extract to:") 

def selectExtractToFile():
    global extractToFilename
    extractToFilename = fd.asksaveasfilename()
    extractToLabel.config(text="Extract to: " + extractToFilename)

extractToSelectBtn = Button(TAB3, text="Select file", command=selectExtractToFile) 

textLbl.grid(column=0, row=2, sticky=tk.W)


extractAlgo = StringVar(TAB3)
extractAlgo.set(OPTIONS[0]) # default value

algorithmMenu = OptionMenu(TAB3, extractAlgo, *OPTIONS)
algorithmMenu.grid(column=1, row=0, sticky=tk.N)

# Extract Button
addBtn = Button(TAB3, text='Extract',   command=extractData)
addBtn.grid(column=2, row=0, sticky=tk.W)

extractStatusLbl = Label(TAB3, text="") 
extractStatusLbl.grid(column=3, row=0, sticky=tk.W)

eImage = Label(TAB3)
eImage.grid(column=0, row=1)

textLbl = Label(TAB3, text="Extracted Data") 
textLbl.grid(column=0, row=2, sticky=tk.W)

#Input Text Area
outputTexArea = Text(TAB3, height=20, width=40)
outputTexArea.grid(column=0, row=3, sticky=tk.N)
#Extract Data Section End

window.mainloop()
