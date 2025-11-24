import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum

class FileFormat(Enum):
    """ Форматы файлов которые поддерживает редактор """
    TXT = "txt"
    JSON = "json"
    XML = "xml"

class TextEditorError(Exception):
    """Исключение для всех ошибок редактора"""
    pass

class DocumentNotFoundError(Exception):
    """Файл не найден"""
    pass

class FileOperationError(Exception):
    """Ошибка чтения/записи"""
    pass

class InvalidPositionError(TextEditorError):
    """Неправильная позиция курсора(Например, когда курсор пытаются поставить в несуществующее место"""
    pass

class TextStyle:
    """Класс для хранения стиля текста"""

    def __init__(self, font: str = "Arial", size: int = 12, bold: bool = False, italic: bool = False, color: str = "#n000000"):
        self.font = font
        self.size = size
        self.bold = bold
        self.italic = italic
        self.color = color

class ParagraphStyle:
    """Класс для хранения стиля параграфа"""

    def __init__(self, alignment: str = "left", line_spacing: float = 1.0, margin_left: int = 0, margin_right: int = 0):
        self.alignment = alignment
        self.line_spacing = line_spacing
        self.margin_left = margin_left
        self.margin_right = margin_right

class Cursor:
    """Класс для курсора в текстовом редакторе"""

    def __init__(self, line = 0, column = 0):
        self._line = line
        self._column = column

    def get_line(self) -> int:
        """Строка"""
        return self._line

    def get_column(self) -> int:
        """Столбец"""
        return self._column

    def set_position(self, line: int, column: int) -> None:
        """Для перемещения курсора"""
        if line < 0 or column < 0:
            raise InvalidPositionError("Неверное значение позиции")
        self._line = line
        self._column = column

