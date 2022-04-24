from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from models import *
from menus import *


def is_user_exist(id):
    try:
        user = User.get(id=id)
        if not user.id:
            raise DoesNotExist
        return True
    except DoesNotExist:
        return False


def checkuser(function):
    def check(update, context):
        if not is_user_exist(id=update.message.from_user.id):
            if update.message.from_user.username:
                username = update.message.from_user.username
            else:
                username = 'none'

            user = User.create(
                id=update.message.from_user.id,
                status='user',
                name=update.message.from_user.first_name,
                surname=update.message.from_user.last_name,
                username=username,
                password='not specified'
            )
            user.save()
        function(update, context)
    return check


def checkorganizer(function):
    def check(update, context):
        user = User.get(id=update.message.from_user.id)
        if user.status == 'organizer':
            function(update, context)
        else:
            text = "Вы не являетесь Организатором.\nЧтобы зарегистрироваться как организатор, напишите команду <code>Регистрация</code>(/register) и задайте пароль два раза через пробел\nЕсли вы уже зарегестрированы, то войдите в аккаунт с помощью /log in пароль"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    return check


def get_event_info(event):
    text = f"Название мероприятия: <b>{event.title}</b>\n" \
               f"Где: {event.space}\n" \
               f"Когда: {event.date}\n" \
               f"Во сколько: {event.time}\n" \
               f"Тип мероприятия: {event.type}\n" \
               f"Стоимость входа: {event.price}\n" \
               f"Количество свободных мест: {event.places}\n" \
               f"Кто идет: {event.members}\n" \
               f"Повторяемость: {event.repeat}\n" \
               f"Описание: {event.about}\n\n"
    return text


def get_profile(user):
    if user:
        text = f"<b>Профиль</b>\n" \
               f"Id: <code>{user.id}</code>\n" \
               f"Статус: {user.status}\n" \
               f"Имя: {user.name}\n" \
               f"Фамилия: {user.surname}\n" \
               f"Юзернейм: @{user.username}\n" \
               f"Телефон: <i>{user.phone}</i>"
        return text


def get_request(request):
    if request:
        text = f"<i><b>Информация о заявке на мероприятие</b></i>\n" \
               f"Мероприятие: <b>{request.title}</b>\n" \
               f"Статус: {request.status}\n" \
               f"Юзернейм: {request.username}\n"
        return text


def get_request_buttons(request):
    buttons = []

    if request.status == 'В обработке':
        buttons.append(InlineKeyboardButton('Одобрить', callback_data=f"@confirm@{request.id}"))
        buttons.append(InlineKeyboardButton('Отметить', callback_data=f"@response@{request.id}"))
        buttons.append(InlineKeyboardButton('Одобрить все', callback_data=f"@confirmall@{request.id}"))
        buttons.append(InlineKeyboardButton('Мест нет', callback_data=f"@decline@{request.id}"))
    # if request.status == 'Принят':
    #     buttons.append(InlineKeyboardButton('Завершить заказ', callback_data=f"@complete@{order.id}"))
    # buttons.append(InlineKeyboardButton('Удалить заказ', callback_data=f"@delete@{order.id}"))
    return InlineKeyboardMarkup(build_menu(buttons, n_cols=2))