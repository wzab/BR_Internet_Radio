#!/usr/bin/python
import gpiod
import time
chip = gpiod.Chip('gpiochip0')
button = chip.get_line(13)
button.request(consumer="its_me", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
while True:
   ev_line = button.event_wait(sec=2)
   if ev_line:
     event = button.event_read()
     print(event)
   else:
     print(".")
     

