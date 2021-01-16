# redisgears-scripts

This is the cronjob to update leaderboards

## Steps

1. clone repo and cd into it
2. make sure pip is installed
   1. wget <https://bootstrap.pypa.io/get-pip.py>
3. define environment variables for REDIS_HOST and REDIS_PORT
4. cp service and timer into /etc/systemd/system/
   1. cp leaderboard_hour_update.timer /etc/systemd/system/leaderboard_hour_update.timer
   2. leaderboard_hour_update.service /etc/systemd/system/leaderboard_hour_update.service
5. reload systemctl
   1. systemctl daemon-reload
6. start service
   1. systemctl start leaderboard_hour_update.service
7. start timer
   1. systemctl start leaderboard_hour_update.timer
8. make sure timer is running by checking its status
   1. systemctl status leaderboard_hour_update.timer
   2. make sure to find enabled and active: active (waiting)
