# ContestBot
 ContestBot is a smart bot that automatically finds and enters contests on twitter. It analyzes contest tweets and supports dynamically retweeting, liking, following, commenting, tagging friends, and direct messaging. It performs only the actions that each contest specifies. It features a built in rate limit system. It is user friendly and fully tunable using only the config.py file.  

Features:  
- unlimited contest searching  
- smart contest detection  
- spam filtering  
- retweeting  
- liking  
- following  
- unfollowing  
- commenting  
- tagging friends  
- direct messaging  
- built in rate limit system  
- 100% tunable from config.py  

Requirements:  
- An approved developer Twitter account (apply here: https://developer.twitter.com/en/application/use-case)

To Use:  
- fork/clone ContestBot project  
- create venv using python 3.7  
- `pip install -r requirements.txt`  
- create a twitter app (https://developer.twitter.com/en/apps) see Requirements above  
- enter settings in config.py  
    - REQUIRED: username, consumer_key, consumer_secret, token, token_secret  
- run main.py  

Run Tests:  
- cd into root project directory (ex: `cd C:\Users\YOURNAME\Desktop\ContestBot`)  
- `pytest ContestBot/tests.py -s`  

Run on Raspberry Pi:
- make Twitter app with read and write privileges
- cd into project directory and install requirements.txt (pip3 install -r requirements.txt)
- fill parameters in config file (API keys, Consumer keys, and settings)
- change permissions to anyone for .sh file
- run on boot  
`sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`
- add this to the end of that file  
`@lxterminal -e sudo python3 /home/pi/Desktop/fullfilepathto.py`
- If running multiple instances on same pi, rename folder to "ContestBot1", change in shell script and auto boot too

Disclaimer:  
This application is for educational purposes only. There is a possibility of Twitter suspension from using this application. I am not responsible for misuse or abuse of this application or any variants of it. I am not responsible for any damages or liability incurred as a result of using this application. Use at your own risk.