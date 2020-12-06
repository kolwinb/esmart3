#!/bin/bashp

#I have flash web server. This will send esmart3 data to my phone and desktop
# got error something like this
#OSError: [Errno 24] Too many open files: '/etc/opt/esmart3/flask/static/css/side_navigation.css'


#recomended method
sysctl -w fs.file-max=100000
echo "fs.file-max = 100000" >> /etc/sysctl.conf
sysctl -p
cat /proc/sys/fs/file-max

#root locked error
#mount -o remount,rw /dev/sdb2 /
#mount -o remount,rw /dev/sdb1 /boot


#user level limit
#you can do this by ulimit command
#temperary after rebooting this will disappeared
ulimit -a
ulimit -n 100000

#limit for specific user like Oracle, MariaDB and Apache 
# add lines to /etc/security/limits.conf

##how to see actual limits
ps aux | grep server.py
cat /proc/4712/limits
echo "*    soft    nofile  unlimited" > /etc/security/limits.conf
#reboot the system to actual affect
