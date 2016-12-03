import Tkinter
import tkFileDialog
import os

root = Tkinter.Tk()
root.withdraw() #use to hide tkinter window
#filetypes = [('all files', '.*'), ('text files', '.txt')]
currdir = os.getcwd()
tempdir = tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Select output file',filetypes=[('text files','.txt')])
if len(tempdir) > 0:
    print "You chose %s" % tempdir 
