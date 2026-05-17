import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('8877687141:AAHVopob1StCFn7HHmmFFIxryNrznwwUAH4')

FOOD_OPTIONS = [
    "🍕 Пицца Маргарита", "🍣 Суши Филадельфия", "🍔 Чизбургер", "🥗 Цезарь с курицей",
    "🍜 Лапша Wok с креветками", "🌯 Буррито с гуакамоле", "🥟 Вареники с вишней",
    "🍲 Том Ям с креветками", "🍝 Паста Карбонара", "🥘 Плов с бараниной",
    "🍱 Роллы Калифорния", "🥪 Сэндвич с индейкой", "🍳 Омлет с беконом",
    "🥣 Греческий суп", "🐟 Лосось на гриле"
]

DRINK_OPTIONS = [
    "☕ Американо", "🍵 Зелёный чай с жасмином", "🧃 Апельсиновый сок", "💧 Вода с лимоном",
    "🥤 Кола", "🍹 Мохито безалкогольный", "🍺 Тёмное пиво", "🥛 Молочный коктейль",
    "🍷 Красное вино", "🥂 Просекко", "🧋 Bubble tea", "🍶 Саке", "🥤 Спрайт",
    "☕ Капучино с корицей", "🍫 Горячий шоколад"
]

MOVIE_OPTIONS = [
    "🎬 Пираты Карибского моря", "😂 1+1", "🥲 Зеленая миля", "🚀 Интерстеллар",
    "❤️ Дневник памяти", "😱 Оно", "🦁 Король Лев", "🔪 Пила",
    "🎭 Джокер", "⚽ Пеле: Рождение легенды", "🧙 Гарри Поттер", "💍 Властелин колец",
    "🤖 Терминатор", "🦸 Мстители", "🎨 Шоу Трумана"
]

ACTIVITY_OPTIONS = [
    "🏃 Пробежка в парке", "🧘 Йога утром", "💪 Тренировка дома", "🚶 Прогулка с музыкой",
    "🛌 Спать до обеда", "📖 Читать книгу", "🎮 Играть в Minecraft", "🍳 Приготовить ужин",
    "🎬 Смотреть сериал", "🚴 Велосипед", "🏊 Бассейн", "🎨 Рисовать картину",
    "🎸 Играть на гитаре", "🧩 Собирать пазл", "📝 Писать дневник"
]

DESSERT_OPTIONS = [
    "🍰 Тирамису", "🍦 Пломбир", "🧁 Капкейк", "🍫 Брауни", "🥧 Яблочный пирог",
    "🍩 Пончик с глазурью", "🍪 Шоколадное печенье", "🍨 Мороженое с вишней"
]

GAME_OPTIONS = [
    "🎮 Minecraft", "🏆 Valorant", "🐉 Genshin Impact", "🚗 GTA V", "⚽ FIFA 24",
    "🧩 Among Us", "🔫 Counter-Strike 2", "🌍 The Witcher 3", "🏀 NBA 2K24"
]

CHOICE_SETS = {
    "food": FOOD_OPTIONS,
    "drink": DRINK_OPTIONS,
    "movie": MOVIE_OPTIONS,
    "activity": ACTIVITY_OPTIONS,
    "dessert": DESSERT_OPTIONS,
    "game": GAME_OPTIONS
}

waiting_for_custom = {}


def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🍔 Что поесть?", callback_data="menu_food"),
        InlineKeyboardButton("🥤 Что попить?", callback_data="menu_drink"),
        InlineKeyboardButton("🎬 Что посмотреть?", callback_data="menu_movie"),
        InlineKeyboardButton("🏃 Чем заняться?", callback_data="menu_activity"),
        InlineKeyboardButton("🍰 Что на десерт?", callback_data="menu_dessert"),
        InlineKeyboardButton("🎮 Во что поиграть?", callback_data="menu_game"),
        InlineKeyboardButton("✏️ Свои варианты", callback_data="menu_custom"),
        InlineKeyboardButton("🎲 Случайный выбор", callback_data="menu_random")
    )
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id


    welcome_text = f"""
✨ *Привет, {user_name}!* ✨

🤖 *Добро пожаловать в бота «Выбери за меня»!*

Я помогу тебе, когда ты не можешь решиться. 
Просто нажми на кнопку — и я сделаю выбор за тебя!

🔥 *Доступные категории:*
🍔 Еда — {len(FOOD_OPTIONS)} вариантов
🥤 Напитки — {len(DRINK_OPTIONS)} вариантов
🎬 Кино — {len(MOVIE_OPTIONS)} вариантов
🏃 Активности — {len(ACTIVITY_OPTIONS)} вариантов
🍰 Десерты — {len(DESSERT_OPTIONS)} вариантов
🎮 Игры — {len(GAME_OPTIONS)} вариантов

📝 *Особенности:*
• Нажми на любую кнопку — я сразу дам ответ
• «Свои варианты» — напиши через запятую, я выберу один раз
• «Случайный выбор» — выберу из всех {len(FOOD_OPTIONS) + len(DRINK_OPTIONS) + len(MOVIE_OPTIONS) + len(ACTIVITY_OPTIONS) + len(DESSERT_OPTIONS) + len(GAME_OPTIONS)} вариантов

👇 *Начинай! Нажми на любую кнопку ниже*
    """

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    user_id = call.from_user.id

    if data.startswith("menu_"):
        category = data.replace("menu_", "")

        if category == "custom":
            waiting_for_custom[user_id] = True
            bot.edit_message_text(
                "✏️ *Напиши свои варианты через запятую*\n\n"
                "Пример: `Спать, Есть, Гулять, Играть`\n\n"
                "Я выберу один случайный вариант и НЕ сохраню его.",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown"
            )

        elif category == "random":
            all_options = []
            for cat in CHOICE_SETS.values():
                all_options.extend(cat)

            if all_options:
                chosen = random.choice(all_options)
                bot.edit_message_text(
                    f"🎲 *Случайный выбор из всех категорий:*\n\n"
                    f"✨ *{chosen}* ✨\n\n"
                    f"📊 Всего доступно вариантов: {len(all_options)}\n\n"
                    f"Нажми /start чтобы выбрать ещё.",
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode="Markdown"
                )
            else:
                bot.answer_callback_query(call.id, "Нет вариантов для выбора!", show_alert=True)

        elif category in CHOICE_SETS:
            options = CHOICE_SETS[category]
            chosen = random.choice(options)

            category_emojis = {
                "food": "🍔", "drink": "🥤", "movie": "🎬",
                "activity": "🏃", "dessert": "🍰", "game": "🎮"
            }
            emoji = category_emojis.get(category, "🎉")

            bot.edit_message_text(
                f"{emoji} *Твой выбор:*\n\n"
                f"🎉 *{chosen}* 🎉\n\n"
                f"📊 Вариантов в этой категории: {len(options)}\n\n"
                f"Нажми /start чтобы выбрать ещё.",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown"
            )

    elif data == "back_to_menu":
        bot.edit_message_text(
            "✨ *Выбери за меня — бот с кнопками* ✨\n\n"
            "Нажми на любую кнопку, и я сразу дам ответ!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )


@bot.message_handler(func=lambda message: True)
def handle_custom_text(message):
    user_id = message.chat.id

    if waiting_for_custom.get(user_id):
        text = message.text
        options = [opt.strip() for opt in text.split(",")]
        options = [opt for opt in options if opt]

        if len(options) < 2:
            bot.send_message(
                message.chat.id,
                "❌ Нужно хотя бы 2 варианта через запятую.\nПример: `Спать, Есть, Гулять`"
            )
            return

        waiting_for_custom[user_id] = False
        chosen = random.choice(options)

        bot.send_message(
            message.chat.id,
            f"📝 *Твои варианты:*\n{', '.join(options)}\n\n"
            f"🎉 *Я выбираю: {chosen}* 🎉\n\n"
            f"✅ Варианты НЕ сохранены.\n\n"
            f"Нажми /start чтобы выбрать ещё.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )


if __name__ == "__main__":
    print("🚀 Бот запущен с расширенными категориями!")
    print("🤖 Напиши /start в Telegram")
    bot.infinity_polling()