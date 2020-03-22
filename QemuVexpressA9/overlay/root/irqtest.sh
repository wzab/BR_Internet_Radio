#!/bin/sh
echo 478 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio478/direction
echo both > /sys/class/gpio/gpio478/edge
python irqtest.py

