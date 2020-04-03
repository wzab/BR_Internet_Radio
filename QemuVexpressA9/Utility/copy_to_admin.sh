#!/bin/bash
set -e
SRC_DIR=buildroot-2020.02/output/images
DST_DIR=../Admin/user_img
cp -L ${SRC_DIR}/rootfs.ext4 ${DST_DIR}/rootfs.ext4
cp ${SRC_DIR}/zImage ${DST_DIR}/zImage_user
cp ${SRC_DIR}/vexpress-v2p-ca9.dtb ${DST_DIR}/vexpress-v2p-ca9-user.dtb

