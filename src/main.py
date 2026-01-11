# src/main.py
from .logger import setup_logger
from .gui import run_gui
import logging

if __name__ == '__main__':
    logger = setup_logger(log_file='converter.log')
    logger.info("Запуск приложения")
    run_gui() 
