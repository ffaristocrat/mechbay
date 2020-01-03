from typing import List, Dict, BinaryIO

from .data import GundamDataFile


class PKDArchive(GundamDataFile):
    header = b"\x20\x44\x4B\x50\x00\x01\x03\x00"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        # Maybe number of bits for long? Always seems to 0x40000000
        long_size = int.from_bytes(buffer.read(4), byteorder="little")
        # Size of the index block which we don't care about tbh
        index_size = int.from_bytes(buffer.read(4), byteorder="little")

        for _ in range(record_count):
            record = {
                "__file_pointer": int.from_bytes(buffer.read(4), byteorder="little"),
                "__file_size": int.from_bytes(buffer.read(4), byteorder="little"),
                "__name_pointer": int.from_bytes(buffer.read(4), byteorder="little"),
            }
            records.append(record)

        for record in records:
            record["filename"] = self.read_string(buffer, record["__name_pointer"] + 20)

        for record in records:
            buffer.seek(record["__file_pointer"])
            record["bytes"] = buffer.read(record["__file_size"])

        return records
