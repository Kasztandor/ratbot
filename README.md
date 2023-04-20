# RatBot
RatBot is a bot specialy made for polish discord server "RatCraft". According to it's usage it have some permanent variables in env.py file, which make bot works correct only in one server.
## Content of env.py
When you would like to make bot works on your server change this values
```python
#Token of your bot
TOKEN = ""
#Roles for levels
roles = [1,2,3,4,5]
#Id of mee6 bot (bypassing buing mee6 premium for lever roles :p)
mee6 = 386237687008591895 #(it is mee6 bot id)
#Channel id of counting game channel 
counting = 123456789
#ID of discord server
guild = discord.Object(id=123456789)
```