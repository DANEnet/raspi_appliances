#!/bin/sh
cd /home/pi/server_monitor/working
python server_monitor.py 2>&1 > /dev/null
