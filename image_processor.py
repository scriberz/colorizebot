import io
from PIL import Image
from google import genai

import config


# Создаем клиент Gemini
client = genai.Client(api_key=config.GEMINI_API_KEY)


def process_image(image_bytes: bytes, prompt: str) -> io.BytesIO:
    """
    Использует Gemini 2.5 Flash Image для генерации нового изображения
    на основе исходного изображения и текстового промта.
    """
    # Загружаем изображение из bytes
    image = Image.open(io.BytesIO(image_bytes))
    
    # Создаем промт для генерации (можно добавить детали для лучшего результата)
    generation_prompt = f"{prompt}"
    
    # Генерируем изображение через Gemini 2.5 Flash Image
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[generation_prompt, image],
    )
    
    # Извлекаем сгенерированное изображение из ответа
    for part in response.parts:
        if part.inline_data is not None:
            generated_image = part.as_image()
            
            # Конвертируем PIL Image в BytesIO
            output = io.BytesIO()
            generated_image.save(output, format='PNG')
            output.seek(0)
            return output
        elif part.text is not None:
            # Если есть текстовый ответ, логируем его (может быть полезно для отладки)
            print(f"Gemini text response: {part.text}")
    
    # Если изображение не найдено в ответе, выбрасываем ошибку
    raise Exception("Не удалось сгенерировать изображение. Попробуйте другой промт.")
