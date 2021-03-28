#!/bin/sh
BASEDIR=$(dirname "$0")
echo 480 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio480/direction
echo both > /sys/class/gpio/gpio480/edge
python ${BASEDIR}/irqtest.py
