##########################
#  --------------------  #
#  |Wav Randomiser GUI|  #
#  --------------------  #
##########################

#pyinstaller --onefile --add-data="pi.gif;img" --icon=.\a.ico --windowed .\randomiser.py

import os, random
import simpleaudio.functionchecks as fc
import simpleaudio as sa

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *

import webbrowser, subprocess

# TODO:
'''
-error　testing
-understand scrollbar
-manual
'''

root = Tk()
root.title("Randomiser GUI")
root.resizable(FALSE, FALSE)

silentVar = StringVar()
rootDir = StringVar()
rootDir.set("Browse for the folder containing the .wav files")
btns = []
btnSVs = []
files = []
chosenFiles = []
currentFile = None  ##delete
easter = True
ii = None
playMenu = None
r = ""


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(sys._MEIPASS)
        print("")
        print(os.listdir(sys._MEIPASS))
        print("")
        print(os.listdir(sys._MEIPASS + "\\img"))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def initialise():
    Label(root, justify=CENTER, text="WAV Randomiser GUI", font=("Times", "22", "bold italic")).grid(row=1)
    global mainFrame1, mainFrame2, mainFrame3, mainFrame4, canvas
    mainFrame1 = Frame(root, padding="0 0 0 0", relief="flat", width=60)
    mainFrame2 = Frame(root, padding="0 0 0 0", relief="flat")
    mainFrame3 = Frame(root, padding="0 0 0 0", relief="flat")
    mainFrame1.grid(row=2)
    # mainFrame1.grid(row=2,columnspan=2)
    mainFrame2.grid(row=4)
    # mainFrame2.grid(row=3,column=1)
    mainFrame3.grid(row=3)
    # mainFrame3.grid(row=3,column=0)

    # 1
    global bBrowse, lRootDir, bSA, bDSA
    Label(mainFrame1, justify=CENTER,
          text="This is the GUI version of the .wav audio randomiser script.\n Select a folder with audio, then select the audio files, \nclick Choose(update selection), then Play(next sound).",
          font=("Times", "12")).grid(row=0)
    bBrowse = Button(mainFrame1, width=20, text="Browse Folder", command=dirBrowse).grid(row=1)
    lRootDir = Label(mainFrame1, justify=CENTER, textvariable=rootDir, font=("Times", "12"))
    lRootDir.grid(row=2)
    lRootDir.bind("<Button-1>", dirOpen)

    # 3
    canvas = Canvas(mainFrame3, highlightthickness=0, relief="flat")
    canvas.pack(side="left", fill="both")
    mainFrame4 = Frame(canvas, padding="0 0 0 0", relief="flat", width=50)
    canvas.create_window((0, 0), window=mainFrame4, anchor='nw')
    myscrollbar = Scrollbar(mainFrame3, orient="vertical", command=canvas.yview)
    myscrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=myscrollbar.set)
    mainFrame3.bind("<Configure>", myfunction)

    # 2
    global silentVar, bChoose, bPlay
    bChoose = Button(mainFrame2, width=20, text="Update Selection", command=choose, state="disabled")
    bChoose.grid(row=1, column=0, columnspan=2)
    bSA = Button(mainFrame2, width=20, text='Select All', command=selectAll, state="disabled")
    bSA.grid(column=0, row=0)
    bDSA = Button(mainFrame2, width=20, text='Deselect All', command=deselectAll, state="disabled")
    bDSA.grid(column=1, row=0)
    bPlay = Button(mainFrame2, width=20, text="Play", command=playMenu, state="disabled")
    bPlay.grid(row=2, column=0, columnspan=2)
    bHelp = Button(mainFrame2, width=20, text="Help", command=helpMenu).grid(row=100, column=0)
    bAbout = Button(mainFrame2, width=20, text="About", command=aboutMenu).grid(row=100, column=1)

    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)
    for child in mainFrame1.winfo_children():
        child.grid_configure(padx=5, pady=5)
    for child in mainFrame2.winfo_children():
        child.grid_configure(padx=5, pady=5)


def dirOpen(event):
    global rootDir
    if rootDir.get()[15:] != "folder containing the .wav files":
        subprocess.Popen('explorer ' + rootDir.get()[15:])


def dirBrowse():
    reset()
    global rootDir, lRootDir, files, bChoose, bPlay, bSA, bDSA
    inputt = str(filedialog.askdirectory() + "").replace("/", "\\")
    if inputt:
        rootDir.set("Chosen Folder: " + inputt)
    else:
        messagebox.showwarning("Warning", "You didn't choose a folder!")
        return
    files = os.listdir(rootDir.get()[15:])
    files = clean(files)
    bPlay.config(state="disabled")
    if len(files) == 0:
        messagebox.showwarning("Warning", "There are no .wav files in this folder!")
        # messagebox.showinfo("Info", "Image Not Found")
        # messagebox.showwarning("Warning", "Image Not Found")
        # messagebox.showerror("Error", "Image Not Found")
        bChoose.config(state="disabled")
        bSA.config(state="disabled")
        bDSA.config(state="disabled")
    else:
        bChoose.config(state="normal")
        bSA.config(state="normal")
        bDSA.config(state="normal")
        generate()


def clean(files):
    f = []
    for i in files:
        if len(i) > 4:
            if i[-4:].lower() == ".wav":
                f.append(i)
    return f


def reset():
    global btnSVs, btns, files
    for i in btns:
        i.destroy()
    btns = []
    btnSVs = []
    files = []


def generate():
    global files, canvas, mainFrame4, btnSVs, btns
    for i in range(len(files)):
        btnSVs.append(StringVar())
        btns.append(Checkbutton(mainFrame4, text=files[i][:-4], variable=btnSVs[i], onvalue='on', offvalue='off'))
        btns[i].grid(row=i)


def selectAll():
    global btnSVs
    for b in btnSVs:
        b.set("on")


def deselectAll():
    global btnSVs
    for b in btnSVs:
        b.set("off")


def choose():
    global btnSVs, btns, chosenFiles, files
    chosenFiles = []
    for i in range(len(files)):
        if btnSVs[i].get() == "on":
            chosenFiles.append(files[i])
    if len(chosenFiles) == 0:
        bPlay.config(state="disabled")
        messagebox.showwarning("Warning", "You haven't selected any of them!")
    else:
        bPlay.config(state="normal")
    print(chosenFiles)


def play():
    global rootDir, chosenFiles, r, silentVar, bSilent, lOutput, ii, easter, bDisp
    r = random.choice(chosenFiles)
    easter = False
    ii = None

    if r:
        try:
            ii = PhotoImage(file=str(rootDir.get()[15:] + "\\" + r[:-4] + ".gif"))
            bDisp.config(state="normal")
        except:
            bDisp.config(state="disabled")
    if not silentVar.get() == "on":
        lOutput.config(text="")
        wave_obj = sa.WaveObject.from_wave_file(rootDir.get()[15:] + "\\" + r)
        play_obj = wave_obj.play()
        # play_obj.wait_done()
    else:
        lOutput.config(text=r[:-4])


def playMenu():
    global lOutput, silentVar, bSilent, playFrame, bDisp, playMenu
    try:
        playMenu.destroy()
    except:
        pass
    playMenu = Toplevel()
    playMenu.title("Play Sound")
    playMenu.resizable(FALSE, FALSE)

    playFrame = Frame(playMenu, padding="10 10 10 10")
    playFrame.grid(row=1)

    Label(playFrame, justify=CENTER, text="Play Menu", font=("Times", "18", "bold italic")).grid(row=0, columnspan=3)

    bSilent = Checkbutton(playFrame, text='Silent', variable=silentVar, onvalue='on', offvalue='off')
    bSilent.grid(column=2, row=1)

    bPlay = Button(playFrame, width=20, text="Play Next Sound", command=play).grid(row=1, column=1)

    bDisp = Button(playFrame, width=20, text="Display", command=dispImage)
    bDisp.grid(row=1, column=0)

    lOutput = Label(playFrame, justify=CENTER, text="", font=("Times", "12"))
    lOutput.grid(row=3, columnspan=3)


def helpMenu():
    helpMenu = Toplevel()
    helpMenu.title("Help")
    helpMenu.resizable(FALSE, FALSE)
    # helpMenu.wm_iconbitmap(bitmap = folder+"\\StumPi_logo.ico")

    helpFrame = Frame(helpMenu, padding="10 10 10 10")
    helpFrame.grid(row=1)
    tHelp = "1. Browse for a folder with audio files in it\n2. Select some files to randomise\n3. Update the selection\n4. Click Play to open the Play Menu\n5. Click Play Next Sound\n6. Click Display to display associated image\n7. Repeat 5 and 6\n\nAll audio must be .wav files\nAll images must be .gif files\nAudio and Images can be converted online or with software\nImages must have the same name as the audio file\ne.g. random.wav and random.gif"
    Label(helpFrame, justify=CENTER, text="Help", font=("Times", "18", "bold italic")).grid(row=0)

    def linkc1(event):
        webbrowser.open_new(r"https://online-audio-converter.com/")

    link1 = Label(helpFrame, text="https://online-audio-converter.com/", font=("Times", "16"), foreground="blue",
                  cursor="hand2")
    link1.grid(row=2)
    link1.bind("<Button-1>", linkc1)

    def linkc2(event):
        webbrowser.open_new(r"https://www.xnview.com/en/xnconvert/")

    link2 = Label(helpFrame, text="https://www.xnview.com/en/xnconvert/", font=("Times", "16"), foreground="blue",
                  cursor="hand2")
    link2.grid(row=3)
    link2.bind("<Button-1>", linkc2)
    Label(helpFrame, justify=LEFT, text=tHelp, font=("Times", "16")).grid(row=1)


def aboutMenu():
    aboutMenu = Toplevel()
    aboutMenu.title("About")
    aboutMenu.resizable(FALSE, FALSE)
    # aboutMenu.wm_iconbitmap(bitmap = folder+"\\StumPi_logo.ico")

    aboutFrame = Frame(aboutMenu, padding="10 10 10 10")
    aboutFrame.grid(row=1)
    tAbout = "This program was initially created for\nlearning Hiragana characters,\nhowever it has many other potential uses,\nsuch as learning Katakana, Kanji\nor even UK Road Signs."
    Label(aboutFrame, justify=CENTER, text="About", font=("Times", "18", "bold italic")).grid(row=0)
    Label(aboutFrame, justify=LEFT, text=tAbout, font=("Times", "16")).grid(row=1)
    Label(aboutFrame, justify=RIGHT, text="\nCopyright Rahul Pai Creations 2011-2017", font=("Times", "9", "italic")).grid(row=120)  ####


def dispImage():
    global playFrame, ii, easter, r
    im = Toplevel()
    im.title("Show")
    im.resizable(FALSE, FALSE)
    imf = Frame(im, padding="10 10 10 10")
    imf.grid(row=1)
    if easter:
        ii = PhotoImage(file=resource_path("img\\pi.gif"))
        Label(imf, text="Hi", font=("Times", "16")).grid(row=1)
    iii = ii
    iii.master = im
    if not silentVar.get() == "on":
        Label(imf, justify=CENTER, text=r[:-4], font=("Times", "16")).grid(row=2)
    if iii:
        lIm = Label(imf, image=iii)
        lIm.grid(row=3)
        lIm.image = iii


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox(ALL), width=200, height=200)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

initialise()
root.mainloop()
