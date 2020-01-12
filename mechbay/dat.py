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


class Stage(GundamDataFile):
    default_filename = "Stage.dat"
    header = b"\x49\x53\x4D\x54\x2F\x01\x00\x00"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []
        
        #incomplete mess

        for i in range(record_count):
            values = [self.read_int(buffer.read(1)) for _ in range(2)]
            size_x = self.read_int(buffer.read(1))
            size_y = self.read_int(buffer.read(1))
            print(size_x, size_y)
            record = {
                "__order": i,
                "values": values,
                "size_x": size_x,
                "size_y": size_y,
                "minimap": self.read_string_length(buffer),
                "background": self.read_string_length(buffer),
                "values2": [self.read_int(buffer.read(1), signed=True) for _ in range(36)],
                "map_tiles": [
                    [self.read_int(buffer.read(4)) for x in range(size_x)]
                    for y in range(size_y)
                ],
                "values3": [self.read_int(buffer.read(1)) for _ in
                    range(59)],
                "bytething": buffer.read(self.read_int(buffer.read(1))),
                "null": buffer.read(2),
                "bytething2": buffer.read(self.read_int(buffer.read(1))),
                "null2": buffer.read(1),
                "unk": self.read_int(buffer.read(1)),
                "bytething3": buffer.read(self.read_int(buffer.read(1))),
                "null3": buffer.read(1),
                "values4": [self.read_int(buffer.read(1)) for _ in range(4)],
                "bytething4": buffer.read(self.read_int(buffer.read(1))),
                
                "valuesz": [self.read_int(buffer.read(1)) for _ in
                    range(8)],
    
            }
            records.append(record)

        return records
