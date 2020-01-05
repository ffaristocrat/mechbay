import json
import os
from typing import List, Dict, ByteString, BinaryIO


class GundamDataFile:
    header: ByteString = None
    default_filename: str = None
    record_count_length: int = 4

    def __init__(self, filename: str = None, header: ByteString = None,
                 record_count_length: int = None):
        self.filename = filename or self.default_filename
        self._start_pos = 0
        if header:
            self.header = header
        if record_count_length is not None:
            self.record_count_length = record_count_length

    @staticmethod
    def read_unit_bytes(byte_string: bytes) -> str:
        series = int.from_bytes(byte_string[0:2], byteorder="little")
        gundam = chr(byte_string[2])
        unit_type = chr(byte_string[4])
        spec = byte_string[5]
        model = int.from_bytes(byte_string[6:8], byteorder="little")

        unit_id = f"{gundam}{series:04}{unit_type}{model:03}{spec:02}"

        return unit_id

    @staticmethod
    def write_unit_bytes(unit_string: str) -> bytes:
        print(unit_string)
        unit_bytes = bytes()
        unit_bytes += int(unit_string[1:5]).to_bytes(2, byteorder="little")
        unit_bytes += bytes(unit_string[0], encoding="utf-8")
        unit_bytes += b"\x00"
        unit_bytes += bytes(unit_string[5], encoding="utf-8")
        unit_bytes += int(unit_string[9:11]).to_bytes(1, byteorder="little")
        unit_bytes += int(unit_string[6:9]).to_bytes(2, byteorder="little")

        return unit_bytes

    def read_string(self, buffer: BinaryIO, offset: int) -> str:
        all_bytes = bytes()
        buffer.seek(offset + self._start_pos)
        while True:
            char = buffer.read(1)
            if char == b"\x00":
                break
            all_bytes += char
        output_string = all_bytes.decode("utf-8")

        return output_string

    def read_header(self, buffer: BinaryIO) -> int:
        self._start_pos = buffer.tell()
        header = buffer.read(len(self.header))
        assert header == self.header
        record_count = int.from_bytes(
            buffer.read(self.record_count_length), byteorder="little"
        )
        return record_count

    def dump(self, filename: str = None, output_filename: str = None):
        filename = filename or self.filename
        output_filename = output_filename or (filename.rpartition(".")[0] + ".json")
        data = {self.filename or os.path.split(filename)[1]: self.read_file(filename)}
        json.dump(data, open(output_filename, "wt"), indent=4)

    def read_file(self, filename: str) -> List[Dict]:
        with open(filename, "rb") as buffer:
            records = self.read(buffer)
        return records

    def read(self, buffer: BinaryIO) -> List[Dict]:
        raise NotImplementedError

    def write_file(self, records: List[Dict], filename: str):
        with open(filename, "wb") as buffer:
            buffer.write(self.write(records))

    def write(self, records: List[Dict]) -> bytes:
        raise NotImplementedError
