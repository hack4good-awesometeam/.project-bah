from Hack4GoodBOT.config import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackContext, CallbackQueryHandler)


# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/enroll - Enroll as a new volunteer\n"
        "/browse - Browse volunteering opportunities\n"
        "/register - Check opportunities I have signed up\n"
        "/attended - Check attended opportunities\n"
        "/upcoming - Check upcoming opportunities\n"
        "/feedback - Submit feedback/blog/reflection\n"
        "/certificate - Request a certificate for attended events"
    )