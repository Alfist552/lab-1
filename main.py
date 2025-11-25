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

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать стиль в словарь (JSON)"""
        return{
            "font": self.font,
            "size": self.size,
            "bold": self.bold,
            "italic": self.italic,
            "color": self.color
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TextStyle":
        """Создать стиль из словаря"""
        return cls(
            font = data.get("font", "Arial"),
            size = data.get("size", 12),
            bold = data.get("bold", False),
            italic = data.get("italic", False),
            color = data.get("color", "#000000")
        )

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


class HistoryManager:
    """Менеджер истории команд для отмены/повтора"""

    def __int__(self, max_history_size: int = 100):
        self.undo_stack = []
        self.redo_stack = []
        self.max_history_size = max_history_size

    def execute_command(self, command: Command) -> None:
        """Добавить в журнал действий выполненную команду"""
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self) -> bool:
        """отмена"""
        if not self.undo_stack:
            return False
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        return True

    def redo(self) -> bool:
        """Повтор отмененной команды"""
        if not self.redo_stack:
            return False

        command = self.redo_stack.pop()
        command.execute()
        self.redo_stack.append(command)
        return True

    def can_undo(self) -> bool:
        """Можно ли отменить действие"""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Можно ли повторить действие"""
        return len(self.redo_stack) > 0

    @staticmethod
    def get_max_history_size() -> int:
        """Максимальный размер истории"""
        return 100

    @staticmethod
    def is_valid_command(command: Command) -> bool:
        """Действительна ли команда"""
        return hasattr(command, "execute") and hasattr(command, 'undo')

class TextBuffer:
    """Класс для управления тектом"""

    def __init__(self):
        self.lines = [""]

    def insert_text(self,line: int, column: int, text: str) -> None:
        """Вставка текста"""
        if line >= len(self.lines):
            raise InvalidPositionError(f"Строка {line} не существует")

        current_line = self.lines[line]
        new_line = current_line[:column] + text + current_line[column:]
        self.lines[line] = new_line

    def delete_text(self,line: int, start_col: int, end_col: int) -> None:
        """Удаление текста"""
        if line >= len(self.lines):
            raise InvalidPositionError(f"Строка {line} не существует")

        current_line = self.lines[line]
        self.lines[line] = current_line[:start_col] +  current_line[end_col:]

    def get_text(self) -> str:
        """Весь текст как 1 строка"""
        return "\n".join(self.lines)

    def set_text(self, text: str) -> None:
        """Установить текст из строки"""
        self.lines = text.split("\n") if text else [""]


