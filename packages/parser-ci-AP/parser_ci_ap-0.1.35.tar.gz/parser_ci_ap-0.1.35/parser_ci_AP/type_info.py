from abc import ABC, abstractmethod
from clang.cindex import CursorKind, Cursor
from pathlib import Path
from typing import List, Optional

from .logger import logger
from .variable_info import VariableInfo

class BaseTypeInfo(ABC):
    def __init__(self, cursor: Cursor, encoding: str):
        self._cursor = cursor
        self.name = cursor.spelling
        self.location = Path(cursor.location.file.name).resolve() if cursor.location.file else Path()
        try:
            self._usr: str = cursor.get_usr()
        except (AttributeError, TypeError, UnicodeDecodeError):
            self._usr = f"{self.name}@{self.location}"
        self.encoding = encoding

        logger.debug(f"Создание BaseTypeInfo для типа: {self.name}")
        self.source_text: str
        self.comment: str

        self.source_text = self._extract_source_text()
        self.comment = self._extract_comments()

    @abstractmethod
    def describe(self) -> str:
        pass

    def _extract_source_text(self) -> str:
        """
        Извлекает исходный текст типа из файла, используя self.encoding.
        """
        extent = self._cursor.extent
        start = extent.start
        end = extent.end

        def extract_lines(lines):
            struct_lines = lines[start.line - 1:end.line]
            struct_lines[0] = struct_lines[0][start.column - 1:]
            struct_lines[-1] = struct_lines[-1][:end.column - 1]
            return "".join(struct_lines).strip()

        try:
            with open(self.location, "r", encoding=self.encoding, errors="replace") as f:
                lines = f.readlines()
                return extract_lines(lines)
        except Exception as e:
            logger.warning(f"{self.name}: ошибка извлечения исходного текста: {e}")
            return f"[!] Ошибка извлечения текста типа {self.name}: {e}"

    def _extract_comments(self) -> str:
        """
        Извлекает комментарии перед определением типа. Поддерживает:
        - однострочные // и ///
        - многострочные /* ... */
        Прерывается на пустой строке.
        """
        try:
            with open(self.location, "r", encoding=self.encoding, errors="replace") as f:
                lines = f.readlines()

            start_line = self._cursor.extent.start.line
            comments = []
            inside_block = False

            for i in range(start_line - 2, -1, -1):
                line = lines[i].rstrip()

                if not line.strip() and not inside_block:
                    break  # пустая строка — стоп

                if "/*" in line and "*/" in line:
                    comments.insert(0, line)
                    continue

                if "*/" in line:
                    inside_block = True
                    comments.insert(0, line)
                    continue

                if inside_block:
                    comments.insert(0, line)
                    if "/*" in line:
                        inside_block = False
                    continue

                if line.strip().startswith("//") or line.strip().startswith("///"):
                    comments.insert(0, line)
                    continue

                break

            return "\n".join(comments).strip()
        except Exception as e:
            logger.warning(f"{self.name}: ошибка извлечения комментариев: {e}")
            return f"[!] Ошибка при извлечении комментариев типа {self.name}: {e}"

    def __str__(self):
        return self.describe()

    def __eq__(self, other):
        if not isinstance(other, BaseTypeInfo):
            return False
        return self._usr == other._usr

    def __hash__(self):
        return hash(self._usr)

class FieldInfo:
    def __init__(
        self,
        name: str,
        type_: str,
        offset: int,
        size: Optional[int],
        is_bitfield: bool,
        bit_width: Optional[int],
        is_anonymous: bool
    ):
        self.name = name
        self.type = type_
        self.offset = offset
        self.size = size
        self.is_bitfield = is_bitfield
        self.bit_width = bit_width
        self.is_anonymous = is_anonymous

    def describe(self, verbose: bool = False) -> str:
        """
        Возвращает строку с описанием поля.
        :param verbose: Если True — подробное описание.
        """
        base = f"name='{self.name}', type='{self.type}', offset={self.offset}, size={self.size}"
        if verbose:
            base += (
                f", is_bitfield={self.is_bitfield}, "
                f"bit_width={self.bit_width}, is_anonymous={self.is_anonymous}"
            )
        return base

class CompositeTypeInfo(BaseTypeInfo):
    def __init__(self, cursor, encoding):
        super().__init__(cursor, encoding)
        self.fields: list = []
        self.size: int

        self.fields = self._extract_fields()
        self.size = self._extract_size()

    def _extract_fields(self) -> List[FieldInfo]:
        fields = []
        for child in self._cursor.get_children():
            if child.kind == CursorKind.FIELD_DECL:
                field_size = None
                try:
                    field_size = child.type.get_size()  # в байтах
                    if field_size == -1:
                        field_size = None
                except Exception as e:
                    logger.warning(f"{self.name}: не удалось получить размер поля {child.spelling}: {e}")

                fields.append(FieldInfo(
                    name=child.spelling,
                    type_=child.type.spelling,
                    offset=child.get_field_offsetof(),  # в битах
                    size=field_size,  # в байтах
                    is_bitfield=child.is_bitfield(),
                    bit_width=child.get_bitfield_width() if child.is_bitfield() else None,
                    is_anonymous=child.is_anonymous()
                ))
        return fields

    def _extract_size(self) -> int:
        try:
            size = self._cursor.type.get_size()
            return size if size != -1 else None
        except Exception as e:
            logger.warning(f"{self.name}: не удалось определить размер: {e}")
            return None

    def describe(self):
        out = [f"{self._type_label()} {self.name} ({self.location})"]

        if self.comment:
            out.append("  Комментарий:")
            out.extend("  " + line for line in self.comment.splitlines())
            out.append("")

        if self.size is not None:
            out.append(f"  sizeof: {self.size} байт")

        if self.fields:
            out.append("  Поля:")
            for field in self.fields:
                out.append("    - " + field.describe())
            out.append("")

        out.append("  Исходный текст:")
        out.append("  -------------------------")
        out.extend("  " + line for line in self.source_text.splitlines())
        return "\n".join(out)

    @abstractmethod
    def _type_label(self) -> str:
        """Возвращает ключевое слово типа: struct / union"""
        pass


class StructInfo(CompositeTypeInfo):
    def __init__(self, cursor, encoding: str):
        super().__init__(cursor, encoding)

    def _type_label(self) -> str:
        return "struct"


class UnionInfo(CompositeTypeInfo):
    def __init__(self, cursor, encoding: str):
        super().__init__(cursor, encoding)

    def _type_label(self) -> str:
        return "union"


class EnumInfo(BaseTypeInfo):
    def __init__(self, cursor, encoding: str):
        super().__init__(cursor, encoding)
        self.constants: List[VariableInfo]
        self.enum_type: str

        self.constants = self._extract_constants()
        self.enum_type = self._extract_enum_type()
        try:
            self.size = self._cursor.enum_type.get_size()
        except Exception:
            logger.warning(f"{self.name}: не удалось получить размер enum: {e}")
            self.size = None

    def describe(self):
        out = [f"enum {self.name} ({self.location})"]

        if self.comment:
            out.append("  Комментарий:")
            out.extend("  " + line for line in self.comment.splitlines())
            out.append("")

        out.append(f"  base type: {self.enum_type} (size: {self.size} байт)")

        if self.constants:
            out.append("  Константы:")
            for const_name, const_value in self.constants:
                out.append(f"    - {const_name} = {const_value}")
            out.append("")

        out.append("  Исходный текст:")
        out.append("  -------------------------")
        out.extend("  " + line for line in self.source_text.splitlines())
        return "\n".join(out)

    def _extract_constants(self):
        constants = []
        for child in self._cursor.get_children():
            if child.kind == CursorKind.ENUM_CONSTANT_DECL:
                const_name = child.spelling
                const_value = child.enum_value
                constants.append((const_name, const_value))
        return constants

    def _extract_enum_type(self):
        try:
            return self._cursor.enum_type.spelling
        except Exception:
            logger.warning(f"{self.name}: не удалось определить базовый тип enum: {e}")
            return "int"

class TypedefInfo(BaseTypeInfo):
    def __init__(self, cursor, encoding: str):
        super().__init__(cursor, encoding)
        self.underlying_type = cursor.underlying_typedef_type.spelling

    def describe(self):
        out = [f"typedef {self.underlying_type} {self.name} ({self.location})"]

        if self.comment:
            out.append("  Комментарий:")
            out.extend("  " + line for line in self.comment.splitlines())
            out.append("")

        out.append("  Исходный текст:")
        out.append("  -------------------------")
        out.extend("  " + line for line in self.source_text.splitlines())

        return "\n".join(out)