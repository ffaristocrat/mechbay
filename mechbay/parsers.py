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
    data_path = "data/resident"
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
    data_path = "data/tmap/resident"
    default_filename = "ActAbilityEffectList.cdb"
    header = b"\x4C\x45\x41\x41\x00\x00\x01\x01"
    definition = {"guid": "guid", "unknown1": "uint:4", "unknown2": "uint:4"}


class BattleBgList(GundamDataFile):
    data_path = "data/resident"
    package = "CellAttributeList.pkd"
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
        fields = ["bgm1", "bgm2", "bgm3"]

        # Consolidate all the string into a set
        all_strings = []
        for r in records:
            for f in fields:
                if r[f] not in all_strings:
                    all_strings.append(r[f])

        pointer = 0
        locations = {}
        index_end = (record_count * record_size) + len(string_bytes)
        for t in all_strings:
            locations[t] = pointer + index_end
            pointer += len(t.encode("utf-8")) + 1

        # and then assign them to the records
        for r in records:
            location = len(string_bytes)
            for f in fields:
                r[f] = locations[f] - location

        string_bytes += self.write_records(self.definition, records)
        string_bytes += b"\x00".join([b.encode("utf-8") for b in all_strings]) + b"\x00"

        return string_bytes


class CellAttributeList(GundamDataFile):
    default_filename = "CellAttributeList.cdb"
    data_path = "data/resident"
    package = "CellAttributeList.pkd"
    header = b"\x4C\x54\x41\x43\x00\x00\x03\x01"
    definition = {
        "name": "pointer:string_null_term",
        "index": "uint:2",
        "type": "uint:1",
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
    data_path = "data/resident"
    header = b"\x4C\x56\x43\x43\x00\x00\x00\x01"
    definition = {
        "character_id": "guid",
        "new_character_id": "guid",
        "change_type": "uint:4",
    }


class CharacterGrowthList(GundamDataFile):
    default_filename = "CharacterGrowthList.cdb"
    data_path = "data/resident"
    package = "CharacterSpecList.pkd"
    header = b"\x52\x47\x48\x43\x00\x00\x00\x01"
    level_ups = 98  # This is blowing up to 998 for the expansion
    constants = {"profile_constant": 332}
    definition = {"profile_constant": "uint:2"}
    level_up_definition = {
        "cmd": "uint:2",
        "rng": "uint:2",
        "mel": "uint:2",
        "def": "uint:2",
        "rct": "uint:2",
        "awk": "uint:2",
        "aux": "uint:2",
        "com": "uint:2",
        "nav": "uint:2",
        "mnt": "uint:2",
        "chr": "uint:2",
    }

    def __new__(cls, *args, **kwargs):
        super().__new__(*args, **kwargs)
        for i in range(cls.level_ups):
            cls.definition[f"level_{i + 2}_index"] = "uint:2"

    def write(self, records: List[Dict]) -> bytes:
        # make a unique list of stat increases
        # replace their entries with the index to those increases
        # then write both blocks

        level_up_stats = []
        for record in records:
            for i in range(self.level_ups):
                assert len(record[f"level_{i + 2}"]) == self.level_ups
                level_ups = tuple(record[f"level_{i + 2}"])
                if level_ups not in level_up_stats:
                    level_up_stats.append(level_ups)
                record[f"level_{i + 2}_index"] = level_up_stats.index(level_ups)

        self.apply_constants(records)
        profile_bytes = self.write_records(self.definition, records)
        level_up_bytes = self.write_records(
            self.level_up_definition,
            [
                {k: i for k, i in zip(self.level_up_definition.keys(), s)}
                for s in level_up_stats
            ],
        )

        string_bytes = self.write_header(len(records))
        string_bytes += self.write_int(len(level_up_stats), 4)
        level_up_pointer = len(string_bytes) + len(profile_bytes) + 4
        string_bytes += self.write_int(level_up_pointer, 4)
        string_bytes += profile_bytes + level_up_bytes

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        profile_count = self.read_header(buffer)
        level_up_count = self.read_int(buffer.read(4))
        level_up_pointer = self.read_int(buffer.read(4))

        # characters have an index to one of these profiles
        # each profile has 98 indexes to a list of stats
        # the stats list states the increase of each stat

        profiles = self.read_records(self.definition, buffer, profile_count)
        buffer.seek(level_up_pointer)
        level_ups = self.read_records(self.level_up_definition, buffer, level_up_count)

        for profile in profiles:
            for i in range(self.level_ups):
                profile[f"level_{i + 2}"] = level_ups[profile[f"level_{i + 2}_index"]]

        return profiles


class CharacterSpecList(GundamDataFile):
    default_filename = "CharacterSpecList.cdb"
    data_path = "data/resident"
    package = "CharacterSpecList.pkd"
    header = b"\x4C\x53\x48\x43\x00\x00\x07\x02"
    character_definition = {
        "guid": "guid",
        "cutin_guid": "guid",
        "image_guid": "guid",
        "index": "int:2",
        "dlc": "uint:2",
        "character_spec_list": "uint:2",
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
        "character_growth": "int:2",
        "ability1": "int:2",
        "ability2": "int:2",
        "ability3": "int:2",
        "bgm1": "uint:2",
        "bgm2": "uint:2",
        "personality": "uint:2",
        "profile_guid": "guid",
        "unique_character_spec_list": "int:2",
        "unknown4": "uint:1",
        "unknown5": "uint:1",
        "unknown6": "int:2",
        "unknown7": "int:2",
        "unknown8": "int:2",
        "unknown9": "int:2",
        "unknown10": "int:2",
        "null": "null:10",
        "scout_cost": "uint:2",
        "skill_acquisition_pattern": "int:2",
        "scoutable": "uint:4",
    }

    npc_definition = {
        "guid": "guid",
        "cutin_guid": "guid",
        "image_guid": "guid",
        "index": "int:2",
        "dlc": "uint:2",
        "character_spec_list": "uint:2",
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
        "character_growth": "int:2",
        "ability1": "int:2",
        "ability2": "int:2",
        "ability3": "int:2",
        "bgm1": "uint:2",
        "bgm2": "uint:2",
        "personality": "uint:2",
    }

    personality_definition = {
        "index": "uint:1",
        "timid": "uint:1",
        "normal": "uint:1",
        "high": "uint:1",
    }

    def write(self, records: List[Dict]) -> bytes:
        personalities = []

        for r in records:
            personality = (
                r["personality_timid"],
                r["personality_normal"],
                r["personality_high"],
            )
            if personality not in personality:
                personalities.append(personality)
            r["personality"] = personalities.index(personality)

        chars = [r for r in records if r["guid"] == "C"]
        npcs = [r for r in records if r["guid"] == "N"]

        char_bytes = self.write_records(self.definition, chars)
        npc_bytes = self.write_records(self.npc_definition, npcs)
        personality_bytes = self.write_records(
            self.personality_definition,
            [
                {"index": i + 1, "timid": p[0], "normal": p[1], "high": p[2]}
                for i, p in enumerate(personalities)
            ],
        )

        string_bytes = self.write_header(len(chars))
        string_bytes += self.write_int(len(npcs), 4)
        npc_pointer = len(string_bytes) + len(char_bytes) + 12
        string_bytes += self.write_int(npc_pointer, 4)
        personality_pointer = npc_pointer + len(npc_bytes)
        string_bytes += self.write_int(personality_pointer, 4)

        string_bytes += self.write_int(832, 4)
        string_bytes += self.write_int(20, 4)

        string_bytes += char_bytes + npc_bytes + personality_bytes

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        ms_count = self.read_header(buffer)
        npc_count = self.read_int(buffer.read(4))
        npc_pointer = self.read_int(buffer.read(4))
        personality_pointer = self.read_int(buffer.read(4))
        self.read_int(buffer.read(2))  # unknown = 832
        self.read_int(buffer.read(2))  # unknown = 20

        chars = []
        npcs = []
        personalities = []

        for i in range(ms_count):
            char = self.read_record(self.character_definition, buffer)
            char["__order"] = i
            chars.append(char)

        buffer.seek(npc_pointer)

        for i in range(npc_count):
            npc = self.read_record(self.npc_definition, buffer)
            npc["__order"] = i
            npcs.append(npc)

        buffer.seek(personality_pointer)
        personality_count = self.read_int(buffer.read(4))
        for i in range(personality_count):
            personality = self.read_record(self.personality_definition, buffer)
            personality["__order"] = i
            personalities.append(personality)

        records = chars + npcs

        for r in records:
            p = personalities[r["personality"]]
            r["personality_timid"] = p["timid"]
            r["personality_normal"] = p["normal"]
            r["personality_high"] = p["high"]

        return records


class CockpitBgTable(GundamDataFile):
    default_filename = "cockpit_bg_table.atp"
    data_path = "data/battle/table"
    header = b"\xC2\x3E\x10\x0A"
    record_count_length = 0

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        return records


class CreditBgmList(GundamDataFile):
    default_filename = "CreditBgmList.cdb"
    data_path = "data/resident"
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
    # Yes, the source file is misspelled
    default_filename = "DatabaseCalcuclation.cdb"
    data_path = "data/resident"
    package = "MiscData.pkd"
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
    data_path = "data/resident"
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
    data_path = "data/tmap/stage"
    header = b"\x00\x00\x00\x01\x4C\x54\x55\x47"
    definition = {"guid": "guid", "required_xp": "uint:4"}


class GroupSendingMissionList(GundamDataFile):
    default_filename = "GroupSendingMissionList.cdb"
    data_path = "data/resident"
    package = "MiscData.pkd"
    header = b"\x4C\x53\x50\x47\x00\x00\x07\x01"

    definition = {
        "exp": "uint:4",
        "cap": "uint:4",
        "unknown2": "uint:4",
        "unknown3": "pointer",
        "unknown4": "uint:4",
        "unknown5": "pointer",
        "unknown5_count": "uint:4",
        "unknown7": "uint:4",
        "unknown8": "uint:4",
        "unknown9": "uint:4",
        "unknown10": "uint:4",
        "unknown11": "uint:4",
        "unknown12": "uint:4",
        "unknown13": "uint:4",
        "unknown14": "uint:4",
        "unknown15": "uint:4",
        "unknown16": "uint:4",
        "dlc_set": "uint:2",
        "dispatch_id": "uint:2",
        "dispatch_id2": "uint:2",
        "unknown20": "uint:2",
        "unknown21": "uint:2",
        "unknown22": "uint:2",
        "unknown23": "uint:2",
        "unknown24": "uint:2",
        "unknown25": "uint:2",
        "unknown26": "uint:2",
        "unknown27": "uint:2",
        "unknown28": "uint:2",
    }


class BTLIdSet(GundamDataFile):
    default_filename = "idset.tbl"
    data_path = "data/sound/voice/BTL"
    header = b"\x54\x53\x44\x49\x00\x01\x02\x00"

    definition = {
        "guint": "uint:4",
    }

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        unknown1_count = self.read_int(buffer.read(4))
        unknown2_count = self.read_int(buffer.read(4))
        unknown3_count = self.read_int(buffer.read(4))
        records = self.read_records(self.definition, buffer, record_count)

        return records


class BTLVoiceTable(GundamDataFile):
    default_filename = "voice_table.tbl"
    data_path = "data/sound/voice/BTL"
    header = b"\x54\x4F\x56\x42\x00\x04\x02\x00"

    definition = {
        "guint": "uint:4",
    }

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        unknown1_count = self.read_int(buffer.read(4))
        unknown2_count = self.read_int(buffer.read(4))
        unknown3_count = self.read_int(buffer.read(4))
        records = self.read_records(self.definition, buffer, record_count)

        return records


class MachineConversionList(GundamDataFile):
    default_filename = "MachineConversionList.cdb"
    data_path = "data/resident"
    package = "MachineSpecList.pkd"
    header = b"\x56\x4E\x43\x4D\x00\x00\x02\x01"
    definition = {
        "guid": "guid",
        "transform_guid": "guid",
        "conversion_type_id": "uint:4",
    }

    conversion_types = {
        2: "refit_1",
        3: "refit_2",
        4: "refit_3",
        5: "",
        6: "",
        8: "",
        16: "transform",
        19: "",
    }


class MachineDesignList(GundamDataFile):
    default_filename = "MachineDesignList.cdb"
    data_path = "data/resident"
    package = "MachineSpecList.pkd"
    header = b"\x49\x53\x44\x4D\x00\x00\x02\x01"
    definition = {
        "first_guid": "guid",
        "second_guid": "guid",
        "result_guid": "guid",
        "index": "uint:4",
    }


class MachineDevelopmentList(GundamDataFile):
    default_filename = "MachineDevelopmentList.cdb"
    data_path = "data/resident"
    package = "MachineSpecList.pkd"
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
    data_path = "data/resident"
    package = "MachineSpecList.pkd"
    header = b"\x00\x00\x01\x01\x52\x47\x43\x4D"
    definition = {}

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
    data_path = "data/resident"
    package = "MachineSpecList.pkd"
    header = b"\x4C\x53\x43\x4D\x03\x00\x05\x02"
    constants = {"fixed7": 7}

    definition = {
        "guid": "guid",  # profile?
        "guid2": "guid",  # dev list?
        "guid3": "guid",
        "hp": "uint:4",
        "index1": "uint:2",
        "dlc_set": "uint:2",
        "name_index": "uint:2",
        "unknown1": "uint:1",  # 0 - 248 (49 distinct)
        "unknown2": "uint:1",  # 0, 1, 2, 3, 5, 13, 15, 16, 22, 23, 26, 27, 31, 39, 40, 42, 43, 44, 45, 46, 51, 52, 54, 55, 56, 58, 59, 62, 67, 69, 70, 71, 76, 77
        "unknown3": "uint:1",  # 0 - 255 (172 distinct)
        "unknown4": "uint:1",  # mostly 0, increments slowly through list to 76
        "unknown5": "uint:1",  # increments of 2, 127 distinct
        "unknown6": "uint:1",  # 0 - 167, 133 distinct
        "unknown7": "uint:2",  # index?
        "unknown8": "uint:2",  # index?
        "unknown9": "uint:2",  # index?
        "unknown10": "uint:2",  # index?
        "unknown11": "uint:2",  # index?
        "null": "null:10",
        "cost": "uint:2",
        "en": "uint:2",
        "atk": "uint:2",
        "def": "uint:2",
        "mob": "uint:2",
        "exp": "uint:2",
        "unknown12": "uint:2",  # increments of 10, to 500
        "unknown14": "uint:1",  # 0 - 255
        "unknown15": "uint:1",  # 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 32
        "unknown16": "uint:1",  # might be binary, 38 distinct
        "unknown17": "uint:1",  # 0, 1, 6, 7, 9, 16, 17, 25, 32, 33, 38, 39, 48, 49, 64, 65, 73
        "size": "uint:1",
        "fixed7": "uint:1",  # always 7
        "unknown18": "int:2",  # -1, 0-86, 34 distinct
        "unknown19": "int:2",  # -1, 1-85, 52 distinct
        "unknown20": "int:2",  # -1, 2-85, 39 distinct
        "unknown21": "int:2",  # -1, 15, 26, 39, 40, 42, 43, 48, 50, 51, 52, 54, 56, 58, 59, 60, 74, 82
        "unknown22": "int:2",  # -1 or 50
        "weapon_index": "int:2",
        "map_weapon_index": "int:2",
        "mov": "uint:1",
        "dimension1": "int:1",  # footprint
        "dimension2": "int:1",
        "weapon_count": "uint:1",
        "map_weapon_count": "uint:1",
        "unknown23": "int:1",  # -1, 0, 1, 2, 3, 4
        "shadow_texture": "int:1",
        "null2": "null:3",
        "unknown28": "uint:1",  # 0, 1, 2, 16, 32, 33, 64, 80, 128, 129, 144, 160
        "unknown29": "uint:1",  # 0, 1, 2, 4, 8, 16, 24
        "unknown30": "uint:1",  # 0, 2, 16, 17, 20, 21, 24, 25
        "null3": "binary:1",
    }
    definition_ws = {
        "guid": "guid",  # profile?
        "guid2": "guid",  # dev list?
        "guid3": "guid",
        "hp": "uint:4",
        "index1": "uint:2",
        "dlc_set": "uint:2",
        "name_index": "uint:2",
        "unknown1": "uint:1",  # 0, 19, 23, 27, 68, 77, 84, 95, 102, 130, 134, 136, 140, 202, 211, 213, 233
        "unknown2": "uint:1",  # 0, 3, 23, 78, 81, 86, 88, 90, 93, 95, 96, 97, 101, 102
        "unknown3": "uint:1",  # 0 - 255, 83 distinct
        "unknown4": "uint:1",  # mostly 0, 77-102, 27 distinct
        "unknown5": "uint:1",  # increments of 2, 82 distinct
        "unknown6": "uint:1",  # 0 - 18,
        "unknown7": "uint:2",  # index?
        "unknown8": "uint:2",  # index?
        "unknown9": "uint:2",  # index?
        "unknown10": "uint:2",  # index?
        "unknown11": "uint:2",  # index?
        "null": "null:10",
        "cost": "uint:2",
        "en": "uint:2",
        "atk": "uint:2",
        "def": "uint:2",
        "mob": "uint:2",
        "exp": "uint:2",
        "unknown12": "uint:2",  # increments of 10, to 500
        "unknown14": "uint:1",  # might be binary? 0 - 255, 67 distinct
        "unknown15": "uint:1",  # 18, 19, 22, 23, 24, 25, 26, 27
        "unknown16": "uint:1",  # 0, 3, 4, 24, 27, 28, 32, 35, 36, 219
        "unknown17": "uint:1",  # 0, 1, 6, 7, 8, 38, 48, 64
        "size": "uint:1",
        "fixed7": "uint:1",  # always 7
        "unknown18": "int:2",  # -1, 8, 20, 30, 42, 46
        "unknown19": "int:2",  # -1, 17, 38, 49, 61
        "unknown20": "int:2",  # -1
        "unknown21": "int:2",  # -1
        "unknown22": "int:2",  # -1
        "weapon_index": "int:2",
        "map_weapon_index": "int:2",
        "mov": "uint:1",
        "dimension1": "int:1",  # footprint
        "dimension2": "int:1",
        "weapon_count": "uint:1",
        "map_weapon_count": "uint:1",
        "unknown23": "int:1",  # -1, 0, 2, 4
        "shadow_texture": "int:1",
        "null2": "null:3",
        "unknown28": "uint:1",  # 0, 1, 2
        "unknown29": "uint:1",  # 100
        "unknown30": "uint:1",  # 80
        "null3": "binary:1",
    }

    size_map = {}

    def write(self, records: List[Dict]) -> bytes:
        self.apply_constants(records)

        ms_records = [r for r in records if r["guid"][5] == "U"]
        ws_records = [r for r in records if r["guid"][5] == "W"]

        string_bytes = self.write_header(len(ms_records))
        string_bytes += self.write_int(len(ws_records), 4)
        string_bytes += self.write_int(457, 4)
        string_bytes += self.write_int(54, 4)

        ms_bytes = self.write_records(self.definition, ms_records)
        ws_bytes = self.write_records(self.definition, ws_records)

        ws_pointer = len(string_bytes) + len(ms_bytes) + 4
        string_bytes += self.write_int(ws_pointer, 4)

        file_length = len(string_bytes) + len(ms_bytes) + len(ws_bytes) + 4
        string_bytes += self.write_int(file_length, 4)

        string_bytes += ms_bytes + ws_bytes

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        ms_count = self.read_header(buffer)
        ws_count = self.read_int(buffer.read(4))
        unknown1 = self.read_int(buffer.read(4))
        unknown2 = self.read_int(buffer.read(4))
        ws_pointer = self.read_int(buffer.read(4))  # to ships
        self.read_int(buffer.read(4))  # file length
        print(unknown1, unknown2)

        ms_records = []
        ws_records = []

        for i in range(ms_count):
            ms = self.read_record(self.definition, buffer)
            ms["__order"] = i
            ms_records.append(ms)

        buffer.seek(ws_pointer)
        for i in range(ws_count):
            ws = self.read_record(self.definition, buffer)
            ws["__order"] = i
            ws_records.append(ws)

        records = ms_records + ws_records
        self.remove_constants(records)

        return records


class MapTypes(GundamDataFile):
    default_filename = "MapTypes.cdb"
    data_path = "data/tmap/resident"
    header = b"\x02\x00\x05\x01\x50\x59\x54\x4D"
    definition = {
        "unk1": "uint:1",
        "unk2": "uint:1",
        "type1": "shpointer:string_null_term",
        "type2": "shpointer:string_null_term",
        "type3": "shpointer:string_null_term",
        "unk3": "uint:1",
        "unk4": "uint:1",
        "index": "uint:2",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        record_size = self.definition_size(self.definition)
        fields = ["type1", "type2", "type3"]

        # Consolidate all the string into a set
        all_strings = []
        for r in records:
            for f in fields:
                if r[f] not in all_strings:
                    all_strings.append(r[f])

        pointer = 0
        locations = {}
        index_end = (record_count * record_size) + len(string_bytes)
        for t in all_strings:
            locations[t] = pointer + index_end
            pointer += len(t.encode("utf-8")) + 1

        # and then assign them to the records
        for r in records:
            location = len(string_bytes)
            for f in fields:
                r[f] = locations[f] - location

        string_bytes += self.write_records(self.definition, records)
        string_bytes += b"\x00".join([b.encode("utf-8") for b in all_strings]) + b"\x00"

        return string_bytes


class MyCharacterConfigurations(GundamDataFile):
    default_filename = "MyCharacterConfigurations.cdb"
    data_path = "data/resident"
    package = "CharacterSpecList.pkd"
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
    data_path = "data/resident"
    package = "MachineSpecList.pkd"
    header = b"\x4C\x43\x4D\x50\x00\x00\x00\x01"
    definition = {"guid": "guid", "pilot_guid": "guid", "custom_guid": "guid"}


class QuestList(GundamDataFile):
    default_filename = "QuestList.cdb"
    data_path = "data/resident"
    package = "StageList.pkd"
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
        "quest_spacing_index": "uint:2",
        "desc_index": "uint:2",
        "null2": "null:2",
        "unknown1": "uint:1",  # TODO: Usually 1, sometimes 2
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
    data_path = "data/resident"
    header = b"\x4C\x47\x4E\x52\x01\x00\x00\x01"

    # TODO: identify mask
    definition = {
        "value_pointer": "pointer:list:uint:2",
        "value_count": "uint:2",
        "mask": "uint:2",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        other_count = self.read_int(buffer.read(4))

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
    data_path = "data/resident"
    package = "MiscData.pkd"
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
    data_path = "data/resident"
    header = b"\x4C\x50\x52\x53\x00\x00\x01\x01"
    definition = {
        "gallery": "series",
        "index": "uint:2",
        # Name in MiscData.tbl, Profile in SeriesProfile.tbl
        "series_index": "uint:2",
    }


class StageClearGetList(GundamDataFile):
    default_filename = "StageClearGetList.cdb"
    data_path = "data/tmap/stage"
    header = b"\x43\x47\x54\x53\x00\x00\x00\x01"
    definition = {"stage_id": "uint:4", "get_units": "cfpointer:list:guid"}


class StageList(GundamDataFile):
    default_filename = "StageList.cdb"
    data_path = "data/resident"
    package = "StageList.pkd"
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

    available_unit_definition = {"guid": "guid", "available_type": "uint:4"}

    def read(self, buffer: BinaryIO) -> List[Dict]:
        difficulties = ["NORMAL", "HARD", "EXTRA", "HELL"]  # INFERNO coming
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
                unit_available = self.read_record(
                    self.available_unit_definition, buffer
                )
                record["units_available"].append(unit_available)

        return records


class SkillAcquisitionPatternList(GundamDataFile):
    default_filename = "SkillAcquisitionPatternList.cdb"
    header = b"\x4C\x51\x41\x53\x00\x00\x00\x01"

    definition = {
        "skill1": "uint:2",
        "level1": "uint:2",
        "skill2": "uint:2",
        "level2": "uint:2",
        "skill3": "uint:2",
        "level3": "uint:2",
        "skill4": "uint:2",
        "level4": "uint:2",
        "skill5": "uint:2",
        "level5": "uint:2",
        "skill6": "uint:2",
        "level6": "uint:2",
        "skill7": "uint:2",
        "level7": "uint:2",
        "skill8": "uint:2",
        "level8": "uint:2",
        "skill9": "uint:2",
        "level9": "uint:2",
    }


class SpecProfileList(GundamDataFile):
    default_filename = "SpecProfileList.cdb"
    data_path = "data/resident"
    header = b"\x4C\x50\x50\x53\x00\x00\x03\x01"

    # These are only informational for the profile pages
    # They don't actually define how these units can be acquired
    definition = {
        "guid": "guid",
        "image_guid": "guid",
        "series": "series",
        "stage_clear_get": "uint:4",
        "dlc_set": "uint:2",
        "profile_id": "uint:2",
        "string_index": "uint:2",
        "quest_id": "uint:2",
        "group_dispatch": "uint:2",
        "scoutable": "uint:2",  # always 1 for W and U
    }

    def write(self, records: List[Dict]) -> bytes:
        ms_records = [r for r in records if r["guid"][5] == "U"]
        ws_records = [r for r in records if r["guid"][5] == "W"]
        char_records = [r for r in records if r["guid"][5] == "C"]

        string_bytes = self.write_header(len(ms_records))
        string_bytes += self.write_int(len(ws_records), 4)
        string_bytes += self.write_int(len(char_records), 4)

        string_bytes += self.write_records(self.definition, ms_records)
        string_bytes += self.write_records(self.definition, ws_records)
        string_bytes += self.write_records(self.definition, char_records)

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
    data_path = "data/resident"
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
    data_path = "data/resident"
    package = "MiscData.pkd"
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
    data_path = "data/resident"
    package = "MachineSpecList.pkd"
    header = b"\x4C\x53\x50\x57\x00\x00\x00\x01"

    """
        name
        range (grid)
        power
        en
        mp
        icon
        type 1 - beam/physical/special
        type 2 - melee/ranged
        map
        tension
        accuracy
        weapon effect
        terrain capability
        terrain effect
    """

    definition = {
        "guid": "guid",
        "name_index": "uint:2",  # MachineSpecList.tbl
        "unk1": "uint:2",
        "power": "uint:2",
        "en": "uint:2",
        "mp": "uint:2",
        "unk6a": "uint:1",  # [0, 136, 168, 170]
        "unk6b": "uint:1",  # [0, 1, 2]
        "index2": "uint:2",  # [1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1811, 1817, 1819]
        "type_index": "uint:1",
        "effect_index": "uint:1",
        "unk9": "uint:2",  # [0, 4, 5]
        "unk10": "uint:2",  # [15, 16, 26, 30, 31]
        "unk11": "int:1",  # [1, 2, 3, 4]
        "unk12": "int:1",  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
        "unk13": "uint:2",  # [65, 70, 75, 80, 85, 90, 1355, 1360, 1365, 1370, 2630, 2635, 2640, 2645, 2650, 3925]
        "icon?": "uint:2",  # [1, 2, 3, 4, 5, 6, 7, 8]
        "null": "null:2",
    }

    map_weapon_definition = {
        "guid": "guid",
        "name_index": "uint:2",
        "unk1": "uint:2",
        "power": "uint:2",
        "en": "uint:2",
        "mp": "uint:2",
        "unk6a": "uint:1",  # [128, 170]
        "unk6b": "uint:1",  # [0, 2]
        "index2": "uint:2",  # [1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1811, 1817, 1819]
        "type_index": "uint:1",  # [7]
        "effect_index": "uint:1",
        "unk9": "uint:2",  # [0, 4]
        "unk10": "uint:2",  # [15, 24, 31]
        "unk11": "int:2",  # [-1, 1812, 1815, 1831]
        "unk12": "int:2",  # [0, 1, 256, 512]
        "unk13": "int:2",  # [3, 4, 258, 769, 1281, 1537]
        "null": "null:2",
    }

    type_definition = {"name_index": "uint:2", "index": "uint:2"}

    effect_definition = {
        "name_index": "uint:2",
        "desc_index": "uint:2",
        "index": "uint:2",
    }

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        weapon_count = self.read_header(buffer)
        map_weapon_count = self.read_int(buffer.read(4))
        map_weapon_pointer = self.read_int(buffer.read(4))
        type_pointer = self.read_int(buffer.read(4))
        effect_pointer = self.read_int(buffer.read(4))

        weapons = self.read_records(self.definition, buffer, weapon_count)

        buffer.seek(map_weapon_pointer)
        map_weapons = self.read_records(
            self.map_weapon_definition, buffer, map_weapon_count
        )

        print("weapons")
        for k in weapons[0].keys():
            print(k, sorted({w[k] for w in weapons}))

        print("map_weapons")
        for k in map_weapons[0].keys():
            print(k, sorted({w[k] for w in map_weapons}))

        buffer.seek(type_pointer)
        type_count = self.read_int(buffer.read(4))
        types = self.read_records(self.type_definition, buffer, type_count)

        buffer.seek(effect_pointer)
        effect_count = self.read_int(buffer.read(4))
        effects = self.read_records(self.effect_definition, buffer, effect_count)

        records = weapons + map_weapons + types + effects

        return records


""" DAT files """


class DlcList(GundamDataFile):
    default_filename = "DlcList.dat"
    header = b"\x08\x80\x80\x80\x08\x12\x04\x08"
    
    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        
        return string_bytes
    
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
    definition = {
        "effect_id": "uint:4",
        "effect_name": "string_len_prefix",
    }


class MapWeaponList(GundamDataFile):
    default_filename = "mapWeaponList.dat"
    header = b"\x57\x4D\x4D\x54"
    
    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        
        return string_bytes
    
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
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        
        return string_bytes
    
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
    data_path = "data/tmap/resident"
    header = b"\x44\x4C\x55\x50"
    
    definition = {
        "stage_id": "uint:4",
        "part": "uint:1",
        "guid": "string_len_prefix",
        "null1": "null:4",
        "effect_name": "string_len_prefix",
        "null2": "null:25",
        "unk1": "uint:2",
        "unk2": "uint:2",
    }


class ScoutMessageId(GundamDataFile):
    default_filename = "scoutMessageid.dat"
    data_path = "data/tmap/resident"
    header = b"\x4D\x53\x4D\x54"
    record_count_length = 2
    definition = {
        "string": "string_len_prefix",
        "unk1": "uint:1",
        "unk2": "uint:1",
        "unk3": "uint:1",
    }


class SteamDlcGroupList(GundamDataFile):
    default_filename = "SteamDlcGroupList.dat"
    header = b""
    
    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        
        return string_bytes
    
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
        record_count = len(records)
        string_bytes = self.write_header(record_count)
        
        return string_bytes
    
    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = []

        # incomplete mess
        
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
                "values2": [self.read_int(buffer.read(1), signed=True) for _ in
                    range(36)],
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
