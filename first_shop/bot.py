import os
from re import U
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from main.models import AdminData

from telegram.ext import ApplicationBuilder
from asgiref.sync import sync_to_async

@sync_to_async
def get_or_create_admin(user):
    try:
        admin = AdminData.objects.get(id=user.id)
        return admin, False
    except AdminData.DoesNotExist:
        admin = AdminData.objects.create(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        )
        return admin, True

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    admin, created = await get_or_create_admin(user)

    if created:
        await update.message.reply_text(
            f'{admin.first_name}, Вітаю вас у чатботі-менеджері для магазину Зоотоварів! 👋'
        )
    else:
        await update.message.reply_text(
            f'З поверненням, {admin.first_name}! 👋'
        )

async def send_order_message(name, phone, product_name, product_price, product_image):
    message = (
        f"Нове замовлення:\n"
        f"Ім'я: {name}\n"
        f"Телефон: {phone}\n"
        f"Продукт: {product_name}\n"
        f"Ціна: {product_price} грн\n"
        f"Зображення продукту: {product_image if product_image else 'Немає зображення'}\n"
    )

    return await print_message(message)

async def print_message(update: Update, context: CallbackContext, message):
    return await update.message.reply_text(message)

def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(print_message)

    app.run_polling()

if __name__ == "__main__":
    main()
