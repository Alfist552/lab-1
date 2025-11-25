import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
import os

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

    def __init__(self, font: str = "Arial", size: int = 12, bold: bool = False, italic: bool = False, color: str = "#000000"):
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

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в стиль для JSON"""
        return{
            "alignment": self.alignment,
            "line_spacing": self.line_spacing,
            "margin_left": self.margin_left,
            "margin_right": self.margin_right
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParagraphStyle":
        """Создание стиля параграфа из словаря"""
        return cls(
            alignment = data.get("alignment", "left"),
            line_spacing = data.get("line_spacing", 1.0),
            margin_left = data.get("margin_left", 0),
            margin_right= data.get("margin_right", 0)
        )

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

    def to_dict(self) -> Dict[str, int]:
        """Преобразование позиции курсора в словарь для JSON"""
        return{
            "line": self._line,
            "column": self._column
        }
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'Cursor':
        """Создать курсор из словаря"""
        return cls(
            line = data.get("line", 0),
            column = data.get("column", 0)
        )

class Selection:
    """Для выделения текста"""

    def __init__(self):
        self.start_line = 0
        self.start_column = 0
        self.end_line = 0
        self.end_column = 0
        self.is_active = False

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

    def __init__(self, document: 'Document', line: int, column: int, text: str):
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
        self.document.text_buffer.delete_text(self.line, self.column, self.text)


class Document:
    """Основной класс документа"""

    def __init__(self, title: str = "Новый документ"):
        self.title = title
        self.text_buffer = TextBuffer()
        self.cursor = Cursor()
        self.selection = Selection()
        self.history = HistoryManager()
        self.created_at = datetime.now()
        self.modified_at = datetime.now()

    def insert_text(self, text: str) -> None:
        """Вставить текст на позицию курсора"""
        line = self.cursor.get_line()
        column = self.cursor.get_column()
        command = InsertTextCommand(self, line, column, text)
        self.history.execute_command(command)
        self.modified_at = datetime.now()

    def get_text(self) -> str:
        """Получить весь текст документа"""
        return self.text_buffer.get_text()

    def set_text(self, text: str) -> None:
        """Установить текст документа"""
        self.text_buffer.set_text(text)
        self.cursor.set_position(0, 0)
        self.modified_at = datetime.now()

    def undo(self) -> bool:
        """Отменить последнее действие"""
        result = self.history.undo()
        if result:
            self.modified_at = datetime.now()
        return result

    def redo(self) -> bool:
        """Повторить последнее отмененное действие"""
        result = self.history.redo()
        if result:
            self.modified_at = datetime.now()
        return result

    def to_xml(self) -> ET.Element:
        """Преобразовать документ в XML"""
        root = ET.Element("document")

        title_elem = ET.SubElement(root, "title")
        title_elem.text = self.title

        content_elem = ET.SubElement(root, "content")
        content_elem.text = self.get_text()

        cursor_elem = ET.SubElement(root, "cursor")
        cursor_elem.set("line", str(self.cursor.get_line()))
        cursor_elem.set("column", str(self.cursor.get_column()))

        return root

    @classmethod
    def from_xml(cls, root: ET.Element) -> 'Document':
        """Создать документ из XML"""
        title_elem = root.find("title")
        title = title_elem.text if title_elem is not None else "Новый документ"

        document = cls(title)

        content_elem = root.find("content")
        if content_elem is not None and content_elem.text:
            document.set_text(content_elem.text)

        cursor_elem = root.find("cursor")
        if cursor_elem is not None:
            line = int(cursor_elem.get("line", "0"))
            column = int(cursor_elem.get("column", "0"))
            document.cursor.set_position(line, column)

        return document

class HistoryManager:
    """Менеджер истории команд для отмены/повтора"""

    def __init__(self, max_history_size: int = 100):
        self.undo_stack = []
        self.redo_stack = []
        self.max_history_size = max_history_size

    def execute_command(self, command: Command) -> None:
        """Добавить в журнал действий выполненную команду"""
        if not self.is_valid_command(command):
            raise TextEditorError("Неверная команда")
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

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование текста в словарь для JSON"""
        return {
            "content": self.get_text(),
            "lines_count": len(self.lines)
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextBuffer':
        """Создание текстового буфера из словаря"""
        buffer = cls()
        content = data.get("content", "")
        buffer.set_text(content)
        return buffer


"""Функции для работы с JSON файлами"""

def save_to_json(document: 'Document', file_path: str) -> None:

    """
    Сохранение документа в JSON файл

    Путь к файлу - file.path

    Документ для сохранения - document

    Если не удастся сохранить файл --> FileOperationError

    """

    try:
        """ Структура данных для JSON"""
        data = {
            "title": document.title,
            "content": document.text_buffer.get_text(),
            "cursor": document.cursor.to_dict(),
            "created_at": document.created_at.isoformat(),
            "modified_at": document.modified_at.isoformat()
        }

        with open(file_path, 'w', encoding = 'utf-8') as file:
            json.dump(data, file, indent = 2, ensure_ascii = False)

    except Exception as e:
        raise FileOperationError(f"Не удалось сохранить в JSON: {str(e)}")

def load_from_json(file_path: str) -> 'Document':

    """

    Загрузка документа из JSON файла

    Путь к JSON файлу - file.path

    Если не удалось загрузить файл - FileOperationError

    Если файл не найден - DocumentNotFoundError

    """
    try:
        if not os.path.exists(file_path):
            raise DocumentNotFoundError(f"Файл {file_path} не найден")

        with open(file_path, 'r', encoding = 'utf-8') as file:
            data = json.load(file)

        document = Document(title = data.get("title" , "Новый документ"))
        document.text_buffer.set_text(data.get("content", ""))


        cursor_data = data.get("cursor", {})
        document.cursor = Cursor.from_dict(cursor_data)

        return document

    except DocumentNotFoundError:
        raise
    except Exception as e:
        raise FileOperationError(f"Ошибка загрузки JSON: {str(e)}")

def save_to_xml(document: Document, file_path: str) -> None:
    """

    Сохранение в XML формат

    Путь к файлу - file.path

    Документ для сохранения - document

    Если не удалось сохранить - FileOperationError

    """

    try:
        root = document.to_xml()
        tree = ET.ElementTree(root)

        tree.write(file_path, encoding = 'utf-8', xml_declaration = True)

    except Exception as e:
        raise FileOperationError(f"Не удалось сохранить в XML: {str(e)}")

def load_from_xml(file_path: str) -> Document:
    """
    Загрузка файла XML

    Аналогично загрузке файлов JSON

    """
    try:
        if not os.path.exists(file_path):
            raise DocumentNotFoundError(f"Файл {file_path} не найден")

        tree = ET.parse(file_path)
        root = tree.getroot()

        return Document.from_xml(root)

    except DocumentNotFoundError:
        raise
    except Exception as e:
        raise FileOperationError(f"Ошибка загрузки XML: {str(e)}")



if __name__ == "__main__":
    try:
        doc = Document("Лабораторная работа №1")
        doc.text_buffer.set_text("""В данной лабораторной работе необходимо реализовать Стиль ООП.
        
        * Обработать исключительные стуации а также разобраться с форматами JSON и XML
        
        * Выполняется вариант 16:Напишите классы для предметной области текстового редактора. 
        
        -Были реализованы основные классы, реализуемые для текстового редактора: удаление, повтор действий,
        
        -вставка, удаление, копирование, вырезание, а также показаны шрифт и параграф
        
        -Курсор можно перемещать по тексту и выделять различные участки для редактирования
        
        Конец образца.""")

        doc.cursor.set_position(1, 5)

        """Сохранение в JSON"""
        save_to_json(doc, "document1.json")
        print("Документ сохранен в JSON")

        """Загрузка из JSON"""
        loaded_doc = load_from_json("document1.json")
        print(f" Документ загружен из JSON файла")
        print(f" Заголовок: {loaded_doc.title}")
        print(f"Количество строк: {len(loaded_doc.text_buffer.lines)}")
        print(f"Курсор: строка {loaded_doc.cursor.get_line()}, столбец {loaded_doc.cursor.get_column()}")
        print(f"Время создания: {loaded_doc.created_at}")
        print(f" Содержимое: {loaded_doc.text_buffer.get_text()}")

        """Сохранение в XML"""
        save_to_xml(doc, "document1.xml")
        print("Документ сохранен в XML")

        """Загрузка из XML"""
        xml_doc = load_from_xml("document1.xml")
        print(f" Документ загружен из XML файла")
        print(f" Заголовок: {xml_doc.title}")
        print(f"Количество строк: {len(xml_doc.text_buffer.lines)}")
        print(f"Курсор: строка {xml_doc.cursor.get_line()}, столбец {xml_doc.cursor.get_column()}")
        print(f"Время создания: {xml_doc.created_at}")
        print(f" Содержимое: {xml_doc.text_buffer.get_text()}")

    except (FileOperationError, DocumentNotFoundError) as e:
        print(f"Ошибка: {e}")

