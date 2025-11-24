import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum

class FileFormat(Enum):
    # Форматы файлов которые поддерживает редактор
    TXT = "txt"
    JSON = "json"
    XML = "xml"