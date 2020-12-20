#!/bin/sh
mkdir -p /mnt/d
mount /dev/mmcblk0p1 /mnt/d
# If the old configuration exists and is correct, move it to the backup
if gzip -t /mnt/d/radio.xml.gz ; then 
   mv /mnt/d/radio.xml.gz /mnt/d/radio.xml.gz.bak
fi
gzip -c /tmp/radio.xml > /mnt/d/radio.xml.gz
umount /mnt/d
