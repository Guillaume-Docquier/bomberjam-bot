@echo off
set defaultBotFolder=%1
set botFolder2=%2
set botFolder3=%3
set botFolder4=%4

IF NOT DEFINED botFolder2 set botFolder2=%defaultBotFolder%
IF NOT DEFINED botFolder3 set botFolder3=%defaultBotFolder%
IF NOT DEFINED botFolder4 set botFolder4=%defaultBotFolder%
@echo on

@scripts\bomberjam.exe --output replay.json^
 "python %defaultBotFolder%\MyBot.py --logging=True"^
 "python %botFolder2%\MyBot.py --logging=True"^
 "python %botFolder3%\MyBot.py --logging=True"^
 "python %botFolder4%\MyBot.py --logging=True"