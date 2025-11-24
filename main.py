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

class Selection:
    """Для выделения текста"""

    def __init__(self):
        self.start_line = 0
        self.start_column = 0
        self.end_line = 0
        self.end_column = 0
        self.is_active = True

    def set_start(self, line: int, column: int) -> None:
        """Начальная позиция выделения"""
        self.start_line = line
        self.start_column = column
        self.is_active = True

    def set_end(self, line: int, column: int) -> None:
        """Конечная позиция выделения"""
        self.end_line = line
        self.end_column = column
        self.is_active = True

    def clear(self) -> None:
        """Сбросить"""
        self.is_active = False

    def get_selected_text(self, lines: list[str]) -> str:
        """Получить выделенный текст"""
        if not self.is_active:
            return ""

        return "текст"

class Command:
    """Команды отмены или повтора"""

    def __init__(self, description: str = ""):
        self.description = description
        self.timestamp = datetime.now()

    def execute(self) -> None:
        """Выполнение команды"""
        pass

    def undo(self) -> None:
        """Отмена команды"""
        pass

class InsertTextCommand(Command):
    """Для вставки текста"""

    def __init__(self, document: 'Document', line: int, column: int, text: str)
        super().__init__(f"Вставка текста в позицию ({line}, {column})")
        self.document = document
        self.line = line
        self.column = column
        self.text = text

    def execute(self) -> None:
        """Вставить текст"""
        self.document.text_buffer.insert_text(self.line, self.column, self.text)

    def undo(self) -> None:
        """Отменить вставку текста"""
        self.document.text_buffer.insert_text(self.line, self.column, self.text)

