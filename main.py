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
