#!/bin/bash

gnome-terminal -- bash -c "ngrok tcp $1 -region $2; exit; exec -a $4 bash"
sleep 15

curl -s http://localhost:$3/api/tunnels > tunnel.json
echo $(python3 tunnels.py)
rm tunnel.json
