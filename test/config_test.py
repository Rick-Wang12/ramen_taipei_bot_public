import configparser

config = configparser.ConfigParser()
config.read("config.ini")

Channel_access_token = config.get("line-bot", "channel_access_token")
print(f"Channel_access_token: {Channel_access_token}")
print(type(Channel_access_token))

Channel_secret = config.get("line-bot", "channel_secret")
print(f"Channel_secret: {Channel_secret}")
print(type(Channel_secret))