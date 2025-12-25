import os

# Bot token from @BotFather – set as env var 'BOT_TOKEN'
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Replace with your real token if hardcoding for test: '8534241684:AAHnISl8xEXysSD26GBZZt0iTs2jX3OH4Zs'

# Admin user IDs (get via @userinfobot)
ADMIN_IDS = [7078689012]  # Add more if needed, e.g., [7078689012, another_id]

# Channel IDs (use @userinfobot or bot API to confirm)
MAIN_CHANNEL_ID = 'https://t.me/+DIfAWc7sGfk2MDk1'  # e.g., '@MyMainChannel'
PRIVATE_CHANNEL_ID = 'https://t.me/+ekRzaY45ZrM0ZGRl'  # e.g., '@MyPrivateChannel'
DB_CHANNEL_ID = -1003527164888  # DB channel for storing forwarded files
LOGGER_CHANNEL_ID = -1003609332664  # Logger channel for user access logs

# MongoDB URI from Atlas or Railway – set as env var 'MONGODB_URI'
MONGODB_URI = os.getenv('MONGODB_URI')  # Replace with your real URI if hardcoding for test: 'mongodb+srv://sanjublogscom_db_user:Mahakal456@cluster0.cwi48dt.mongodb.net/?appName=Cluster0'
