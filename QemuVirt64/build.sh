#!/bin/bash
set -e
wget https://buildroot.org/downloads/buildroot-2021.02.tar.bz2
tar -xjf buildroot-2021.02.tar.bz2
cp BR_config buildroot-2021.02/.config
cd buildroot-2021.02
for i in ../patches/* ; do
   patch -p1 < $i
done
make


