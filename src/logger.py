# src/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional

def setup_logger(log_file: str = 'app.log', level: int = logging.INFO) -> logging.Logger:
    """
    Настраивает логгер с выводом в консоль и файл.

    Args:
        log_file (str): Путь к файлу лога. По умолчанию 'app.log'.
        level (int): Уровень логирования. По умолчанию INFO.

    Returns:
        logging.Logger: Настроенный логгер.
    """
    # Создаём директорию для логов, если не существует
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    full_log_path = os.path.join(log_dir, log_file)

    logger = logging.getLogger('image_to_pdf')
    logger.setLevel(level)

    # Форматтер
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Хендлер для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Хендлер для файла с ротацией (макс 5 МБ, 3 бэкапа)
    file_handler = RotatingFileHandler(full_log_path, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Пример использования: logger = setup_logger()
