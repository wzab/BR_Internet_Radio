#!/usr/bin/python
import select
import sys
f=open("/sys/class/gpio/gpio"+sys.argv[1]+"/value","r")
e=select.epoll()
e.register(f,select.EPOLLPRI)
while True:
  print (f.read())
  e.poll()
  f.seek(0,0)
