@echo off
ECHO Installing the required packages for the bot!
TIMEOUT 3

python -3 -m pip install -U fortnitepy
python -3 -m pip install -U aiohttp
python -3 -m pip install -U colorama
python -3 -m pip install -U BenBotAsync
python -3 -m pip install -U livejson
python -3 -m pip install -U aiofiles

ECHO Done! Now run START BOT.bat
PAUSE

