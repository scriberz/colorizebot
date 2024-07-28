from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from image_processor import process_image
import config
import io

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправьте мне изображение для раскраски.')

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('photo.jpg')
    with open('photo.jpg', 'rb') as image_file:
        processed_image = process_image(image_file)
        update.message.reply_photo(photo=processed_image)

def main() -> None:
    updater = Updater(config.TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
