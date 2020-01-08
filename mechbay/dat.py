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
            stage_id = int.from_bytes(buffer.read(4), byteorder="little")
            length = int.from_bytes(buffer.read(1), byteorder="little")
            effect_id = buffer.read(length).decode(encoding="utf-8")

            record = {"effect_id": stage_id, "effect_name": effect_id}
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
            length = int.from_bytes(buffer.read(1), byteorder="little")
            unit_id = buffer.read(length).decode(encoding="utf-8")
            length = int.from_bytes(buffer.read(1), byteorder="little")
            weapon_id = buffer.read(length).decode(encoding="utf-8")
            record = {"unit_id": unit_id, "weapon_id": weapon_id}
            records.append(record)

        for record in records:
            record["values"] = [
                int.from_bytes(buffer.read(1), byteorder="little") for _ in range(4)
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
