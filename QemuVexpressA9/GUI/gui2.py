#!/usr/bin/python3

# Sources:
# https://lazka.github.io/pgi-docs
# https://python-gtk-3-tutorial.readthedocs.io/en/latest/button_widgets.html
# https://developer.gnome.org/gtk3/stable/
# Threads: https://wiki.gnome.org/Projects/PyGObject/Threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

import threading
# Communication part
import struct
pipc_magick = 0x6910
import posix_ipc as pipc
mq_to_qemu = pipc.MessageQueue("/to_qemu",flags=pipc.O_CREAT, read=False, write=True)
mq_from_qemu = pipc.MessageQueue("/from_qemu",flags=pipc.O_CREAT, read=True, write=False)


def send_change(nof_pin, state):
    s=struct.pack(">HBB",pipc_magick,nof_pin,state)
    mq_to_qemu.send(s)

def recv_change(msg):
    mg, pin, state = struct.unpack(">HBB",msg)
    print("mg=",mg," pin=",pin," state=",state) 
    if mg != pipc_magick:
        raise Exception("Wrong magick number in GPIO IPC message") 
    if state == 0:
        s = 0
    else:
        s = 1
    GLib.idle_add(MyLeds[pin-24].change_state,s)
    
def receiver():
    while True:
        msg = mq_from_qemu.receive()
        recv_change(msg[0])
        
class MySwitch(Gtk.Switch):
    def __init__(self,number):
        super().__init__()
        self.number = number

class MyButton(Gtk.Button):
    def __init__(self,number):
        super().__init__(label=str(number))
        self.number = number
        
class MyLed(Gtk.Label):
    color = Gdk.color_parse('gray')
    rgba0 = Gdk.RGBA.from_color(color)
    color = Gdk.color_parse('green')
    rgba1 = Gdk.RGBA.from_color(color)
    del color
    
    def __init__(self, number):
        super().__init__( label=str(number))
        self.number = number
        self.change_state(0)
    
    def change_state(self,state):
        if state == 1:
            self.override_background_color(0,self.rgba1)
        else:
            self.override_background_color(0,self.rgba0)
    
MyLeds = []
        
class SwitchBoardWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Switch Demo")
        self.set_border_width(10)
        mainvbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        self.add(mainvbox)
        #Create the switches
        label = Gtk.Label(label = "Stable switches: left 0, right 1")
        mainvbox.pack_start(label,True,True,0)
        hbox = Gtk.Box(spacing=6)
        for i in range(0,12):
            vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
            label = Gtk.Label(label = str(i))
            vbox.pack_start(label,True,True,0)            
            switch = MySwitch(i)
            switch.connect("notify::active", self.on_switch_activated)
            switch.set_active(False)
            vbox.pack_start(switch,True,True,0)            
            hbox.pack_start(vbox, True, True, 0)
        mainvbox.pack_start(hbox,True,True,0)
        #Create the buttons
        label = Gtk.Label(label = "Unstable buttons: pressed 0, released 1")
        mainvbox.pack_start(label,True,True,0)
        hbox = Gtk.Box(spacing=6)
        for i in range(12,24):
            button = MyButton(i)
            button.connect("button-press-event", self.on_button_clicked,0)
            button.connect("button-release-event", self.on_button_clicked,1)
            hbox.pack_start(button,True,True,0)            
        mainvbox.pack_start(hbox,True,True,0)
        #Create the LEDS
        label = Gtk.Label(label = "LEDs")
        mainvbox.pack_start(label,True,True,0)
        hbox = Gtk.Box(spacing=6)
        for i in range(24,32):
            led = MyLed(i)
            MyLeds.append(led)
            hbox.pack_start(led,True,True,0)            
        mainvbox.pack_start(hbox,True,True,0)
            
    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = 0
        else:
            state = 1
        #MyLeds[switch.number].change_state(state)
        send_change(switch.number,state)
        print("Switch #"+str(switch.number)+" was turned", state)
        return True

    def on_button_clicked(self, button,gparam, state):
        print("pressed!")
        send_change(button.number,state)
        print("Button #"+str(button.number)+" was turned", state)
        return True


win = SwitchBoardWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()

thread = threading.Thread(target=receiver)
thread.daemon = True
thread.start()

Gtk.main()


