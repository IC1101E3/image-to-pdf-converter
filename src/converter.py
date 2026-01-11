# src/converter.py
import img2pdf
from PIL import Image
import os
from typing import List, Optional
import logging

logger = logging.getLogger('image_to_pdf.converter')

SUPPORTED_FORMATS = {'jpg', 'jpeg', 'png'}  # Константа для поддерживаемых форматов

def validate_images(image_paths: List[str]) -> List[str]:
    """
    Проверяет, являются ли файлы изображениями поддерживаемых форматов.

    Args:
        image_paths (List[str]): Список путей к файлам.

    Returns:
        List[str]: Список валидных путей.
    """
    valid_paths = []
    for path in image_paths:
        if not os.path.isfile(path):
            logger.warning(f"Файл не существует: {path}")
            continue
        ext = os.path.splitext(path)[1].lower().lstrip('.')
        if ext not in SUPPORTED_FORMATS:
            logger.warning(f"Неподдерживаемый формат: {path} ({ext})")
            continue
        try:
            Image.open(path)  # Проверяем, открывается ли изображение
            valid_paths.append(path)
        except Exception as e:
            logger.error(f"Ошибка открытия изображения {path}: {e}")
    return valid_paths

def convert_to_pdf(image_paths: List[str], output_path: str) -> Optional[str]:
    """
    Конвертирует список изображений в PDF.

    Args:
        image_paths (List[str]): Список путей к изображениям.
        output_path (str): Путь к выходному PDF.

    Returns:
        Optional[str]: Путь к PDF или None при ошибке.
    """
    valid_images = validate_images(image_paths)
    if not valid_images:
        logger.error("Нет валидных изображений для конвертации")
        return None

    try:
        with open(output_path, 'wb') as f:
            f.write(img2pdf.convert(valid_images))
        logger.info(f"Успешная конвертация: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Ошибка конвертации: {e}")
        return None
