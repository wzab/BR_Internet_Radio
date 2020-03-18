#!/bin/bash
set -e
wget https://buildroot.org/downloads/buildroot-2020.02.tar.bz2
tar -xjf buildroot-2020.02.tar.bz2
cp BR_config buildroot-2020.02/.config
cp 0002-orange-pi-audio.patch buildroot-2020.02/linux/
cd buildroot-2020.02
make

