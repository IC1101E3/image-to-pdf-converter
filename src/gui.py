# src/gui.py
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QMessageBox
from typing import List, Optional
from .converter import convert_to_pdf
import logging
import sys
import os

logger = logging.getLogger('image_to_pdf.gui')

class ConverterWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.image_paths: List[str] = []
        self.output_path: Optional[str] = None
        self.init_ui()

    def init_ui(self) -> None:
        """Инициализирует пользовательский интерфейс."""
        self.setWindowTitle('Конвертер изображений в PDF')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Выберите изображения и путь для PDF', self)
        layout.addWidget(self.label)

        select_images_btn = QPushButton('Выбрать изображения', self)
        select_images_btn.clicked.connect(self.select_images)
        layout.addWidget(select_images_btn)

        select_output_btn = QPushButton('Выбрать путь для PDF и новое имя файла', self)
        select_output_btn.clicked.connect(self.select_output)
        layout.addWidget(select_output_btn)

        convert_btn = QPushButton('Конвертировать', self)
        convert_btn.clicked.connect(self.perform_conversion)
        layout.addWidget(convert_btn)

        self.setLayout(layout)

    def select_images(self) -> None:
        """Открывает диалог для выбора изображений."""
        files, _ = QFileDialog.getOpenFileNames(self, 'Выбрать изображения', '', 'Images (*.jpg *.jpeg *.png)')
        if files:
            self.image_paths = files
            self.label.setText(f'Выбрано изображений: {len(files)}')
            logger.info(f"Выбраны изображения: {files}")

    def select_output(self) -> None:
        """Открывает диалог для выбора пути вывода PDF."""
        file, _ = QFileDialog.getSaveFileName(self, 'Сохранить PDF', '', 'PDF (*.pdf)')
        if file:
            # Добавляем расширение .pdf, если оно отсутствует
            if not file.lower().endswith('.pdf'):
                file += '.pdf'
            self.output_path = file
            self.label.setText(f'Путь вывода: {file}')
            logger.info(f"Выбран путь вывода: {file}")

    def perform_conversion(self) -> None:
        """Выполняет конвертацию и показывает результат."""
        if not self.image_paths or not self.output_path:
            QMessageBox.warning(self, 'Ошибка', 'Выберите изображения и путь для PDF')
            return

        result = convert_to_pdf(self.image_paths, self.output_path)
        if result:
            QMessageBox.information(self, 'Успех', f'PDF создан: {result}')
        else:
            QMessageBox.error(self, 'Ошибка', 'Конвертация не удалась')

def run_gui() -> None:
    """Запускает приложение GUI."""
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec_())
