#!/bin/sh
#Create the symbolic link in the /tmp
#Switch off SSL verification for Internet radios
cat >> $1/etc/mpd.conf <<MPD_CONF_CORRECTION
input {
  plugin "curl"
  verify_peer "no"
}
MPD_CONF_CORRECTION
ln -sf /tmp/mpd $1/var/lib/mpd

