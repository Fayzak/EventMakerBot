import telegram
from datetime import date, datetime as dt
from models import *
from core import *

users_confirm = []

def btn_handler(update, context):
    query = update.callback_query
    data = query.data.split("@")[1:]

    if data[0] == 'joinevent':
        event = Event.get(title=data[1])
        users_confirm.clear()
        if event.approval == 'Нет':
            user = User.get(id=query.from_user.id)
            try:
                old_request = Requests.get(title=event.title, username=f'@{user.username}')
                text = "Вы уже подали заявку на данное мероприятие\n" + get_request(old_request)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text,
                                         parse_mode=ParseMode.HTML)
            except Exception:
                if user.phone == 'not specified':
                    text = 'Без номера телефона мы не можем принять вашу заявку!\nВведите свой номер телефона для связи через команду /phone'
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=text,
                                             parse_mode=ParseMode.HTML)
                else:

                    new_request = Requests(
                        title=event.title,
                        date=date.today(),
                        time=dt.now().strftime("%H:%M:%S"),
                        username=f'@{user.username}'
                    )

                    new_request.save()

                    text = get_request(new_request)
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=text,
                                             parse_mode=ParseMode.HTML)

                    organizers = User.select().where(User.username == event.organizer)

                    for organizer in organizers:
                        context.bot.send_message(
                            chat_id=organizer.id,
                            text=f"<b>Поступила новая заявка!</b>\n" + get_request(new_request),
                            parse_mode=ParseMode.HTML,
                            reply_markup=get_request_buttons(new_request)
                        )
        elif event.approval == 'Да':
            user = User.get(id=query.from_user.id)
            try:
                old_request = Requests.get(title=event.title, username=f'@{user.username}')
                text = "Вы уже подали заявку на данное мероприятие\n" + get_request(old_request)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text,
                                         parse_mode=ParseMode.HTML)
            except Exception:
                new_request = Requests(
                    title=event.title,
                    status='Одобрена',
                    date=date.today(),
                    time=dt.now().strftime("%H:%M:%S"),
                    username=f'@{user.username}'
                )

                new_request.save()

                if event.members == 'Пока никого':
                    event.members = []

                users_confirm.append(f'@{user.username}')

                event.members = ','.join(users_confirm)
                event.places = event.places - 1
                if event.places <= 0:
                    event.hidden = 1
                event.save()

                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Ваша заявка на мероприятие <b>{event.title}</b> была <i>одобрена!</i>',
                    parse_mode=telegram.ParseMode.HTML,
                )

    if data[0] == 'confirm':
        request = Requests.get(id=int(data[1]))
        request.status = 'Одобрена'
        request.save()

        users_confirm.append(request.username)

        event = Event.get(title=request.title)
        if event.members == 'Пока никого':
            event.members = []
        event.members = ','.join(users_confirm)
        event.places = event.places - 1
        if event.places <= 0:
            event.hidden = 1
        event.save()

        context.bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
            reply_markup=None
        )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы успешно одобрили заявку!',
            parse_mode=telegram.ParseMode.HTML,
        )
        context.bot.send_message(
            chat_id=User.get(username=request.username[1:]).id,
            text=f'Ваша заявка на мероприятие <b>{request.title}</b> была <i>одобрена!</i>',
            parse_mode=telegram.ParseMode.HTML,
        )

    if data[0] == 'reject':
        request = Requests.get(id=int(data[1]))
        request.status = 'Отклонена'
        request.save()

        context.bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
            reply_markup=None
        )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы успешно отклонили заявку!',
            parse_mode=telegram.ParseMode.HTML,
        )
        context.bot.send_message(
            chat_id=User.get(username=request.username[1:]).id,
            text=f'Ваша заявка на мероприятие <b>{request.title}</b> была <i>отклонена!</i>',
            parse_mode=telegram.ParseMode.HTML,
        )
