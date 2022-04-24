import telegram
from datetime import date, datetime as dt
from models import *
from core import *


def btn_handler(update, context):
    query = update.callback_query
    data = query.data.split("@")[1:]

    if data[0] == 'joinevent':
        event = Event.get(title=data[1])
        user = User.get(id=query.from_user.id)
        try:
            old_request = Requests.get(title=event.title)
            text = "Вы уже подали заявку на данное мероприятие\n" + get_request(old_request)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text,
                                 parse_mode=ParseMode.HTML)
        except Exception:
            new_request = Requests(
                title=event.title,
                date=date.today(),
                time=dt.now().strftime("%H:%M:%S"),
                username=user.username
            )

            new_request.save()

            text = get_request(new_request)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=text,
                                     parse_mode=ParseMode.HTML)

            organizers = User.select().where(User.status == 'organizer')
            for organizer in organizers:
                context.bot.send_message(
                    chat_id=organizer.id,
                    text=f"<b>Поступил новый заказ!</b>\n" + get_request(new_request),
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_request_buttons(new_request)
                )
