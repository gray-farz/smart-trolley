from tkinter import *
import tkinter as tk
from tkinter import ttk,font

from mainClass import MainClass
        
ver_win=1400
hor_win=1000
x_win=8
y_win=8

root_asli = Tk()
root_asli.geometry("%dx%d+%d+%d" % (ver_win,hor_win,x_win,y_win))
app=MainClass(root_asli)



