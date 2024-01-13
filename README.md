# RatBot
RatBot is a bot specialy made for polish discord server "RatCraft". According to it's usage it have some permanent variables in env.py file, which make bot works correct only in one server.
## Content of env.py
When you would like to make bot works on your server change this values
```python
#Token of your bot
TOKEN = ""
#Roles for levels from lowest to highest
ROLES = [0,1,2,3,4,5,6,7,8,9]
#IDs of fun channels
COUNTING_CHANNEL = 0
MEMES_CHANNEL = 0
LASTLETTER_CHANNEL = 0
#ID of discord server
GUILD_ID = 0
#ID/IDS of role/roles allowing bot controling
BOT_CONTROLLER = 0
#Birthday role ID
BIRTHDAY_ROLE = 0
#Birthday channel ID
BIRTHDAY_CHANNEL = 0
#MC Rcon ip
RCON_IP = "ip"
#MC Rcon password
RCON_PASSWORD = "password"
```