#!/bin/bash

<<<<<<< HEAD
python3 ~/Script/PP-01/ngrokserverstart.py
=======
python3 ngrokserverstart.py
>>>>>>> 1c3a96c39b05c8287672b4b520f08e8d02d885d8
sleep 10

gnome-terminal -- bash -c "python3 ~/Script/PP-01/bill.py; exit; exec bash"



gnome-terminal -- bash -c "python3 ~/Script/PS-01/app.py; exit; exec bash" 

echo finish...
