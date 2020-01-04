from typing import List, Dict, BinaryIO

from .data import GundamDataFile


class AbilitySpecList(GundamDataFile):
    default_filename = "AbilitySpecList.cdb"
    header = b"\x4C\x4C\x42\x41\x01\x00\x0C\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class ActAbilityEffectList(GundamDataFile):
    default_filename = "ActAbilityEffectList.cdb"
    header = b"\x4C\x45\x41\x41\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "unit_id": self.read_unit_bytes(buffer.read(8)),
                "values": [
                    int.from_bytes(buffer.read(4), byteorder="little") for _ in range(2)
                ],
            }
            records.append(record)

        return records


class BattleBgList(GundamDataFile):
    default_filename = "BattleBgList.cdb"
    header = b"\x47\x42\x54\x42\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "pointer": int.from_bytes(buffer.read(4), byteorder="little")
                + len(self.header)
                + 4
            }

        for record in records:
            record["bg_name"] = self.read_string(buffer, record["pointer"])

        return records


class CellAttributeList(GundamDataFile):
    default_filename = "CellAttributeList.cdb"
    header = b"\x4C\x54\x41\x43\x00\x00\x03\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "pointer": int.from_bytes(buffer.read(4), byteorder="little"),
                "values": [
                    int.from_bytes(buffer.read(1), byteorder="little", signed=False)
                    for _ in range(20)
                ],
            }
            records.append(record)

        return records


class CharacterConversionList(GundamDataFile):
    default_filename = "CharacterConversionList.cdb"
    header = b"\x4C\x56\x43\x43\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            records.append(
                {
                    "first_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "second_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "index": int.from_bytes(buffer.read(4), byteorder="little"),
                }
            )

        return records


class CharacterGrowthList(GundamDataFile):
    default_filename = "CharacterGrowthList.cdb"
    header = b"\x52\x47\x48\x43\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class CharacterSpecList(GundamDataFile):
    default_filename = "CharacterSpecList.cdb"
    header = b"\x4C\x53\x48\x43\x00\x00\x07\x02"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class CreditBgmList(GundamDataFile):
    default_filename = "CreditBgmList.cdb"
    header = b""

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class DatabaseCalculation(GundamDataFile):
    # The source file is misspelled
    default_filename = "DatabaseCalcuclation.cdb"
    header = b"\x43\x4C\x41\x43\x00\x00\x06\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class GalleryMovieList(GundamDataFile):
    default_filename = "GalleryMovieList.cdb"
    header = b"\x4C\x56\x4D\x47\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class GetUnitList(GundamDataFile):
    default_filename = "GetUnitList.cdb"
    header = b"\x00\x00\x00\x01\x4C\x54\x55\x47"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "unit_id": self.read_unit_bytes(buffer.read(8)),
                "cost": int.from_bytes(buffer.read(4), byteorder="little"),
            }
            records.append(record)

        return records


class GroupSendingMissionList(GundamDataFile):
    default_filename = "GroupSendingMissionList.cdb"
    header = b"\x00\x00\x00\x01\x4C\x54\x55\x47"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            record = {
                "unit_id": self.read_unit_bytes(buffer.read(8)),
                "cost": int.from_bytes(buffer.read(4), byteorder="little"),
            }
            records.append(record)

        return records


class MachineConversionList(GundamDataFile):
    default_filename = "MachineConversionList.cdb"
    header = b"\x4C\x56\x43\x43\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            records.append(
                {
                    "first_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "second_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "index": int.from_bytes(buffer.read(4), byteorder="little"),
                }
            )

        return records


class MachineDesignList(GundamDataFile):
    default_filename = "MachineDesignList.cdb"
    header = b"\x49\x53\x44\x4D\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            records.append(
                {
                    "first_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "second_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "result_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "index": int.from_bytes(buffer.read(4), byteorder="little"),
                }
            )

        return records


class MachineDevelopmentList(GundamDataFile):
    default_filename = "MachineDevelopmentList.cdb"
    header = b"\x56\x45\x44\x4D\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            unit_id = self.read_unit_bytes(buffer.read(8))
            # The pointer is garbage so we don't use it.
            pointer = int.from_bytes(buffer.read(4), byteorder="little")
            index = int.from_bytes(buffer.read(2), byteorder="little")
            child_count = int.from_bytes(buffer.read(2), byteorder="little")

            record = {
                "unit_id": unit_id,
                "index": index,
                "child_count": child_count,
                "children": [],
            }
            records.append(record)

        # Proceed immediately into reading the next block
        for record in records:
            for _ in range(record["child_count"]):
                child = {
                    "unit_id": self.read_unit_bytes(buffer.read(8)),
                    "level": int.from_bytes(buffer.read(4), byteorder="little"),
                }
                record["children"].append(child)

        return records


class MachineGrowthList(GundamDataFile):
    default_filename = "MachineGrowthList.cdb"
    header = b"\x4C\x53\x43\x4D\x03\x00\x05\x02"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class MapTypes(GundamDataFile):
    default_filename = "MapTypes.cdb"
    header = b"\x02\x00\x05\x01\x50\x59\x54\x4D"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class MyCharacterConfigurations(GundamDataFile):
    default_filename = "MyCharacterConfigurations.cdb"
    header = b"\x43\x48\x43\x4D\x01\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class PersonalMachineList(GundamDataFile):
    default_filename = "PersonalMachineList.cdb"
    header = b"\x4C\x43\x4D\x50\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class QuestList(GundamDataFile):
    default_filename = "QuestList.cdb"
    header = b"\x4C\x54\x45\x51\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class RangeDataList(GundamDataFile):
    default_filename = "RangeDataList.cdb"
    header = b"\x4C\x47\x4E\x52\x01\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []
        # unknown, long int = 16?
        # _ = int.from_bytes(buffer.read_file(4), byteorder="little")

        for _ in range(record_count):
            records.append(
                {
                    "length": int.from_bytes(buffer.read(2), byteorder="little"),
                    "mask": int.from_bytes(buffer.read(2), byteorder="little"),
                    # pointer is probably garbage
                    "pointer": int.from_bytes(buffer.read(4), byteorder="little"),
                }
            )

        for record in records:
            buffer.seek(record["pointer"] + record["length"])
            record["data"] = [
                int.from_bytes(buffer.read(1), byteorder="little")
                for _ in range(record["length"])
            ]

        return records


class SeriesList(GundamDataFile):
    default_filename = "SeriesList.cdb"
    header = b"\x4C\x52\x45\x53\x01\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            logo_num = int.from_bytes(buffer.read(2), byteorder="little")
            logo_g = chr(int.from_bytes(buffer.read(2), byteorder="little"))
            logo1 = f"{logo_g}{logo_num:04}"
            logo_num = int.from_bytes(buffer.read(2), byteorder="little")
            logo_g = chr(int.from_bytes(buffer.read(2), byteorder="little"))
            logo2 = f"{logo_g}{logo_num:04}"

            record = {
                "logo1": logo1,
                "logo2": logo2,
                "index": int.from_bytes(buffer.read(2), byteorder="little"),
                # Ranges from 0-4
                "val": int.from_bytes(buffer.read(1), byteorder="little"),
                # 0 or 1
                "flag": int.from_bytes(buffer.read(1), byteorder="little"),
            }
            records.append(record)

        return records


class SeriesProfileList(GundamDataFile):
    default_filename = "SeriesProfileList.cdb"
    header = b"\x4C\x50\x52\x53\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class StageList(GundamDataFile):
    default_filename = "StageList.cdb"
    header = b"\x4C\x47\x54\x53\x00\x00\x0B\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for _ in range(record_count):
            stage_id = int.from_bytes(buffer.read(4), byteorder="little")
            logo_num = int.from_bytes(buffer.read(2), byteorder="little")
            logo_g = chr(int.from_bytes(buffer.read(2), byteorder="little"))
            req_stage_id = int.from_bytes(buffer.read(4), byteorder="little")
            record = {
                "stage_id": stage_id,
                "series_logo": f"{logo_g}{logo_num:04}",
                "req_stage_id": req_stage_id,
                "rewards": [
                    int.from_bytes(buffer.read(4), byteorder="little") for _ in range(6)
                ],
                "guest_unit_count": int.from_bytes(buffer.read(4), byteorder="little"),
                # The pointer is garbage so we don't use it.
                "pointer": int.from_bytes(buffer.read(4), byteorder="little"),
                "null": int.from_bytes(buffer.read(2), byteorder="little"),
                "index": int.from_bytes(buffer.read(2), byteorder="little"),
                "bgm": int.from_bytes(buffer.read(2), byteorder="little"),
                "movie": int.from_bytes(buffer.read(2), byteorder="little"),
                "values": [
                    int.from_bytes(buffer.read(2), byteorder="little")
                    for _ in range(24)
                ],
                "series_end": int.from_bytes(buffer.read(4), byteorder="little"),
            }
            records.append(record)

        for record in records:
            record["guest_units"] = []
            for _ in range(record["guest_unit_count"]):
                guest_unit = {
                    "unit_id": self.read_unit_bytes(buffer.read(8)),
                    "unit_count": int.from_bytes(buffer.read(4), byteorder="little"),
                }
                record["guest_units"].append(guest_unit)

        return records


class SkillAcquisitionPatternList(GundamDataFile):
    default_filename = "SkillAcquisitionPatternList.cdb"
    header = b"\x4C\x51\x41\x53\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class SpecProfileList(GundamDataFile):
    default_filename = "SpecProfileList.cdb"
    header = b"\x4C\x50\x50\x53\x00\x00\x03\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class TitleBgmList(GundamDataFile):
    default_filename = "TitleBgmList.cdb"
    header = b""

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class TutorialList(GundamDataFile):
    default_filename = "TutorialList.cdb"
    header = b"\x4F\x54\x55\x54\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class WeaponSpecList(GundamDataFile):
    default_filename = "WeaponSpecList.cdb"
    header = b"\x4C\x53\x50\x57\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []
        
        # series of data
        # followed by two small blocks
        # 8 * (value, index)
        # 31 * (value, value, index)

        return records
