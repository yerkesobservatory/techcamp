#!/bin/sh

# Start a screen with named window and run commands in it
screen -S flyscreen -t win1 -A -d -m
# Start a screen with named second window and run commands in it
screen -S flyscreen -X screen -t win2
# Run a command in the first window (\n is for new line)
screen -S flyscreen -p win1 -X stuff 'cd ~
ls
'
# Run a command in the second window
screen -S flyscreen -p win2 -X stuff 'cd ~/instruments
ls -lath
'