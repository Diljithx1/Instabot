import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
from instamoda import login_instagram, boost_followers, check_status

load_dotenv()
TOKEN = os.getenv("8173982703:AAExTFqe37Tn28dtX5_RwpAOfsB6Tmu-_XQ")

LOGIN_USER, LOGIN_PASS = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to InstaModa Bot!\nUse /login to begin.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/login - Login with Instagram account\n"
        "/boost - Start follower boost\n"
        "/status - Check account status\n"
        "/help - Show this help"
    )

async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter Instagram username:")
    return LOGIN_USER

async def login_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['ig_user'] = update.message.text
    await update.message.reply_text("Enter Instagram password:")
    return LOGIN_PASS

async def login_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data['ig_user']
    password = update.message.text
    success = await login_instagram(username, password)
    if success:
        await update.message.reply_text(f"✅ Logged in as {username}")
    else:
        await update.message.reply_text("❌ Login failed.")
    return ConversationHandler.END

async def boost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data.get('ig_user')
    if not username:
        await update.message.reply_text("Please /login first.")
        return
    msg = await boost_followers(username)
    await update.message.reply_text(msg)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data.get('ig_user')
    if not username:
        await update.message.reply_text("Please /login first.")
        return
    st = await check_status(username)
    await update.message.reply_text(st)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("boost", boost))
    app.add_handler(CommandHandler("status", status))

    conv = ConversationHandler(
        entry_points=[CommandHandler("login", login_start)],
        states={
            LOGIN_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_user)],
            LOGIN_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_pass)],
        },
        fallbacks=[],
    )
    app.add_handler(conv)

    print("🚀 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
