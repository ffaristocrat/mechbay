import os
from typing import List, Dict, BinaryIO

from .data import GundamDataFile

LANGUAGES = ["english", "japanese", "korean", "schinese", "tchinese/hk", "tchinese/tw"]


class TBLData(GundamDataFile):
    pass


class StringTBL(GundamDataFile):
    header = b"\x54\x52\x54\x53\x00\x01\x01\x00"

    definition = {"index": "uint:4", "string": "uint:4"}

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        string_start = len(string_bytes) + (record_count * 8)

        # We pad out a 16 byte row with null bytes
        # after the index
        padding = 16 - (string_start % 16)
        string_start += padding

        for record in records:
            string_bytes += self.write_int(record.get("index", 0), 4)
            string_bytes += self.write_int(string_start, 4)

            string_start += len(record["string"].encode("utf-8")) + 1

        string_bytes += b"\x00" * padding

        for record in records:
            string_bytes += self.write_string_null_term(record["string"])

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = self.read_records(self.definition, buffer, record_count)

        for record in records:
            # Pointers in StringTBLs work slightly differently
            record["string"] = self.read_string_null_term(buffer, record["string"])

        return records


class Localisation:
    def __init__(self, data_path: str, filename: str):
        self.data_path = data_path
        self.filename = filename

    def read_file(self) -> List[Dict]:
        records = None
        for language in LANGUAGES:
            localisation = self.read_localization(language)
            if not records:
                records = localisation[:]

            if len(records) != len(localisation):
                raise ValueError(f"Length of {language} string table does not match")

            for r, l in zip(records, localisation):
                if r["index"] != l["index"]:
                    raise ValueError(f"Index field in {language} does not match")
                r[language] = l["string"]

        for r in records:
            del r["string"]

        return records

    def write_file(self, records: List[Dict], output_data_path: str = None):
        for l in LANGUAGES:
            # try to read language
            # fall back to english then japanese
            # then put in an error
            localized = [
                {
                    "string": r.get(
                        l, r.get("english", r.get("japanese", "missing string"))
                    ),
                    "index": r["index"],
                }
                for r in records
            ]
            self.write_localization(localized, l, output_data_path)

    def write_localization(
        self, records: List[Dict], language: str, output_data_path: str = None
    ):
        full_path = os.path.join(
            output_data_path or self.data_path,
            language,
            self.filename,
        )
        StringTBL().write_file(records, full_path)

    def read_localization(
        self, language: str, input_data_path: str = None
    ) -> List[Dict]:
        full_path = os.path.join(
            input_data_path or self.data_path,
            language,
            self.filename,
        )
        records = StringTBL().read_file(full_path)
        return records


class VoiceTable(StringTBL):
    header = b"\x54\x52\x54\x53\x00\x01\x01\x00"

    def write(self, records: List[Dict]) -> bytes:
        for r in records:
            r["string"] = ",".join([r["voice_id"], r["val1"], r["val2"], r["val3"]])
        byte_string = super().write(records)

        return byte_string

    def read(self, buffer: BinaryIO) -> List[Dict]:
        records = super().read(buffer)

        for record in records:
            unpack = record.pop("string").split(",")
            record["voice_id"] = unpack[0]
            record["val1"] = int(unpack[1])
            record["val2"] = int(unpack[2])
            record["val3"] = int(unpack[3])

        return records


class Weapon(GundamDataFile):
    header = b"\x54\x4E\x50\x57\x00\x00\x02\x00"
    default_filename = "weapon.tbl"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        """ I think this might be for display purposes only """

        weapon_count = self.read_header(buffer)
        record_count = self.read_int(buffer.read(4))
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "unit_id": self.read_int(buffer.read(4)),
                "weapons_count": self.read_int(buffer.read(4)),
                "__weapons_offset": self.read_int(buffer.read(4)),
                "weapons": [],
            }
            records.append(record)
            print(record)

        # Now read the weapons
        weapons = []
        for i in range(weapon_count):
            # 80
            weapon = {
                "values": [self.read_int(buffer.read(1)) for _ in range(6)],
                "values2": [self.read_int(buffer.read(1)) for _ in range(1)],
                "values3": [self.read_int(buffer.read(1)) for _ in range(12)],
                "unit_id": self.read_int(buffer.read(4)),
                "values5": [self.read_int(buffer.read(1)) for _ in range(20)],
                "values6": [self.read_int(buffer.read(1)) for _ in range(2)],
                "values7": [self.read_int(buffer.read(1)) for _ in range(28)],
            }
            weapons.append(weapon)
            print(weapon)

        # Now read the lookup table
        lookup = StringTBL().read(buffer)
        for l in lookup:
            print(l)

        return records
