import json
import os
from copy import deepcopy
from functools import lru_cache
from typing import List, Dict, ByteString, BinaryIO, Union, Any, Tuple, Optional


class GundamDataFile:
    signature: ByteString = None
    data_path: str = None
    package: str = None
    default_filename: str = None
    record_count_length: int = 4
    definitions: Dict[str, Dict[str, Dict]] = {}
    constants: Dict = None

    def __init__(self, base_path: str = "."):
        self.base_path = base_path

    def default_file_path(self) -> str:
        return os.path.join(self.base_path, self.data_path, self.default_filename)

    @staticmethod
    def read_int(
        byte_string: bytes, byteorder: str = "little", signed: bool = False
    ) -> int:
        return int.from_bytes(byte_string, byteorder=byteorder, signed=signed)

    @staticmethod
    def write_int(
        value: int, length: int, byteorder: str = "little", signed: bool = False
    ) -> bytes:
        return value.to_bytes(length, byteorder=byteorder, signed=signed)

    @staticmethod
    def read_series_bytes(byte_string: bytes) -> str:
        num = int.from_bytes(byte_string[0:2], byteorder="little")
        g = chr(int.from_bytes(byte_string[2:], byteorder="little"))

        series = f"{g}{num:04}"
        return series

    @staticmethod
    def write_series_bytes(series_string: str) -> bytes:
        string_bytes = bytes()
        string_bytes += int(series_string[1:]).to_bytes(2, byteorder="little")
        string_bytes += ord(series_string[0]).to_bytes(2, byteorder="little")

        return string_bytes

    @staticmethod
    def read_guid_bytes(byte_string: bytes) -> Union[str, bytes, None]:
        if byte_string == b"\x00\x00\x00\x00\x00\x00\x00\x00":
            return None

        try:
            series = int.from_bytes(byte_string[0:2], byteorder="little")
            gundam = chr(byte_string[2])
            if gundam != "G":
                raise TypeError

            unit_type = chr(byte_string[4])
            spec = byte_string[5]
            model = int.from_bytes(byte_string[6:8], byteorder="little")

            unit_id = f"{gundam}{series:04}{unit_type}{model:03}{spec:02}"
        except (TypeError, IndexError):
            return byte_string

        return unit_id

    @staticmethod
    def write_guid_bytes(unit_string: Optional[str]) -> bytes:
        if not unit_string:
            return b"\x00" * 8

        unit_bytes = bytes()
        unit_bytes += int(unit_string[1:5]).to_bytes(2, byteorder="little")
        unit_bytes += bytes(unit_string[0], encoding="utf-8")
        unit_bytes += b"\x00"
        unit_bytes += bytes(unit_string[5], encoding="utf-8")
        unit_bytes += int(unit_string[9:11]).to_bytes(1, byteorder="little")
        unit_bytes += int(unit_string[6:9]).to_bytes(2, byteorder="little")

        return unit_bytes

    @staticmethod
    def read_string_null_term(buffer: BinaryIO, offset: int = None) -> str:
        all_bytes = bytes()
        if offset is not None:
            buffer.seek(offset)

        while True:
            char = buffer.read(1)
            if char == b"\x00":
                break
            all_bytes += char
        output_string = all_bytes.decode("utf-8")

        return output_string

    @staticmethod
    def write_string_null_term(string: str) -> bytes:
        byte_string = string.encode("utf-8") + b"\x00"
        return byte_string

    @classmethod
    def read_string_length(cls, buffer: BinaryIO) -> str:
        length = cls.read_int(buffer.read(1))
        output_string = buffer.read(length).decode("utf-8")

        return output_string

    @classmethod
    def write_string_length(cls, string: str) -> bytes:
        byte_string = cls.write_int(len(string), length=1) + string.encode("utf-8")

        return byte_string

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {},
            "pointers": {},
            "size": {
                table: cls.definition_size(definition)
                for table, definition in cls.definitions.items()
            },
        }

        for table, definition in cls.definitions.items():
            header["counts"][table] = cls.read_int(buffer.read(cls.record_count_length))

        tables = list(cls.definitions.keys())
        for table in tables[1:]:
            header["pointers"][table] = cls.read_int(buffer.read(4))
        header["pointers"][tables[0]] = buffer.tell()

        return header

    @classmethod
    def make_basic_header(
        cls, records: Dict[str, List[Dict]], byte_strings: Dict[str, bytes]
    ) -> Dict[str, Dict[str, int]]:
        header = {
            "counts": {table: len(data) for table, data in records.items()},
            "pointers": {},
            "size": {
                table: cls.definition_size(definition)
                for table, definition in cls.definitions.items()
            },
            "block_size": {
                table: len(byte_string) for table, byte_string in byte_strings.items()
            },
        }
        return header

    @classmethod
    def calculate_header(
        cls, records: Dict[str, List[Dict]], byte_strings: Dict[str, bytes]
    ) -> Dict[str, Dict[str, int]]:
        header = cls.make_basic_header(records, byte_strings)
        tables = list(records.keys())
        pointer = len(tables) * cls.record_count_length + len(tables[1:]) * 4
        for i, table in enumerate(tables):
            # skip the first table by default
            if i != 0:
                header["pointers"][table] = pointer
            pointer += len(byte_strings[table])

        return header

    @classmethod
    def write_header(cls, header: Dict[str, Dict[str, int]]) -> bytes:
        string_bytes = bytes()
        string_bytes += cls.signature
        for table, record_count in header["counts"].items():
            string_bytes += cls.write_int(record_count, cls.record_count_length)

        for table, pointer in header["pointers"].items():
            string_bytes += cls.write_int(pointer, 4)

        return string_bytes

    def dump(self, data_filename: str = None, json_filename: str = None):
        data_filename = data_filename or self.default_file_path()
        json_filename = json_filename or (data_filename.rpartition(".")[0] + ".json")
        data = {
            self.default_filename
            or os.path.split(data_filename)[1]: self.read_file(data_filename)
        }
        os.makedirs(os.path.split(json_filename)[0], exist_ok=True)
        json.dump(data, open(json_filename, "wt"), indent=4)

    def load(self, json_filename: str = None, data_filename: str = None):
        data_filename = data_filename or self.default_file_path()
        json_filename = json_filename or (data_filename.rpartition(".")[0] + ".json")
        records = json.load(open(json_filename, "rt"))[
            self.default_filename or os.path.split(data_filename)[1]
        ]
        self.write_file(records, data_filename)

    def read_file(self, filename: str = None) -> Dict[str, List[Dict]]:
        filename = filename or self.default_file_path()
        with open(filename, "rb") as buffer:
            records = self.read(buffer)
        return records

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = {}
        header = self.read_header(buffer)
        for table_name, definition in self.definitions.items():
            try:
                buffer.seek(header["pointers"][table_name])
            except KeyError:
                pass
            records[table_name] = self.read_records(
                definition, buffer, header["counts"][table_name]
            )

        records = self.post_processing(records)
        self.remove_constants(records)

        return records

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        return records

    @classmethod
    def pre_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        return records

    def write_file(self, records: Dict[str, List[Dict]], filename: str):
        filename = filename or self.default_file_path()
        os.makedirs(os.path.split(filename)[0], exist_ok=True)
        with open(filename, "wb") as buffer:
            buffer.write(self.write(records))

    @classmethod
    def write_blocks(cls, records: Dict[str, List[Dict]]) -> Dict[str, bytes]:
        byte_blocks = {}
        for table, definition in cls.definitions.items():
            byte_blocks[table] = cls.write_records(definition, records[table])
        return byte_blocks

    @classmethod
    def combine_blocks(
        cls, byte_blocks: Dict[str, bytes], header: bytes = None
    ) -> bytes:
        byte_string = bytes()
        if header is not None:
            byte_string += header
        for table, block in byte_blocks.items():
            byte_string += block
        return byte_string

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        records = deepcopy(records)
        self.apply_constants(records)
        records = self.pre_processing(records)

        byte_blocks = self.write_blocks(records)

        header = self.calculate_header(records, byte_blocks)
        header_bytes = self.write_header(header)

        byte_string = self.combine_blocks(byte_blocks, header_bytes)

        return byte_string

    @classmethod
    def definition_size(cls, definition: Dict) -> int:
        size = 0
        for field_type in definition.values():
            _, byte_count, _, _ = cls.parse_field_type(field_type)
            size += byte_count
        return size

    @staticmethod
    def bit_smash(field: str, value: int, sub_fields: List[str]) -> Dict[str, int]:
        smashed = {
            f"{field}_{sf}": 1 if value and value & (2 ** i) else 0
            for i, sf in enumerate(sub_fields)
        }
        return smashed

    @staticmethod
    def bit_smush(field: str, smashed: Dict[str, int], sub_fields: List[str]) -> int:
        value = 0

        for i, sf in enumerate(sub_fields):
            if smashed[f"{field}_{sf}"] == 1:
                value += 2 ** i

        return value

    @classmethod
    def header_length(cls) -> int:
        return len(cls.signature) + cls.record_count_length

    @classmethod
    def apply_constants(cls, records: Union[List[Dict], Dict[str, List[Dict]]]) -> None:
        if isinstance(records, dict):
            for record_set in records.values():
                cls._apply_constants(record_set)
        else:
            cls._apply_constants(records)

    @classmethod
    def _apply_constants(cls, records: List[Dict]) -> None:
        if not cls.constants:
            return

        for r in records:
            for c, v in cls.constants.items():
                if r.get(c) is not None and r[c] != v:
                    print(f"WARNING: {c} has mismatched constant {r[c]} != {v}")
                else:
                    r[c] = v

    @classmethod
    def remove_constants(
        cls, records: Union[List[Dict], Dict[str, List[Dict]]]
    ) -> None:
        if isinstance(records, dict):
            for record_set in records.values():
                cls._remove_constants(record_set)
        else:
            cls._remove_constants(records)

    @classmethod
    def _remove_constants(cls, records: List[Dict]) -> None:
        if not cls.constants:
            return

        for r in records:
            for c, v in cls.constants.items():
                if r.get(c) is not None and r[c] != v:
                    print(f"WARNING: {c} has mismatched constant {r[c]} != {v}")
                else:
                    r.pop(c, None)

    @classmethod
    def write_records(cls, definition: Dict, records: List[Dict]) -> bytes:
        cls.apply_constants(records)

        main_block_size = len(records) * cls.definition_size(definition)
        child_bytes = bytes()

        # Assemble child blocks while filling in pointers
        for field, field_type in definition.items():
            base_type, byte_count, is_list, child_type = cls.parse_field_type(
                field_type
            )
            if base_type not in ["pointer", "cfpointer"]:
                continue

            for i, r in enumerate(records):
                r[f"{field}_pointer"] = (
                    main_block_size
                    - (i * cls.definition_size(definition))
                    + len(child_bytes)
                )

                if is_list:
                    r[f"{field}_count"] = len(r[field])
                    for c in r[field]:
                        child_bytes += cls.write_field(child_type, c)
                else:
                    child_bytes += cls.write_field(child_type, r[field])

        byte_string = bytes()
        for record in records:
            byte_string += cls.write_record(definition, record)

        byte_string += child_bytes

        return byte_string

    @classmethod
    def read_records(
        cls, definition: Dict, buffer: BinaryIO, record_count: int
    ) -> List[Dict]:
        records = []

        for i in range(record_count):
            record = cls.read_record(definition, buffer)
            records.append(record)

        return records

    @classmethod
    def read_record(cls, definition: Dict, buffer: BinaryIO) -> Dict[str, Any]:
        location = buffer.tell()
        record = {}
        for field, field_type in definition.items():
            value = cls.read_field(field_type, buffer, location)

            if field_type.startswith("null") and value is None:
                continue
            record[field] = value

        return record

    @classmethod
    def write_record(cls, definition: Dict, record: Dict) -> bytes:
        byte_string = bytes()
        for field, field_type in definition.items():
            base_type, byte_count, is_list, _ = cls.parse_field_type(field_type)

            if "pointer" not in base_type:
                return cls.write_field(field_type, record[field])

            pointer_type = "uint:2" if "sh" in base_type else "uint:4"
            count_type = "uint:2" if "2c" in base_type else "uint:4"

            if "cf" in base_type:
                byte_string += cls.write_field(count_type, record.pop(f"{field}_count"))
                byte_string += cls.write_field(
                    pointer_type, record.pop(f"{field}_pointer")
                )
            elif "pointer" in base_type and is_list:
                byte_string += cls.write_field(
                    pointer_type, record.pop(f"{field}_pointer")
                )
                byte_string += cls.write_field(count_type, record.pop(f"{field}_count"))
            elif "pointer" in base_type and not is_list:
                byte_string += cls.write_field(
                    pointer_type, record.pop(f"{field}_pointer")
                )

        return byte_string

    @staticmethod
    @lru_cache
    def parse_field_type(
        field_type: str
    ) -> Tuple[str, Optional[int], bool, Optional[str]]:
        ft = field_type.split(":")

        base_type = ft.pop(0)
        byte_count = None
        is_list = False
        child_type = None

        if base_type in ["uint", "int", "null", "bytes", "binary"]:
            byte_count = int(ft.pop(0))
        elif base_type in ["guid"]:
            byte_count = 8
        elif base_type in ["series"]:
            byte_count = 4

        if "pointer" not in base_type:
            return base_type, byte_count, is_list, child_type

        byte_count = 2 if "sh" in base_type else 4

        if len(ft) > 1 and ft[0] == "list":
            ft.pop(0)
            is_list = True
            byte_count += 2 if "2c" in base_type else 4
        child_type = ":".join(ft)

        return base_type, byte_count, is_list, child_type

    @classmethod
    def read_field(
        cls, field_type: str, buffer: BinaryIO, location: int = None
    ) -> Union[List, Dict, int, str, bytes]:
        value = None
        base_type, byte_count, is_list, child_type = cls.parse_field_type(field_type)

        if base_type in ["uint"]:
            value = cls.read_int(buffer.read(byte_count))
        elif base_type in ["int"]:
            value = cls.read_int(buffer.read(byte_count), signed=True)
        elif base_type in ["binary"]:
            value = bin(cls.read_int(buffer.read(byte_count)))[2:].zfill(byte_count * 8)
        elif base_type in ["string_len_prefix"]:
            value = cls.read_string_length(buffer)
        elif base_type in ["string_null_term"]:
            value = cls.read_string_null_term(buffer)
        elif base_type in ["guid"]:
            value = cls.read_guid_bytes(buffer.read(8))
        elif base_type in ["series"]:
            value = cls.read_series_bytes(buffer.read(4))
        elif base_type in ["bytes"]:
            value = buffer.read(byte_count)
        elif base_type in ["null"]:
            value = buffer.read(byte_count)
            if value != (b"\x00" * byte_count):
                print(f"{field_type} not null: {value}")
            else:
                value = None
        elif "pointer" in base_type:
            if not is_list and not child_type:
                return cls.read_int(buffer.read(byte_count)) + location

            elif is_list:
                count_size = 2 if "2c" in base_type else 4

                # if list count is first in the pair
                if "cf" in base_type:
                    list_count = cls.read_int(buffer.read(count_size))
                    pointer = (
                        cls.read_int(buffer.read(byte_count - count_size)) + location
                    )
                else:
                    pointer = (
                        cls.read_int(buffer.read(byte_count - count_size)) + location
                    )
                    list_count = cls.read_int(buffer.read(count_size))

                value = []
                save_location = buffer.tell()
                buffer.seek(pointer)
                for _ in range(list_count):
                    v = cls.read_field(child_type, buffer)
                    value.append(v)
                buffer.seek(save_location)

            else:
                pointer = cls.read_int(buffer.read(byte_count)) + location
                save_location = buffer.tell()
                buffer.seek(pointer)
                value = cls.read_field(child_type, buffer)
                buffer.seek(save_location)

        return value

    @classmethod
    def write_field(cls, field_type: str, value: Union[int, str, bytes]) -> bytes:
        byte_string = bytes()
        base_type, byte_count, is_list, child_type = cls.parse_field_type(field_type)

        if isinstance(value, bytes):
            return value
        elif base_type in ["int"]:
            byte_string += cls.write_int(value, byte_count, signed=True)
        elif base_type in ["uint"]:
            byte_string += cls.write_int(value, byte_count)
        elif base_type in ["binary"]:
            byte_string += cls.write_int(int(f"0b{value}", 2), byte_count)
        elif base_type in ["string_len_prefix"]:
            byte_string += cls.write_string_length(value)
        elif base_type in ["string_null_term"]:
            byte_string += cls.write_string_null_term(value)
        elif base_type in ["guid"]:
            byte_string += cls.write_guid_bytes(value)
        elif base_type in ["series"]:
            byte_string += cls.write_series_bytes(value)
        elif base_type in ["bytes"]:
            byte_string += (value + ("\x00" * byte_count))[0:byte_count]
        elif base_type in ["null"]:
            if (
                value is not None
                and isinstance(value, bytes)
                and len(value) == byte_count
            ):
                byte_string += value
            else:
                byte_string += b"\x00" * byte_count
        elif "pointer" in base_type:
            byte_count = 2 if "sh" in base_type else 4
            byte_string += cls.write_int(value, byte_count)

        return byte_string
