
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = '7876262231:AAH1J7Tci9CrI5IizkrT8PUvnMI74jJ3Vzo'
API_KEY = '5554c997b9d04eccbbdcb89902d5ecc9'

def get_random_recipe():
    url = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    recipe = data['recipes'][0]
    return {
        'title': recipe['title'],
        'image': recipe['image'],
        'ingredients': [ing['original'] for ing in recipe['extendedIngredients']],
        'instructions': recipe['instructions'] or "Инструкция не найдена"
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_recipe(update)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_recipe(query)

async def send_recipe(target):
    recipe = get_random_recipe()
    ingredients_text = "\n".join(f"• {item}" for item in recipe['ingredients'])

    caption = f"🍽 <b>{recipe['title']}</b>\n\n"               f"🛒 <b>Ингредиенты:</b>\n{ingredients_text}\n\n"               f"📋 <b>Инструкция:</b>\n{recipe['instructions']}"

    keyboard = [[InlineKeyboardButton("Другой рецепт 🔁", callback_data="another")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(target, Update):
        await target.message.reply_photo(photo=recipe['image'], caption=caption, parse_mode='HTML', reply_markup=reply_markup)
    else:
        await target.edit_message_media(
            media=InputMediaPhoto(media=recipe['image'], caption=caption, parse_mode='HTML'),
            reply_markup=reply_markup
        )

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()
