import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from core import *

@checkuser
def start(update, context):
    text = "Hello!\n" \
           "Я бот, который поможет тебе организовать мероприятие мечты!\n" \
           "Для того чтобы узнать что я умею, напиши /help"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

@checkuser
def help(update, context):
    text = '<b>Список комманд:</b>\n' \
           '<code>Мероприятия</code> (/events) - Список мероприятий\n' \
           '<code>Присоединиться</code> (/join) - Присоединиться к мероприятию\n' \
           '<code>Создать</code> (/create) - Создать мероприятие\n' \
           '<code>Профиль</code> (/events) - Посмотреть свой профиль\n' \
           '<code>Помощь</code> (/events) - Информация о функционале бота\n'

    menu = get_menu('main')

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=menu.reply_markup,
                             parse_mode=ParseMode.HTML)

@checkuser
def all_messages(update, context):
    text = "Я не знаю как на это ответить.\nВоспользуйтесь разделом Помощь (/help)"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML)

@checkuser
def events(update, context):
    text = "Текущие доступные мероприятия\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML)

    list_of_events = Event.select()
    if list_of_events:
        for event in list_of_events:
            if event.hidden == 0:
                text = get_event_info(event)
                footer_keyboard = [
                    InlineKeyboardButton('Записаться', callback_data=f'@joinevent@{event.title}'),
                ]
                reply_markup = InlineKeyboardMarkup([footer_keyboard])
                context.bot.send_message(chat_id=update.effective_chat.id,
                                        text=text,
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=reply_markup)
    else:
        text = "<i>Нет доступных мероприятий!</i>\nВы можете создать свое! Напиши команду Создать (/create)"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text,
                                 parse_mode=ParseMode.HTML)


@checkuser
def join(update, context):
    text = "Выберите мероприятие для записи"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML)
    events(update, context)

@checkuser
def my_profile(update, context):
    user = User.get(id=update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=get_profile(user),
                             parse_mode=ParseMode.HTML)
@checkuser
def my_phone(update, context):
    user = User.get(id=update.message.from_user.id)
    if len(context.args) != 0:
        user.phone = context.args[0]
        user.save()
        text = "Вы успешно установили номер телефона!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        my_profile(update, context)
    else:
        text = "Для ввода номера телефона введите /phone <i>номер телеофона</i>"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
