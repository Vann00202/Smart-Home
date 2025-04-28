#!/bin/bash

sleep 10

cd /home/smart-homme/Smart-Home/pi-src/webserver/rebuild/
ng serve --host 192.168.12.1 --port 4200 &

sleep 10

cd /home/smart-homme/Smart-Home/pi-src/
pipenv run /home/smart-homme/Smart-Home/pi-src/main.py &

wait
