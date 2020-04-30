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

TERRAIN_SPACE = 1
TERRAIN_AIR = 2
TERRAIN_LAND = 4
TERRAIN_SURFACE = 8
TERRAIN_UNDERWATER = 16


class AbilitySpecList(GundamDataFile):
    default_filename = "AbilitySpecList.cdb"
    header = b"\x4C\x4C\x42\x41\x01\x00\x0C\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
    definition = {
        "guid": "guid",
        "unknown1": "uint4",
        "unknown2": "uint4",
    }


class BattleBgList(GundamDataFile):
    default_filename = "BattleBgList.cdb"
    header = b"\x47\x42\x54\x42\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            location = buffer.tell()
            record = {
                "__order": i,
                "__pointer": self.read_int(buffer.read(4)) + location,
                "index": self.read_int(buffer.read(2)),
                "type?": self.read_int(buffer.read(1)),
                "values": [self.read_int(buffer.read(1), signed=True) for _ in range(17)],
            }
            records.append(record)

        for record in records:
            record["name"] = self.read_string_null_term(buffer, record.pop("__pointer"))

        return records


class CharacterConversionList(GundamDataFile):
    default_filename = "CharacterConversionList.cdb"
    header = b"\x4C\x56\x43\x43\x00\x00\x00\x01"
    definition = {
        "character_id": "guid",
        "new_character_id": "guid",
        "change_type": "uint4",
    }


class CharacterGrowthList(GundamDataFile):
    default_filename = "CharacterGrowthList.cdb"
    header = b"\x52\x47\x48\x43\x00\x00\x00\x01"
    level_ups = 98
    profile_constant = 332

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []
        npcs = []

        npc_count = self.read_int(buffer.read(4))  # 224
        npc_pointer = self.read_int(buffer.read(4))  # 95452
        pointer2 = self.read_int(buffer.read(4))  # 111580
        unknown2 = self.read_int(buffer.read(2))  # 832
        unknown3 = self.read_int(buffer.read(2))  # 20

        # block 1
        # 112 bytes per record
        # block 2
        # 72 bytes per record
        # block 3
        # 1 byte per record?

        for i in range(record_count):
            # 112 bytes per record
            record = {
                "__order": i,
                "guid": self.read_guid_bytes(buffer.read(8)),
                "guid2": self.read_guid_bytes(buffer.read(8)),
                "chara_org": self.read_guid_bytes(buffer.read(8)),
                "unknown1": self.read_int(buffer.read(2), signed=True),
                "dlc_set": self.read_int(buffer.read(2)),
                # in language/*/CharacterSpecList.tbl
                "display_name_index": self.read_int(buffer.read(2)),
                "unknown3": self.read_int(buffer.read(1)),
                "unknown4": self.read_int(buffer.read(1)),
                "ranged": self.read_int(buffer.read(2)),
                "melee": self.read_int(buffer.read(2)),
                "defense": self.read_int(buffer.read(2)),
                "reaction": self.read_int(buffer.read(2)),
                "awaken": self.read_int(buffer.read(2)),
                "command": self.read_int(buffer.read(2)),
                "auxiliary": self.read_int(buffer.read(2)),
                "communications": self.read_int(buffer.read(2)),
                "navigation": self.read_int(buffer.read(2)),
                "maintenance": self.read_int(buffer.read(2)),
                "charisma": self.read_int(buffer.read(2)),
                "experience": self.read_int(buffer.read(2)),
                "out_value": self.read_int(buffer.read(2)),
                # in resident/CharacterGrowth.cdb
                "growth_profile": self.read_int(buffer.read(2)),
                "skills": [
                    self.read_int(buffer.read(2), signed=True) for _ in range(3)
                ],
                "bgm1": self.read_int(buffer.read(2)),
                "bgm2": self.read_int(buffer.read(2)),
                "personality_index": self.read_int(buffer.read(2)),
                "guid4": self.read_guid_bytes(buffer.read(8)),
                "unique_name_index": self.read_int(buffer.read(2), signed=True),
                "unknown5a": self.read_int(buffer.read(1), signed=False),
                "unknown5b": self.read_int(buffer.read(1), signed=False),
                "values2": [
                    self.read_int(buffer.read(2), signed=True) for _ in range(5)
                ],
                "__null": buffer.read(10),
                "scout_cost": self.read_int(buffer.read(2)),
                "__unknown6": self.read_int(buffer.read(2)),
                "recruitable": self.read_int(buffer.read(4)),
            }
            if record["unique_name_index"] == -1:
                record["unique_name_index"] = record["display_name_index"]
            for i in range(4):
                record[f"unknown6_bit{i}"] = 1 if record["__unknown6"] & 2 ** i else 0
            del record["__null"]
            records.append(record)

        buffer.seek(npc_pointer)
        
        for i in range(npc_count):
            # 72 bytes per record
            npc = {
                "__order": i,
                "guid": self.read_guid_bytes(buffer.read(8)),
                "guid2": self.read_guid_bytes(buffer.read(8)),
                "chara_org": self.read_guid_bytes(buffer.read(8)),
                "unknown1": self.read_int(buffer.read(2), signed=True),
                "dlc_set": self.read_int(buffer.read(2)),
                # in language/*/CharacterSpecList.tbl
                "unique_name_index": self.read_int(buffer.read(2)),
                "unknown3": self.read_int(buffer.read(1)),
                "unknown4": self.read_int(buffer.read(1)),
                "ranged": self.read_int(buffer.read(2)),
                "melee": self.read_int(buffer.read(2)),
                "defense": self.read_int(buffer.read(2)),
                "reaction": self.read_int(buffer.read(2)),
                "awaken": self.read_int(buffer.read(2)),
                "command": self.read_int(buffer.read(2)),
                "auxiliary": self.read_int(buffer.read(2)),
                "communications": self.read_int(buffer.read(2)),
                "navigation": self.read_int(buffer.read(2)),
                "maintenance": self.read_int(buffer.read(2)),
                "charisma": self.read_int(buffer.read(2)),
                "experience": self.read_int(buffer.read(2)),
                "out_value": self.read_int(buffer.read(2)),
                "growth_profile": self.read_int(buffer.read(2)),
                "skills": [
                    self.read_int(buffer.read(2), signed=True) for _ in range(3)
                ],
                "bgm1": self.read_int(buffer.read(2)),
                "bgm2": self.read_int(buffer.read(2)),
                "personality_index": self.read_int(buffer.read(2)),
            }
            npcs.append(npc)

        print(buffer.tell())
        buffer.seek(pointer2)
        personality_count = self.read_int(buffer.read(4))
        personalities = []
        for i in range(personality_count):
            personality = {
                # Adds up to 100
                "__order": i,
                "index": self.read_int(buffer.read(1)),
                "timid": self.read_int(buffer.read(1)),
                "normal": self.read_int(buffer.read(1)),
                "high": self.read_int(buffer.read(1)),
            }
            personalities.append(personality)
            print(personality)

        records.extend(npcs)
        # records.extend(personalities)

        return records


class CreditBgmList(GundamDataFile):
    default_filename = "CreditBgmList.cdb"
    header = b""

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
    definition = {
        "guid": "guid",
        "required_xp": "uint4",
    }


class GroupSendingMissionList(GundamDataFile):
    default_filename = "GroupSendingMissionList.cdb"
    header = b"\x4C\x53\x50\x47\x00\x00\x07\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
    definition = {
        "guid": "guid",
        "transform_guid": "guid",
        "conversion_type_id": "uint4",
    }

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        for record in records:
            string_bytes += self.write_guid_bytes(record["guid"])
            string_bytes += self.write_guid_bytes(record["transform_guid"])
            string_bytes += self.write_int(record["conversion_type_id"], 4)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            record = {
                "__order": i,
                "guid": self.read_guid_bytes(buffer.read(8)),
                "transform_guid": self.read_guid_bytes(buffer.read(8)),
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
    definition = {
        "first_guid": "guid",
        "second_guid": "guid",
        "result_guid": "guid",
        "index": "uint4",
    }


class MachineDevelopmentList(GundamDataFile):
    default_filename = "MachineDevelopmentList.cdb"
    header = b"\x56\x45\x44\x4D\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        child_start = len(string_bytes) + (record_count * 16)
        for record in records:
            pointer = child_start - len(string_bytes)
            child_count = len(record["children"])
            string_bytes += self.write_guid_bytes(record["guid"])
            string_bytes += int(pointer).to_bytes(4, byteorder="little")
            string_bytes += int(record["index"]).to_bytes(4, byteorder="little")
            string_bytes += int(child_count).to_bytes(4, byteorder="little")
            child_start += child_count * 12

        for record in records:
            for child in record["children"]:
                string_bytes += self.write_guid_bytes(child["guid"])
                string_bytes += int(child["level"]).to_bytes(4, byteorder="little")

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        for i in range(record_count):
            location = buffer.tell()
            guid = self.read_guid_bytes(buffer.read(8))
            # Pointer is relative to the start of this index record
            pointer = self.read_int(buffer.read(4))
            index = self.read_int(buffer.read(2))
            child_count = self.read_int(buffer.read(2))

            record = {
                "__order": i,
                "__pointer": pointer + location,
                "guid": guid,
                "index": index,
                "__child_count": child_count,
                "children": [],
            }
            records.append(record)

        for record in records:
            buffer.seek(record.pop("__pointer"))
            for _ in range(record.pop("__child_count")):
                child = {
                    "guid": self.read_guid_bytes(buffer.read(8)),
                    "level": self.read_int(buffer.read(4)),
                }
                record["children"].append(child)

        return records


class MachineGrowthList(GundamDataFile):
    default_filename = "MachineGrowthList.cdb"
    header = b"\x00\x00\x01\x01\x52\x47\x43\x4D"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        unit_count = self.read_header(buffer)
        records = []
        units = []
        header_values = [self.read_int(buffer.read(4)) for _ in range(3)]
        pointer1 = self.read_int(buffer.read(4))  # to ships
        pointer2 = self.read_int(buffer.read(4))  # to emplacements
        print(header_values)

        for i in range(unit_count):
            # 108 byte chunk
            unit = {
                "__order": i,
                "profile_guid": self.read_guid_bytes(buffer.read(8)),
                "dev_list_guid": self.read_guid_bytes(buffer.read(8)),
                "guid": self.read_guid_bytes(buffer.read(8)),
                "hp": self.read_int(buffer.read(4)),
                "index1": self.read_int(buffer.read(2)),
                "dlc_set": self.read_int(buffer.read(2)),
                "name_index": self.read_int(buffer.read(2)),
                "values1": [self.read_int(buffer.read(1)) for _ in range(6)],
                "values1b": [self.read_int(buffer.read(2)) for _ in range(5)],
                "__null": buffer.read(10),
    
                "production_cost": self.read_int(buffer.read(2)),
                "en": self.read_int(buffer.read(2)),
                "att": self.read_int(buffer.read(2)),
                "def": self.read_int(buffer.read(2)),
                "mob": self.read_int(buffer.read(2)),
                "exp": self.read_int(buffer.read(2)),
                # "unknown1": self.read_int(buffer.read(2)),
    
                "values2": [self.read_int(buffer.read(1)) for _ in range(6)],
                "size": self.read_int(buffer.read(1)),
                "fixed7": self.read_int(buffer.read(1)),  # always 7
                "values3": [
                    self.read_int(buffer.read(2), signed=True) for _ in range(5)
                ],
                "weapon_index": self.read_int(buffer.read(2), signed=True),
                "map_weapon_index": self.read_int(buffer.read(2), signed=True),
                "move": self.read_int(buffer.read(1)),
                "dimensions": [
                    self.read_int(buffer.read(1), signed=True) for _ in range(2)
                ],
                "weapon_count": self.read_int(buffer.read(1)),
                "map_weapon_count": self.read_int(buffer.read(1)),
                "values4": [
                    self.read_int(buffer.read(1), signed=True) for _ in range(4)
                ],
                "values5": [
                    self.read_int(buffer.read(1), signed=False) for _ in range(4)
                ],
                "__null2": self.read_int(buffer.read(1)),
            }
            del unit["__null"]
            del unit["__null2"]
            records.append(unit)

        return records


class MapTypes(GundamDataFile):
    default_filename = "MapTypes.cdb"
    header = b"\x02\x00\x05\x01\x50\x59\x54\x4D"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
    definition = {
        "guid": "guid",
        "pilot_guid": "guid",
        "custom_guid": "guid",
    }


class QuestList(GundamDataFile):
    default_filename = "QuestList.cdb"
    header = b"\x4C\x54\x45\x51\x00\x00\x02\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
                    "__pointer": self.read_int(buffer.read(4)) + location,
                }
            )

        for record in records:
            buffer.seek(record.pop("__pointer"))
            record["values"] = [
                self.read_int(buffer.read(1)) for _ in range(record["length"])
            ]

        return records


class SeriesList(GundamDataFile):
    default_filename = "SeriesList.cdb"
    header = b"\x4C\x52\x45\x53\x01\x00\x02\x01"
    definition = {
        "series_logo_l": "series_guid",
        "series_logo_s": "series_guid",
        "string_index": "uint2",
        "era": "uint1",
        "flag": "uint1",
    }

    # Era names are in messagestring.tbl
    # starting from index = 109112
    ERA = {
        0: None,
        1: "After Colony",
        2: "Cosmic Era",
        3: "A.D.",
        4: "Post Disaster",
    }


class SeriesProfileList(GundamDataFile):
    default_filename = "SeriesProfileList.cdb"
    header = b"\x4C\x50\x52\x53\x00\x00\x01\x01"
    definition = {
        "gallery": "series_guid",
        "value": "uint2",
        "string_index": "uint2",
    }


class StageClearGetList(GundamDataFile):
    default_filename = "StageClearGetList.cdb"
    header = b"\x43\x47\x54\x53\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        units_start = len(string_bytes) + (record_count * 12)
        for record in records:
            pointer = units_start - len(string_bytes)
            unit_count = len(record["get_units"])
            string_bytes += self.write_guid_bytes(record["stage_id"])
            string_bytes += self.write_int(unit_count, 4)
            string_bytes += self.write_int(pointer, 4)
            units_start += unit_count * 8

        for record in records:
            for get_unit in record["get_units"]:
                string_bytes += self.write_guid_bytes(get_unit)

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
                record["get_units"].append(self.read_guid_bytes(buffer.read(8)))

        return records


class StageList(GundamDataFile):
    default_filename = "StageList.cdb"
    header = b"\x4C\x47\x54\x53\x00\x00\x0B\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        difficulties = ["NORMAL", "HARD", "EXTRA", "HELL"]
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
            record["terrain_space"] = 1 if record["terrain"] & TERRAIN_SPACE else 0
            record["terrain_air"] = 1 if record["terrain"] & TERRAIN_AIR else 0
            record["terrain_land"] = 1 if record["terrain"] & TERRAIN_LAND else 0
            record["terrain_surface"] = 1 if record["terrain"] & TERRAIN_SURFACE else 0
            record["terrain_underwater"] = 1 if record["terrain"] & TERRAIN_UNDERWATER else 0

            del record["terrain"]
            del record["__null"]

            records.append(record)

        for record in records:
            # available units appears to be only for informational purposes in the
            # stage screen
            buffer.seek(record.pop("__pointer"))
            for _ in range(record.pop("__units_available_count")):
                unit_available = {
                    "guid": self.read_guid_bytes(buffer.read(8)),
                    "available_type": self.read_int(buffer.read(4)),
                }
                record["units_available"].append(unit_available)

        return records


class SkillAcquisitionPatternList(GundamDataFile):
    default_filename = "SkillAcquisitionPatternList.cdb"
    header = b"\x4C\x51\x41\x53\x00\x00\x00\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        for record in records:
            for v in record["values"]:
                string_bytes += self.write_int(v, 4)
    
        return string_bytes

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
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        ms_count = self.read_header(buffer)
        ws_count = self.read_int(buffer.read(4))
        char_count = self.read_int(buffer.read(4))

        records = []

        for i in range(ms_count + ws_count + char_count):
            record = {
                "__order": i,
                "guid": self.read_guid_bytes(buffer.read(8)),
                "guid2": self.read_guid_bytes(buffer.read(8)),
                "series": self.read_series_bytes(buffer.read(4)),
                "unk1": self.read_int(buffer.read(2)),
                "unk2": self.read_int(buffer.read(2)),
                "unk3": self.read_int(buffer.read(2)),
                "unk4": self.read_int(buffer.read(2)),
                # .... maybe?
                "profile_index": self.read_int(buffer.read(2)),
                "unk6": self.read_int(buffer.read(2)),
                "unk7": self.read_int(buffer.read(2)),
                "unk8": self.read_int(buffer.read(2)),
            }
            records.append(record)

        return records


class TitleBgmList(GundamDataFile):
    default_filename = "TitleBgmList.cdb"
    header = b""

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
    definition = {
        "tutorial_id1": "uint4",
        "tutorial_id2": "uint4",
        "tutorial_id3": "uint4",
        "index": "uint2",
        "unknown": "uint2",
    }


class WeaponSpecList(GundamDataFile):
    default_filename = "WeaponSpecList.cdb"
    header = b"\x4C\x53\x50\x57\x00\x00\x01\x01"

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

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
