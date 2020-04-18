#!/bin/sh
BASEDIR=$(dirname "$0")
NUM=0
echo ${NUM} > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio${NUM}/direction
echo both > /sys/class/gpio/gpio${NUM}/edge
python ${BASEDIR}/irqtest.py ${NUM}

