import telebot
from telebot import types
from deep_translator import GoogleTranslator
import database as db

TOKEN = '7966898381:AAHQtlq_ZM5LWcbNgOQRhxaaqPN8cBAVkuQ'
bot = telebot.TeleBot(TOKEN)

LANGUAGES = {
    '🇬🇧 English': 'en',
    '🇷🇺 Русский': 'ru',
    '🇰🇿 Қазақша': 'kk',
    '🇹🇷 Türkçe': 'tr',
    '🇩🇪 Deutsch': 'de',
    '🇫🇷 Français': 'fr'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Hello, {user_name}! 👋\n"
        f"I am a Translator Bot. Send me any text, and "
        f"I will translate it into your chosen language.\n\n"
        f"⚙️ Current target language: *{db.get_user_lang(message.chat.id).upper()}*\n\n"
        f"If you want to change the language, use the /languages command or just send a text."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "📖 *Bot Usage Guide:*\n\n"
        "1. Just send me any word or sentence — I will translate it into your target language.\n"
        "2. /languages — Choose target translation language.\n"
        "3. /history — View your last 5 translations."
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


@bot.message_handler(commands=['languages'])
def change_language(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(lang) for lang in LANGUAGES.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Please select your target translation language from the buttons below:", reply_markup=markup)


@bot.message_handler(commands=['history'])
def show_history(message):
    history = db.get_history(message.chat.id)
    if not history:
        bot.send_message(message.chat.id, "Your translation history is empty. 🤷‍♂️")
        return
    res = "📜 *Your last 5 translations:*\n\n"
    for orig, trans in history:
        res += f"🔹 *Original:* {orig}\n🔸 *Translation:* {trans}\n\n"
    bot.send_message(message.chat.id, res, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()

    if not text:
        bot.send_message(message.chat.id, "❌ Error: Text cannot be empty!")
        return

    if text in LANGUAGES:
        lang_code = LANGUAGES[text]
        db.set_user_lang(message.chat.id, lang_code)
        remove_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, f"✅ Language successfully changed to: *{text}*", reply_markup=remove_markup,
                         parse_mode="Markdown")
        return

    if text.startswith('/'):
        bot.send_message(message.chat.id, "❌ Unknown command. If you need help, press /help.")
        return

    target_lang = db.get_user_lang(message.chat.id)

    try:
        bot.send_chat_action(message.chat.id, 'typing')
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        db.add_history(message.chat.id, text, translated)
        response = f"✨ *Translation ({target_lang.upper()}):*\n\n{translated}"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ An error occurred during translation. Please try again.")


if __name__ == '__main__':
    db.init_db()
    bot.infinity_polling()
