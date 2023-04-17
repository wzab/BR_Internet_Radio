#!/bin/bash
set -e
wget https://buildroot.org/downloads/buildroot-2023.02.tar.xz
tar -xJf buildroot-2023.02.tar.xz
cp BR_config buildroot-2023.02/.config
cd buildroot-2023.02
make

