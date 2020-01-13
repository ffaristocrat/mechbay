import os
from typing import List, Dict, BinaryIO

from .data import GundamDataFile


RESIDENT = {
    "CharacterSpecList.pkd": [
        "CharacterSpecList.cdb",
        "CharacterGrowthList.cdb",
        "SkillAcquisitionPatternList.cdb",
        "MyCharacterConfigurations.cdb",
    ],
    "MachineSpecList.pkd": [
        "RangeDataList.cdb",
        "MachineGrowthList.cdb",
        "WeaponSpecList.cdb",
        "MachineSpecList.cdb",
        "MachineConversionList.cdb",
        "PersonalMachineList.cdb",
        "MachineDevelopmentList.cdb",
        "MachineDesignList.cdb",
    ],
    "MiscData.pkd": [
        "DatabaseCaluclation.cdb",
        "SeriesList.cdb",
        "GroupSendingMissionList.cdb",
        "TutorialList.cdb",
    ],
    "StageList.pkd": ["StageList.cdb", "QuestList.cdb", "GetUnitList.cdb"],
    "CellAttributeList.pkd": ["CellAttributeList.cdb", "BattleBgList.cdb"],
}


class PKDArchive(GundamDataFile):
    header = b"\x20\x44\x4B\x50\x00\x01\x03\x00"

    def write(self, records: List[Dict]) -> bytes:
        padding = 64
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)
        # Maybe number of bits for long? Always seems to 0x40000000
        string_bytes += self.write_int(64, 4)

        # index size
        index_size = (record_count * 12) + sum(
            [len(r["filename"].encode("utf-8")) + 1 for r in records]
        )
        string_bytes += self.write_int(index_size, 4)

        # initial pointers
        name_start = record_count * 12
        file_start = index_size + 20
        file_start += padding - (file_start % padding)
        for record in records:
            # File pointer
            string_bytes += self.write_int(file_start, 4)

            # File size
            string_bytes += self.write_int(len(record["bytes"]), 4)
            file_start += len(record["bytes"])
            # Pad to 64 byte increments
            file_start += padding - (file_start % padding)

            # name pointer
            string_bytes += self.write_int(name_start, 4)
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
        long_size = self.read_int(buffer.read(4))
        # Size of the index block which we don't care about tbh
        index_size = self.read_int(buffer.read(4))

        for _ in range(record_count):
            record = {
                "__file_pointer": self.read_int(buffer.read(4)),
                "__file_size": self.read_int(buffer.read(4)),
                # +20 for header bytes
                "__name_pointer": self.read_int(buffer.read(4))
                + 20,
            }
            records.append(record)

        for record in records:
            record["filename"] = self.read_string_null_term(
                buffer, record["__name_pointer"]
            )

        for record in records:
            buffer.seek(record["__file_pointer"])
            record["bytes"] = buffer.read(record["__file_size"])

        return records

    def pack_files(self, filenames) -> bytes:
        records = []
        for filename in filenames:
            with open(filename, "rb") as file:
                record = {"filename": os.path.split(filename)[1], "bytes": file.read()}
                records.append(record)

        return self.write(records)
