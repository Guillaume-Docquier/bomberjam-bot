@echo off
set logging=%1
set scriptsFolder=
set defaultBotFolder=%2
set botFolder2=%3
set botFolder3=%4
set botFolder4=%5

IF DEFINED defaultBotFolder set defaultBotFolder=%defaultBotFolder%\
IF DEFINED botFolder2 set botFolder2=%botFolder2%\
IF DEFINED botFolder3 set botFolder3=%botFolder3%\
IF DEFINED botFolder4 set botFolder4=%botFolder4%\

IF NOT DEFINED defaultBotFolder set scriptsFolder=..\
IF NOT DEFINED botFolder2 set botFolder2=%defaultBotFolder%
IF NOT DEFINED botFolder3 set botFolder3=%defaultBotFolder%
IF NOT DEFINED botFolder4 set botFolder4=%defaultBotFolder%
@echo on

%scriptsFolder%scripts\bomberjam.exe --output replay.json^
 "python %defaultBotFolder%MyBot.py --logging=%logging%"^
 "python %botFolder2%MyBot.py --logging=%logging%"^
 "python %botFolder3%MyBot.py --logging=%logging%"^
 "python %botFolder4%MyBot.py --logging=%logging%"