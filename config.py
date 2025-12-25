import os

BOT_TOKEN = os.getenv('BOT_TOKEN')  # From BotFather
ADMIN_IDS = [123456789, 987654321]  # List of admin user IDs (get via @userinfobot)

MAIN_CHANNEL_ID = -1001234567890  # Main channel ID (use @userinfobot or bot API)
PRIVATE_CHANNEL_ID = -1000987654321  # Private channel ID
DB_CHANNEL_ID = -1001122334455  # DB channel for files
LOGGER_CHANNEL_ID = -1005566778899  # Logger channel

MONGODB_URI = os.getenv('MONGODB_URI')  # From MongoDB Atlas or Railway
