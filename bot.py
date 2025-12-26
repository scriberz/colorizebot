import pytz
# Патчим get_localzone до импорта telegram, чтобы возвращал pytz timezone
try:
    from tzlocal import get_localzone
    _original_get_localzone = get_localzone
    def _patched_get_localzone():
        return pytz.UTC
    import tzlocal
    tzlocal.get_localzone = _patched_get_localzone
except:
    pass

# Патчим apscheduler.util.astimezone
from apscheduler import util as apscheduler_util
_original_astimezone = apscheduler_util.astimezone
def _patched_astimezone(obj):
    if obj is None:
        return pytz.UTC
    if isinstance(obj, pytz.BaseTzInfo):
        return obj
    # Если это zoneinfo timezone, конвертируем в pytz
    try:
        from zoneinfo import ZoneInfo
        if isinstance(obj, ZoneInfo):
            # Получаем имя timezone и конвертируем в pytz
            tz_name = str(obj)
            return pytz.timezone(tz_name)
    except:
        pass
    # Если ничего не помогло, возвращаем UTC
    return pytz.UTC
apscheduler_util.astimezone = _patched_astimezone

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from image_processor import process_image
import config
import io


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Пришли мне фото с подписью‑промтом в одном сообщении,\n"
        "я сгенерирую новую картинку и отправлю её обратно."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message

    # Фото + подпись как промт
    prompt = message.caption or "Сделай из этого изображения красивую стилизованную картинку."

    # Отправляем сообщение о том, что идет обработка
    status_msg = await message.reply_text("🔄 Анализирую изображение и генерирую новую картинку...")

    try:
        photo_file = await message.photo[-1].get_file()

        buffer = io.BytesIO()
        await photo_file.download_to_memory(buffer)
        image_bytes = buffer.getvalue()

        processed_image = process_image(image_bytes, prompt)

        await status_msg.delete()
        await message.reply_photo(photo=processed_image)
    except Exception as e:
        await status_msg.edit_text(f"❌ Ошибка: {str(e)}\n\nПопробуйте еще раз или используйте другой промт.")


def main() -> None:
    import logging
    import sys
    
    # Включаем логирование в файл и консоль
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler('bot.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Запуск бота...")
        application = Application.builder().token(config.TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

        logger.info("Бот запущен, ожидание обновлений...")
        application.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}", exc_info=True)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
