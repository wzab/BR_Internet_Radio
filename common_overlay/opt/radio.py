import os
import time                                                                     
from itertools import cycle                                                     
from flask import Flask, render_template,request,redirect                                        
import flask_wtf
from flask_wtf import FlaskForm # For new Flask
#from flask_wtf import Form as FlaskForm # for old Flask in Plx 2016.4
from wtforms import FieldList, FormField
from wtforms import StringField,SubmitField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired
from classes import *
import mpd
import threading

cfg_file = "/etc/radio.xml"
# https://stackoverflow.com/questions/46653424/flask-wtforms-fieldlist-with-booleanfield
# escaping based on https://stackoverflow.com/questions/1546717/escaping-strings-for-use-in-xml
# Connect to the mpd daemon
mpc = mpd.MPDClient()
mpc_lock = threading.Lock()
radio_quit = False

# Default configuration
config=ctempl()
config.mycfg=ctempl()
config.mycfg.radios=[
  xradio("Złote przeboje","http://stream10.radioagora.pl/zp_waw_128.mp3"),
  xradio("Trójka","http://mp3.polskieradio.pl:8904/"),
  ]
config.mycfg.now_play="0"
config.mycfg.stopped=False
try:
   ncfg = open(cfg_file,"rt").read()
   nconfig = decode_xml(ncfg)
   config = nconfig
except Exception:
   pass
#Start playing the previously played station
if not config.mycfg.stopped:
   nst = int(config.mycfg.now_play)
   with mpc_lock:
      mpc.connect("localhost",6600)
      mpc.clear()
      mpc.add(config.mycfg.radios[nst].url)
      mpc.play()
      mpc.close()
      mpc.disconnect()
#Start the thread that attempts to reinitialize playing
def mpd_revive():
   while not radio_quit:
      if not config.mycfg.stopped:
         with mpc_lock:
            mpc.connect("localhost",6600)
            if mpc.status()['state']=='stop':
               mpc.play()
            mpc.close()
            mpc.disconnect()
      time.sleep(10)
revive = threading.Thread(target=mpd_revive,args=())
revive.start()

app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'

# https://stackoverflow.com/questions/6036082/call-a-python-function-from-jinja2
@app.context_processor
def utility_processor():
    def goto_url(target=""):
      print("I\'m supposed to go to: "+target)
    def goto_ipcams():
      print("I\'m supposed to go to: ipcams")

    def goto_tvicams():
      print("I\'m supposed to go to: TVIcams")

    def goto_hdmicams():
      print("I\'m supposed to go to: HDMIcams")
    return dict(goto_url=goto_url,goto_ipcams=goto_ipcams,goto_tvicams=goto_tvicams,goto_hdmicams=goto_hdmicams)

# Radio services

class Radio(FlaskForm):
    rname = StringField('')
    url = StringField('')
    play = SubmitField('Play')
    up = SubmitField('Up')
    down = SubmitField('Down')
    remove = SubmitField('Del')

class RadioUI(FlaskForm):
    radios = FieldList(FormField(Radio), min_entries=0)
    new_name = StringField('Name')
    new_url = StringField('Url')
    add_first = SubmitField('Insert')
    add_last = SubmitField('Append')
    stop = SubmitField('Stop')
    jump = SubmitField('List')
    save = SubmitField('Save')

class RadioItem(FlaskForm):
    rname = StringField('')
    url = HiddenField('')
    play = SubmitField('Play')
class RadioList(FlaskForm):
    stop = SubmitField('Stop')
    jump = SubmitField('Edit')
    save = SubmitField('Save')
    radios = FieldList(FormField(RadioItem),min_entries=0)


@app.route("/",methods=['GET','POST'])
def list_radios():
    #Create the object containing just the names and urls
    state = RadioList(obj=config.mycfg)
    if state.validate_on_submit():
       state.populate_obj(config.mycfg)
       for i in range(0,len(state.radios)):
          rs = state.radios[i]
          if rs.play.data:
             print("Selected: "+str(i))
             #Here we should start playing the selected radio
             config.mycfg.now_play = str(i)
             config.mycfg.stopped = False
             with mpc_lock:
                mpc.connect("localhost",6600)
                mpc.clear()
                mpc.add(rs.url.data)
                mpc.play()
                mpc.close()
                mpc.disconnect()
       if state.stop.data:
             #We stop playing at all
             config.mycfg.stopped = True
             with mpc_lock:
                mpc.connect("localhost",6600)
                mpc.clear()
                mpc.close()
                mpc.disconnect()
       if state.save.data:
             #We save data to the file
             cfg = config.encode('root',0)
             with open(cfg_file,'wt') as fo:
               fo.write(cfg)
               os.system('sync')
       if state.jump.data:
           return redirect("/edit")
       return redirect("/")
    else:
       print("not validated")
    print(state.errors)
    print(str(state))
    return render_template('radio_list.html',title='Radios',state=state)


@app.route("/edit",methods=['GET','POST'])
def update_radios():
    state = RadioUI(obj=config.mycfg)
    if state.validate_on_submit():
       state.populate_obj(config.mycfg)
       for i in range(0,len(state.radios)):
          rs = state.radios[i]
          if rs.play.data:
             print("Selected: "+str(i))
             #Here we should start playing the selected radio
             config.mycfg.now_play = str(i)
             config.mycfg.stopped = False
             with mpc_lock:
                mpc.connect("localhost",6600)
                mpc.clear()
                mpc.add(rs.url.data)
                mpc.play()
                mpc.close()
                mpc.disconnect()
          if rs.remove.data:
             tmp = config.mycfg.radios[0:i] + config.mycfg.radios[i+1:]
             config.mycfg.radios = tmp
          if rs.up.data:
             if i>0:
                tmp = config.mycfg.radios[i]
                config.mycfg.radios[i] = config.mycfg.radios[i-1]
                config.mycfg.radios[i-1] = tmp
          if rs.down.data:
             if i<len(state.radios)-1:
                tmp = config.mycfg.radios[i]
                config.mycfg.radios[i] = config.mycfg.radios[i+1]
                config.mycfg.radios[i+1] = tmp
       if state.stop.data:
             #We stop playing at all
             config.mycfg.stopped = True
             with mpc_lock:
                mpc.connect("localhost",6600)
                mpc.clear()
                mpc.close()
                mpc.disconnect()
       if state.save.data:
             #We save data to the file
             cfg = config.encode('root',0)
             with open(cfg_file,'wt') as fo:
               fo.write(cfg)
               os.system('sync')
       if state.add_first.data:
             config.mycfg.radios.insert(0,xradio(state.new_name.data,state.new_url.data))
       if state.add_last.data:
             config.mycfg.radios.append(xradio(state.new_name.data,state.new_url.data))
       if state.jump.data:
           return redirect("/")
       return redirect("/edit")
    else:
       print("not validated")
    print(state.errors)
    print(str(state))
    return render_template('radios.html',title='Edit radios',state=state)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8810)

