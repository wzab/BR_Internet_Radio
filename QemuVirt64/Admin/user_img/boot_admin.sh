#!/bin/bash
(
  export PATH=../buildroot-2021.02/output/host/bin:../../Utility/buildroot-2021.02/output/host/bin:$PATH
  mkimage -T script -C none -n 'Start script' -d boot_admin.txt boot.scr
)