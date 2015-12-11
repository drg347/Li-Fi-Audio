from Tkinter import *
from tkFileDialog import *
import functools
import serial

ser = serial.Serial('COM3', 9600)
record_notes = []
record = False
note_freq_map = {'C1': 33,
                'CS1': 35,
                'D1': 37,
                'DS1': 39,
                'E1': 41,
                'F1': 44,
                'FS1': 46,
                'G1': 49,
                'GS1': 52,
                'A1': 55,
                'AS1': 58,
                'B1': 62,
                'C2': 65,
                'CS2': 69,
                'D2': 73,
                'DS2': 78,
                'E2': 82,
                'F2': 87,
                '0': 0}

def callback(event, param):
    note = param
    record_notes.append(note)
    freq = note_freq_map[note]
    ser.write(str(freq))
        
def clear_recording(event):
    del record_notes[:]

def play_recording(event):
    notes = record_notes
    if len(notes) > 0:
        for note in notes:
            freq = note_freq_map[note]
            ser.write(str(freq))

def save_recording(event):
    fname = asksaveasfile(mode='w', defaultextension=".notes")
    if fname is None: 
        return
    content = str.join(',', record_notes)
    fname.write(content)
    fname.close()


def open_recording(event):
    del record_notes[:]
    fname = askopenfilename(parent = root)
    if fname:
        try:
                with open(fname) as f:
                    content = f.read()
                    notes = content.split(',')
                    for note in notes:
                        record_notes.append(note)
        except:
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
                return

root = Tk()
root.title("LiFi - Piano")
root.geometry('{}x{}'.format(1200,550))

play_rec = Button(root, text = 'Play Recording', bg = 'green')
play_rec.place(x = 45, y = 50, width = 240, height = 25)
play_rec.bind("<Button-1>", functools.partial(play_recording))

clear_rec = Button(root, text = 'Clear Recording', bg = 'red')
clear_rec.place(x = 335, y = 50, width = 240, height = 25)
clear_rec.bind("<Button-1>", functools.partial(clear_recording))

save_rec = Button(root, text = 'Save Recording', bg = 'blue')
save_rec.place(x = 625, y = 50, width = 240, height = 25)
save_rec.bind("<Button-1>", functools.partial(save_recording))

open_rec = Button(root, text = 'Open Recording', bg = 'white')
open_rec.place(x = 915, y = 50, width = 240, height = 25)
open_rec.bind("<Button-1>", functools.partial(open_recording))

# normal notes
c1 = Button(root, text = 'C1', bg = 'white')
c1.place(x = 50, y = 100, width = 100, height = 400)
c1.bind("<Button-1>", functools.partial(callback, param = 'C1'))
d1 = Button(root, text = 'D1', bg = 'white')
d1.place(x = 150, y = 100, width = 100, height = 400)
d1.bind("<Button-1>", functools.partial(callback, param = 'D1'))
e1 = Button(root, text = 'E1', bg = 'white')
e1.place(x = 250, y = 100, width = 100, height = 400)
e1.bind("<Button-1>", functools.partial(callback, param = 'E1'))
f1 = Button(root, text = 'F1', bg = 'white')
f1.place(x = 350, y = 100, width = 100, height = 400)
f1.bind("<Button-1>", functools.partial(callback, param = 'F1'))
g1 = Button(root, text = 'G1', bg = 'white')
g1.place(x = 450, y = 100, width = 100, height = 400)
g1.bind("<Button-1>", functools.partial(callback, param = 'G1'))
a1 = Button(root, text = 'A1', bg = 'white')
a1.place(x = 550, y = 100, width = 100, height = 400)
a1.bind("<Button-1>", functools.partial(callback, param = 'A1'))
b1 = Button(root, text = 'B1', bg = 'white')
b1.place(x = 650, y = 100, width = 100, height = 400)
b1.bind("<Button-1>", functools.partial(callback, param = 'B1'))
c2 = Button(root, text = 'C2', bg = 'white')
c2.place(x = 750, y = 100, width = 100, height = 400)
c2.bind("<Button-1>", functools.partial(callback, param = 'C2'))
d2 = Button(root, text = 'D2', bg = 'white')
d2.place(x = 850, y = 100, width = 100, height = 400)
d2.bind("<Button-1>", functools.partial(callback, param = 'D2'))
e2 = Button(root, text = 'E2', bg = 'white')
e2.place(x = 950, y = 100, width = 100, height = 400)
e2.bind("<Button-1>", functools.partial(callback, param = 'E2'))
f2 = Button(root, text = 'F2', bg = 'white')
f2.place(x = 1050, y = 100, width = 100, height = 400)
f2.bind("<Button-1>", functools.partial(callback, param = 'F2'))

# sharp notes
cs1 = Button(root, text = 'CS1', bg = 'black', fg = 'white')
cs1.place(x = 120, y = 100, width = 60, height = 300)
cs1.bind("<Button-1>", functools.partial(callback, param = 'CS1'))
ds1 = Button(root, text = 'DS1', bg = 'black', fg = 'white')
ds1.place(x = 220, y = 100, width = 60, height = 300)
ds1.bind("<Button-1>", functools.partial(callback, param = 'DS1'))
fs1 = Button(root, text = 'FS1', bg = 'black', fg = 'white')
fs1.place(x = 420, y = 100, width = 60, height = 300)
fs1.bind("<Button-1>", functools.partial(callback, param = 'FS1'))
gs1 = Button(root, text = 'GS1', bg = 'black', fg = 'white')
gs1.place(x = 520, y = 100, width = 60, height = 300)
gs1.bind("<Button-1>", functools.partial(callback, param = 'GS1'))
as1 = Button(root, text = 'AS1', bg = 'black', fg = 'white')
as1.place(x = 620, y = 100, width = 60, height = 300)
as1.bind("<Button-1>", functools.partial(callback, param = 'AS1'))
cs2 = Button(root, text = 'CS2', bg = 'black', fg = 'white')
cs2.place(x = 820, y = 100, width = 60, height = 300)
cs2.bind("<Button-1>", functools.partial(callback, param = 'CS2'))
ds2 = Button(root, text = 'DS2', bg = 'black', fg = 'white')
ds2.place(x = 920, y = 100, width = 60, height = 300)
ds2.bind("<Button-1>", functools.partial(callback, param = 'DS2'))

root.mainloop()
