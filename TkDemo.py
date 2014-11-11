import piplates.ppDAQC as ppDAQC
import time
from Tkinter import *

addr=0

def callback():
    ppDAQC.CLOSE()
    root.destroy()  
  
def task():
    val=ppDAQC.getADC(addr,8)
    VccText.set(val)
    for i in range(0,8):        
        val=ppDAQC.getADC(addr,i)
        analogin[i].set(val)
        j=ppDAQC.getDINbit(addr,i)
        chkivar[i].set(j)        
    root.after(1000,task)

def toggleChk(par): 
    if chkovar[par].get()==1:       
        ppDAQC.setDOUTbit(addr,par)
    else:
        ppDAQC.clrDOUTbit(addr,par)

def DoDAC0():
    ppDAQC.setDAC(addr,0,DACin0.get())
        
def DoDAC1():
    ppDAQC.setDAC(addr,1,DACin1.get())

def setADDR():
    global addr
    addr=int(ADDRenter.get())
    ADDRin.set(ADDRenter.get())
    
                      
root = Tk()
root.config(bg="black")
root.wm_title("ppDAQC Demo")

af=Frame(root,bg="#000444000",padx=4,pady=4)
root.columnconfigure(1,weight=1)
root.rowconfigure(0,weight=1)
af.grid(row=2,column=0, sticky=N+S+W+E)

dof=Frame(root,bg="#000000444",padx=4,pady=4)
dof.columnconfigure(0,weight=1)
dof.rowconfigure(0,weight=5)
dof.columnconfigure(1,weight=1)
dof.rowconfigure(1,weight=5)
dof.grid(row=2,column=1, sticky=N+S+W+E)

dif=Frame(root,bg="#444000000",padx=10,pady=1)
dif.grid(row=2,column=2, sticky=N+S+W+E)

dacf=Frame(root,bg="#888888000",padx=5,pady=5
           ,height=200, width=300)
dacf.grid(row=1,column=1,columnspan=2, sticky=N+S+W+E)

imgf=Frame(root,bg="white")
imgf.grid(row=0,column=0,rowspan=2)

sysf=Frame(root,bg="black")
sysf.grid(row=0,column=1, columnspan=2)

Label(sysf,text="Board Address: "
      ,bg="black",fg="White").grid(row=0,column=0,columnspan=2,sticky=E)
ADDRin=StringVar()
ADDRin.set("0")
ADDRenter=StringVar()
ADDRenter.set("0")
Label(sysf,textvariable=ADDRin
      ,bg="black",fg="White").grid(row=0,column=2,columnspan=2, sticky=W)
addrentry=Entry(sysf,textvariable=ADDRenter
                ,width=1).grid(row=1,column=0)
ADDRbutton=Button(sysf,text="Set",command=setADDR,padx=4,pady=4).grid(row=1, column=1, sticky=W)

QUITbutton=Button(sysf,text="Quit",command=callback,padx=4,pady=4).grid(row=1, column=3,sticky=E)

Label(af,text="Power Supply Voltage:",padx=4,pady=4
      ,bg="#000444000",fg="White").grid(row=1,column=0,sticky=E)

VccText=StringVar()
VccText.set("initializing")
Label(af,textvariable=VccText,padx=4,pady=4,bg="#000444000",fg="White").grid(row=1,column=1, sticky=W)

analogin = range(8)
for i in range(0,8):
    Label(af,text="A/D Channel "+str(i)+":"
          ,padx=4,pady=4,bg="#000444000"
          ,fg="White").grid(row=i+2,column=0,sticky=E)    
    analogin[i]=StringVar()
    analogin[i].set("initializing")
    Label(af,textvariable=analogin[i],padx=4,pady=4,bg="#000444000",fg="White").grid(row=i+2,column=1, sticky=W)

Label(dof,text="Digital Outputs"
      ,padx=4,pady=4,bg="#000000444"
      ,fg="White").grid(row=0,column=0,sticky=N)

chkovar = range(7)
for i in range(0,7):
    ppDAQC.clrDOUTbit(0,i)
    chkovar[i]=IntVar()
    chkovar[i].set(0)
    Checkbutton(dof,text="Digital Output "+str(i)
                ,padx=4,pady=5, indicatoron=1
                ,bg="#000000444",fg="White", variable=chkovar[i], selectcolor="blue"
                ,command=lambda j=i: toggleChk(j)).grid(row=i+1,column=0)

Label(dif,text="Digital Inputs"
      ,padx=4, pady=8,bg="#444000000"
      ,fg="White").grid(row=0,column=0,sticky=N)

chkivar = range(8)
for i in range(0,8):
    chkivar[i]=IntVar()
    chkivar[i].set(0)
    Label(dif,text="Digital Input "+str(i)+":"
          ,padx=4,pady=4,bg="#444000000"
          ,fg="White").grid(row=1+i,column=0, sticky=W)
    Label(dif,textvariable=str(chkivar[i])
          ,padx=4,pady=4,bg="#444000000"
          ,fg="White").grid(row=1+i,column=1, sticky=W)

Label(dacf,text="Digital to Analog Converters:"
      ,bg="#888888000",fg="White"
      ,padx=20,pady=8).grid(row=0, column=0,columnspan=2)

DACin0=DoubleVar()
DACin1=DoubleVar()
D2A0=Entry(dacf,textvariable=DACin0,width=5).grid(row=1, column=0)
D2A1=Entry(dacf,textvariable=DACin1,width=5).grid(row=2, column=0)
DAC0button=Button(dacf,text="Enter DAC0",command=DoDAC0
                  ,padx=4,pady=4).grid(row=1, column=1)
DAC1button=Button(dacf,text="Enter DAC1",command=DoDAC1
                  ,padx=4,pady=4).grid(row=2, column=1)

logo=PhotoImage(file="3D-ppLogoSmall.gif")
Label(imgf,image=logo,anchor="center").grid(row=0,column=0)

root.wm_protocol("WM_DELETE_WINDOW", callback)
root.after(1000,task)
root.mainloop()
ppDAQC.CLOSE()

