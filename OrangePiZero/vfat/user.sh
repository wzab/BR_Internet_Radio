#!/bin/bash
gzip -c -d /mnt/d/radio.xml.gz > /etc/radio.xml
cp /mnt/d/wpa_supplicant.conf > /etc
