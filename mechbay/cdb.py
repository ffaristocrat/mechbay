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
    definition = {"guid": "guid", "unknown1": "uint:4", "unknown2": "uint:4"}


class BattleBgList(GundamDataFile):
    default_filename = "BattleBgList.cdb"
    header = b"\x47\x42\x54\x42\x00\x00\x00\x01"
    definition = {
        "bgm1": "pointer:string_null_term",
        "bgm2": "pointer:string_null_term",
        "bgm3": "pointer:string_null_term",
        "value": "uint:4",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        record_size = self.definition_size(self.definition)

        # Consolidate all the bgm string ids into a set
        all_music = []
        for r in records:
            for b in r["bg_name"]:
                if b not in all_music:
                    all_music.append(b)

        pointer = 0
        locations = {}
        for i, bgm in enumerate(all_music):
            locations[bgm] = pointer
            pointer += len(bgm.encode("utf-8")) + 1

        index_end = (record_count * record_size) + len(string_bytes)

        # and then assign them to the records
        for r in records:
            r["pointers"] = [locations[b] + index_end for b in r["bg_name"]]

        for record in records:
            location = len(string_bytes)
            for pointer in record.pop("pointers"):
                # pointers are relative to the location of the *first* pointer
                string_bytes += self.write_int(pointer - location, 4)

            string_bytes += self.write_int(record["value"], 4)
            location += record_size

        string_bytes += b"\x00".join([b.encode("utf-8") for b in all_music]) + b"\x00"

        return string_bytes


class CellAttributeList(GundamDataFile):
    default_filename = "CellAttributeList.cdb"
    header = b"\x4C\x54\x41\x43\x00\x00\x03\x01"
    definition = {
        "name": "pointer:string_null_term",
        "index": "uint:2",
        "type?": "uint:1",
        "unknown1": "int:1",
        "unknown2": "int:1",
        "unknown3": "int:1",
        "unknown4": "int:1",
        "unknown5": "int:1",
        "unknown6": "int:1",
        "unknown7": "int:1",
        "unknown8": "int:1",
        "unknown9": "int:1",
        "unknown10": "int:1",
        "unknown11": "int:1",
        "unknown12": "int:1",
        "unknown13": "int:1",
        "unknown14": "int:1",
        "unknown15": "int:1",
        "unknown16": "int:1",
        "unknown17": "int:1",
    }


class CharacterConversionList(GundamDataFile):
    default_filename = "CharacterConversionList.cdb"
    header = b"\x4C\x56\x43\x43\x00\x00\x00\x01"
    definition = {
        "character_id": "guid",
        "new_character_id": "guid",
        "change_type": "uint:4",
    }


class CharacterGrowthList(GundamDataFile):
    default_filename = "CharacterGrowthList.cdb"
    header = b"\x52\x47\x48\x43\x00\x00\x00\x01"
    constants = {"level_ups": 90, "profile_constant": 332}

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        # make a unique list of stat increases
        # replace their entries with the index to those increases
        # then write both blocks

        level_up_stats = []
        for record in records:
            assert len(record["level_up_stats"]) == self.constants["level_ups"]
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

        pointer = (record_count * 2 * (self.constants["level_ups"] + 1)) + 20
        string_bytes += self.write_int(pointer, 4)

        index_lookup = {s: i for i, s in enumerate(level_up_stats)}
        for record in records:
            string_bytes += self.write_int(self.constants["profile_constant"], 2)
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
            assert self.read_int(buffer.read(2)) == self.constants["profile_constant"]
            record = {
                "__order": i,
                "__stats_index": [
                    self.read_int(buffer.read(2))
                    for _ in range(self.constants["level_ups"])
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
    character_definition = {
        "guid": "guid",
        "guid2": "guid",
        "chara_org": "guid",
        "unknown1": "int:2",
        "dlc_set": "uint:2",
        "display_name_index": "uint:2",  # in language/*/CharacterSpecList.tbl
        "unknown2": "uint:1",
        "unknown3": "uint:1",
        "ranged": "uint:2",
        "melee": "uint:2",
        "defense": "uint:2",
        "reaction": "uint:2",
        "awaken": "uint:2",
        "command": "uint:2",
        "auxiliary": "uint:2",
        "communications": "uint:2",
        "navigation": "uint:2",
        "maintenance": "uint:2",
        "charisma": "uint:2",
        "experience": "uint:2",
        "out_value": "uint:2",
        "growth_profile": "uint:2",  # in resident/CharacterGrowth.cdb
        "skill1": "int:2",
        "skill2": "int:2",
        "skill3": "int:2",
        "bgm1": "uint:2",
        "bgm2": "uint:2",
        "personality_index": "uint:2",
        "guid4": "guid",
        "unique_name_index": "int:2",
        "unknown4": "int:1",
        "unknown5": "int:1",
        "unknown6": "int:2",
        "unknown7": "int:2",
        "unknown8": "int:2",
        "unknown9": "int:2",
        "unknown10": "int:2",
        "__null": "null:10",
        "scout_cost": "uint:2",
        "unknown11": "uint:2",
        "recruitable": "uint:4",
    }

    npc_definition = {
        "guid": "guid",
        "guid2": "guid",
        "chara_org": "guid",
        "unknown1": "int:2",
        "dlc_set": "uint:2",
        "display_name_index": "uint:2",  # in language/*/CharacterSpecList.tbl
        "unknown2": "uint:1",
        "unknown3": "uint:1",
        "ranged": "uint:2",
        "melee": "uint:2",
        "defense": "uint:2",
        "reaction": "uint:2",
        "awaken": "uint:2",
        "command": "uint:2",
        "auxiliary": "uint:2",
        "communications": "uint:2",
        "navigation": "uint:2",
        "maintenance": "uint:2",
        "charisma": "uint:2",
        "experience": "uint:2",
        "out_value": "uint:2",
        "growth_profile": "uint:2",  # in resident/CharacterGrowth.cdb
        "skill1": "int:2",
        "skill2": "int:2",
        "skill3": "int:2",
        "bgm1": "uint:2",
        "bgm2": "uint:2",
        "personality_index": "uint:2",
    }

    personality_definition = {
        "index": "uint:1",
        "timid": "uint:1",
        "normal": "uint:1",
        "high": "uint:1",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []
        npcs = []
        personalities = []

        npc_count = self.read_int(buffer.read(4))  # 224
        npc_pointer = self.read_int(buffer.read(4))  # 95452
        personality_pointer = self.read_int(buffer.read(4))  # 111580
        unknown2 = self.read_int(buffer.read(2))  # 832
        unknown3 = self.read_int(buffer.read(2))  # 20

        for i in range(record_count):
            record = self.read_record(self.character_definition, buffer)

            if record["unique_name_index"] == -1:
                record["unique_name_index"] = record["display_name_index"]

            record.update(
                **self.bit_smash(
                    "unknown11", record["unknown11"], [str(i) for i in range(4)]
                )
            )

            records.append(record)

        buffer.seek(npc_pointer)

        for i in range(npc_count):
            npc = self.read_record(self.npc_definition, buffer)
            npcs.append(npc)

        buffer.seek(personality_pointer)
        personality_count = self.read_int(buffer.read(4))
        for i in range(personality_count):
            personality = self.read_record(self.personality_definition, buffer)
            personalities.append(personality)

        records.extend(npcs)

        for r in records:
            r["personality"] = personalities[r["personality_index"]]

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
    definition = {"guid": "guid", "required_xp": "uint:4"}


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
        "conversion_type_id": "uint:4",
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


class MachineDesignList(GundamDataFile):
    default_filename = "MachineDesignList.cdb"
    header = b"\x49\x53\x44\x4D\x00\x00\x02\x01"
    definition = {
        "first_guid": "guid",
        "second_guid": "guid",
        "result_guid": "guid",
        "index": "uint:4",
    }


class MachineDevelopmentList(GundamDataFile):
    default_filename = "MachineDevelopmentList.cdb"
    header = b"\x56\x45\x44\x4D\x00\x00\x02\x01"
    definition = {
        "guid": "guid",
        "children_pointer": "uint:4",
        "index": "uint:2",
        "children_count": "uint:2",
    }
    child_definition = {"guid": "guid", "level": "uint:4"}

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        child_start = len(string_bytes) + (record_count * 16)
        for record in records:
            record["children_pointer"] = child_start - len(string_bytes)
            record["children_count"] = len(record["children"])
            child_start += record["children_count"] * 12

            string_bytes += self.write_record(self.definition, record)

        for record in records:
            for child in record["children"]:
                string_bytes += self.write_record(self.child_definition, child)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = self.read_records(self.definition, buffer, record_count)

        for record in records:
            record["children"] = []
            buffer.seek(record.pop("children_pointer"))

            for _ in range(record.pop("children_count")):
                child = self.read_record(self.child_definition, buffer)
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
            record = {"__order": i}
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
    definition = {
        "unknown1": "uint:2",
        "unknown2": "uint:2",
        "unknown3": "uint:2",
        "unknown4": "uint:2",
        "unknown5": "uint:2",
        "unknown6": "uint:2",
    }
    definition2 = {"unknown1": "null_term_string"}

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

    definition = {
        "guid": "guid",
        "index": "uint:2",
        "string_name_index": "uint:2",
        "male": "uint:2",
        "null": "null:2",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        custom_count = self.read_header(buffer)
        npc_count = self.read_int(buffer.read(4))
        record_count3 = self.read_int(buffer.read(4))
        record_count4 = self.read_int(buffer.read(4))
        pointer1 = self.read_int(buffer.read(4)) + 40
        pointer2 = self.read_int(buffer.read(4))
        pointer3 = self.read_int(buffer.read(4))
        pointer4 = self.read_int(buffer.read(4))

        print(custom_count, npc_count, record_count3, record_count4)

        buffer.seek(pointer1)
        customs = self.read_records(self.definition, buffer, custom_count)
        buffer.seek(pointer2)
        npcs = self.read_records(self.definition, buffer, npc_count)
        # buffer.seek(pointer3)
        # records3 = self.read_records(self.definition, buffer, record_count3)

        records = customs + npcs

        return records


class PersonalMachineList(GundamDataFile):
    default_filename = "PersonalMachineList.cdb"
    header = b"\x4C\x43\x4D\x50\x00\x00\x00\x01"
    definition = {"guid": "guid", "pilot_guid": "guid", "custom_guid": "guid"}


class QuestList(GundamDataFile):
    default_filename = "QuestList.cdb"
    header = b"\x4C\x54\x45\x51\x00\x00\x02\x01"
    definition = {
        "guid1": "pointer:list:guid",
        "guid2": "pointer:list:guid",
        "guid3": "pointer:list:guid",
        "quest_value": "uint:4",
        "stages": "pointer:list:uint:4",
        "turns": "uint:2",
        "quest_type": "uint:2",
        "null": "null:8",
        "series": "series",
        "stage_id": "uint:4",
        "component_rewards": "pointer:list:uint:2",
        "machine_rewards": "pointer:list:guid",
        "pilot_rewards": "pointer:list:guid",
        "ability_rewards": "pointer:list:uint:2",
        "prereq_stage_id": "uint:4",
        "quest_id": "uint:2",
        "dlc_set": "uint:2",
        "quest_name_index": "uint:2",
        "spacing_index": "uint:2",
        "desc_index": "uint:2",
        "null2": "null:2",
        "unknown1": "uint:1",  # TODO: Identify unknown. Usually 1, sometimes 2
        "cooldown_reward": "uint:1",
        "null3": "null:2",
    }

    quest_types = {
        1: "Any pilot in list in any unit in list maxes out GET Gauge",
        2: "Register all units in list to Production List",
        3: "Register any unit in list to Production List",
        11: "Pilots exchanges blows in stage",
        12: "Fulfill secret condition",
        13: "Pilot defeats pilot with super high morale",
        14: "Pilot destroys number of units",
        15: "Clear stage within turn limit",
        16: "Destroy number of units within turn limit",
        19: "Pilot defeats unit within turn limit",
        20: "Fulfill all secret conditions",
        21: "Pilot defeats unit with weapon",
        22: "Pilot defeats pilot after exchanging number of blows",
        24: "Sortie unit",
        25: "Use weapon",
        26: "Sortie pilot",
        27: "Clear stage with warship group",
        28: "Clear stage with raid group",
        29: "Sortie pilot in unit",
        30: "Sortie pilot with ability in unit",
        31: "Use weapon with pilot in unit",
        32: "Pilot uses link-up",
        71: "Complete number of group dispatches",
        81: "Develop any unit",
        82: "Enhance any unit",
        83: "Produce any unit",
        91: "Clear stages in list",
        93: "Total number of kills",
        94: "Register number of units to production/scout lists",
        96: "Clear all stages in list? series?",
        99: "Not sure",
    }

    def write(self, records: List[Dict]) -> bytes:
        for record in records:
            # Just repeats the series id for some reason
            if record["quest_type"] in [1]:
                record["stage_id"] = self.write_series_bytes(record["stage_id"])

            # instead of a guid it's an ability id
            elif record["quest_type"] in [30]:
                # we need to skip 4 bytes
                record["guid2"] = [
                    b"\x00\x00\x00\x00" + self.write_int(int(v), 4)
                    for v in record["guid2"]
                ]

        return super().write(records)

    def read(self, buffer: BinaryIO) -> List[Dict]:
        records = super().read(buffer)

        for record in records:
            # Just repeats the series id for some reason
            if record["quest_type"] in [1]:
                stage_bytes = self.write_int(record["stage_id"], 4)
                record["stage_id"] = self.read_series_bytes(stage_bytes)

            # instead of a guid it's an ability id
            elif record["quest_type"] in [30]:
                # we need to skip 4 bytes
                record["guid2"] = [
                    self.read_int(self.write_guid_bytes(v)[4:8])
                    for v in record["guid2"]
                ]

        return records


class RangeDataList(GundamDataFile):
    default_filename = "RangeDataList.cdb"
    header = b"\x4C\x47\x4E\x52\x01\x00\x00\x01"

    # TODO: identify mask
    definition = {"value_count": "uint:2", "mask": "uint:2", "value_pointer": "pointer"}

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        # TODO: Finish writing

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = self.read_records(self.definition, buffer, record_count)

        for record in records:
            buffer.seek(record.pop("value_pointer"))

            # TODO: Identify values
            record["values"] = [
                self.read_int(buffer.read(1)) for _ in range(record.pop("value_count"))
            ]

        return records


class SeriesList(GundamDataFile):
    default_filename = "SeriesList.cdb"
    header = b"\x4C\x52\x45\x53\x01\x00\x02\x01"
    # TODO: identify unknowns
    definition = {
        "series_logo_l": "series",
        "series_logo_s": "series",
        "string_index": "uint:2",
        "era": "uint:1",
        "unknown1": "uint:1",  # always 1 or 0
    }

    # Era names are in messagestring.tbl
    # starting from index = 109112
    ERA = {0: None, 1: "After Colony", 2: "Cosmic Era", 3: "A.D.", 4: "Post Disaster"}


class SeriesProfileList(GundamDataFile):
    default_filename = "SeriesProfileList.cdb"
    header = b"\x4C\x50\x52\x53\x00\x00\x01\x01"
    definition = {"gallery": "series", "value": "uint:2", "string_index": "uint:2"}


class StageClearGetList(GundamDataFile):
    default_filename = "StageClearGetList.cdb"
    header = b"\x43\x47\x54\x53\x00\x00\x00\x01"
    definition = {"stage_id": "uint:4", "get_units": "cfpointer:list:guid"}


class StageList(GundamDataFile):
    default_filename = "StageList.cdb"
    header = b"\x4C\x47\x54\x53\x00\x00\x0B\x01"

    definition = {
        "stage_id": "uint:4",
        "series": "series",
        "required_stage_id": "uint:4",
        "reward1": "uint:4",
        "reward2": "uint:4",
        "reward3": "uint:4",
        "reward4": "uint:4",
        "reward5": "uint:4",
        "reward6": "uint:4",
        "units_available_count": "uint:4",
        "units_available_pointer": "pointer",
        "__null": "null:2",
        "index": "uint:2",
        "bgm": "uint:2",
        "series2": "uint:2",
        "unknown1": "uint:2",
        "unknown2": "uint:2",
        "unknown3": "uint:2",
        "unknown4": "uint:2",
        "unknown5": "uint:2",
        "unknown6": "uint:2",
        "unknown7": "uint:2",
        "unknown8": "uint:2",
        "unknown9": "uint:2",
        "unknown10": "uint:2",
        "unknown11": "uint:2",
        "unknown12": "uint:2",
        "unknown13": "uint:2",
        "unknown14": "uint:2",
        "unknown15": "uint:2",
        "unknown16": "uint:2",
        "unknown17": "uint:2",
        "unknown18": "uint:2",
        "unknown19": "uint:2",
        "unknown20": "uint:2",
        "unknown21": "uint:2",
        "unknown22": "uint:1",
        "unknown23": "uint:1",
        "unknown24": "uint:1",
        "unknown25": "uint:1",
        "unknown26": "uint:1",
        "terrain": "uint:1",
        "series_end": "uint:4",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        difficulties = ["NORMAL", "HARD", "EXTRA", "HELL"]
        terrain = ["space", "air", "land", "surface", "underwater"]
        record_count = self.read_header(buffer)
        records = self.read_records(self.definition, buffer, record_count)

        for record in records:
            record.update(self.bit_smash("terrain", record["terrain"], terrain))

            # available units appears to be only for informational purposes in the
            # stage screen
            record["units_available"] = []
            buffer.seek(record.pop("units_available_pointer"))
            for _ in range(record.pop("units_available_count")):
                unit_available = {
                    "guid": self.read_guid_bytes(buffer.read(8)),
                    "available_type": self.read_int(buffer.read(4)),
                }
                record["units_available"].append(unit_available)

        return records


class SkillAcquisitionPatternList(GundamDataFile):
    default_filename = "SkillAcquisitionPatternList.cdb"
    header = b"\x4C\x51\x41\x53\x00\x00\x00\x01"

    definition = {
        "unknown1": "uint:2",
        "unknown2": "uint:2",
        "unknown3": "uint:2",
        "unknown4": "uint:2",
        "unknown5": "uint:2",
        "unknown6": "uint:2",
        "unknown7": "uint:2",
        "unknown8": "uint:2",
        "unknown9": "uint:2",
        "unknown10": "uint:2",
        "unknown11": "uint:2",
        "unknown12": "uint:2",
        "unknown13": "uint:2",
        "unknown14": "uint:2",
        "unknown15": "uint:2",
        "unknown16": "uint:2",
        "unknown17": "uint:2",
        "unknown18": "uint:2",
    }


class SpecProfileList(GundamDataFile):
    default_filename = "SpecProfileList.cdb"
    header = b"\x4C\x50\x50\x53\x00\x00\x03\x01"

    # TODO: identify unknowns
    definition = {
        "guid": "guid",
        "guid2": "guid",
        "series": "series",
        "unknown1": "uint:2",
        "unknown2": "uint:2",
        "unknown3": "uint:2",
        "unknown4": "uint:2",
        "profile_index": "uint:2",
        "unknown5": "uint:2",
        "unknown6": "uint:2",
        "unknown7": "uint:2",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        # TODO: parse out

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        ms_count = self.read_header(buffer)
        ws_count = self.read_int(buffer.read(4))
        char_count = self.read_int(buffer.read(4))

        record_count = ms_count + ws_count + char_count
        records = self.read_records(self.definition, buffer, record_count)

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
        "tutorial_id1": "uint:4",
        "tutorial_id2": "uint:4",
        "tutorial_id3": "uint:4",
        "index": "uint:2",
        "unknown": "uint:2",
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
