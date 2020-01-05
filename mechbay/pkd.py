from typing import List, Dict, BinaryIO

from .data import GundamDataFile


class PKDArchive(GundamDataFile):
    header = b"\x20\x44\x4B\x50\x00\x01\x03\x00"

    def write(self, records: List[Dict]) -> bytes:
        padding = 64
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += int(record_count).to_bytes(4, byteorder="little")
        # Maybe number of bits for long? Always seems to 0x40000000
        string_bytes += (64).to_bytes(4, byteorder="little")

        # index size
        index_size = (record_count * 12) + sum([len(r["filename"].encode("utf-8")) + 1 for r in records])
        string_bytes += index_size.to_bytes(4, byteorder="little")

        # initial pointers
        name_start = record_count * 12
        file_start = index_size + 20
        file_start += padding - (file_start % padding)
        for record in records:
            # File pointer
            string_bytes += file_start.to_bytes(4, byteorder="little")

            # File size
            string_bytes += len(record["bytes"]).to_bytes(4, byteorder="little")
            file_start += len(record["bytes"])
            # Pad to 64 byte increments
            file_start += padding - (file_start % padding)

            # name pointer
            string_bytes += name_start.to_bytes(4, byteorder="little")
            name_start += len(record["filename"].encode("utf-8")) + 1

        for record in records:
            string_bytes += record["filename"].encode("utf-8") + b"\x00"
        string_bytes += (padding - (len(string_bytes) % padding)) * b"\x00"

        for record in records:
            string_bytes += record["bytes"]
            string_bytes += (padding - (len(string_bytes) % padding)) * b"\x00"

        return string_bytes

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
                # +20 for header bytes
                "__name_pointer":
                    int.from_bytes(buffer.read(4), byteorder="little") + 20,
            }
            records.append(record)

        for record in records:
            record["filename"] = self.read_string(buffer, record["__name_pointer"])

        for record in records:
            buffer.seek(record["__file_pointer"])
            record["bytes"] = buffer.read(record["__file_size"])

        return records
