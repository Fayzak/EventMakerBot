from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

from user_commands import *
from organizer_commands import *
from buttons_commands import *

def command_handler(dispatcher):
    # User commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex("Помощь"), help))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.regex("Мероприятия"), events))
    dispatcher.add_handler(CommandHandler("events", events))
    dispatcher.add_handler(MessageHandler(Filters.regex("Присоединиться"), join))
    dispatcher.add_handler(CommandHandler("join", join))
    dispatcher.add_handler(MessageHandler(Filters.regex("Профиль"), my_profile))
    dispatcher.add_handler(CommandHandler("profile", my_profile))
    dispatcher.add_handler(CommandHandler("phone", my_phone))

    # Organizer commands
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("log", log))

    # Create  event
    new_event_handler = ConversationHandler(
        entry_points=[CommandHandler("create", create), MessageHandler(Filters.regex("Создать"), create)],
        states={
                0: [CallbackQueryHandler(pattern=r'@startevent', callback=title)],
                1: [MessageHandler(Filters.text, event_date)],
                2: [MessageHandler(Filters.text, time)],
                3: [MessageHandler(Filters.text, space)],
                4: [MessageHandler(Filters.text, type)],
                5: [MessageHandler(Filters.text, price)],
                6: [MessageHandler(Filters.text, approval)],
                7: [MessageHandler(Filters.text, places)],
                8: [MessageHandler(Filters.text, about)],
                9: [MessageHandler(Filters.text, phone)],
                10: [MessageHandler(Filters.text, finish_event)],
            },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(new_event_handler)

    # Buttons
    dispatcher.add_handler(CallbackQueryHandler(btn_handler))

    # Utils
    dispatcher.add_handler(MessageHandler(Filters.text, all_messages))