#!/bin/bash
(
  export PATH=../buildroot-2020.02/output/host/bin:../../Utility/buildroot-2020.02/output/host/bin:$PATH
  mkimage -T script -C none -n 'Start script' -d boot_user.txt boot.scr
)