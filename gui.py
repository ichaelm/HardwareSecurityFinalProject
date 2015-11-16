from Tkinter import *
import sys
import glob
import serial
import Tkinter as tk
import key_comm
import random
import math
import rsa

shared_modulous = 208297667
public_key = 46769

BAUD_RATE = 115200

class Layout:

    def __init__(self, root):
        main_frame = Frame(root)
        main_frame.configure(bg="light grey", relief="sunken")
        desc_label = Label(main_frame, bg="light grey", text="Please select your authenticator:").pack(side=TOP, anchor=W, expand=NO, padx=16, pady=(16, 0))
        row_1_frame = Frame(main_frame, bg="light grey")
        self.variable = StringVar(root)
        devices = self.get_devices()
        self.variable.set(devices[0])
        self.device_selector = apply(OptionMenu, (row_1_frame, self.variable) + tuple(devices))
        self.device_selector.configure(bg="light grey", width=48)
        self.device_selector.pack(side=LEFT, anchor=NW, padx=(16,0), expand=NO)
        auth_button = Button(row_1_frame, text="Authenticate", bg="light grey", highlightbackground="light grey", width=12, command=self.authenticate).pack(side=LEFT, anchor=NW, padx=8)
        refresh_button = Button(row_1_frame, text="Refresh", bg="light grey", highlightbackground="light grey", width=8, command=self.refresh).pack(side=LEFT, anchor=NW, padx=8)
        row_1_frame.pack(fill=BOTH, expand=YES)
        text_frame = Frame(main_frame, bg="light grey")
        scroll_bar = Scrollbar(text_frame)
        self.text = Text(text_frame, wrap="word", yscrollcommand=scroll_bar.set, borderwidth=0, highlightthickness=0)
        self.text.insert(END, "Waiting for authenticator...\n")
        self.text.bind("<1>", lambda event: self.text.focus_set())
        self.text.configure(state=DISABLED)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_bar.config(command=self.text.yview)
        self.text.pack(side=LEFT, fill=BOTH, expand=YES)
        text_frame.pack(fill=BOTH, expand=YES, padx=16, pady=(0,16))
        main_frame.pack(fill=BOTH, expand=YES)
        self.device = key_comm.KeyDevice(self.variable.get());


    def get_devices(self):
        return self.serial_ports()

    def authenticate(self):
        self.console_write(self.variable.get())
        uuid = self.device.get_id()
        print('got uuid: ' + str(uuid))
        noonce = self.rand_32bit()
        print('nonce = ' + str(noonce))
        self.console_write(noonce)
        enc_noonce = self.device.encrypt(noonce)
        print('encrypted noonce = ' + str(enc_noonce))
        dec_noonce = rsa.decrypt(enc_noonce, public_key, shared_modulous)
        print('decrypted noonce = ' + str(dec_noonce))
        self.console_write(dec_noonce)
        if (noonce == dec_noonce):
            self.console_write("Authentication Seccuessful!")
        else:
            self.console_write("Authentication Failed!")

    def refresh(self):
        print("REFRESHING!!!")
        devices = self.get_devices()
        self.variable.set(devices[0])
        self.device_selector['menu'].delete(0, 'end')
        for device in devices:
            self.device_selector['menu'].add_command(label=device, command=tk._setit(self.variable, device))

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def console_write(self, message):
        self.text.configure(state=NORMAL)
        self.text.insert(END, str(message)+"\n")
        self.text.configure(state=NORMAL)

    def rand_32bit(self):
        return random.randint(0, pow(2, 16))




root = Tk()
root.title("Authenticator")
layout = Layout(root)
root.mainloop()
