#!/bin/bash
# Set up the X11 screen simulator
Xvfb :1 -ac -screen 0 1920x1080x24 &
x11vnc -ncache 10 -ncache_cr -passwd headless -display :1 -forever -shared -logappend /var/log/x11vnc.log -bg -noipv6
# Start TWS Offline installation
DISPLAY=:1 ./tws-latest-standalone-linux-x64.sh
# Launch TWS Offline
DISPLAY=:1 /root/Jts/1011/tws