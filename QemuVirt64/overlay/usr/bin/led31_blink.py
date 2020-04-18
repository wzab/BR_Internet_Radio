#!/usr/bin/python
import gpiod
import time
chip = gpiod.Chip('gpiochip0')
led1 = chip.get_line(31)
led1.request(consumer="its_me", type=gpiod.LINE_REQ_DIR_OUT)
while True:
   led1.set_value(1)
   time.sleep(0.5)
   led1.set_value(0)
   time.sleep(0.5)

