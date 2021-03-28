#!/bin/bash
set -e
SRC_DIR=buildroot-2021.02/output/images
DST_DIR=../Admin/user_img
cp -L ${SRC_DIR}/rootfs.ext4 ${DST_DIR}/rootfs.ext4
cp ${SRC_DIR}/Image ${DST_DIR}/Image_user

