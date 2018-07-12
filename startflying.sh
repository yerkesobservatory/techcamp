#!/bin/sh

# Start a screen with output window
screen -S flyscreen -t output -A -d -m
# Start log window
screen -S flyscreen -X screen -t log
# Start incam window
screen -S flyscreen -X screen -t incam
# Start insense window
screen -S flyscreen -X screen -t insense
# Start data window
screen -S flyscreen -X screen -t data
# Start flask window
screen -S flyscreen -X screen -t flask

## Start the programs

# Run output
screen -S flyscreen -p output -X stuff 'cd ~/techcamp/programs
python3 output.py ../configs/master.ini
'
# Display log
screen -S flyscreen -p log -X stuff 'tail -f ~/space_log.txt
'
# Run incam
screen -S flyscreen -p incam -X stuff 'cd ~/techcamp/programs
python3 incam.py ../configs/master.ini
'
# Run insensor
screen -S flyscreen -p insense -X stuff 'cd ~/techcamp/programs
python3 insensor.py ../configs/master.ini
'
# Run flask
screen -S flyscreen -p flask -X stuff 'cd ~/techcamp/programs
python flaskserver.py
'
