from typing import List, Dict, BinaryIO

from .data import GundamDataFile


class CockpitBgTable(GundamDataFile):
    default_filename = "cockpit_bg_table.atp"
    header = b"\xC2\x3E\x10\x0A"
    record_count_length = 0

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records
