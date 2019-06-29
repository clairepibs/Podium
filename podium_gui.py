from tkinter import *
import sys
import tkinter.messagebox
import tkinter.font as tkFont
import podium_MotorControl as mc
import RPi.GPIO as GPIO
from time import sleep
import threading
import config as c

# INITIALIZE VARIABLES

# Other flags
stop_threads = 0
HIGH = 1
LOW = 0

# Stepper motor outputs
dir_x = 17
pul_x = 27
dir_y = 2
pul_y = 3

# Limit switch pins
lim_x_pos = 24
lim_x_neg = 23
lim_y_pos = 12
lim_y_neg = 25

#pendant pins
save_but = 20
zero_but = 21
up_but = 6
down_but = 13
right_but = 19
left_but = 26

# INITIALIZE GPIO PINS

#programming the GPIO by Board numbers (see board pinout)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#enable pin as either output or input
GPIO.setup(dir_x,GPIO.OUT)
GPIO.setup(pul_x,GPIO.OUT)
GPIO.setup(dir_y,GPIO.OUT)
GPIO.setup(pul_y,GPIO.OUT)

# Set GPIO switch input pins for internal resistance
GPIO.setup(up_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(down_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(right_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(left_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(save_but,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(zero_but,GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(lim_x_pos,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lim_x_neg,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lim_y_pos,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lim_y_neg,GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Global variables used in GUI
stepoption = {"Zero Coordinate X"}
channeloption = {"Nominal Acceleration"}
iterations = 1
motoroption = {"X Axis"}
stop_gui_thread = 0
check_go = True
text_size = 12


class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

class MenuBar(tkinter.Menu):
    def __init__(self, master):
        tkinter.Menu.__init__(self, master)
        master.title("PODIUM")

        #Set up file menu
        fileMenu = Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Exit", command=self.QuitSafely)

        editMenu = Menu(self, tearoff=0)
        self.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Instrument", command=self.editInstrument)
        editMenu.add_command(label="Channel", command=self.editChannel)
        editMenu.add_command(label="Sequence", command=self.editSequence)
        editMenu.add_command(label="Step", command=self.editStep)

        manualMenu = Menu(self, tearoff=0)
        self.add_cascade(label="Manual", menu=manualMenu)
        manualMenu.add_command(label="Motor Control", command=self.motorControlMenu)

    def QuitSafely(self):
        # exit program safely
        mc.cleanup()
        mc.shutoff_lcd()
        stop_gui_thread = True
        main.destroy()

    def editInstrument(self):
        InstrumentWindow()

    def editChannel(self):
        ChannelWindow()

    def editSequence(self):
        SequenceWindow()

    def editStep(self):
        StepWindow()

    def motorControlMenu(self):
        MotorControlWindow()


class MainWindow(tkinter.Tk):
    def __init__(self):
        global index
        global iterations

        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.geometry("300x240")
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=text_size, family="Helvetica", weight = "bold")
        self.option_add("*Font", self.default_font)

        # Frame to hold x axis frame and y axis frame
        self.axisFrame =Frame(self, bd = 3, relief = RAISED, padx = 5, pady = 5)
        self.axisFrame.grid(row=0, column=0, sticky= (N, S, E, W))

        # Set up sequencer frame on home screen
        self.sequencerframe = Frame(self, bd=3, relief=RAISED, padx=5, pady=5)
        self.sequencerframe.grid(row=0, column=1, sticky=(N, S, E, W))

        # Configure overall column and row sizes
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # Set up x axis frame on left frame
        self.xframe = Frame(self.axisFrame, bd = 4, relief = RAISED)
        self.xframe.grid(row=0, column=0, sticky = (N, S, E, W))
        self.xlabel = Label(self.xframe, text="X AXIS").grid(row=0, column=0, sticky=N, rowspan=2, columnspan=2)

        # Set up y axis frame on left frame
        self.yframe = Frame(self.axisFrame, bd = 4, relief = RAISED)
        self.yframe.grid(row=1, column=0, sticky= (N, S, E, W))
        self.ylabel = Label(self.yframe, text="Y AXIS").grid(row=0, column=0, rowspan=2,
                                                                          columnspan=2)

        # Set up position frame on left frame
        self.posframe = Frame(self.axisFrame, bd = 4, relief = RAISED)
        self.posframe.grid(row=2, column=0, sticky= (N, S, E, W))


        # Configure x and y control column and row sizes
        self.axisFrame.columnconfigure(0, weight=1)
        self.axisFrame.rowconfigure(0, weight=2)
        self.axisFrame.rowconfigure(1, weight=2)
        self.axisFrame.rowconfigure(2, weight=1)

        # Add x system outputs
        self.currentPosLabelX = Label(self.xframe, text="Current Position (mm):").grid(row=2, column=0, sticky=W)
        self.currentPosAnswerX = Label(self.xframe, text='0.000')
        self.currentPosAnswerX.grid(row=2, column=1, sticky=E)
        self.plusLimLabelX = Label(self.xframe, text="At Positive Limit?").grid(row=4, column=0, sticky=W)
        self.plusLimAnswerX = Label(self.xframe, text="No")
        self.plusLimAnswerX.grid(row=4, column=1, sticky=E)
        self.minusLimLabelX = Label(self.xframe, text="At Negative Limit?").grid(row=5, column=0, sticky=W)
        self.minusLimAnswerX = Label(self.xframe, text="Yes")
        self.minusLimAnswerX.grid(row=5, column=1, sticky=E)

        # Add x user inputs
        self.toLimPlus_buttonX = Button(self.xframe, text="To Limit +", command=self.toLimPlusX)
        self.toLimPlus_buttonX.grid(row=6, column=0, sticky=E+W)
        self.toLimMinus_buttonX = Button(self.xframe, text="To Limit -", command=self.toLimMinusX)
        self.toLimMinus_buttonX.grid(row=6, column=1, sticky=E+W)
        self.zeroAxis_buttonX = Button(self.xframe, text="Set as Zero X", command=self.zeroAxisX)
        self.zeroAxis_buttonX.grid(row=8, column=0, sticky=E+W)

        # Configure column and row sizes in x control
        self.xframe.columnconfigure(0, weight=1)
        self.xframe.columnconfigure(1, weight=1)
        self.xframe.rowconfigure(0, weight=1)
        self.xframe.rowconfigure(1, weight=1)
        self.xframe.rowconfigure(2, weight=1)
        self.xframe.rowconfigure(3, weight=1)
        self.xframe.rowconfigure(4, weight=1)
        self.xframe.rowconfigure(5, weight=1)
        self.xframe.rowconfigure(6, weight=1)
        self.xframe.rowconfigure(7, weight=1)
        self.xframe.rowconfigure(8, weight=1)
        self.xframe.rowconfigure(9, weight=1)

        # Add y system outputs
        self.currentPosLabelY = Label(self.yframe, text="Current Position (mm):").grid(row=2, column=0, sticky=W)
        self.currentPosAnswerY = Label(self.yframe, text='0.000')
        self.currentPosAnswerY.grid(row=2, column=1, sticky=E)
        self.plusLimLabelY = Label(self.yframe, text="At Positive Limit?").grid(row=4, column=0, sticky=W)
        self.plusLimAnswerY = Label(self.yframe, text="No")
        self.plusLimAnswerY.grid(row=4, column=1, sticky=E)
        self.minusLimLabelY = Label(self.yframe, text="At Negative Limit?").grid(row=5, column=0, sticky=W)
        self.minusLimAnswerY = Label(self.yframe, text="Yes")
        self.minusLimAnswerY.grid(row=5, column=1, sticky=E)

        # Add y user inputs
        self.toLimPlus_buttonY = Button(self.yframe, text="To Limit +", command=self.toLimPlusY)
        self.toLimPlus_buttonY.grid(row=6, column=0, sticky=E+W)
        self.toLimMinus_buttonY = Button(self.yframe, text="To Limit -", command=self.toLimMinusY)
        self.toLimMinus_buttonY.grid(row=6, column=1, sticky=E+W)
        self.zeroAxis_buttonY = Button(self.yframe, text="Set as Zero Y", command=self.zeroAxisY)
        self.zeroAxis_buttonY.grid(row=8, column=0, sticky=E+W)

        # Configure column and row sizes in y control
        self.yframe.columnconfigure(0, weight=1)
        self.yframe.columnconfigure(1, weight=1)
        self.yframe.rowconfigure(0, weight=1)
        self.yframe.rowconfigure(1, weight=1)
        self.yframe.rowconfigure(2, weight=1)
        self.yframe.rowconfigure(3, weight=1)
        self.yframe.rowconfigure(4, weight=1)
        self.yframe.rowconfigure(5, weight=1)
        self.yframe.rowconfigure(6, weight=1)
        self.yframe.rowconfigure(7, weight=1)
        self.yframe.rowconfigure(8, weight=1)
        self.yframe.rowconfigure(9, weight=1)

        # Add position labels and entries
        self.enterNewPosLabel = Label(self.posframe, text="ENTER NEW POSITION (mm):").grid(row=0, column=0, sticky=N, columnspan=4)
        self.enterXLabel = Label(self.posframe, text="X:").grid(row=1, column=0)
        self.enterXEntry = Entry(self.posframe)
        self.enterXEntry.grid(row=1, column=1, sticky=E + W)
        self.enterYLabel = Label(self.posframe, text="Y:").grid(row=1, column=2)
        self.enterYEntry = Entry(self.posframe)
        self.enterYEntry.grid(row=1, column=3, sticky=E + W)
        self.go_button = Button(self.posframe, text="Go", fg="green", command=self.letsgo)
        self.go_button.grid(row=2, column=0, sticky=E + W, columnspan=2)
        self.stop_button = Button(self.posframe, text="STOP", fg="red", command=self.stop)
        self.stop_button.grid(row=2, column=2, sticky=E + W, columnspan=2)

        #Configure column and row sizes in position frame
        self.posframe.columnconfigure(0, weight=1)
        self.posframe.columnconfigure(1, weight=1)
        self.posframe.columnconfigure(2, weight=1)
        self.posframe.columnconfigure(3, weight=1)
        self.posframe.rowconfigure(0, weight=1)
        self.posframe.rowconfigure(1, weight=1)
        self.posframe.rowconfigure(2, weight=1)


        # SEQUENCER

        # Set up buttons frame on right frame
        self.topframe = Frame(self.sequencerframe, bd=1, relief=RAISED)
        self.topframe.grid(row=0, column=0, sticky=(N, S, E, W))
        self.toplabel = Label(self.topframe, text="COORDINATE SEQUENCE").grid(row=0, column=0, sticky=N, rowspan=2,
                                                                          columnspan=2)
        # Set up bottom frame on right frame
        self.bottomframe = Frame(self.sequencerframe, bd=1, relief=RAISED)
        self.bottomframe.grid(row=1, column=0, sticky=(N, S, E, W))

        # Configure column and row sizes
        self.sequencerframe.columnconfigure(0, weight=1)
        self.sequencerframe.rowconfigure(0, weight=1)
        self.sequencerframe.rowconfigure(1, weight=1)

        # Top right frame: set buttons and entries for coordinate sequencer
        self.seqRun_button = Button(self.topframe, text="Run", fg="green", command=self.seqRun)
        self.seqRun_button.grid(row=2, column=0, sticky=E + W)
        self.seqStop_button = Button(self.topframe, text="STOP", fg="red", command=self.stop)
        self.seqStop_button.grid(row=2, column=1, sticky=E + W)
        self.addLine_button = Button(self.topframe, text="Add Line", command=self.addLine)
        self.addLine_button.grid(row=3, column=0, sticky=E + W, columnspan = 2)

        # Set up sequencer with entries and scrollbar
        self.seqCanvas = ResizingCanvas(self.bottomframe, width = 500, height = 500, scrollregion=(0,0,500,500))
        self.listFrame = Frame(self.seqCanvas, bd = 4)
        self.vsb = Scrollbar(self.bottomframe, orient="vertical")
        self.vsb.pack(side=RIGHT, fill=Y)
        self.vsb.config(command=self.seqCanvas.yview)
        self.seqCanvas.config(yscrollcommand=self.vsb.set)
        self.seqCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.seqCanvas.configure(yscrollcommand=self.vsb.set)

        self.seqCanvas.create_window((5,5), window=self.listFrame, anchor='nw', width = 500)

        self.xTitle = Label(self.listFrame, text="X Position (mm)").grid(row=0, column=1)
        self.yTitle = Label(self.listFrame, text="Y Position (mm)").grid(row=0, column=2)
        self.waitTimeTitle = Label(self.listFrame, text="Wait Time (s)").grid(row=0, column=3)
        self.manualTitle = Label(self.listFrame, text="Manual\nWait?").grid(row=0, column=4)

        #Set up entries for sequencer accordingly
        self.indexList = []
        self.xSeqs = []
        self.ySeqs = []
        self.waitEntries = []
        self.manualOptions = []

        self.indexVal = {}
        self.xSeq = {}
        self.ySeq = {}
        self.waitEntry = {}
        self.manualOption = {}

        for i in range(1,26):
            for j in range(0,5):
                if j == 0:
                    self.indexVal[i] = Label(self.listFrame, text=str(i))
                    self.indexVal[i].grid(row=i, column=0)
                elif j == 1:
                    self.xSeq[i] = Entry(self.listFrame)
                    self.xSeq[i].grid(row=i, column=1)
                elif j == 2:
                    self.ySeq[i] = Entry(self.listFrame)
                    self.ySeq[i].grid(row=i, column=2)
                elif j == 3:
                    self.waitEntry[i] = Entry(self.listFrame)
                    self.waitEntry[i].grid(row=i, column=3)
                elif j == 4:
                    self.manualOption[i] = IntVar()
                    self.manualCheck = Checkbutton(self.listFrame, variable=self.manualOption[i], command = self.ifchecked)
                    self.manualCheck.grid(row=i, column=4)


        #Configure sequencer format
        self.listFrame.columnconfigure(0, weight=1)
        self.listFrame.columnconfigure(1, weight=50)
        self.listFrame.columnconfigure(2, weight=50)
        self.listFrame.columnconfigure(3, weight=50)
        self.listFrame.columnconfigure(4, weight=1)

        self.topframe.columnconfigure(0, weight=1)
        self.topframe.columnconfigure(1, weight=1)
        self.topframe.rowconfigure(0, weight=1)
        self.topframe.rowconfigure(1, weight=1)
        self.topframe.rowconfigure(2, weight=1)
        self.topframe.rowconfigure(3, weight=1)
        self.topframe.rowconfigure(4, weight=3)
        self.topframe.rowconfigure(5, weight=3)

        MainWindow.update(self)
        self.seqCanvas.config(scrollregion=self.seqCanvas.bbox(ALL))

    def lim_stop(self, *args):
        print("Limit GUI Daemon started")

        while 1:
            if c.stop_lim_thread:
                c.stop_lim_thread = 0
                break
            if GPIO.input(lim_y_pos) == False:
                print('Pos y lim trig')
                c.posYtrig = "Yes"
                self.stop()
                # Set direction
##                GPIO.output(mc.down.direc, mc.down.dir)
##                while GPIO.input(lim_y_pos) == False:
##                    mc.down.step(mc.down.nom_speed)
                continue
            elif GPIO.input(lim_y_neg) == False:
                print('Neg y lim trig')
                c.negYtrig = "Yes"
                self.stop()
                # Set direction
##                GPIO.output(mc.up.direc, mc.up.dir)
##                while GPIO.input(lim_y_neg) == False:
##                    mc.up.step(mc.up.nom_speed)
                continue
            elif GPIO.input(lim_x_pos) == False:
                print('Pos x lim trig')
                c.posXtrig = "Yes"
                self.stop()
##                # Set direction
####                GPIO.output(mc.left.direc, mc.left.dir)
####                while GPIO.input(lim_x_pos) == False:
####                    mc.left.step(mc.left.nom_speed)
                continue
            elif GPIO.input(lim_x_neg) == False:
                print('Neg x lim trig')
                c.negXtrig = "Yes"
                self.stop()
                # Set direction
##                GPIO.output(mc.right.direc, mc.right.dir)
##                while GPIO.input(lim_x_neg) == False:
##                    mc.right.step(mc.right.nom_speed)
                continue
            sleep(0.25)

    def toLimPlusX(self):

        print("Send to positive X limit!")

##        mc.right.go_lim()

##        c.stopflag = 0
##        moving_gui = threading.Thread(target = self.go(distx,0))
##        moving_gui.start()

    def toLimMinusX(self):

        print("Send to negative X limit!")

##        mc.left.go_lim()

##        c.stopflag = 0
##        moving_gui = threading.Thread(target = self.go(distx,0))
##        moving_gui.start()

    def toLimPlusY(self):

        print("Send to positive Y limit!")

##        mc.up.go_lim()

##        c.stopflag = 0
##        moving_gui = threading.Thread(target = self.go(0,disty))
##        moving_gui.start()

    def toLimMinusY(self):

        print("Send to negative Y limit!")

##        mc.down.go_lim()


##        c.stopflag = 0
##        moving_gui = threading.Thread(target = self.go(0,disty))
##        moving_gui.start()

    def zeroAxisX(self):
        c.zero_x = c.x_loc
        c.x_loc = 0
        print("Set X coordinate as reference zero!")
        print('X Location is ', c.x_loc)
        self.currentPosAnswerX['text'] = ("%.3f" % c.x_loc)

    def zeroAxisY(self):
        c.zero_y = c.y_loc
        c.y_loc = 0
        print("Set Y coordinate as reference zero!")
        print('Y Location is ', c.y_loc)
        self.currentPosAnswerY['text'] = ("%.3f" % c.y_loc)

    def check_go(self, distx, disty):
        
        print("distx = ", distx)
        print("Max x = ", c.max_x)
        print("X loc = ", c.x_loc)
        print("X zero = ", c.zero_y)
        if distx > c.max_x - (c.x_loc + c.zero_x) or distx < -1 * (c.x_loc + c.zero_x):
            print("Desired location exceeds max X coordinates by {}mm".format(str(distx)))
            return False
        elif disty > c.max_y - (c.y_loc + c.zero_y) or disty < -1 * (c.y_loc + c.zero_y):
            print("Desired location exceeds max Y coordinates by {}mm".format(str(disty)))
            return False
        else:
            return True

    def go(self,distx,disty):

        print("Gui move daemon initialized")
        stepsx = int(distx * c.steps_per_mm)
        stepsy = int(disty * c.steps_per_mm)
        print('Number of mm in x direction: ', distx)
        print('Number of mm in y direction: ', disty)

        if stepsx != 0:
            if stepsx > 0:
                print("Moving right")
                GPIO.output(mc.right.direc, mc.right.dir)
                i = 0
                while i < abs(stepsx):
                    mc.right.step(mc.right.nom_speed)
                    i = i +1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break
            else:
                print("Moving left")
                GPIO.output(mc.left.direc, mc.left.dir)
                i = 0
                while i < abs(stepsx):
                    mc.left.step(mc.left.nom_speed)
                    i = i +1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break

        if stepsy != 0:
            if stepsy > 0:
                print("Moving up")
                GPIO.output(mc.up.direc, mc.up.dir)
                i = 0
                while i < abs(stepsy):
                    mc.up.step(mc.up.nom_speed)
                    i = i +1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break
            else:
                print("Moving down")
                GPIO.output(mc.down.direc, mc.down.dir)
                i = 0
                while i < abs(stepsy):
                    mc.down.step(mc.down.nom_speed)
                    i = i +1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break
        
##        GPIO.output(pul_x, HIGH)
##        GPIO.output(pul_y, HIGH)

        print("Gui move daemon ending b/c end of sequence")


    def letsgo(self):
        if self.enterXEntry.get() == '':
            x = 0
        else:
            x = float(self.enterXEntry.get())

        if self.enterYEntry.get() == '':
            y = 0
        else:
            y = float(self.enterYEntry.get())

        print(str(x))
        print(str(y))

        distx = x - c.x_loc  # In mm
        disty = y - c.y_loc

  #      if self.check_go(distx,disty) == False:
      #      print("Error, outside of range!")
##                    limanswer = tkinter.messagebox.askokcancel("Boundary Error",
##                                                           "Point exceeds limit! Please enter new coordinate.")
##                    if limanswer == 'ok':
##                        return
    #    else:
        c.stopflag = 0
        moving_gui = threading.Thread(target = self.go(distx,disty))
        moving_gui.start()

    def stop(self):
        print("Stop motor!")
        c.stopflag = 1
        mc.hard_stop()

    def seq_list_initialize(self):
        self.xSeqs = []
        self.ySeqs = []
        self.waitEntries = []
        self.manualOptions = []

        for i in range(1, len(self.xSeq)+1):
            if len(self.xSeq[i].get()) != 0:
                self.xSeqs.append(float(self.xSeq[i].get()))
            if len(self.ySeq[i].get()) != 0:
                self.ySeqs.append(float(self.ySeq[i].get()))
            self.manualOptions.append(self.manualOption[i].get())
            if self.manualOption[i].get() == 1:
                self.waitEntries.append(0)
            elif len(self.waitEntry[i].get()) != 0:
                self.waitEntries.append(float(self.waitEntry[i].get()))

        print(self.xSeqs)
        print(self.ySeqs)
        print(self.waitEntries)
        print(self.manualOptions)
        print("Length of sequence: ", len(self.xSeqs))


    def seqRun(self):
        global iterations
        print("Run sequence!")

        self.seq_list_initialize()

        count = 0
        while count < iterations:
            for i in range(0, len(self.xSeqs)):
                distx = self.xSeqs[i] - c.x_loc  # In mm
                disty = self.ySeqs[i] - c.y_loc
                if self.check_go(distx,disty) == False:
                    print("Error, outside of range, go to next?")
                    limanswer = tkinter.messagebox.askokcancel("Boundary Error",
                                                           "Point exceeds limit! OK to skip, Cancel to terminate")
                    if limanswer == 'ok':
                        print("Continue to next point on sequence")
                        i +=1
                        distx = self.xSeqs[i] - c.x_loc  # In mm
                        disty = self.ySeqs[i] - c.y_loc
                        continue
                    if limanswer == 'cancel':
                        print("Terminating sequence")
                        self.stop()
                        break
                else:
                    c.stopflag = 0
                    moving_gui = threading.Thread(target = self.go(distx,disty))
                    moving_gui.start()

                if c.stopflag == 1:
                    mc.hard_stop()
                    break

                if self.manualOptions[i] == True:
                    manualanswer = tkinter.messagebox.askokcancel("Manual Wait Time",
                                                                "Press OK when ready to continue to next point!")
                    if manualanswer == 'ok':
                        print("Continue on to next point")
                        continue
                    elif manualanswer == 'cancel':
                        print("Terminating sequence")
                        mc.hard_stop()
                        break
                    pass
                else:
                    print("Waiting {} seconds" .format(str(self.waitEntries[i])))
                    sleep(self.waitEntries[i])
                    continue

            count += 1
            
        GPIO.output(pul_x, HIGH)
        GPIO.output(pul_y, HIGH)

    def addLine(self):
        print("Add line to sequence!")
        self.seq_list_initialize()
        print('Rows of entries before adding: ', len(self.manualOptions))

        i = len(self.manualOptions) + 1

        self.indexVal[i] = Label(self.listFrame, text=str(i))
        self.indexVal[i].grid(row=i, column=0)
        self.indexList.append(self.indexVal[i])
        self.xSeq[i] = Entry(self.listFrame)
        self.xSeq[i].grid(row=i, column=1)
        self.xSeqs.append(self.xSeq[i].get())
        self.ySeq[i] = Entry(self.listFrame)
        self.ySeq[i].grid(row=i, column=2)
        self.ySeqs.append(self.ySeq[i].get())
        self.waitEntry[i] = Entry(self.listFrame)
        self.waitEntry[i].grid(row=i, column=3)
        self.waitEntries.append(self.waitEntry[i].get())
        self.manualOption[i] = IntVar()
        self.manualOptions.append(self.manualOption[i])
        self.manualCheck = Checkbutton(self.listFrame, variable=self.manualOption[i], command=self.ifchecked)
        self.manualCheck.grid(row=i, column=4)

        MainWindow.update(self)
        self.seqCanvas.config(scrollregion=self.seqCanvas.bbox(ALL))

        print('Rows of entries after adding: ', len(self.manualOptions))

    def add_coord(self, *args):
        '''
        Adds a coordinate to list on GUI, increases index
        INPUTS:
        OUTPUTS:
        '''

        global index

        self.xSeqs.append(c.x_loc)
        self.ySeqs.append(c.y_loc)
        self.waitEntries.append(0)
        self.manualOptions.append(1)

        index = len(self.xSeqs)
        print(index)
        
        x = round(c.x_loc,3)
        y = round(c.y_loc,3)
        
        self.xSeq[index].insert(0, str(x))
        self.ySeq[index].insert(0, str(y))

        # Print new index number
        mc.print_lcd_ind(index)

    def ifchecked(self):
        for i in range(1,26):
            if self.manualOption[i].get() == 1:
                self.waitEntry[i].configure(state='disabled')
            else:
                self.waitEntry[i].configure(state='normal')


    def print_pos_gui(self):
        #This is the daemon function

        global stop_gui_thread

        sleep(1)

        print('GUI print daemon starting')

        while 1:
            self.currentPosAnswerX['text'] = ("%.3f" %c.x_loc)
            self.currentPosAnswerY['text'] = ("%.3f" %c.y_loc)
            
            #Reset limit triggers to "No" -- this may be problematic
            self.plusLimAnswerX['text'] = c.posXtrig
            self.plusLimAnswerY['text'] = c.posYtrig
            self.minusLimAnswerX['text'] = c.negXtrig
            self.minusLimAnswerY['text'] = c.negYtrig

            sleep(0.25)

            if stop_gui_thread:
                stop_gui_thread = 0
                break

#This window is only here because we are not sure if any port configuration will be required at TRIUMF (may be deleted)
class InstrumentWindow(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.title("Instrument Editor")
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=12, family="Helvetica", weight="bold")
        self.option_add("*Font", self.default_font)

        self.instrvar = StringVar(self)
        self.choices = {'Pendant', 'Raspberry Pi'}
        self.instrvar.set('Pendant')

        self.instrPopUpMenu = OptionMenu(self, self.instrvar, *self.choices)
        self.chooseOptionLabel = Label(self, text="Choose Instrument:").grid(row=0, column=0, sticky=W)
        self.instrPopUpMenu.grid(row=0, column=1, sticky=E + W)
        self.changeInstrLabel = Label(self, text="Change Port:").grid(row=1, column=0, sticky=W)
        self.changeInstrEntry = Entry(self)
        self.changeInstrEntry.grid(row=1, column=1, sticky=E + W)

        self.apply_button = Button(self, text="Apply Change", command=self.apply)
        self.apply_button.grid(row=2, column=0, sticky=E + W)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=2, column=1, sticky=E + W)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def apply(self):
        print("Apply instrument change - adjust!")
        # Again, we are not sure whether this is necessary or not.

    def cancel(self):
        print("Cancel change - erase entry line!")
        self.changeInstrEntry.delete(0, END)

class ChannelWindow(tkinter.Tk):
    def __init__(self):
        global channeloption

        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.title("Channel Editor")
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=text_size, family="Helvetica", weight = "bold")
        self.option_add("*Font", self.default_font)

        self.channelvar = StringVar(self)
        self.choices = {'Nominal Velocity', 'Nominal Acceleration'}
        self.channelvar.set('Nominal Velocity')

        self.channelPopUpMenu = OptionMenu(self, self.channelvar, *self.choices, command=self.check)
        channeloption = ('Nominal Velocity')
        self.chooseOptionLabel = Label(self, text="Choose Channel Property:").grid(row=0, column=0, sticky=W)
        self.channelPopUpMenu.grid(row=0, column=1, sticky=E + W)
        self.changeChannelLabel = Label(self, text="Change to:").grid(row=1, column=0, sticky=W)
        self.changeChannelEntry = Entry(self)
        self.changeChannelEntry.grid(row=1, column=1, sticky=E + W)

        self.apply_button = Button(self, text="Apply Change", command=self.apply)
        self.apply_button.grid(row=2, column=0, sticky=E + W)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=2, column=1, sticky=E + W)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def apply(self):

        print("Apply channel change - adjust coordinates!")
        if channeloption == ('Nominal Velocity'):
            c.nom_speed = float(self.changeChannelEntry.get())
            print(c.nom_speed)
        elif channeloption == ('Nominal Acceleration'):
            c.nom_accel = float(self.changeChannelEntry.get())
            print(c.nom_accel)

    def cancel(self):
        print("Cancel change - erase entry line!")
        self.changeChannelEntry.delete(0, END)

    def check(self, value):
        global channeloption
        channeloption = value
        print(channeloption)


class SequenceWindow(tkinter.Tk):
    def __init__(self):

        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.title("Sequence Editor")
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=text_size, family="Helvetica", weight = "bold")
        self.option_add("*Font", self.default_font)

        self.iterationsLabel = Label(self, text="Iterations:").grid(row=0, column=0, sticky=W)
        self.iterationsEntry = Entry(self)
        self.iterationsEntry.grid(row=0, column=1, sticky=E + W)

        self.apply_button = Button(self, text="Apply Change", command=self.apply)
        self.apply_button.grid(row=2, column=0, sticky=E + W)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=2, column=1, sticky=E + W)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def apply(self):
        print("Apply iterations change - adjust coordinates!")
        global iterations
        iterations = int(self.iterationsEntry.get())
        print(iterations)

    def cancel(self):
        print("Cancel change - erase entry line!")
        self.iterationsEntry.delete(0, END)


class StepWindow(tkinter.Tk):
    def __init__(self):
        global stepoption

        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.title("Step Editor")
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=text_size, family="Helvetica", weight = "bold")
        self.option_add("*Font", self.default_font)

        self.stepvar = StringVar(self)
        self.choices = {'Zero Coordinate X', 'Zero Coordinate Y'}
        self.stepvar.set('Zero Coordinate X')

        self.stepPopUpMenu = OptionMenu(self, self.stepvar, *self.choices, command=self.check)
        stepoption = 'Zero Coordinate X'
        self.chooseOptionLabel = Label(self, text="Choose Step:").grid(row=0, column=0, sticky=W)
        self.stepPopUpMenu.grid(row=0, column=1, sticky=E+W)
        self.changeStepLabel = Label(self, text="Change to (mm):").grid(row=1, column=0, sticky=W)
        self.changeStepEntry = Entry(self)
        self.changeStepEntry.grid(row=1, column=1, sticky=E + W)

        self.apply_button = Button(self, text="Apply Change", command=self.apply)
        self.apply_button.grid(row=2, column=0, sticky=E + W)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=2, column=1, sticky=E + W)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def apply(self):
        global stepoption
        mw = MainWindow()
        mw.withdraw()
        mw.destroy()

        print("Apply step change - adjust coordinates!")
        print(stepoption)

        if stepoption == ('Zero Coordinate X'):
            #Set as new x zero coordinate
            c.zero_x = float(self.changeStepEntry.get())
            c.x_loc = c.x_loc - c.zero_x
            print('X Location is ', c.x_loc)
            mw.currentPosAnswerX['text'] = ("%.3f" % c.x_loc)
        elif stepoption == ('Zero Coordinate Y'):
            #Set as new y zero coordinate
            c.zero_y = float(self.changeStepEntry.get())
            c.y_loc = c.y_loc - c.zero_y
            print('X Location is ', c.y_loc)
            mw.currentPosAnswerX['text'] = ("%.3f" % c.y_loc)

    def cancel(self):
        print("Cancel change - erase entry line!")
        self.changeStepEntry.delete(0, END)

    def check(self, value):
        global stepoption
        stepoption = value


class MotorControlWindow(tkinter.Tk):
    def __init__(self):
        global motoroption

        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.title("Motor Control")
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=text_size, family="Helvetica", weight="bold")
        self.option_add("*Font", self.default_font)

        self.motorvar = StringVar(self)
        self.choices = {'X Axis', 'Y Axis'}
        self.motorvar.set('X Axis')

        self.motorPopUpMenu = OptionMenu(self, self.motorvar, *self.choices, command = self.check)
        motoroption = ('X Axis')
        self.chooseOptionLabel = Label(self, text="Choose Axis:").grid(row=0, column=0, sticky=W)
        self.motorPopUpMenu.grid(row=0, column=1, sticky=E + W)

        self.currentPosLabel = Label(self, text="Current Position (mm):").grid(row=1, column=0, sticky=W)
        #NEED TO CHANGE THIS
        if motoroption == ('X Axis'):
            self.PosAnswer = Label(self)
            self.PosAnswer.grid(row=1, column=1, sticky=E)
            self.PosAnswer['text'] = ("%.3f" % c.x_loc)
        elif motoroption == ('Y Axis'):
            self.PosAnswer = Label(self)
            self.PosAnswer.grid(row=1, column=1, sticky=E)
            self.PosAnswer['text'] = ("%.3f" % c.y_loc)

        self.destinationLabel = Label(self, text="Destination:").grid(row=2, column=0, sticky=W)
        self.destinationEntry = Entry(self)
        self.destinationEntry.grid(row=2, column=1, sticky=E + W)

        self.move_button = Button(self, text="Move", fg = "green", command=self.letsmove).grid(row=3, column=0, sticky=E + W)
        self.stop_button = Button(self, text="STOP", fg = "red", command=self.stop).grid(row=3, column=1, sticky=E + W)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        printing_mot = threading.Thread(target = MotorControlWindow.print_pos_mot)
        printing_mot.setDaemon(True)
        printing_mot.start()

    def print_pos_mot(self):
        while 1:
            if motoroption == ('X Axis'):
                mot.PosAnswer['text'] = ("%.3f" % c.x_loc)
            elif motoroption == ('Y Axis'):
                mot.PosAnswer['text'] = ("%.3f" % c.y_loc)
            else:
                mot.PosAnswer['text'] = '0'
            sleep(0.25)

            if stop_gui_thread:
                stop_gui_thread = 0
                break
    
    def check_move(self, distx, disty):

        if distx > c.max_x - (c.x_loc + c.zero_x) or distx < -1 * (c.x_loc + c.zero_x):
            print("Desired location exceeds max X coordinates by {}mm".format(str(distx)))
            #return False
        elif disty > c.max_y - (c.y_loc + c.zero_y) or disty < -1 * (c.y_loc + c.zero_y):
            print("Desired location exceeds max Y coordinates by {}mm".format(str(disty)))
            #return False
        else:
            return True
        return True

    def move(self, distx, disty):

        print("Gui move daemon initialized")
        stepsx = int(distx * c.steps_per_mm)
        stepsy = int(disty * c.steps_per_mm)
        print('Number of steps in x direction: ', distx)
        print('Number of steps in y direction: ', disty)

        if stepsx != 0:
            if stepsx > 0:
                print("Moving right")
                i = 0
                while i < abs(stepsx):
                    mc.right.step(mc.right.nom_speed)
                    i = i + 1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break
            else:
                print("Moving left")
                i = 0
                while i < abs(stepsx):
                    mc.left.step(mc.left.nom_speed)
                    i = i + 1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break

        if stepsy != 0:
            if stepsy > 0:
                print("Moving up")
                i = 0
                while i < abs(stepsy):
                    mc.up.step(mc.up.nom_speed)
                    i = i + 1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break
            else:
                print("Moving down")
                i = 0
                while i < abs(stepsy):
                    mc.down.step(mc.down.nom_speed)
                    i = i + 1
                    main.update()
                    if c.stopflag:
                        print("Gui move daemon ending b/c STOP")
                        break
        print("Gui move daemon ending b/c end of sequence")
        
        if motoroption == ('X Axis'):
            self.PosAnswer['text'] = ("%.3f" % c.x_loc)
        elif motoroption == ('Y Axis'):
            self.PosAnswer['text'] = ("%.3f" % c.y_loc)

    def letsmove(self):
        print("Send motor to entered position!")
        if motoroption == ('X Axis'):
            x = float(self.destinationEntry.get())
            y = c.y_loc

        if motoroption == ('Y Axis'):
            x = c.x_loc
            y = float(self.destinationEntry.get())

        distx = x - c.x_loc  # In mm
        disty = y - c.y_loc

##        if self.check_move(distx, disty) == False:
##            print("Error, outside of range!")
##            limanswer = tkinter.messagebox.askokcancel("Boundary Error",
##                                                       "Point exceeds limit! Please enter new coordinate.")
##            if limanswer == 'ok':
##                return

        c.stopflag = 0
        moving_motor_control = threading.Thread(target=self.move(distx, disty))
        moving_motor_control.start()

    def stop(self):
        print("Stop motor!")
        c.stopflag = 1
        mc.hard_stop()

    def check(self, value):
        global motoroption
        motoroption = value
        print('Axis choice: ', motoroption)

if __name__ == "__main__":

    # Initialize daemon thread for printing
    printing = threading.Thread(target = mc.print_pos_lcd)
    printing.setDaemon(True)
    printing.start()

    main = MainWindow()
    main.geometry("800x500")

    #c.stop_lim_thread = 1

    printing_gui = threading.Thread(target = main.print_pos_gui)
    printing_gui.setDaemon(True)
    printing_gui.start()

    limitcheck = threading.Thread(target = main.lim_stop)
    limitcheck.setDaemon(True)
    limitcheck.start()

    # Start interrupts
    GPIO.add_event_detect(right_but, GPIO.FALLING, callback = mc.right.move_pend, bouncetime = 400)
    GPIO.add_event_detect(left_but, GPIO.FALLING, callback = mc.left.move_pend, bouncetime = 400)
    GPIO.add_event_detect(up_but, GPIO.FALLING, callback = mc.up.move_pend, bouncetime = 400)
    GPIO.add_event_detect(down_but, GPIO.FALLING, callback = mc.down.move_pend, bouncetime = 400)

    GPIO.add_event_detect(zero_but, GPIO.FALLING, callback = mc.set_zero_pend, bouncetime = 500)
    GPIO.add_event_detect(save_but, GPIO.FALLING, callback = main.add_coord, bouncetime = 500)

    main.mainloop()

    #mc.cleanup()
    
    mc.stop_daemon()
    mc.shutoff_lcd()
