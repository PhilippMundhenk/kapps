#{
#   sleep 60
   mntroot rw
   killall python
#   mkfifo /tmp/test.fifo
   cd /mnt/us/kapps
#   python kapps.py >> /mnt/us/kapps/kapps.log 2>&1 &
   python kapps.py &
   sleep 10
   /mnt/us/extensions/WebLaunch/bin/start.sh
#} &
return 0

