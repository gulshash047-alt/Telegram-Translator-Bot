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
        f"Сәлем, {user_name}! 👋\n"
        f"Мен — Аудармашы ботпын. Маған кез келген мәтінді жіберсеңіз, "
        f"оны сіз таңдаған тілге аударып беремін.\n\n"
        f"⚙️ Қазіргі таңдалған аудару тілі: *{db.get_user_lang(message.chat.id).upper()}*\n\n"
        f"Тілді өзгерткіңіз келсе, /settings командасын басыңыз немесе мәтін жібере беріңіз."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "📖 *Ботты қолдану нұсқаулығы:*\n\n"
        "1. Маған жай ғана сөз немесе сөйлем жіберіңіз — мен оны сіз таңдаған тілге аударамын.\n"
        "2. /settings — Аударылатын тілді таңдау.\n"
        "3. /history — Соңғы 5 аударма тарихын көру.\n"
        "4. /languages — Қолжетімді тілдер тізімі."
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


@bot.message_handler(commands=['settings', 'languages'])
def change_language(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(lang) for lang in LANGUAGES.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Төмендегі батырмалардан аударғыңыз келетін тілді таңдаңыз:", reply_markup=markup)


@bot.message_handler(commands=['history'])
def show_history(message):
    history = db.get_history(message.chat.id)
    if not history:
        bot.send_message(message.chat.id, "Сізде әлі аударма тарихы жоқ. 🤷‍♂️")
        return
    res = "📜 *Соңғы 5 аудармаңыз:*\n\n"
    for orig, trans in history:
        res += f"🔹 *Түпнұсқа:* {orig}\n🔸 *Аударма:* {trans}\n\n"
    bot.send_message(message.chat.id, res, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()

    if not text:
        bot.send_message(message.chat.id, "❌ Қате: Мәтін бос болмауы керек!")
        return

    if text in LANGUAGES:
        lang_code = LANGUAGES[text]
        db.set_user_lang(message.chat.id, lang_code)
        remove_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, f"✅ Аудару тілі сәтті өзгертілді: *{text}*", reply_markup=remove_markup,
                         parse_mode="Markdown")
        return

    if text.startswith('/'):
        bot.send_message(message.chat.id, "❌ Белгісіз команда. Көмек қажет болса /help басыңыз.")
        return

    target_lang = db.get_user_lang(message.chat.id)

    try:
        bot.send_chat_action(message.chat.id, 'typing')
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        db.add_history(message.chat.id, text, translated)
        response = f"✨ *Аударма ({target_lang.upper()}):*\n\n{translated}"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Аударма кезінде қате шықты. Қайта көріңіз.")


if __name__ == '__main__':
    db.init_db()
    bot.infinity_polling()