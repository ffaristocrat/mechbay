from typing import List, Dict, BinaryIO

from .data import GundamDataFile


class TBLData(GundamDataFile):
    pass


class StringTBL(GundamDataFile):
    header = b"\x00\x00\x00\x00\x00\x01\x01\x00"

    def _write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += int(record_count).to_bytes(4, byteorder="little")

        string_start = 12 + (record_count * 8)

        # We pad out a 16 byte row with null bytes
        # after the index
        padding = 16 - (string_start % 16)
        string_start += padding

        for record in records:
            string_bytes += int(record["index"]).to_bytes(4, byteorder="little")
            string_bytes += int(string_start).to_bytes(4, byteorder="little")
            string_start += len(record["string"].encode("utf-8")) + 1

        string_bytes += b"\x00" * padding

        for record in records:
            string_bytes += record["string"].encode("utf-8") + b"\x00"

        return string_bytes

    def _read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "index": int.from_bytes(buffer.read(4), byteorder="little"),
                "pointer": int.from_bytes(buffer.read(4), byteorder="little"),
            }
            records.append(record)

        for record in records:
            record["string"] = self.read_string(buffer, record["pointer"])

        return records
