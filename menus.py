from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from collections import namedtuple

menus = {
    'main': {
        'type': 'reply',
        'body': [
            {
                'text': 'Main menu',
                'buttons': [
                    KeyboardButton("Мероприятия"),
                    KeyboardButton("Присоединиться"),
                    KeyboardButton("Создать"),
                    KeyboardButton("Профиль"),
                    KeyboardButton("Помощь"),
                ],
                'header': None,
                'footer': None,
                'n_cols': 2
            },
        ]
    },
}


def get_menu(tag):
    try:
        menu_name = tag.split("#")[1]
    except:
        menu_name = tag
    try:
        menu_page = int(tag.split("#")[2])
    except:
        menu_page = 0

    try:
        cur_menu = menus[menu_name]['body'][menu_page]
        if menus[menu_name]['body'][menu_page]['text']:
            text = menus[menu_name]['body'][menu_page]['text']
        else:
            text = None
    except Exception as e:
        return False

    markup = build_menu(buttons=cur_menu['buttons'],
                        n_cols=cur_menu['n_cols'],
                        header_buttons=cur_menu['header'],
                        footer_buttons=cur_menu['footer'])

    menu = namedtuple('menu', 'reply_markup text tag page type')
    menu.tag = tag
    menu.page = menu_page
    menu.type = menus[menu_name]['type']
    menu.text = text

    if menus[menu_name]['type'] == 'inline':
        menu.reply_markup = InlineKeyboardMarkup(markup)
    if menus[menu_name]['type'] == 'reply':
        menu.reply_markup = ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)

    return menu

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu