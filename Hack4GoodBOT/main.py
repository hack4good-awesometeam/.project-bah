import Miscellaneous.response
from Hack4GoodBOT.config import config
from Hack4GoodBOT.command import (start_command, help_command, browse_command, enroll_command, attended_command,
                                  register_command, upcoming_command, feedback_command)
from telegram import Update
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackQueryHandler)


# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Main
def main() -> None:
    # Set up the bot
    print('Starting Hack4GoodBOT...')
    app = Application.builder().token(config.TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command.start_command))
    app.add_handler(CommandHandler("help", help_command.help_command))
    app.add_handler(CommandHandler("browse", browse_command.browse_command))
    app.add_handler(CommandHandler("register", register_command.register_command))
    app.add_handler(CommandHandler("attended", attended_command.attended_command))
    app.add_handler(CommandHandler("upcoming", upcoming_command.upcoming_command))
    app.add_handler(CommandHandler("feedback", feedback_command.feedback_command))

    # Callback query handler for buttons
    app.add_handler(CallbackQueryHandler(register_command.button_callback_handler, pattern='^register_'))
    app.add_handler(
        CallbackQueryHandler(register_command.confirmation_callback_handler, pattern='^(confirm_registration'
                                                                                     '|cancel_registration)$'))

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('enroll', enroll_command.start_enroll)],
        states={
            enroll_command.NAME: [MessageHandler(filters.TEXT, enroll_command.ask_name)],
            enroll_command.AGE: [MessageHandler(filters.TEXT, enroll_command.ask_gender)],
            enroll_command.GENDER: [CallbackQueryHandler(enroll_command.ask_work_status)],
            enroll_command.WORK_STATUS: [CallbackQueryHandler(enroll_command.ask_immigration_status)],
            enroll_command.IMMIGRATION_STATUS: [CallbackQueryHandler(enroll_command.ask_interests)],
            enroll_command.INTERESTS: [CallbackQueryHandler(enroll_command.ask_skills)],
            enroll_command.SKILLS: [CallbackQueryHandler(enroll_command.ask_summary)],
            enroll_command.SUMMARY: [CallbackQueryHandler(enroll_command.confirm_summary)]
        },
        fallbacks=[CommandHandler('cancel', enroll_command.cancel)]
    )

    # Add the conversation handler to the dispatcher
    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Miscellaneous.response.handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()
