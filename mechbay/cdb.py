from typing import List, Dict, BinaryIO

from .data import GundamDataFile

CHARACTER_STATS = [
    "cmd",
    "rng",
    "mel",
    "def",
    "rct",
    "awk",
    "aux",
    "com",
    "nav",
    "mnt",
    "chr",
]


class AbilitySpecList(GundamDataFile):
    default_filename = "AbilitySpecList.cdb"
    header = b"\x4C\x4C\x42\x41\x01\x00\x0C\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records


class ActAbilityEffectList(GundamDataFile):
    default_filename = "ActAbilityEffectList.cdb"
    header = b"\x4C\x45\x41\x41\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)

        for record in records:
            string_bytes += self.write_unit_bytes(record["unit_id"])
            for v in record["values"]:
                string_bytes += self.write_int(v, 4)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "unit_id": self.read_unit_bytes(buffer.read(8)),
                "values": [self.read_int(buffer.read(4)) for _ in range(2)],
            }
            records.append(record)

        return records


class BattleBgList(GundamDataFile):
    default_filename = "BattleBgList.cdb"
    header = b"\x47\x42\x54\x42\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)

        # Consolidate all the bgm string ids into a set
        all_music = set()
        for r in records:
            for b in r["bg_name"]:
                all_music.add(b)
        all_music = list(all_music)

        # then calculate pointer offsets for each string
        row = {b: i for i, b in enumerate(all_music)}
        location = 0
        locations = {}
        for b, i in row.items():
            locations[b] = location
            location += len(b.encode("utf-8")) + 1
        index_size = (record_count * 16) + len(string_bytes)

        # and then assign them to the records
        for r in records:
            r["__locations"] = [locations[b] + index_size for b in r["bg_name"]]

        for record in records:
            location = len(string_bytes)
            for l in record.pop("__locations"):
                # pointers are relative to the location of the *first* pointer
                string_bytes += self.write_int(l - location, 4)

            string_bytes += self.write_int(record["value"], 4)
            location += 16

        string_bytes += b"\x00".join([b.encode("utf-8") for b in all_music]) + b"\x00"

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            location = buffer.tell()
            record = {
                "__order": i,
                "__pointers": [
                    location + self.read_int(buffer.read(4)) for _ in range(3)
                ],
                "value": self.read_int(buffer.read(4)),
            }
            records.append(record)

        for record in records:
            pointers = record.pop("__pointers")
            record["bg_name"] = [
                self.read_string_null_term(buffer, p) for p in pointers
            ]

        return records


class CellAttributeList(GundamDataFile):
    default_filename = "CellAttributeList.cdb"
    header = b"\x4C\x54\x41\x43\x00\x00\x03\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            location = buffer.tell()
            record = {
                "__order": i,
                "__pointer": self.read_int(buffer.read(4)) + location,
                "values": [self.read_int(buffer.read(1)) for _ in range(20)],
            }
            records.append(record)

        for record in records:
            record["data"] = self.read_string_null_term(buffer, record.pop("__pointer"))

        return records


class CharacterConversionList(GundamDataFile):
    default_filename = "CharacterConversionList.cdb"
    header = b"\x4C\x56\x43\x43\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)

        for record in records:
            string_bytes += self.write_unit_bytes(record["character_id"])
            string_bytes += self.write_unit_bytes(record["new_character_id"])
            string_bytes += self.write_int(record["change_type"], 4)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            records.append(
                {
                    "__order": i,
                    "character_id": self.read_unit_bytes(buffer.read(8)),
                    "new_character_id": self.read_unit_bytes(buffer.read(8)),
                    "change_type": self.read_int(buffer.read(4)),
                }
            )

        return records


class CharacterGrowthList(GundamDataFile):
    default_filename = "CharacterGrowthList.cdb"
    header = b"\x52\x47\x48\x43\x00\x00\x00\x01"
    level_ups = 98
    profile_constant = 332

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)

        # make a unique list of stat increases
        # replace their entries with the index to those increases
        # then write both blocks

        level_up_stats = []
        for record in records:
            assert len(record["level_up_stats"]) == self.level_ups
            record["__stats_strings"] = []

            # have to convert to a string for the set
            for level in record["level_up_stats"]:
                stat_string = ",".join([str(int(level[s])) for s in CHARACTER_STATS])
                if stat_string not in level_up_stats:
                    level_up_stats.append(stat_string)
                record["__stats_strings"].append(stat_string)

        level_up_stats = list(level_up_stats)
        stat_count = len(level_up_stats)
        string_bytes += self.write_int(stat_count, 4)

        pointer = (record_count * 2 * (self.level_ups + 1)) + 20
        string_bytes += self.write_int(pointer, 4)

        index_lookup = {s: i for i, s in enumerate(level_up_stats)}
        for record in records:
            string_bytes += self.write_int(self.profile_constant, 2)
            for s in record.pop("__stats_strings"):
                string_bytes += self.write_int(index_lookup[s], 2)

        for stats in level_up_stats:
            for s in stats.split(","):
                string_bytes += self.write_int(int(s), 1)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        stat_count = self.read_int(buffer.read(4))
        pointer = self.read_int(buffer.read(4))

        records = []
        level_up_stats = []

        # characters have an index to one of these profiles
        # each profile has 98 indexes to a list of stats
        # the stats list states the increase of each stat

        for i in range(record_count):
            # first value is always 332
            assert self.read_int(buffer.read(2)) == self.profile_constant
            record = {
                "__order": i,
                "__stats_index": [
                    self.read_int(buffer.read(2)) for _ in range(self.level_ups)
                ],
            }
            records.append(record)

        buffer.seek(pointer)
        for i in range(stat_count):
            # 11 byte blocks
            level_up_stat = {
                stat: self.read_int(buffer.read(1)) for stat in CHARACTER_STATS
            }
            level_up_stats.append(level_up_stat)

        for record in records:
            record["level_up_stats"] = [
                level_up_stats[stat_index] for stat_index in record.pop("__stats_index")
            ]

        return records


class CharacterSpecList(GundamDataFile):
    default_filename = "CharacterSpecList.cdb"
    header = b"\x4C\x53\x48\x43\x00\x00\x07\x02"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        unknown1 = self.read_int(buffer.read(4))
        pointer1 = self.read_int(buffer.read(4))
        pointer2 = self.read_int(buffer.read(4))
        unknown2 = self.read_int(buffer.read(4))

        print(unknown1, unknown2)

        # block 1
        # 112 bytes per record
        # block 2
        # 184 byte per record
        # block 3
        # 1 byte per record?

        for i in range(record_count):
            record = {
                "__order": i,
                "unit1": self.read_unit_bytes(buffer.read(8)),
                "unit2": self.read_unit_bytes(buffer.read(8)),
                "unit3": self.read_unit_bytes(buffer.read(8)),
                "unkonwn2": self.read_int(buffer.read(2), signed=True),
                "unknown": self.read_int(buffer.read(2), signed=True),
                # in language/*/CharacterSpecList.tbl
                "name_index": self.read_int(buffer.read(2), signed=True),
                "unknown3": self.read_int(buffer.read(2), signed=True),
                "stats": {
                    s: self.read_int(buffer.read(2), signed=True)
                    for s in CHARACTER_STATS
                },
                "unknown6": self.read_int(buffer.read(2), signed=True),
                "unknown7": self.read_int(buffer.read(2), signed=True),
                # in resident/CharacterGrowth.cdb
                "growth_profile": self.read_int(buffer.read(2), signed=True),
                "values1": [
                    self.read_int(buffer.read(2), signed=True) for _ in range(6)
                ],
                "unit4": self.read_unit_bytes(buffer.read(8)),
                "unknown4": self.read_int(buffer.read(2), signed=True),
                "unknown5": self.read_int(buffer.read(2), signed=False),
                "values2": [
                    self.read_int(buffer.read(2), signed=True) for _ in range(5)
                ],
                "values3": [
                    self.read_int(buffer.read(2), signed=True) for _ in range(9)
                ],
            }
            records.append(record)

        return records


class CreditBgmList(GundamDataFile):
    default_filename = "CreditBgmList.cdb"
    header = b""

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

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

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records


class GalleryMovieList(GundamDataFile):
    default_filename = "GalleryMovieList.cdb"
    header = b"\x4C\x56\x4D\x47\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records


class GetUnitList(GundamDataFile):
    default_filename = "GetUnitList.cdb"
    header = b"\x00\x00\x00\x01\x4C\x54\x55\x47"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += int(record_count).to_bytes(4, byteorder="little")

        for record in records:
            string_bytes += self.write_unit_bytes(record["unit_id"])
            string_bytes += int(record["score_cost"]).to_bytes(4, byteorder="little")

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "unit_id": self.read_unit_bytes(buffer.read(8)),
                "score_cost": self.read_int(buffer.read(4)),
            }
            records.append(record)

        return records


class GroupSendingMissionList(GundamDataFile):
    default_filename = "GroupSendingMissionList.cdb"
    header = b"\x4C\x53\x50\x47\x00\x00\x07\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        unknown = self.read_int(buffer.read(4))
        unknown = self.read_int(buffer.read(4))
        pointer = self.read_int(buffer.read(4))

        for i in range(record_count):
            # 92 byte records
            record = {"__order": i, "data": buffer.read(92)}
            records.append(record)

        return records


class MachineConversionList(GundamDataFile):
    default_filename = "MachineConversionList.cdb"
    header = b"\x56\x4E\x43\x4D\x00\x00\x02\x01"

    conversion_types = {
        19: "",
        16: "transform",
        2: "refit_1",
        3: "refit_2",
        4: "refit_3",
        5: "",
        6: "",
        8: "",
    }

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += int(record_count).to_bytes(4, byteorder="little")

        for record in records:
            string_bytes += self.write_unit_bytes(record["unit_id"])
            string_bytes += self.write_unit_bytes(record["transform_unit_id"])
            string_bytes += self.write_int(record["conversion_type_id"], 4)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "unit_id": self.read_unit_bytes(buffer.read(8)),
                "transform_unit_id": self.read_unit_bytes(buffer.read(8)),
                "conversion_type_id": self.read_int(buffer.read(4)),
            }
            record["conversion_type"] = self.conversion_types[
                record["conversion_type_id"]
            ]

            records.append(record)

        return records


class MachineDesignList(GundamDataFile):
    default_filename = "MachineDesignList.cdb"
    header = b"\x49\x53\x44\x4D\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += int(record_count).to_bytes(4, byteorder="little")

        for record in records:
            string_bytes += self.write_unit_bytes(record["first_unit_id"])
            string_bytes += self.write_unit_bytes(record["second_unit_id"])
            string_bytes += self.write_unit_bytes(record["result_unit_id"])
            string_bytes += int(record["index"]).to_bytes(4, byteorder="little")

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            records.append(
                {
                    "__order": i,
                    "first_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "second_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "result_unit_id": self.read_unit_bytes(buffer.read(8)),
                    "index": self.read_int(buffer.read(4)),
                }
            )

        return records


class MachineDevelopmentList(GundamDataFile):
    default_filename = "MachineDevelopmentList.cdb"
    header = b"\x56\x45\x44\x4D\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += int(record_count).to_bytes(4, byteorder="little")

        child_start = len(string_bytes) + (record_count * 16)
        for record in records:
            pointer = child_start - len(string_bytes)
            child_count = len(record["children"])
            string_bytes += self.write_unit_bytes(record["unit_id"])
            string_bytes += int(pointer).to_bytes(4, byteorder="little")
            string_bytes += int(record["index"]).to_bytes(4, byteorder="little")
            string_bytes += int(child_count).to_bytes(4, byteorder="little")
            child_start += child_count * 12

        for record in records:
            for child in record["children"]:
                string_bytes += self.write_unit_bytes(child["unit_id"])
                string_bytes += int(child["level"]).to_bytes(4, byteorder="little")

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            location = buffer.tell()
            unit_id = self.read_unit_bytes(buffer.read(8))
            # Pointer is relative to the start of this index record
            pointer = self.read_int(buffer.read(4))
            index = self.read_int(buffer.read(2))
            child_count = self.read_int(buffer.read(2))

            record = {
                "__order": i,
                "__pointer": pointer + location,
                "unit_id": unit_id,
                "index": index,
                "__child_count": child_count,
                "children": [],
            }
            records.append(record)

        # Proceed immediately into reading the next block
        for record in records:
            buffer.seek(record.pop("__pointer"))
            for _ in range(record.pop("__child_count")):
                child = {
                    "unit_id": self.read_unit_bytes(buffer.read(8)),
                    "level": self.read_int(buffer.read(4)),
                }
                record["children"].append(child)

        return records


class MachineGrowthList(GundamDataFile):
    default_filename = "MachineGrowthList.cdb"
    header = b"\x00\x00\x01\x01\x52\x47\x43\x4D"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i
            }
            records.append(record)

        return records


class MachineSpecList(GundamDataFile):
    default_filename = "MachineSpecList.cdb"
    header = b"\x4C\x53\x43\x4D\x03\x00\x05\x02"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        unit_count = self.read_header(buffer)
        records = []
        units = []
        value1 = self.read_int(buffer.read(4))
        value2 = self.read_int(buffer.read(4))
        value3 = self.read_int(buffer.read(4))
        value4 = self.read_int(buffer.read(4))
        value5 = self.read_int(buffer.read(4))

        for i in range(unit_count):
            # 108 byte chunk
            unit = {
                "__order": i,
                "unit_id1": self.read_unit_bytes(buffer.read(8)),
                "unit_id2": self.read_unit_bytes(buffer.read(8)),
                "unit_id3": self.read_unit_bytes(buffer.read(8)),
                "cost?": self.read_int(buffer.read(4)),
                "index1": self.read_int(buffer.read(2)),
                "index2": self.read_int(buffer.read(2)),
                "index3": self.read_int(buffer.read(2)),
                "values2": [self.read_int(buffer.read(2)) for _ in range(20)],
                "values1": [
                    self.read_int(buffer.read(1), signed=True) for _ in range(34)
                ],
            }
            records.append(unit)

        return records


class MapTypes(GundamDataFile):
    default_filename = "MapTypes.cdb"
    header = b"\x02\x00\x05\x01\x50\x59\x54\x4D"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records


class MyCharacterConfigurations(GundamDataFile):
    default_filename = "MyCharacterConfigurations.cdb"
    header = b"\x43\x48\x43\x4D\x01\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records


class PersonalMachineList(GundamDataFile):
    default_filename = "PersonalMachineList.cdb"
    header = b"\x4C\x43\x4D\x50\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)

        for record in records:
            string_bytes += self.write_unit_bytes(record["unit_id"])
            string_bytes += self.write_unit_bytes(record["pilot_id"])
            string_bytes += self.write_unit_bytes(record["custom_unit_id"])

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "unit_id": self.read_unit_bytes(buffer.read(8)),
                "pilot_id": self.read_unit_bytes(buffer.read(8)),
                "custom_unit_id": self.read_unit_bytes(buffer.read(8)),
            }
            records.append(record)

        return records


class QuestList(GundamDataFile):
    default_filename = "QuestList.cdb"
    header = b"\x4C\x54\x45\x51\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

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

        for i in range(record_count):
            location = buffer.tell()
            records.append(
                {
                    "__order": i,
                    "length": self.read_int(buffer.read(2)),
                    "mask": self.read_int(buffer.read(2)),
                    # pointer is probably garbage
                    "__pointer": self.read_int(buffer.read(4)) + location,
                }
            )

        for record in records:
            buffer.seek(record.pop("pointer"))
            record["values"] = [
                self.read_int(buffer.read(1)) for _ in range(record["length"])
            ]

        return records


class SeriesList(GundamDataFile):
    default_filename = "SeriesList.cdb"
    header = b"\x4C\x52\x45\x53\x01\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += record_count.to_bytes(4, byteorder="little")

        for record in records:
            string_bytes += self.write_series_bytes(record["series_logo_l"])
            string_bytes += self.write_series_bytes(record["series_logo_s"])
            string_bytes += self.write_int(record["string_index"], 2)
            string_bytes += self.write_int(record["value"], 1)
            string_bytes += self.write_int(record["flag"], 1)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "series_logo_l": self.read_series_bytes(buffer.read(4)),
                "series_logo_s": self.read_series_bytes(buffer.read(4)),
                "string_index": self.read_int(buffer.read(2)),
                # Ranges from 0-4
                "value": self.read_int(buffer.read(1)),
                # 0 or 1
                "flag": self.read_int(buffer.read(1)),
            }
            records.append(record)

        return records


class SeriesProfileList(GundamDataFile):
    default_filename = "SeriesProfileList.cdb"
    header = b"\x4C\x50\x52\x53\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()

        string_bytes += self.header
        record_count = len(records)
        string_bytes += int(record_count).to_bytes(4, byteorder="little")

        for record in records:
            string_bytes += self.write_series_bytes(record["series"])
            string_bytes += self.write_int(record["value"], 2)
            string_bytes += self.write_int(record["string_index"], 2)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "gallery": self.read_series_bytes(buffer.read(4)),
                "value": self.read_int(buffer.read(2)),
                "string_index": self.read_int(buffer.read(2)),
            }
            records.append(record)

        return records


class StageClearGetList(GundamDataFile):
    default_filename = "StageClearGetList.cdb"
    header = b"\x43\x47\x54\x53\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        string_bytes = bytes()
    
        string_bytes += self.header
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)

        units_start = len(string_bytes) + (record_count * 12)
        for record in records:
            pointer = units_start - len(string_bytes)
            unit_count = len(record["get_units"])
            string_bytes += self.write_unit_bytes(record["stage_id"])
            string_bytes += self.write_int(unit_count, 4)
            string_bytes += self.write_int(pointer, 4)
            units_start += unit_count * 8

        for record in records:
            for get_unit in record["get_units"]:
                string_bytes += self.write_unit_bytes(get_unit)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            location = buffer.tell()
            record = {
                "__order": i,
                "stage_id": self.read_int(buffer.read(4)),
                "__get_count": self.read_int(buffer.read(4)),
                "__pointer": self.read_int(buffer.read(4)) + location,
                "get_units": [],
            }
            records.append(record)

        for record in records:
            buffer.seek(record.pop("__pointer"))
            for _ in range(record.pop("__get_count")):
                record["get_units"].append(self.read_unit_bytes(buffer.read(8)))

        return records


class StageList(GundamDataFile):
    default_filename = "StageList.cdb"
    header = b"\x4C\x47\x54\x53\x00\x00\x0B\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        difficulties = ["NORMAL", "HARD", "EXTRA", "HELL"]
        SPACE = 1
        AIR = 2
        LAND = 4
        SURFACE = 8
        UNDERWATER = 16
        
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            location = buffer.tell()
            record = {
                "__order": i,
                "stage_id": self.read_int(buffer.read(4)),
                "series": self.read_series_bytes(buffer.read(4)),
                "required_stage_id": self.read_int(buffer.read(4)),
                "rewards": [self.read_int(buffer.read(4)) for _ in range(6)],
                "__units_available_count": self.read_int(buffer.read(4)),
                "__pointer": self.read_int(buffer.read(4)) + location,
                "__null": self.read_int(buffer.read(2)),
                "index": self.read_int(buffer.read(2)),
                "bgm": self.read_int(buffer.read(2)),
                "series2": self.read_int(buffer.read(2)),
                "values": [self.read_int(buffer.read(2)) for _ in range(21)],
                "values2": [self.read_int(buffer.read(1)) for _ in range(5)],
                "terrain": self.read_int(buffer.read(1)),
                "series_end": self.read_int(buffer.read(4)),
                "units_available": [],
            }
            record["terrain_space"] = 1 if record["terrain"] & SPACE else 0
            record["terrain_air"] = 1 if record["terrain"] & AIR else 0
            record["terrain_land"] = 1 if record["terrain"] & LAND else 0
            record["terrain_surface"] = 1 if record["terrain"] & SURFACE else 0
            record["terrain_underwater"] = 1 if record["terrain"] & UNDERWATER else 0
            del record["terrain"]

            records.append(record)

        for record in records:
            # available units appears to be only for informational purposes in the
            # stage screen
            buffer.seek(record.pop("__pointer"))
            for _ in range(record.pop("__units_available_count")):
                unit_available = {
                    "unit_id": self.read_unit_bytes(buffer.read(8)),
                    "available_type": self.read_int(buffer.read(4)),
                }
                record["units_available"].append(unit_available)

        return records


class SkillAcquisitionPatternList(GundamDataFile):
    default_filename = "SkillAcquisitionPatternList.cdb"
    header = b"\x4C\x51\x41\x53\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "values": [
                    self.read_int(buffer.read(2)) for _ in range(18)
                ]
            }
            records.append(record)

        return records


class SpecProfileList(GundamDataFile):
    default_filename = "SpecProfileList.cdb"
    header = b"\x4C\x50\x50\x53\x00\x00\x03\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records


class TitleBgmList(GundamDataFile):
    default_filename = "TitleBgmList.cdb"
    header = b""

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records


class TutorialList(GundamDataFile):
    default_filename = "TutorialList.cdb"
    header = b"\x4F\x54\x55\x54\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        pass

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

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

        for i in range(record_count):
            record = {"__order": i}
            records.append(record)

        return records
