from PIL import Image, ImageOps
import io

def process_image(image: io.BytesIO) -> io.BytesIO:
    img = Image.open(image)
    # Пример простого преобразования: инвертирование цветов
    img = ImageOps.invert(img.convert('RGB'))
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output
