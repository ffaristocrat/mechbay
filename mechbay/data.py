import json
import os
from typing import List, Dict, ByteString, BinaryIO, Union, Any


class GundamDataFile:
    header: ByteString = None
    default_filename: str = None
    record_count_length: int = 4
    definition: Dict[str, str] = None
    constants: Dict = None

    def __init__(
        self,
        filename: str = None,
        header: ByteString = None,
        record_count_length: int = None,
    ):
        self.filename = filename or self.default_filename
        if header:
            self.header = header
        if record_count_length is not None:
            self.record_count_length = record_count_length

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
    def read_guid_bytes(byte_string: bytes) -> Union[str, None]:
        if byte_string == b"\x00\x00\x00\x00\x00\x00\x00\x00":
            return None

        series = int.from_bytes(byte_string[0:2], byteorder="little")
        gundam = chr(byte_string[2])
        unit_type = chr(byte_string[4])
        spec = byte_string[5]
        model = int.from_bytes(byte_string[6:8], byteorder="little")

        unit_id = f"{gundam}{series:04}{unit_type}{model:03}{spec:02}"

        return unit_id

    @staticmethod
    def write_guid_bytes(unit_string: Union[str, None]) -> bytes:
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
    def read_header(cls, buffer: BinaryIO) -> int:
        header = buffer.read(len(cls.header))
        assert header == cls.header
        record_count = cls.read_int(buffer.read(cls.record_count_length))
        return record_count

    @classmethod
    def write_header(cls, record_count: int) -> bytes:
        string_bytes = bytes()
        string_bytes += cls.header
        string_bytes += cls.write_int(record_count, 4)
        return string_bytes

    def dump(self, data_filename: str = None, json_filename: str = None):
        data_filename = data_filename or self.filename
        json_filename = json_filename or (data_filename.rpartition(".")[0] + ".json")
        data = {
            self.filename
            or os.path.split(data_filename)[1]: self.read_file(data_filename)
        }
        json.dump(data, open(json_filename, "wt"), indent=4)

    def load(self, json_filename: str = None, data_filename: str = None):
        data_filename = data_filename or self.filename
        json_filename = json_filename or (data_filename.rpartition(".")[0] + ".json")
        records = json.load(open(json_filename, "rt"))[
            self.filename or os.path.split(data_filename)[1]
        ]
        self.write_file(records, data_filename)

    def read_file(self, filename: str) -> List[Dict]:
        with open(filename, "rb") as buffer:
            records = self.read(buffer)
        return records

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = self.read_records(self.definition, buffer, record_count)
        return records

    def write_file(self, records: List[Dict], filename: str):
        with open(filename, "wb") as buffer:
            buffer.write(self.write(records))

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        string_bytes += self.write_records(self.definition, records)

        return string_bytes

    @classmethod
    def apply_constants(cls, records: List[Dict]) -> None:
        if not cls.constants:
            return

        for r in records:
            r.update(**cls.constants)

    @classmethod
    def remove_constants(cls, records: List[Dict]) -> None:
        if not cls.constants:
            return

        for r in records:
            for c in cls.constants:
                if c in r:
                    del r[c]

    @classmethod
    def write_records(cls, definition: Dict, records: List[Dict]) -> bytes:
        byte_string = bytes()
        cls.apply_constants(records)

        for record in records:
            byte_string += cls.write_record(definition, record)

        return byte_string

    @classmethod
    def read_records(
        cls, definition: Dict, buffer: BinaryIO, record_count: int
    ) -> List[Dict]:
        records = []

        for i in range(record_count):
            record = cls.read_record(definition, buffer)
            record["__order"] = i
            records.append(record)

        cls.remove_constants(records)

        return records

    @classmethod
    def read_record(cls, definition: Dict, buffer: BinaryIO) -> Dict[str, Any]:
        location = buffer.tell()
        record = {}
        for field, field_type in definition.items():
            value = cls.read_field(field_type, buffer, location)

            if not field_type.startswith("null"):
                record[field] = value

        return record

    @classmethod
    def write_record(cls, definition: Dict, record: Dict) -> bytes:
        byte_string = bytes()
        for field, field_type in definition.items():
            cls.write_field(field_type, record[field])

        return byte_string

    @classmethod
    def read_field(
        cls, field_type: str, buffer: BinaryIO, location: int = None
    ) -> Union[int, str, bytes]:
        value = None

        if field_type.startswith("int"):
            value = cls.read_int(
                buffer.read(int(field_type.replace("int", ""))), signed=True
            )
        elif field_type.startswith("uint"):
            value = cls.read_int(
                buffer.read(int(field_type.replace("uint", ""))), signed=False
            )
        elif field_type in ["string_len_prefix"]:
            value = cls.read_string_length(buffer)
        elif field_type in ["string_null_term"]:
            value = cls.read_string_null_term(buffer)
        elif field_type in ["guid"]:
            value = cls.read_guid_bytes(buffer.read(8))
        elif field_type in ["series_guid"]:
            value = cls.read_series_bytes(buffer.read(4))
        elif field_type.startswith("bytes"):
            value = buffer.read(int(field_type.replace("bytes", "")))
        elif field_type in ["pointer"]:
            value = cls.read_int(buffer.read(4), signed=False) + location
        elif field_type.startswith("null"):
            value = buffer.read(int(field_type.replace("null", "")))

        return value

    @classmethod
    def write_field(cls, field_type: str, value: Union[int, str, bytes]) -> bytes:
        byte_string = bytes()
        if field_type.startswith("int"):
            byte_string += cls.write_int(value, int(field_type[-1]), signed=True)
        elif field_type.startswith("uint"):
            byte_string += cls.write_int(value, int(field_type[-1]), signed=False)
        elif field_type in ["len_string"]:
            byte_string += cls.write_string_length(value)
        elif field_type in ["null_string"]:
            byte_string += cls.write_string_null_term(value)
        elif field_type in ["guid"]:
            byte_string += cls.write_guid_bytes(value)
        elif field_type in ["series_guid"]:
            byte_string += cls.write_series_bytes(value)
        elif field_type.startswith("bytes"):
            byte_length = int(field_type.replace("bytes", ""))
            byte_string += (value + ("\x00" * byte_length))[0:byte_length]
        elif field_type in ["pointer"]:
            byte_string += cls.write_int(value, 4, signed=False)
        elif field_type.startswith("null"):
            byte_length = int(field_type.replace("null", ""))
            byte_string += "\x00" * byte_length

        return byte_string
