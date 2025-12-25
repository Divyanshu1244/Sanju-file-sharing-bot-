from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from pymongo import MongoClient
import config

# MongoDB setup
client = MongoClient(config.MONGODB_URI)
db = client['file_bot']
files_collection = db['files']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Check forced subscriptions
    if not await check_subscription(user.id, config.MAIN_CHANNEL_ID) or not await check_subscription(user.id, config.PRIVATE_CHANNEL_ID):
        keyboard = [
            [InlineKeyboardButton("Subscribe to Main", url=f"https://t.me/c/{str(config.MAIN_CHANNEL_ID)[4:]}")],
            [InlineKeyboardButton("Subscribe to Private", url=f"https://t.me/c/{str(config.PRIVATE_CHANNEL_ID)[4:]}")],
            [InlineKeyboardButton("Check Subscription", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Subscribe to both channels to access files.", reply_markup=reply_markup)
        return
    await update.message.reply_text("Welcome! Use /upload to add files (admins only).")

async def check_subscription(user_id, channel_id):
    try:
        member = await context.bot.get_chat_member(channel_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def check_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if await check_subscription(user_id, config.MAIN_CHANNEL_ID) and await check_subscription(user_id, config.PRIVATE_CHANNEL_ID):
        await query.edit_message_text("Subscription confirmed! You can now access files.")
    else:
        await query.answer("You haven't subscribed yet.")

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in config.ADMIN_IDS:
        await update.message.reply_text("Admin only.")
        return
    if not update.message.document:
        await update.message.reply_text("Send a file to upload.")
        return
    # Forward to DB channel
    forwarded = await context.bot.forward_message(chat_id=config.DB_CHANNEL_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    # Generate link (using file ID)
    file_id = forwarded.document.file_id
    link = f"https://t.me/{context.bot.username}?start=file_{file_id}"
    # Store in MongoDB
    files_collection.insert_one({'file_id': file_id, 'link': link})
    await update.message.reply_text(f"File uploaded. Share link: {link}")

async def handle_file_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    if not args or not args[0].startswith('file_'):
        return
    file_id = args[0][5:]
    # Check subs
    if not await check_subscription(user.id, config.MAIN_CHANNEL_ID) or not await check_subscription(user.id, config.PRIVATE_CHANNEL_ID):
        await update.message.reply_text("Subscribe first.")
        return
    # Log user
    log_msg = f"User: {user.username} ({user.first_name} {user.last_name}) ID: {user.id} accessed file {file_id}"
    await context.bot.send_message(chat_id=config.LOGGER_CHANNEL_ID, text=log_msg)
    # Send file with protect_content=True
    await context.bot.send_document(chat_id=user.id, document=file_id, protect_content=True)

def main():
    application = Application.builder().token(config.BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("upload", upload))
    application.add_handler(CallbackQueryHandler(check_sub_callback, pattern="check_sub"))
    application.add_handler(MessageHandler(filters.Document.ALL, upload))  # For direct uploads
    application.run_polling()

if __name__ == '__main__':
    main()
