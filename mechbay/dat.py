from typing import List, Dict, BinaryIO

from .data import GundamDataFile


class DlcList(GundamDataFile):
    default_filename = "DlcList.dat"
    header = b"\x08\x80\x80\x80\x08\x12\x04\x08"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
            }
            records.append(record)

        return records


class EffectList(GundamDataFile):
    default_filename = "effectList.dat"
    header = b"\x4C\x45\x4D\x54"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "effect_id": self.read_int(buffer.read(4)),
                "effect_name": self.read_string_length(buffer),
            }
            records.append(record)

        return records


class MapWeaponList(GundamDataFile):
    default_filename = "mapWeaponList.dat"
    header = b"\x57\x4D\x4D\x54"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "unit_id": self.read_string_length(buffer),
                "weapon_id": self.read_string_length(buffer),
            }
            records.append(record)

        for record in records:
            record["values"] = [
                self.read_int(buffer.read(1)) for _ in range(4)
            ]

        return records


class MovieList(GundamDataFile):
    default_filename = "movieList.dat"
    header = b"\x4C\x4D\x4D\x54"
    record_count_length = 2

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
            }
            records.append(record)

        return records


class PowerUpList(GundamDataFile):
    default_filename = "powerUpList.dat"
    header = b"\x44\x4C\x55\x50"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
            }
            records.append(record)

        return records


class ScoutMessageId(GundamDataFile):
    default_filename = "scoutMessageid.dat"
    header = b"\x4D\x53\x4D\x54"
    record_count_length = 2

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "string": self.read_string_length(buffer),
                "value1": self.read_int(buffer.read(1)),
                "value2": self.read_int(buffer.read(1)),
                "value3": self.read_int(buffer.read(1)),
            }
            records.append(record)

        return records


class SteamDlcGroupList(GundamDataFile):
    default_filename = "SteamDlcGroupList.dat"
    header = b""

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
            }
            records.append(record)

        return records
