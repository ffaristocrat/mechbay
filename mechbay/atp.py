from typing import List, Dict, BinaryIO

from .data import GundamDataFile


class CockpitBgTable(GundamDataFile):
    filename = "cockpit_bg_table.atp"
    header = b"\xC2\x3E\x10\x0A"
    record_count_length = 0

    def _write(self, records: List[Dict]) -> bytes:
        pass

    def _read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


