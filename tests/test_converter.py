# tests/test_converter.py
import pytest
from src.converter import validate_images, convert_to_pdf
from typing import List
import os
import tempfile
from PIL import Image

@pytest.fixture
def temp_images() -> List[str]:
    """Создаёт временные изображения для тестов."""
    paths = []
    for i in range(2):
        path = tempfile.mktemp(suffix='.png')
        img = Image.new('RGB', (100, 100), color='black')
        img.save(path)
        paths.append(path)
    yield paths
    for path in paths:
        os.remove(path)

def test_validate_images(temp_images: List[str]) -> None:
    """Тестирует валидацию изображений."""
    valid = validate_images(temp_images)
    assert len(valid) == 2

    invalid_path = 'nonexistent.jpg'
    assert validate_images([invalid_path]) == []

def test_convert_to_pdf(temp_images: List[str]) -> None:
    """Тестирует конвертацию в PDF."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf:
        result = convert_to_pdf(temp_images, pdf.name)
        assert result == pdf.name
        assert os.path.exists(result)
    os.remove(result)
