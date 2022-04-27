import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from models import *
from core import *
from menus import *


@checkuser
def log(update, context):
    user = User.get(id=update.message.from_user.id)

    if len(context.args) != 0:
        if context.args[0] == 'out':
            if user.status == 'organizer':
                user.status = 'user'
                user.save()
                text = "Вы изменили ваш статус на Участник"
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        elif context.args[0] == 'in':
            try:
                if user.status == 'user':
                    if (context.args[1] == user.password) and (context.args[1] != 'not specified'):
                        user.status = 'organizer'
                        user.save()
                        text = "Вы изменили ваш статус на Организатор\nЕсли вы хотите выйти из аккаунта, напишите <code>log out</code>"
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                    else:
                        text = "Неверный пароль! Попробуйте еще раз"
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            except IndexError:
                text = "Введите пожалуйста свой пароль после ключевого слова in"
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        text = "Для входа в аккаунт введите /log in пароль\nДля выхода введите /log out"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

@checkuser
def register(update, context):
    user = User.get(id=update.message.from_user.id)

    if len(context.args) != 0:
        if user.status == 'user':
            first_attempt = context.args[0]
            second_attempt = context.args[1]
            if first_attempt == second_attempt:
                user.password = first_attempt
                user.status = 'organizer'
                user.save()
                text = "Вы зарегестрированы как Организатор.\n<b><i>Обязательно запомните свой пароль!</i></b>\nЕсли вы хотите выйти из аккаунта, напишите <code>/log out</code>"
                context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
            else:
                text = "Введенные пароли не совпадают, попробуйте еще раз!"
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        else:
            text = "Вы уже являетесь Организатором своего мероприятия!"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


# @checkuser
# @checkorganizer
def create(update, context):
    user = User.get(id=update.message.from_user.id)
    if user.status == 'organizer':
        text = "Чтобы начать создание мероприятия, нажмите кнопку ниже\nЧтобы отменить создание мероприятия, напишите <code>/cancel</code>"

        footer_keyboard = [
            InlineKeyboardButton('Начать', callback_data='@startevent'),
        ]

        context.user_data['state'] = 1

        reply_markup = InlineKeyboardMarkup([footer_keyboard])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text,
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=reply_markup)

        return 0
    elif user.status == 'user':
        text = "Вы не являетесь Организатором.\nЧтобы зарегистрироваться как организатор, напишите команду <code>/register</code> и задайте пароль два раза через пробел\nЕсли вы уже зарегестрированы, то войдите в аккаунт с помощью <code>/log in</code> <i>пароль</i>"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


def title(update, context):
    query = update.callback_query
    query.edit_message_text(text=query.message.text, reply_markup=None)

    text = 'Укажите название'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    context.user_data['state'] = 2
    return 1


def event_date(update, context):
    try:
        context.user_data['title'] = update.message.text
        event = Event.get(title=context.user_data['title'])

        text = 'Мепроприятие с таким названием уже существует!\nПожалуйста, попробуйте снова и задайте другое название'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

        return ConversationHandler.END
    except:
        text = 'Укажите дату начала'

        context.user_data['title'] = update.message.text

        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
        context.user_data['state'] = 3
        return 2


def time(update, context):
    text = 'Укажите время начала'

    context.user_data['date'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 4
    return 3


def space(update, context):
    text = 'Укажите место проведения'

    context.user_data['time'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 5
    return 4


def type(update, context):
    text = 'Укажите тип мероприятия'

    context.user_data['space'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 6
    return 5


def price(update, context):
    text = 'Укажите стоимость входа (в рублях)'

    context.user_data['type'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 7
    return 6


def approval(update, context):
    text = 'Укажите, можно ли влключить автоматическое одобрение заявок\n<b>(Строго: <i>Да</i> или <i>Нет</i>)</b>'

    context.user_data['price'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 8
    return 7


def places(update, context):
    text = 'Укажите количество мест'

    context.user_data['approval'] = update.message.text.lower()

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 9
    return 8


def about(update, context):
    text = 'Расскажите участникам о чем ваше мероприятие'

    context.user_data['places'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 10
    return 9


def phone(update, context):
    text = 'Укажите свой номер телефона для связи'

    context.user_data['about'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 11
    return 10


def cancel(update, context):
    text = 'Создание мероприятия отменено'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def finish_event(update, context):
    user = User.get(id=update.message.from_user.id)

    event = Event(
        title=context.user_data['title'],
        organizer=user.username,
        date=context.user_data['date'],
        time=context.user_data['time'],
        space=context.user_data['space'],
        type=context.user_data['type'],
        price=context.user_data['price'],
        approval=context.user_data['approval'],
        places=context.user_data['places'],
        about=context.user_data['about'],
    )


    context.user_data['phone'] = update.message.text
    user.phone = context.user_data['phone']
    user.save()

    event.save()

    text = get_event_info(event)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


    return ConversationHandler.END

