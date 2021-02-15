from io import BytesIO
from typing import List, Dict, BinaryIO

from .data import GundamDataFile
from .strings import StringTBL

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
    data_path = "resident"
    default_filename = "AbilitySpecList.cdb"
    signature = b"\x4C\x4C\x42\x41\x00\x00\x0D\x01"
    constants = {
        # "fixed99": 99,
        "fixed1": 1
    }

    definitions = {
        "unitAbilities": {  # 8 bytes now 16
            "index": "uint:2",
            "name": "uint:2",
            "effect": "uint:2",
            # "unk1": "uint:2",
            "unk2": "2cfpointer:list:uint:2",
            "null": "null:4",
        },
        "unitModifications": {  # 40 bytes now 60
            "index": "uint:2",
            "name": "int:2",
            "effect": "uint:2",
            "unk1": "2cfpointer:list:uint:2",
            # "unk2": "uint:4",
            # "unk3": "pointer",
            "unk3": "cfpointer:list:int:6",
            "unk4": "pointer",
            "cost": "uint:2",
            "dlc_set": "uint:2",
            "sort_effect": "uint:2",
            "sort_japanese": "uint:2",
            "sort_t_chinese": "int:2",
            "sort_s_chinese": "int:2",
            "sort_korean": "int:2",
            "sort_english": "int:2",
            "null1": "null:10",
            "unlock_order": "uint:2",
            "unk5": "uint:2",
            "unk6": "uint:2",
            "flag": "uint:2",
            "unk7": "uint:2",
        },
        "characterAbilities": {  # 34 bytes now 40
            "index": "uint:2",
            "name": "uint:2",
            "effect": "uint:2",
            "unk1": "uint:2",
            "unk2": "uint:1",
            "unk3": "uint:1",
            "unk4": "uint:2",
            "sort_effect": "uint:2",
            "sort_japanese": "uint:2",
            "sort_t_chinese": "int:2",
            "sort_s_chinese": "int:2",
            "sort_korean": "int:2",
            "sort_english": "int:2",
            "unk5": "uint:2",
            "unk6": "uint:2",
            "unk7": "uint:2",
            "unk8": "uint:2",
            "unk9": "uint:2",
            "cost": "uint:2",
            "rarity": "uint:1",
            "unk10": "uint:1",
            "unk11": "uint:2",
        },
        "characterSkills": {  # 14 bytes still
            "index": "uint:2",
            "name": "uint:2",
            "effect": "uint:2",
            "desc": "uint:2",
            "number": "uint:1",
            # 1 = 1 Character in area   001
            # 2 = All units in area     010
            # 3 = All units on map      011
            # 5 = 1 warship unit        101
            "valid_targets": "uint:1",
            # 0 = All
            # 1 = Own forces
            # 1 = Own/Guest forces
            # 2 = Own forces (Group Only)
            "length": "uint:1",
            # 0 = Immediate
            # 1 = Lasts for 1 turn
            # 2 = Once
            "stack": "uint:1",
            "priority": "uint:1",
            "unk8": "uint:1",  # 0 & 1 - offense vs defense?
        },
        "effects": {  # 132 bytes
            "desc": "uint:2",
            "unit_hp": "int:2",
            "unit_energy": "int:2",
            "unit_attack": "int:2",
            "unit_defense": "int:2",
            "unit_mobility": "int:2",
            "power_ranged": "int:2",
            "power_melee": "int:2",
            "power_physical": "int:2",
            "power_beam": "int:2",
            "power_map": "int:2",
            "power_linkup_warship": "int:2",
            "power_linkup_raid": "int:2",
            "char_melee": "int:2",
            "char_ranged": "int:2",
            "char_defense": "int:2",
            "char_reaction": "int:2",
            "char_awaken": "int:2",
            "char_command": "int:2",
            "char_auxiliary": "int:2",
            "char_communication": "int:2",
            "char_navigation": "int:2",
            "char_maintenance": "int:2",
            "char_charisma": "int:2",
            "adjust_mp": "int:2",
            "adjust_hp": "int:2",
            "adjust_en": "int:2",
            "bonus_xp": "int:2",
            "bonus_score": "int:2",
            "sell_price": "int:2",
            "received_physical_ranged": "int:2",
            "received_physical_melee": "int:2",
            "received_beam_ranged": "int:2",
            "received_beam_melee": "int:2",
            "received_special_ranged": "int:2",
            "received_special_melee": "int:2",
            "received_map": "int:2",
            "nullify_physical_ranged": "int:2",
            "nullify_physical_melee": "int:2",
            "nullify_beam_ranged": "int:2",
            "nullify_beam_melee": "int:2",
            "null2": "null:4",
            "reduce_map": "int:2",
            "damage_dealt": "int:2",
            "damage_taken": "int:2",
            "condition1": "int:2",
            "condition2": "int:2",
            "condition3": "int:2",
            "filter": "uint:1",
            "null3": "null:1",
            "movement": "int:1",
            "terrain_space": "int:1",
            "terrain_atmospheric": "int:1",
            "terrain_ground": "int:1",
            "terrain_surface": "int:1",
            "terrain_underwater": "int:1",
            "range_ranged": "int:1",
            "range_melee": "int:1",
            "range_physical": "int:1",
            "range_beam": "int:1",
            "null4": "null:1",
            "consumption_en_ranged": "int:1",
            "consumption_en_melee": "int:1",
            "consumption_en_physical": "int:1",
            "consumption_en_beam": "int:1",
            "consumption_en_map": "int:1",
            "null5": "null:1",
            "consumption_mp": "int:1",
            "crit_rate_ranged": "int:1",
            "crit_rate_melee": "int:1",
            "crit_rate_physical": "int:1",
            "crit_rate_beam": "int:1",
            "null6": "null:1",
            "accuracy": "int:1",
            "evasion": "int:1",
            "null7": "null:1",
            "max_chance_step": "int:1",
            "max_areas": "int:1",
            "null8": "null:1",
            "range": "int:1",
            "type": "int:2",
            # 0 = passive
            # 1 = start of turn
            #    condition3 = stack?
            # 4 = morale is high
            # 5 = conditional on stat
            # 6 = conditional on ability
            # 9 =
        },
    }

    ability_filters = [
        "pilot",
        "warship",
        "unit",
        "weapon",
        "recovery",
        "accuracy",
        "reduce",
        "other",
    ]

    mod_flags = [
        "ms_usable",
        "ws_usable",
        "flag_unk",
        "type1",
        "type2",
        # 1 = on damage
        # 2 =
        # 3 = start of turn
        "grant_ability",
        # condition1 + 1000
        "rarity1",
        "rarity2",
    ]

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {
                table: cls.read_int(buffer.read(cls.record_count_length))
                for table, definition in cls.definitions.items()
            },
            "pointers": {},
            "size": {
                table: cls.definition_size(definition)
                for table, definition in cls.definitions.items()
            },
        }

        # seems to be the same value as unit mod count
        cls.read_int(buffer.read(4))

        tables = list(cls.definitions.keys())
        for table in tables[1:]:
            header["pointers"][table] = cls.read_int(buffer.read(4))
        header["pointers"][tables[0]] = buffer.tell()

        return header

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        for r in records["effects"]:
            r.update(cls.bit_smash("filter", r.pop("filter"), cls.ability_filters))

        for r in records["unitModifications"]:
            r.update(cls.bit_smash("", r.pop("flag"), cls.mod_flags))
            r["rarity"] = r.pop("rarity1", 0) + (r.pop("rarity2", 0) * 2)
            r["type"] = r.pop("type1", 0) + (r.pop("type2", 0) * 2)

        return records

    @classmethod
    def pre_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        for r in records["effects"]:
            r["filter"] = cls.bit_smush("filter", r, cls.ability_filters)

        for r in records["unitModifications"]:
            r["rarity1"] = r["rarity"] % 2
            r["rarity2"] = r["rarity"] // 2
            r["type1"] = r["type"] % 2
            r["type2"] = r["type"] // 2

            r["flag"] = cls.bit_smush("", r, cls.mod_flags)

        return records


class ActAbilityEffectList(GundamDataFile):
    data_path = "tmap/resident"
    default_filename = "ActAbilityEffectList.cdb"
    signature = b"\x4C\x45\x41\x41\x00\x00\x01\x01"
    definitions = {
        "units": {"guid": "guid", "unknown1": "uint:4", "unknown2": "uint:4"}
    }


class BattleBgList(GundamDataFile):
    data_path = "resident"
    package = "CellAttributeList.pkd"
    default_filename = "BattleBgList.cdb"
    signature = b"\x47\x42\x54\x42\x00\x00\x00\x01"
    definitions = {
        "bgm": {
            "bgm1": "pointer:string_null_term",
            "bgm2": "pointer:string_null_term",
            "bgm3": "pointer:string_null_term",
            "value": "uint:4",
        }
    }

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        fields = ["bgm1", "bgm2", "bgm3"]
        main_table = "bgm"

        # Consolidate all the string into a set
        all_strings = []
        for r in records[main_table]:
            for f in fields:
                if r[f] not in all_strings:
                    all_strings.append(r[f])

        pointer = 0
        locations = {}
        index_end = (
            len(records[main_table])
            * self.definition_size(self.definitions[main_table])
        ) + 12
        for t in all_strings:
            locations[t] = pointer + index_end
            pointer += len(t.encode("utf-8")) + 1

        # and then assign them to the records
        for r in records[main_table]:
            location = 12
            for f in fields:
                r[f] = locations[f] - location

        byte_blocks = {
            main_table: self.write_records(
                self.definitions[main_table], records[main_table]
            ),
            "all_strings": b"\x00".join([b.encode("utf-8") for b in all_strings])
            + b"\x00",
        }
        header = self.make_basic_header(records, byte_blocks)
        header_bytes = self.write_header(header)
        string_bytes = self.combine_blocks(byte_blocks, header_bytes)

        return string_bytes


class BTLIdSet(GundamDataFile):
    default_filename = "idset.tbl"
    data_path = "sound/voice/BTL"
    signature = b"\x54\x53\x44\x49\x00\x01\x02\x00"

    definitions = {"ids": {"guint": "uint:4"}}


class BTLVoiceTable(GundamDataFile):
    default_filename = "voice_table.tbl"
    data_path = "sound/voice/BTL"
    signature = b"\x54\x4F\x56\x42\x00\x04\x02\x00"

    definitions = {"voices": {"guint": "uint:4"}}


class CellAttributeList(GundamDataFile):
    default_filename = "CellAttributeList.cdb"
    data_path = "resident"
    package = "CellAttributeList.pkd"
    signature = b"\x4C\x54\x41\x43\x00\x00\x03\x01"
    definitions = {
        "cells": {
            "name": "pointer:string_null_term",
            "index": "uint:2",
            "type": "uint:1",
            "unk1": "int:1",
            "unk2": "int:1",
            "unk3": "int:1",
            "unk4": "int:1",
            "unk5": "int:1",
            "unk6": "int:1",
            "unk7": "int:1",
            "unk8": "int:1",
            "unk9": "int:1",
            "unk10": "int:1",
            "unk11": "int:1",
            "unk12": "int:1",
            "unk13": "int:1",
            "unk14": "int:1",
            "unk15": "int:1",
            "unk16": "int:1",
            "unk17": "int:1",
        }
    }


class CharacterConversionList(GundamDataFile):
    default_filename = "CharacterConversionList.cdb"
    data_path = "resident"
    signature = b"\x4C\x56\x43\x43\x00\x00\x00\x01"
    constants = {"fixed1": 1}
    definitions = {
        "characters": {"character": "guid", "conversion": "guid", "fixed1": "uint:4"}
    }


class CharacterGrowthList(GundamDataFile):
    default_filename = "CharacterGrowthList.cdb"
    data_path = "resident"
    package = "CharacterSpecList.pkd"
    signature = b"\x52\x47\x48\x43\x00\x00\x02\x01"
    level_ups = 98  # This is blowing up to 998 for the expansion
    constants = {"fixed332": 332}
    definitions = {
        "profiles": {
            "fixed332": "uint:2",
            "level2": "uint:2",
            "level3": "uint:2",
            "level4": "uint:2",
            "level5": "uint:2",
            "level6": "uint:2",
            "level7": "uint:2",
            "level8": "uint:2",
            "level9": "uint:2",
            "level10": "uint:2",
            "level11": "uint:2",
            "level12": "uint:2",
            "level13": "uint:2",
            "level14": "uint:2",
            "level15": "uint:2",
            "level16": "uint:2",
            "level17": "uint:2",
            "level18": "uint:2",
            "level19": "uint:2",
            "level20": "uint:2",
            "level21": "uint:2",
            "level22": "uint:2",
            "level23": "uint:2",
            "level24": "uint:2",
            "level25": "uint:2",
            "level26": "uint:2",
            "level27": "uint:2",
            "level28": "uint:2",
            "level29": "uint:2",
            "level30": "uint:2",
            "level31": "uint:2",
            "level32": "uint:2",
            "level33": "uint:2",
            "level34": "uint:2",
            "level35": "uint:2",
            "level36": "uint:2",
            "level37": "uint:2",
            "level38": "uint:2",
            "level39": "uint:2",
            "level40": "uint:2",
            "level41": "uint:2",
            "level42": "uint:2",
            "level43": "uint:2",
            "level44": "uint:2",
            "level45": "uint:2",
            "level46": "uint:2",
            "level47": "uint:2",
            "level48": "uint:2",
            "level49": "uint:2",
            "level50": "uint:2",
            "level51": "uint:2",
            "level52": "uint:2",
            "level53": "uint:2",
            "level54": "uint:2",
            "level55": "uint:2",
            "level56": "uint:2",
            "level57": "uint:2",
            "level58": "uint:2",
            "level59": "uint:2",
            "level60": "uint:2",
            "level61": "uint:2",
            "level62": "uint:2",
            "level63": "uint:2",
            "level64": "uint:2",
            "level65": "uint:2",
            "level66": "uint:2",
            "level67": "uint:2",
            "level68": "uint:2",
            "level69": "uint:2",
            "level70": "uint:2",
            "level71": "uint:2",
            "level72": "uint:2",
            "level73": "uint:2",
            "level74": "uint:2",
            "level75": "uint:2",
            "level76": "uint:2",
            "level77": "uint:2",
            "level78": "uint:2",
            "level79": "uint:2",
            "level80": "uint:2",
            "level81": "uint:2",
            "level82": "uint:2",
            "level83": "uint:2",
            "level84": "uint:2",
            "level85": "uint:2",
            "level86": "uint:2",
            "level87": "uint:2",
            "level88": "uint:2",
            "level89": "uint:2",
            "level90": "uint:2",
            "level91": "uint:2",
            "level92": "uint:2",
            "level93": "uint:2",
            "level94": "uint:2",
            "level95": "uint:2",
            "level96": "uint:2",
            "level97": "uint:2",
            "level98": "uint:2",
            "level99": "uint:2",
        },
        "level_ups": {
            "cmd": "uint:1",
            "rng": "uint:1",
            "mel": "uint:1",
            "def": "uint:1",
            "rct": "uint:1",
            "awk": "uint:1",
            "aux": "uint:1",
            "com": "uint:1",
            "nav": "uint:1",
            "mnt": "uint:1",
            "chr": "uint:1",
        },
    }

    @classmethod
    def pre_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        # make a unique list of stat increases
        # replace their entries with the index to those increases

        records["level_ups"] = []
        unique_lu = []

        for r in records["profiles"]:
            for level, lu in r.items():
                if not level.startswith("level"):
                    continue
                level_up = tuple([lu.get(cs, 0) for cs in CHARACTER_STATS])
                if level_up not in unique_lu:
                    unique_lu.append(level_up)
                    records["level_ups"].append(lu)
                    r[level] = len(records["level_ups"]) - 1

        return records

    @classmethod
    def calculate_header(
        cls, records: Dict[str, List[Dict]], byte_blocks: Dict[str, bytes]
    ) -> Dict[str, Dict[str, int]]:
        header = {
            "counts": {
                "profiles": len(records["profiles"]),
                "level_ups": len(records["level_ups"]),
            },
            "pointers": {"level_ups": len(byte_blocks["profiles"]) + 20},
        }
        return header

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        for r in records["profiles"]:
            for k, v in r.items():
                if k.startswith("level"):
                    r[k] = records["level_ups"][v]

        return records


class CharacterSpecList(GundamDataFile):
    default_filename = "CharacterSpecList.cdb"
    data_path = "resident"
    package = "CharacterSpecList.pkd"
    signature = b"\x4C\x53\x48\x43\x00\x00\x07\x02"
    definitions = {
        "characters": {
            "guid": "guid",
            "cutin_guid": "guid",
            "image_guid": "guid",
            "index": "int:2",
            "dlc": "uint:2",
            "name": "uint:2",
            "unk1": "uint:1",
            "unk2": "uint:1",
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
            "unique_name": "int:2",
            "unk3a": "uint:1",
            "unk3b": "uint:1",
            "sort_japanese": "uint:2",
            "sort_t_chinese": "int:2",
            "sort_s_chinese": "int:2",
            "sort_korean": "int:2",
            "sort_english": "int:2",
            "null": "null:10",
            "scout_cost": "uint:2",
            "skill_acquisition_pattern": "int:2",
            "scoutable": "uint:4",
        },
        "custom": {
            "guid": "guid",
            "cutin_guid": "guid",
            "image_guid": "guid",
            "index": "int:2",
            "dlc": "uint:2",
            "name": "uint:2",
            "unk1": "uint:1",
            "unk2": "uint:1",
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
            "unique_name": "int:2",
            "unk3a": "uint:1",
            "unk3b": "uint:1",
            "sort_japanese": "uint:2",
            "sort_t_chinese": "int:2",
            "sort_s_chinese": "int:2",
            "sort_korean": "int:2",
            "sort_english": "int:2",
            "null": "null:10",
            "scout_cost": "uint:2",
            "skill_acquisition_pattern": "int:2",
            "scoutable": "uint:4",
        },
        "npcs": {
            "guid": "guid",
            "cutin_guid": "guid",
            "image_guid": "guid",
            "index": "int:2",
            "dlc": "uint:2",
            "name": "uint:2",
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
        },
        "personalities": {
            "index": "uint:1",
            "timid": "uint:1",
            "normal": "uint:1",
            "high": "uint:1",
        },
    }

    @classmethod
    def pre_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        personalities = []
        for r in records["characters"]:
            personality = (
                r["personality"]["timid"],
                r["personality"]["normal"],
                r["personality"]["high"],
            )
            if personality not in personalities:
                personalities.append(
                    {
                        "index": len(personalities) + 1,
                        "timid": personality[0],
                        "normal": personality[1],
                        "high": personality[2],
                    }
                )
            r["personality"] = personalities.index(personality)
        records["personalities"] = personalities

        return records

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        records = self.pre_processing(records)

        byte_blocks = {}
        for table, definition in self.definitions.items():
            byte_blocks[table] = self.write_records(definition, records[table])

        byte_blocks["personalities"] = (
            self.write_int(len(records["personalities"]), 4)
            + byte_blocks["personalities"]
        )

        all_count = len(records["characters"]) + len(records["custom"])
        string_bytes = self.signature
        string_bytes += self.write_int(all_count, 4)
        string_bytes += self.write_int(len(records["npcs"]), 4)
        npc_pointer = len(string_bytes) + len(byte_blocks["characters"]) + 12

        string_bytes += self.write_int(npc_pointer, 4)
        personality_pointer = npc_pointer + len(byte_blocks["npcs"])
        string_bytes += self.write_int(personality_pointer, 4)

        string_bytes += self.write_int(len(records["characters"]), 2)
        string_bytes += self.write_int(len(records["custom"]), 2)

        for table, definition in self.definitions.items():
            string_bytes += byte_blocks[table]

        return string_bytes

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {
                "characters": cls.read_int(buffer.read(cls.record_count_length)),
                "npcs": cls.read_int(buffer.read(cls.record_count_length)),
            },
            "pointers": {
                "npcs": cls.read_int(buffer.read(4)),
                "personalities": cls.read_int(buffer.read(4)),
            },
            "size": {
                table: cls.definition_size(definition)
                for table, definition in cls.definitions.items()
            },
        }

        # it then gives a count for characters & custom characters
        header["counts"]["characters"] = cls.read_int(buffer.read(2))
        header["counts"]["custom"] = cls.read_int(buffer.read(2))

        header["pointers"]["characters"] = buffer.tell()
        character_block_size = (
            header["size"]["characters"] * header["counts"]["characters"]
        )
        header["pointers"]["custom"] = (
            header["pointers"]["characters"] + character_block_size
        )

        buffer.seek(header["pointers"]["personalities"])
        header["counts"]["personalities"] = cls.read_int(buffer.read(4))
        header["pointers"]["personalities"] += 4

        return header

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:

        people = ["characters", "custom", "npcs"]
        for p in people:
            for r in records[p]:
                r["personality"] = records["personalities"][r["personality"]]

        return records


class CockpitBgTable(GundamDataFile):
    default_filename = "cockpit_bg_table.atp"
    data_path = "battle/table"
    signature = b"\xC2\x3E\x10\x0A"
    record_count_length = 0


class CreditBgmList(GundamDataFile):
    default_filename = "CreditBgmList.cdb"
    data_path = "resident"
    signature = b""


class CutIn(GundamDataFile):
    default_filename = "cutin.tbl"
    data_path = "battle/table"
    signature = b"\x54\x54\x55\x43\x00\x01\x01\x00"
    definitions = {
        "main": {
            # 28 bytes
            "fprefix": "uint:4",
            "null1": "null:1",
            "unk2": "uint:1",
            "unk3": "binary:1",
            "null2": "null:3",
            "unk5b": "uint:2",
            "unk6": "uint:1",
            "unk7": "uint:1",
            "unk8": "uint:1",
            "unk9": "uint:1",
            "guid": "uint:4",  # for special cutins?
            "null3": "null:8",
        }
    }

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = super().read(buffer)

        # There's then a normal string table attached to the end
        strings = StringTBL().read(BytesIO(buffer.read()))["strings"]

        for r in records["main"]:
            index = r["fprefix"]
            r["fprefix"] = strings[index]["string"]

        return records


class DatabaseCalculation(GundamDataFile):
    # Yes, the source file is misspelled
    default_filename = "DatabaseCalcuclation.cdb"
    data_path = "resident"
    package = "MiscData.pkd"
    signature = b"\x43\x4C\x41\x43\x00\x00\x0A\x01"

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        return {}


class GalleryMovieList(GundamDataFile):
    default_filename = "GalleryMovieList.cdb"
    data_path = "resident"
    signature = b"\x4C\x56\x4D\x47\x00\x00\x00\x01"


class GetUnitList(GundamDataFile):
    default_filename = "GetUnitList.cdb"
    data_path = "resident"
    signature = b"\x00\x00\x00\x01\x4C\x54\x55\x47"
    definitions = {"units": {"get": "guid", "score": "uint:4"}}


class GroupSendingMissionList(GundamDataFile):
    default_filename = "GroupSendingMissionList.cdb"
    data_path = "resident"
    package = "MiscData.pkd"
    signature = b"\x4C\x53\x50\x47\x00\x00\x07\x01"

    definitions = {
        "missions": {
            "difficulty": "uint:4",
            "total_completion": "uint:4",
            "recommended": "pointer:list:bytes:16",  # 16 bytes
            "capital": "uint:4",
            "onetime": "pointer:list:bytes:12",  # 12 bytes
            "units": "pointer:list:bytes:12",  # 12 bytes
            "characterAbilities": "pointer:list:bytes:4",  # 4 bytes
            "unitModifications": "pointer:list:bytes:4",  # 4 bytes
            "availability": "pointer:list:uint:1",  # 1 byte
            "null": "null:8",
            "dlc_set": "uint:2",
            "dispatch_id": "uint:2",
            "dispatch_id2": "uint:2",
            "name": "uint:2",
            "description": "uint:2",
            "dispatch_time": "uint:2",
            "exp": "uint:2",
            "unknown24": "uint:2",
            "unknown25": "uint:2",
            "timing": "uint:1",
            "terrain": "uint:1",
            "cooldowns": "uint:1",
            "cooldown_threshold": "uint:1",
            "null2": "null:2",
        }
    }

    child_definitions = {
        "recommended": {
            "filter_pointer": "uint:4",
            "filter_count": "uint:4",
            "bonus": "uint:2",
            "name": "uint:2",
            "unk2": "uint:4",
        },
        "onetime": {
            "id": "bytes:8",  # depends on type
            "completion": "uint:1",
            "type": "uint:1",
            "null": "null:2",
        },
        "units": {
            "unit": "guid",
            "threshold": "uint:1",
            "quantity": "uint:1",
            "null": "null:2",
        },
        "unitModifications": {
            "unitModification": "uint:2",
            "threshold": "uint:1",
            "quantity": "uint:1",
        },
        "characterAbilities": {
            "characterAbility": "uint:2",
            "threshold": "uint:1",
            "quantity": "uint:1",
        },
    }

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        terrain = ["atmospheric", "ground", "underwater"]

        for i, record in enumerate(records["missions"]):
            for field, definition in cls.child_definitions.items():
                record[field] = [
                    cls.read_record(definition, BytesIO(val))
                    for val in record.pop(field)
                ]

            del record["dispatch_id2"]

            for cr in record["onetime"]:
                if cr["type"] in [1]:
                    guid = cls.read_guid_bytes(cr.pop("id"))
                    if "C" in guid:
                        cr["character"] = guid
                    else:
                        # rewards just the unit
                        # doesn't register it
                        cr["unit"] = guid
                elif cr["type"] in [2, 3, 4, 5]:
                    # only use last 4 bytes
                    value = cls.read_int(cr.pop("id")[4:8])
                    if cr["type"] == 2:
                        cr["unitModification"] = value
                    elif cr["type"] == 3:
                        cr["characterAbility"] = value
                    elif cr["type"] == 4:
                        cr["bgm"] = value
                    elif cr["type"] == 5:
                        cr["cooldowns"] = value

            record["terrain_space"] = 1 if record["terrain"] == 0 else 0
            record.update(cls.bit_smash("terrain", record.pop("terrain"), terrain))

        return records


class IdSet(GundamDataFile):
    default_filename = "idset.tbl"
    data_path = "battle/table"
    signature = b"\x54\x53\x44\x49\x00\x01\x02\x00"
    definitions = {
        "main": {
            # 68 bytes
            "guid": "uint:4",
            "null1": "null:1",
            "unk1": "uint:1",
            "null2": "null:4",
            "unk4": "uint:2",
            "null3": "null:56",
        }
    }

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {
                "main": cls.read_int(buffer.read(4)),
                "unk1": cls.read_int(buffer.read(4)),
                "unk2": cls.read_int(buffer.read(4)),
                "unk3": cls.read_int(buffer.read(4)),
            },
            "pointers": {"main": buffer.tell()},
        }

        return header

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = super().read(buffer)

        return records


class MachineConversionList(GundamDataFile):
    default_filename = "MachineConversionList.cdb"
    data_path = "resident"
    package = "MachineSpecList.pkd"
    signature = b"\x56\x4E\x43\x4D\x00\x00\x02\x01"
    definitions = {"units": {"unit": "guid", "transform": "guid", "type": "uint:4"}}

    conversion_types = {
        2: "refit_1",
        3: "refit_2",
        4: "refit_3",
        5: "purge",
        6: "escape",
        8: "leader",
        16: "transform",
        19: "special",  # only used for
    }


class MachineDesignList(GundamDataFile):
    default_filename = "MachineDesignList.cdb"
    data_path = "resident"
    package = "MachineSpecList.pkd"
    signature = b"\x49\x53\x44\x4D\x00\x00\x02\x01"
    definitions = {
        "designs": {
            "first": "guid",
            "second": "guid",
            "result": "guid",
            "index": "uint:4",
        }
    }


class MachineDevelopmentList(GundamDataFile):
    default_filename = "MachineDevelopmentList.cdb"
    data_path = "resident"
    package = "MachineSpecList.pkd"
    signature = b"\x56\x45\x44\x4D\x00\x00\x02\x01"
    definitions = {
        "units": {
            "unit": "guid",
            "children_pointer": "pointer",
            "index": "uint:2",
            "children_count": "uint:2",
        }
    }
    child_definition = {"guid": "guid", "level": "uint:4"}

    @classmethod
    def pre_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        child_size = cls.definition_size(cls.definitions["children"])
        pointer = 12 + len(records["units"]) * child_size
        records["children"] = []
        for i, record in enumerate(records["units"]):
            record["children_pointer"] = pointer
            record["children_count"] = len(record["children"])
            records["children"].extend(record["children"])
            pointer += child_size * record["children_count"]

        return records

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        byte_string = super().write(records)
        for record in records["units"]:
            for child in record["children"]:
                byte_string += self.write_record(self.child_definition, child)

        return byte_string

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = super().read(buffer)

        for record in records["units"]:
            record["children"] = []
            buffer.seek(record.pop("children_pointer"))

            for _ in range(record.pop("children_count")):
                child = self.read_record(self.child_definition, buffer)
                record["children"].append(child)

        return records


class MachineGrowthList(GundamDataFile):
    default_filename = "MachineGrowthList.cdb"
    data_path = "resident"
    package = "MachineSpecList.pkd"
    signature = b"\x00\x00\x02\x01\x52\x47\x43\x4D"
    definitions = {
        "table1": {
            "unk1": "uint:2",
            "index": "uint:1",
            "unk3": "uint:1",
            "unk4": "uint:1",
            "unk5": "uint:1",
            "unk6": "uint:2",
        },
        "table2": {"unk1": "uint:2", "index": "uint:2"},
        "table3": {"unk1": "uint:2", "index": "uint:2"},
    }


class MachineSpecList(GundamDataFile):
    default_filename = "MachineSpecList.cdb"
    data_path = "resident"
    package = "MachineSpecList.pkd"
    signature = b"\x4C\x53\x43\x4D\x03\x00\x05\x02"
    constants = {"fixed7": 7, "wsfixed100": 100, "wsfixed80": 80, "wsfixed70": 70}

    definitions = {
        "units": {
            "guid": "guid",  # profile?
            "guid2": "guid",  # dev list?
            "guid3": "guid",
            "hp": "uint:4",
            "index1": "uint:2",
            "dlc_set": "uint:2",
            "name": "uint:2",
            "unk1": "uint:2",  # 0 - 248 (49 distinct)
            # "unk2": "uint:1",
            "unk3": "uint:2",  # 0 - 255 (172 distinct)
            # "unk4": "uint:1",  # mostly 0, increments slowly through list to 76
            "unk5": "uint:1",  # increments of 2, 127 distinct
            "unk6": "uint:1",  # 0 - 167, 133 distinct
            "sort_japanese": "uint:2",
            "sort_t_chinese": "int:2",
            "sort_s_chinese": "int:2",
            "sort_korean": "int:2",
            "sort_english": "int:2",
            "null1": "null:10",
            "cost": "uint:2",
            "energy": "uint:2",
            "attack": "uint:2",
            "defense": "uint:2",
            "mobility": "uint:2",
            "base_exp_level_up": "uint:2",
            "points": "uint:2",
            "unk10": "uint:1",
            "unk11": "uint:1",
            "unk12": "uint:1",
            "unk13": "uint:1",
            "size": "uint:1",
            "fixed7": "uint:1",
            "ability1": "int:2",
            "ability2": "int:2",
            "ability3": "int:2",
            "ability4": "int:2",
            "ability5": "int:2",
            "weapons": "int:2",
            "map_weapons": "int:2",
            "movement": "uint:1",
            "unk15": "int:1",  # footprint?
            "unk16": "int:1",
            "weapon_count": "uint:1",
            "map_weapon_count": "uint:1",
            "unk17": "int:1",
            "shadow": "uint:1",
            "unk18": "null:3",
            "unk20": "uint:1",
            "unk21": "uint:1",
            "unk22": "uint:1",
            "null3": "null:1",
        },
        "warships": {
            "guid": "guid",  # profile?
            "guid2": "guid",  # dev list?
            "guid3": "guid",
            "hp": "uint:4",
            "index1": "uint:2",
            "dlc_set": "uint:2",
            "name": "uint:2",
            "unk1": "uint:1",
            "unk2": "uint:1",
            "unk3": "uint:1",
            "unk4": "uint:1",
            "unk5": "uint:1",
            "unk6": "uint:1",
            "sort_japanese": "uint:2",
            "sort_t_chinese": "int:2",
            "sort_s_chinese": "int:2",
            "sort_korean": "int:2",
            "sort_english": "int:2",
            "null": "null:10",
            "cost": "uint:2",
            "energy": "uint:2",
            "attack": "uint:2",
            "defense": "uint:2",
            "mobility": "uint:2",
            "base_exp_level_up": "uint:2",
            "points": "uint:2",
            "unk9": "uint:1",
            "unk10": "uint:1",
            "unk11": "uint:1",
            "unk12": "uint:1",
            "size": "uint:1",
            "fixed7": "uint:1",
            "ability1": "int:2",
            "ability2": "int:2",
            "ability3": "int:2",
            "ability4": "int:2",
            "ability5": "int:2",
            "weapons": "int:2",
            "map_weapons": "int:2",
            "movement": "uint:1",
            "unk14": "int:1",  # footprint?
            "unk15": "int:1",
            "weapon_count": "uint:1",
            "map_weapon_count": "uint:1",
            "unk16": "int:1",  # -1, 0, 2, 4
            "shadow": "uint:1",
            "unk17": "null:3",
            "teams": "uint:1",  # 0, 1, 2
            "wsfixed100": "uint:1",  # 100
            "wsfixed80": "uint:1",  # 80
            "wsfixed70": "uint:1",  # 70
        },
    }
    size_map = {}

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        flags = {
            "unk13": ["A", "B", "C", "D", "E", "F", "G", "H"],
            "unk20": [
                "gundam",
                "zaku",
                "--2",
                "--3",
                "tank",
                "no_defense",
                "ground",
                "space",
            ],
            "unk21": ["8", "9", "10", "11", "union_flag"],
            "unk22": ["ride_sfs", "sfs", "18", "commander", "unit"],
        }
        for k, v in flags.items():
            for r in records["units"]:
                r.update(**cls.bit_smash("flag", r.pop(k), v))
        return records

    @classmethod
    def calculate_header(
        cls, records: Dict[str, List[Dict]], byte_strings: Dict[str, bytes]
    ) -> Dict[str, Dict[str, int]]:
        header = cls.make_basic_header(records, byte_strings)
        header["counts"]["unk1"] = 457
        header["counts"]["unk1"] = 54

        header["pointers"]["warships"] = 32 + header["block_size"]["units"]
        header["pointers"]["file_size"] = (
            header["pointers"]["warships"] + header["block_size"]["warships"]
        )

        return header

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {
                "units": cls.read_int(buffer.read(4)),
                "warships": cls.read_int(buffer.read(4)),
            },
            "pointers": {},
            "unknown": {},
        }
        header["unknown"]["a"] = cls.read_int(buffer.read(4))  # unknown = 457
        header["unknown"]["b"] = cls.read_int(buffer.read(4))  # unknown = 54

        header["pointers"]["warships"] = cls.read_int(buffer.read(4))
        header["unknown"]["c"] = cls.read_int(buffer.read(4))  # file length?
        header["pointers"]["units"] = buffer.tell()

        return header


class MapTypes(GundamDataFile):
    default_filename = "MapTypes.cdb"
    data_path = "tmap/resident"
    signature = b"\x02\x00\x05\x01\x50\x59\x54\x4D"
    definitions = {
        "types": {
            "unk1": "uint:1",
            "unk2": "uint:1",
            "type1": "shpointer:string_null_term",
            "type2": "shpointer:string_null_term",
            "type3": "shpointer:string_null_term",
            "unk3": "uint:1",
            "unk4": "uint:1",
            "index": "uint:2",
        }
    }

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        header = self.calculate_header(records, {})
        header_bytes = self.write_header(header)

        fields = ["type1", "type2", "type3"]

        # Consolidate all the string into a set
        all_strings = []
        for r in records["types"]:
            for f in fields:
                if r[f] not in all_strings:
                    all_strings.append(r[f])

        pointer = 0
        locations = {}
        index_end = (header["counts"]["types"] * header["size"]["types"]) + len(
            header_bytes
        )
        for t in all_strings:
            locations[t] = pointer + index_end
            pointer += len(t.encode("utf-8")) + 1

        # and then assign them to the records
        for r in records["types"]:
            location = len(header_bytes)
            for f in fields:
                r[f] = locations[f] - location

        type_bytes = self.write_records(self.definitions["types"], records["types"])
        name_bytes = b"\x00".join([b.encode("utf-8") for b in all_strings]) + b"\x00"

        return header_bytes + name_bytes + type_bytes


class MyCharacterConfigurations(GundamDataFile):
    default_filename = "MyCharacterConfigurations.cdb"
    data_path = "resident"
    package = "CharacterSpecList.pkd"
    signature = b"\x43\x48\x43\x4D\x01\x00\x02\x01"
    constants = {"fixed71": 71}

    definitions = {
        "outfits": {
            "image_guid": "guid",
            "index": "uint:2",
            "name": "uint:2",
            "is_male": "uint:4",
        },
        "voices": {
            "voice_guid": "guid",
            "index": "uint:2",
            "name": "uint:2",
            "is_male": "uint:4",
        },
        "names": {"index": "uint:2", "name": "uint:2", "is_male": "uint:2"},
        "bgm": {
            "unknown": "pointer",
            "series": "uint:2",
            "fixed71": "uint:2",
            "null": "null:4",
            "index": "uint:2",
            "dlc_set": "uint:2",
            "name": "uint:2",
            "unk10": "uint:2",
        },
    }
    unknown_definition = {
        "unk1": "uint:1",
        "unk2": "uint:1",
        "unk3": "uint:1",
        "unk4": "uint:1",
    }

    @classmethod
    def calculate_header(
        cls, records: Dict[str, List[Dict]], byte_strings: Dict[str, bytes]
    ) -> Dict[str, Dict[str, int]]:
        header = cls.make_basic_header(records, byte_strings)
        header["pointers"]["outfits"] = 0
        header["pointers"]["voices"] = 40 + header["block_size"]["outfits"]
        header["pointers"]["names"] = (
            header["pointers"]["voices"] + header["block_size"]["voices"]
        )
        header["pointers"]["bgm"] = (
            header["pointers"]["names"] + header["block_size"]["names"]
        )

        return header

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        self.apply_constants(records)

        bgm = records.pop("bgm")
        byte_blocks = self.write_blocks(records)

        all_values = []
        unk_len = self.definition_size(self.unknown_definition)
        bgm_bytes = bytes()
        bgm_bytes_size = self.definition_size(self.definitions["bgm"]) * len(bgm)

        for r in bgm:
            vals = tuple(r["unknown"].values())
            if vals not in all_values:
                all_values.append(vals)
            r["unknown_pointer"] = (
                bgm_bytes_size - len(bgm_bytes) + (unk_len * all_values.index(vals))
            )
            bgm_bytes += self.write_record(self.definitions["bgm"], r)
        byte_blocks["bgm"] = bgm_bytes

        unk_bytes = bytes()
        for vals in all_values:
            unk_bytes += self.write_record(
                self.unknown_definition,
                {k: v for k, v in zip(self.unknown_definition.keys(), vals)},
            )
        byte_blocks["unk"] = unk_bytes

        header = self.calculate_header(records, byte_blocks)
        header_bytes = self.write_header(header)
        string_bytes = self.combine_blocks(byte_blocks, header_bytes)

        return string_bytes

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {
                "outfits": cls.read_int(buffer.read(4)),
                "voices": cls.read_int(buffer.read(4)),
                "names": cls.read_int(buffer.read(4)),
                "bgm": cls.read_int(buffer.read(4)),
            },
            "pointers": {
                "outfits": cls.read_int(buffer.read(4)) + 40,
                "voices": cls.read_int(buffer.read(4)),
                "names": cls.read_int(buffer.read(4)),
                "bgm": cls.read_int(buffer.read(4)),
            },
            "size": {
                table: cls.definition_size(definition)
                for table, definition in cls.definitions.items()
            },
        }

        return header

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = super().read(buffer)

        for r in records["bgm"]:
            buffer.seek(r.pop("unknown"))
            r["unknown"] = self.read_record(self.unknown_definition, buffer)

        return records


class PersonalMachineList(GundamDataFile):
    default_filename = "PersonalMachineList.cdb"
    data_path = "resident"
    package = "MachineSpecList.pkd"
    signature = b"\x4C\x43\x4D\x50\x00\x00\x00\x01"
    definitions = {"units": {"unit": "guid", "pilot": "guid", "custom": "guid"}}


class QuestList(GundamDataFile):
    default_filename = "QuestList.cdb"
    data_path = "resident"
    package = "StageList.pkd"
    signature = b"\x4C\x54\x45\x51\x00\x00\x02\x01"
    definitions = {
        "quests": {
            "guid1": "pointer:list:guid",
            "guid2": "pointer:list:bytes:8",
            "guid3": "pointer:list:guid",
            "quest_value": "uint:4",
            "stages": "pointer:list:bytes:4",
            "turns": "uint:2",
            "type": "uint:2",
            "null": "null:8",
            "series": "series",
            "stage": "bytes:4",
            "unitModifications": "pointer:list:uint:2",
            "productions": "pointer:list:guid",
            "characters": "pointer:list:guid",
            "characterAbilities": "pointer:list:uint:2",
            "prereq_stage_id": "uint:4",
            "quest": "uint:2",
            "dlc_set": "uint:2",
            "name": "uint:2",
            "desc2": "uint:2",
            "desc": "uint:2",
            "pre_req_quest": "uint:2",
            "hidden": "uint:1",  # TODO: 1 if visible from start, 2 if hidden
            "cooldowns": "uint:1",
            "null2": "null:2",
        }
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
        91: "Clear all stages in list",
        93: "Total number of kills",
        94: "Register number of units to production/scout lists",
        96: "Clear all stages in all series",
        99: "Unknown",
    }

    @classmethod
    def pre_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        for record in records["quests"]:
            if record["quest_type"] in [1, 96, 103]:
                record["stage"] = cls.write_series_bytes(record["stage"])
            else:
                record["stage"] = cls.write_int(record["stage"], 4)

            if record["quest_type"] in [96, 103]:
                record["stages"] = [cls.write_series_bytes(s) for s in record["stages"]]
            else:
                record["stages"] = [cls.write_int(s, 4) for s in record["stages"]]

            # instead of a guid it's an ability id
            if record["quest_type"] in [30]:
                # we need to skip 4 bytes
                record["guid2"] = [
                    b"\x00\x00\x00\x00" + cls.write_int(int(r), 4)
                    for r in record["guid2"]
                ]
            else:
                record["guid2"] = [cls.write_guid_bytes(r) for r in record["guid2"]]

        return records

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        for record in records["quests"]:
            # Just repeats the series id for some reason
            if record["type"] in [1, 96, 103]:
                record["stage"] = cls.read_series_bytes(record["stage"])
            else:
                record["stage"] = cls.read_int(record["stage"])

            if record["type"] in [96, 103]:
                record["stages"] = [cls.read_series_bytes(s) for s in record["stages"]]
            else:
                record["stages"] = [cls.read_int(s) for s in record["stages"]]

            # instead of a guid it's an ability id
            if record["type"] in [30]:
                # we need to skip 4 bytes
                record["guid2"] = [cls.read_int(r[4:8]) for r in record["guid2"]]
            else:
                record["guid2"] = [cls.read_guid_bytes(r) for r in record["guid2"]]

        return records


class RangeDataList(GundamDataFile):
    default_filename = "RangeDataList.cdb"
    data_path = "resident"
    signature = b"\x4C\x47\x4E\x52\x01\x00\x00\x01"

    # TODO: identify mask
    definitions = {"ranges": {"values": "pointer2c:list:uint:2", "mask": "uint:2"}}

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        header = super().read_header(buffer)
        header["counts"]["other"] = cls.read_int(buffer.read(4))
        header["pointers"]["ranges"] = buffer.tell()

        return header


class SeriesList(GundamDataFile):
    default_filename = "SeriesList.cdb"
    data_path = "resident"
    package = "MiscData.pkd"
    signature = b"\x4C\x52\x45\x53\x02\x00\x02\x01"
    # TODO: identify unknowns
    definitions = {
        "series": {
            "series_logo_l": "series",
            "series_logo_s": "series",
            "name": "uint:2",
            "era": "uint:1",
            "base_game": "uint:1",
        }
    }

    # Era names are in messagestring.tbl
    # starting from index = 109112
    ERA = {0: None, 1: "After Colony", 2: "Cosmic Era", 3: "A.D.", 4: "Post Disaster"}


class SeriesProfileList(GundamDataFile):
    default_filename = "SeriesProfileList.cdb"
    data_path = "resident"
    signature = b"\x4C\x50\x52\x53\x00\x00\x01\x01"
    definitions = {
        "main": {
            "gallery": "series",
            "index": "uint:2",
            # Name in MiscData.tbl, Profile in SeriesProfile.tbl
            "series_index": "uint:2",
        }
    }


class StageClearGetList(GundamDataFile):
    default_filename = "StageClearGetList.cdb"
    data_path = "tmap/stage"
    signature = b"\x43\x47\x54\x53\x00\x00\x00\x01"
    definitions = {"main": {"stage_id": "uint:4", "get_units": "cfpointer:list:guid"}}


class StageList(GundamDataFile):
    default_filename = "StageList.cdb"
    data_path = "resident"
    package = "StageList.pkd"
    signature = b"\x4C\x47\x54\x53\x00\x00\x0C\x01"
    constants = {
        "fixed100a": 100,
        "fixed100b": 100,
        "fixed30": 30,
        "fixed50": 50,
        "fixed70": 70,
    }

    definitions = {
        "stages": {
            "stage": "uint:4",
            "series": "series",
            "required_stage": "uint:4",
            "capital1": "uint:4",
            "capital2": "uint:4",
            "capital3": "uint:4",
            "capital4": "uint:4",
            "capital5": "uint:4",
            "capital6": "uint:4",
            "capital7": "uint:4",
            "units_available_count": "uint:4",
            "units_available_pointer": "pointer",
            "dlc_set": "uint:2",
            "name": "uint:2",
            "bgm": "uint:2",
            "series2": "uint:2",
            "unk1": "uint:2",
            "unk2": "uint:2",
            "unk3": "uint:2",
            "unk4": "uint:2",
            "unk5": "uint:2",
            "unk6": "uint:2",
            "unk7": "uint:2",
            "unk8": "uint:2",
            "unk9": "uint:2",
            "unk10": "uint:2",
            "unk11": "uint:2",
            "unk12": "uint:2",
            "unk13": "uint:2",
            "null2": "null:16",
            "unk14": "uint:2",
            "fixed100a": "uint:2",
            "fixed30": "uint:1",
            "fixed50": "uint:1",
            "fixed70": "uint:1",
            "fixed100b": "uint:1",
            "terrain": "uint:1",
            "series_end": "uint:1",
        }
    }

    available_unit_definition = {"guid": "guid", "type": "uint:4"}

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = super().read(buffer)

        terrain = ["space", "air", "land", "surface", "underwater"]
        for record in records["stages"]:
            record.update(self.bit_smash("terrain", record.pop("terrain"), terrain))

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
    data_path = "resident"
    signature = b"\x4C\x51\x41\x53\x00\x00\x00\x01"

    definitions = {
        "main": {
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
    }


class SpecProfileList(GundamDataFile):
    default_filename = "SpecProfileList.cdb"
    data_path = "resident"
    signature = b"\x4C\x50\x50\x53\x00\x00\x03\x01"
    constants = {"fixed1": 1}

    definitions = {
        "units": {
            "guid": "guid",
            "image_guid": "guid",
            "series": "series",
            "stage_clear_get": "uint:4",
            "dlc_set": "uint:2",
            "profile_id": "uint:2",
            "string_index": "uint:2",
            "quest_id": "uint:2",
            "group_dispatch": "uint:2",
            "fixed1": "uint:2",
        },
        "warships": {
            "guid": "guid",
            "image_guid": "guid",
            "series": "series",
            "stage_clear_get": "uint:4",
            "dlc_set": "uint:2",
            "profile_id": "uint:2",
            "string_index": "uint:2",
            "quest_id": "uint:2",
            "group_dispatch": "uint:2",
            "fixed1": "uint:2",
        },
        "characters": {
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
        },
    }

    @classmethod
    def calculate_header(
        cls, records: Dict[str, List[Dict]], byte_strings: Dict[str, bytes]
    ) -> Dict[str, Dict[str, int]]:
        header = cls.make_basic_header(records, byte_strings)
        # no pointer list

        return header

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {},
            "pointers": {},
            "size": {
                table: cls.definition_size(definition)
                for table, definition in cls.definitions.items()
            },
        }

        for table, definition in cls.definitions.items():
            header["counts"][table] = cls.read_int(buffer.read(cls.record_count_length))

        tables = list(cls.definitions.keys())

        for i, table in enumerate(tables):
            if i == 0:
                header["pointers"][table] = buffer.tell()
            else:
                header["pointers"][table] = header["pointers"][tables[i - 1]] + (
                    header["counts"][tables[i - 1]] * header["size"][tables[i - 1]]
                )

        return header


class TitleBgmList(GundamDataFile):
    default_filename = "TitleBgmList.cdb"
    data_path = "resident"
    signature = b""


class TutorialList(GundamDataFile):
    default_filename = "TutorialList.cdb"
    data_path = "resident"
    package = "MiscData.pkd"
    signature = b"\x4F\x54\x55\x54\x00\x00\x01\x01"

    # Uses messagestrings.tbl
    definitions = {
        "main": {
            "title": "uint:4",
            "text": "uint:4",
            "next": "uint:4",
            "index": "uint:2",
            "unknown": "uint:2",  # Mostly 1, some 3, one 0
        }
    }


class WeaponSpecList(GundamDataFile):
    default_filename = "WeaponSpecList.cdb"
    data_path = "resident"
    package = "MachineSpecList.pkd"
    signature = b"\x4C\x53\x50\x57\x00\x00\x00\x01"

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

    definitions = {
        "weapons": {
            "guid": "guid",
            "name": "uint:2",  # MachineSpecList.tbl
            "range_grid": "uint:2",
            "power": "uint:2",
            "en": "uint:2",
            "mp": "uint:2",
            "terrain": "uint:2",  # [0, 136, 168, 170]
            "index2a": "uint:1",
            "type": "uint:1",
            "type2": "uint:1",  # one is probably the icon?
            "effect": "uint:1",
            "tension": "uint:2",
            "unk10": "uint:2",  # [15, 16, 26, 30, 31]
            "min_range": "int:1",
            "max_range": "int:1",
            "accuracy": "uint:1",
            "critical": "uint:1",
            "unk11": "uint:2",  # [1, 2, 3, 4, 5, 6, 7, 8]
            "null": "null:2",
        },
        "mapWeapons": {
            "guid": "guid",
            "name": "uint:2",
            "range_grid": "uint:2",
            "power": "uint:2",
            "en": "uint:2",
            "mp": "uint:2",
            "terrain": "uint:2",  # [128, 170]
            "index2a": "uint:1",
            "type": "uint:1",
            "type2": "uint:1",  # one is probably the icon?
            "effect": "uint:1",
            "tension": "uint:2",
            "unk10": "uint:2",  # [15, 24, 31]
            "unk11": "int:2",  # [-1, 1812, 1815, 1831]
            "unk12a": "int:1",
            "unk12b": "int:1",
            "unk13a": "int:1",  # 1-4
            "unk13b": "int:1",  # 0-6
            "null": "null:2",
        },
        "types": {"name": "uint:2", "index": "uint:2"},
        "effects": {"name": "uint:2", "desc": "uint:2", "index": "uint:2"},
    }

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {
                "weapons": cls.read_int(buffer.read(4)),
                "mapWeapons": cls.read_int(buffer.read(4)),
            },
            "pointers": {
                "mapWeapons": cls.read_int(buffer.read(4)),
                "types": cls.read_int(buffer.read(4)),
                "effects": cls.read_int(buffer.read(4)),
                "weapons": buffer.tell(),
            },
            "size": {
                table: cls.definition_size(definition)
                for table, definition in cls.definitions.items()
            },
        }

        old_position = buffer.tell()
        buffer.seek(header["pointers"]["types"])
        header["counts"]["types"] = cls.read_int(buffer.read(4))
        header["pointers"]["types"] += 4
        buffer.seek(header["pointers"]["effects"])
        header["counts"]["effects"] = cls.read_int(buffer.read(4))
        header["pointers"]["effects"] += 4
        buffer.seek(old_position)

        return header

    @classmethod
    def post_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        tf = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for table, table_records in records.items():
            if table not in ["weapons", "mapWeapons"]:
                continue
            for r in table_records:
                del r["type2"]
                r.update(**cls.bit_smash("terrain", r.pop("terrain"), tf))

        return records

    @classmethod
    def pre_processing(cls, records: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        for table, table_records in records.items():
            if table not in ["weapons", "mapWeapons"]:
                continue
            for r in table_records:
                r["type2"] = r["type"]

        return records


""" DAT files """


class DlcList(GundamDataFile):
    default_filename = "DlcList.dat"
    signature = b"\x08\x80\x80\x80\x08\x12\x04\x08"


class EffectList(GundamDataFile):
    default_filename = "effectList.dat"
    signature = b"\x4C\x45\x4D\x54"
    definitions = {"main": {"effect_id": "uint:4", "effect_name": "string_len_prefix"}}


class MapWeaponList(GundamDataFile):
    default_filename = "mapWeaponList.dat"
    signature = b"\x57\x4D\x4D\x54"
    definitions = {
        "mapWeapons": {
            "unit_id": "string_len_prefix",
            "weapon_id": "string_len_prefix",
            "unk1": "uint:1",
            "unk2": "uint:1",
            "unk3": "uint:1",
            "unk4": "uint:1",
        }
    }


class MovieList(GundamDataFile):
    default_filename = "movieList.dat"
    signature = b"\x4C\x4D\x4D\x54"
    record_count_length = 2


class PowerUpList(GundamDataFile):
    default_filename = "powerUpList.dat"
    data_path = "tmap/resident"
    signature = b"\x44\x4C\x55\x50"

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
    data_path = "tmap/resident"
    signature = b"\x4D\x53\x4D\x54"
    record_count_length = 2
    definitions = {
        "main": {
            "string": "string_len_prefix",
            "unk1": "uint:1",
            "unk2": "uint:1",
            "unk3": "uint:1",
        }
    }


class SteamDlcGroupList(GundamDataFile):
    default_filename = "SteamDlcGroupList.dat"
    signature = b""


class Stage(GundamDataFile):
    default_filename = "Stage.dat"
    signature = b"\x49\x53\x4D\x54\x2F\x01\x00\x00"

    definitions = {"areas": {}}

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        header = self.read_header(buffer)
        records = {"areas": []}

        # incomplete mess
        # Null byte at the start?
        print(self.read_int(buffer.read(1)))

        for i in range(header["counts"]["areas"]):
            value = self.read_int(buffer.read(1))
            size_x = self.read_int(buffer.read(1))
            size_y = self.read_int(buffer.read(1))
            print(size_x, size_y)
            record = {
                "__order": i,
                "value": value,
                "size_x": size_x,
                "size_y": size_y,
                "minimap": self.read_string_length(buffer),
                "background": self.read_string_length(buffer),
                "unk0": self.read_int(buffer.read(4)),
                "values2": [
                    self.read_int(buffer.read(1), signed=True) for _ in range(20)
                ],
                "ffbytes": "bytes:12",  # probably a mask?
                "map_tiles": [
                    [self.read_int(buffer.read(4)) for _ in range(size_x)]
                    for __ in range(size_y)
                ],
                "unk3": self.read_int(buffer.read(1)),
                "unk4": [
                    [self.read_int(buffer.read(1)) for __ in range(11)]
                    for _ in range(3)
                ],
                "unk5": buffer.read(3),
                "bunk7": buffer.read(self.read_int(buffer.read(1))),
                "unk8": buffer.read(2),
                "unk9": buffer.read(9),
                "unk10": buffer.read(3),
                "bunk11": buffer.read(self.read_int(buffer.read(1))),
                "unk12": buffer.read(1),
                "unk13": buffer.read(7),
                "name": self.read_string_length(buffer),  # referred to by script
            }
            records["areas"].append(record)
            for k, v in record.items():
                print(k, v)

        return records


class StageCondition(GundamDataFile):
    default_filename = "StageConditions.dat"
    signature = b"\x43\x53\x4D\x54\x64\x00\x00\x00"
    record_count_length = 0

    definitions = {
        "conditions": {
            "mission_japanese": "string_len_prefix",
            "mission_tw_t_chinese": "string_len_prefix",
            "mission_hk_t_chinese": "string_len_prefix",
            "mission_s_chinese": "string_len_prefix",
            "mission_korean": "string_len_prefix",
            "mission_english": "string_len_prefix",
            "mission_unk1": "bytes:16",
            "mission2_japanese": "string_len_prefix",
            "mission2_tw_t_chinese": "string_len_prefix",
            "mission2_hk_t_chinese": "string_len_prefix",
            "mission2_s_chinese": "string_len_prefix",
            "mission2_korean": "string_len_prefix",
            "mission2_english": "string_len_prefix",
            "mission2_unk1": "bytes:65",
            "mission3_japanese": "string_len_prefix",
            "mission3_tw_t_chinese": "string_len_prefix",
            "mission3_hk_t_chinese": "string_len_prefix",
            "mission3_s_chinese": "string_len_prefix",
            "mission3_korean": "string_len_prefix",
            "mission3_english": "string_len_prefix",
            "mission3_unk1": "bytes:2",
            "mission3b_japanese": "string_len_prefix",
            "mission3b_tw_t_chinese": "string_len_prefix",
            "mission3b_hk_t_chinese": "string_len_prefix",
            "mission3b_s_chinese": "string_len_prefix",
            "mission3b_korean": "string_len_prefix",
            "mission3b_english": "string_len_prefix",
            "mission3b_unk1": "bytes:17",
            "mission4_japanese": "string_len_prefix",
            "mission4_tw_t_chinese": "string_len_prefix",
            "mission4_hk_t_chinese": "string_len_prefix",
            "mission4_s_chinese": "string_len_prefix",
            "mission4_korean": "string_len_prefix",
            "mission4_english": "string_len_prefix",
            "mission4_unk1": "bytes:59",
            "mission5_japanese": "string_len_prefix",
            "mission5_tw_t_chinese": "string_len_prefix",
            "mission5_hk_t_chinese": "string_len_prefix",
            "mission5_s_chinese": "string_len_prefix",
            "mission5_korean": "string_len_prefix",
            "mission5_english": "string_len_prefix",
            "mission5_unk1": "bytes:36",
            "mission6_japanese": "string_len_prefix",
            "mission6_tw_t_chinese": "string_len_prefix",
            "mission6_hk_t_chinese": "string_len_prefix",
            "mission6_s_chinese": "string_len_prefix",
            "mission6_korean": "string_len_prefix",
            "mission6_english": "string_len_prefix",
            "mission6_unk1": "bytes:16",
            "mission7_japanese": "string_len_prefix",
            "mission7_tw_t_chinese": "string_len_prefix",
            "mission7_hk_t_chinese": "string_len_prefix",
            "mission7_s_chinese": "string_len_prefix",
            "mission7_korean": "string_len_prefix",
            "mission7_english": "string_len_prefix",
            "mission7_unk1": "bytes:7",
            "mission8_japanese": "string_len_prefix",
            "mission8_tw_t_chinese": "string_len_prefix",
            "mission8_hk_t_chinese": "string_len_prefix",
            "mission8_s_chinese": "string_len_prefix",
            "mission8_korean": "string_len_prefix",
            "mission8_english": "string_len_prefix",
            "mission8_unk1": "bytes:16",
            "mission9_japanese": "string_len_prefix",
            "mission9_tw_t_chinese": "string_len_prefix",
            "mission9_hk_t_chinese": "string_len_prefix",
            "mission9_s_chinese": "string_len_prefix",
            "mission9_korean": "string_len_prefix",
            "mission9_english": "string_len_prefix",
            "mission9_unk1": "bytes:65",
            "mission10_japanese": "string_len_prefix",
            "mission10_tw_t_chinese": "string_len_prefix",
            "mission10_hk_t_chinese": "string_len_prefix",
            "mission10_s_chinese": "string_len_prefix",
            "mission10_korean": "string_len_prefix",
            "mission10_english": "string_len_prefix",
            "mission10_unk1": "bytes:17",
            "mission11_japanese": "string_len_prefix",
            "mission11_tw_t_chinese": "string_len_prefix",
            "mission11_hk_t_chinese": "string_len_prefix",
            "mission11_s_chinese": "string_len_prefix",
            "mission11_korean": "string_len_prefix",
            "mission11_english": "string_len_prefix",
            "mission11_unk1": "bytes:58",
            "mission12_japanese": "string_len_prefix",
            "mission12_tw_t_chinese": "string_len_prefix",
            "mission12_hk_t_chinese": "string_len_prefix",
            "mission12_s_chinese": "string_len_prefix",
            "mission12_korean": "string_len_prefix",
            "mission12_english": "string_len_prefix",
            "mission12_unk1": "bytes:16",
            "mission13_japanese": "string_len_prefix",
            "mission13_tw_t_chinese": "string_len_prefix",
            "mission13_hk_t_chinese": "string_len_prefix",
            "mission13_s_chinese": "string_len_prefix",
            "mission13_korean": "string_len_prefix",
            "mission13_english": "string_len_prefix",
            "mission13_unk1": "bytes:7",
            "mission14_japanese": "string_len_prefix",
            "mission14_tw_t_chinese": "string_len_prefix",
            "mission14_hk_t_chinese": "string_len_prefix",
            "mission14_s_chinese": "string_len_prefix",
            "mission14_korean": "string_len_prefix",
            "mission14_english": "string_len_prefix",
            "mission14_unk1": "bytes:16",
            "mission15_japanese": "string_len_prefix",
            "mission15_tw_t_chinese": "string_len_prefix",
            "mission15_hk_t_chinese": "string_len_prefix",
            "mission15_s_chinese": "string_len_prefix",
            "mission15_korean": "string_len_prefix",
            "mission15_english": "string_len_prefix",
            "mission15_unk1": "bytes:5",
        }
    }

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        header = super().read_header(buffer)
        header["counts"]["conditions"] = 1

        return header
