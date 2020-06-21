#!/bin/bash

ps -A | grep ngrok > ngrokStatus.txt
grep -q -w 'ngrok' ngrokStatus.txt

echo $?

