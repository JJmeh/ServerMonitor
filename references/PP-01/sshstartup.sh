#!/bin/bash

killall ngrok
export DISPLAY=:0.0
gnome-terminal --command "bash -c \"ngrok tcp 22 -region ap; exec bash\""
sleep 15

curl http://localhost:4040/api/tunnels > tunnel.json
url=$(python3 tunnels.py)
curl -X POST -H 'Content-type: application/text' --data '"\$url"' https://nyxserverbot.herokuapp.com/data