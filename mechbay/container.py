import os
from copy import deepcopy
from io import BytesIO
import mechbay.parsers as parsers
from .pkd import PKDArchive
from .strings import Localisation


class Container:
    file_list: list[dict] = []
    parse_list: list[dict] = []
    localisations: list[dict] = []
    string_maps: list[dict] = []
    index_maps: list[dict] = []

    def __init__(self, read_data_path: str = "./data", write_data_path: str = "./mods"):
        self.read_path = read_data_path
        self.write_path = write_data_path

    def read_files(self) -> dict[str, bytes]:
        # first read in the raw bytes of all the files
        raw_data = {}
        for file in self.file_list:
            print(f"Reading {file['filename']}")
            with open(
                os.path.join(self.read_path, file["data_path"], file["filename"]), "rb"
            ) as f:
                raw_bytes = f.read()
            if isinstance(file.get("archive"), list):
                raw_data.update(**PKDArchive().read(BytesIO(raw_bytes)))
            else:
                raw_data[file["filename"]] = raw_bytes

        return raw_data

    def write_files(self, raw_data: dict[str, bytes]):
        for file in self.file_list:
            print(f"Writing {file['filename']}")
            full_path = os.path.join(
                self.write_path, file["data_path"], file["filename"]
            )
            with open(full_path, "wb") as f:
                if file["archive"]:
                    f.write(
                        PKDArchive().write({f: raw_data[f] for f in file["archive"]})
                    )
                else:
                    f.write(raw_data[file["filename"]])

    def parse_data(self, raw_data: dict[str, bytes]) -> dict[str, list[dict]]:
        data = {}
        for file in self.parse_list:
            print(f"Parsing {file['table']}")
            records = file["parser_class"]().read(BytesIO(raw_data[file["filename"]]))
            if isinstance(records, dict):
                for sub_table, values in records.items():
                    data[f"{file['table']}.{sub_table}"] = values
            else:
                data[file["table"]] = records

        return data

    def compose_data(self, records: dict[str, list[dict]]) -> dict[str, bytes]:
        # now compose them with their specific classes
        raw_data = {}
        for file in self.parse_list:
            records_to_compose = {}
            for table, table_data in records.items():
                if table.startswith(file["table"]):
                    sub_table = table.rpartition(".")[-1]
                    records[sub_table] = table_data

            print(f"Composing {file['table']}")
            raw_data[file["filename"]] = file["parser_class"]().write(
                records_to_compose
            )

        return raw_data

    def read_localisations(self) -> dict[str, dict[int, dict]]:
        # read in localisations
        strings = {}
        for file in self.localisations:
            print(f"Reading {file['filename']}")
            strings[file["table"]] = file["parser_class"].read_files(
                os.path.join(self.read_path, file["data_path"]), file["filename"]
            )
        return strings

    def write_localisations(self, localisations: dict[str, dict[int, dict]]):
        for file in self.localisations:
            print(f"Writing {file['filename']}")
            file["parser_class"].write_files(
                records=localisations[file["table"]],
                output_data_path=os.path.join(self.read_path, file["data_path"]),
                filename=file["filename"],
            )

    def map_strings(
        self, localisations: dict[str, dict[int, dict]], records: dict[str, list[dict]]
    ) -> dict[str, list[dict]]:
        for mapping in self.string_maps:
            for record in records[mapping["table"]]:
                if (
                    mapping.get("missing_value") is not None
                    and record[mapping["field"]] == mapping["missing_value"]
                ):
                    record[mapping["field"]] = {}
                    continue

                try:
                    record[mapping["field"]] = localisations[mapping["strings"]][
                        record[mapping["field"]]
                    ]
                except KeyError:
                    print(
                        f"Missing index {mapping['field']} "
                        f"in {mapping['table']} for {mapping['strings']}"
                    )
        return records

    def index_strings(self, data: dict[str, list[dict]]) -> dict[str, dict[int, dict]]:
        localisations = {
            localisation["table"]: {} for localisation in self.localisations
        }
        for mapping in self.string_maps:
            for record in data[mapping["table"]]:
                if (
                    mapping.get("missing_value") is not None
                    and mapping["field"] not in record
                ):
                    record[mapping["field"]] = mapping["missing_value"]
                    continue

                index = len(localisations[mapping["strings"]])
                localisations[mapping["strings"]][index] = record.pop(mapping["field"])
                record[mapping["field"]] = index

        return localisations

    @staticmethod
    def map_to_index(value: int, index: list[dict], index_field: str) -> dict:
        for i in index:
            if value == i[index_field]:
                return i.copy()

        print(f"WARNING: Index {value} not found in {index_field}")
        return {}

    def populate_indexes(self, records: dict[str, list[dict]]):
        for index in self.index_maps:
            for r in records[index["table"]]:
                if (
                    index.get("missing_value") is not None
                    and r[index["table_field"]] == index["missing_value"]
                ):
                    continue
                r[index["table_field"]] = self.map_to_index(
                    value=r[index["table_field"]],
                    index=records[index["index"]],
                    index_field=index.get("index_field", "index"),
                )
        return records

    @staticmethod
    def extract_index(record: dict, record_field: str, index_field: str) -> dict:
        record[record_field] = record[record_field][index_field]
        return record

    def post_processing(
        self, localisations: dict[str, dict[int, dict]], records: dict[str, list[dict]]
    ) -> dict[str, list[dict]]:
        return records

    def pre_processing(self, records: dict[str, list[dict]]) -> dict[str, list[dict]]:
        return records

    def read(self) -> dict[str, list[dict]]:
        # first read in the raw bytes of all the files
        raw_data = self.read_files()

        # now parse them with their specific classes
        records = self.parse_data(raw_data)

        # read in localisations
        localisations = self.read_localisations()

        # map localisation strings onto data
        records = self.map_strings(localisations, records)

        # custom post processing
        records = self.post_processing(localisations, records)

        # fill in data from subtables for certain fields
        records = self.populate_indexes(records)

        return records

    def write(self, data: dict[str, list[dict]]):
        data = deepcopy(data)

        data = self.pre_processing(data)

        # compile the localisations
        localisations = self.index_strings(data)

        # write them out
        self.write_localisations(localisations)

        # compose all the files
        raw_data = self.compose_data(data)

        # package and write all files
        self.write_files(raw_data)


class CharacterSpecList(Container):
    """
    Character data is composed of
        data/resident/CharacterSpecList.pkd
            CharacterSpecList.cdb - Stats of all characters
            CharacterGrowthList.cdb - Stat growth profiles
            SkillAcquisitionPatternList.cdb - Skill gain profiles
            MyCharacterConfigurations.cdb - Custom character configs

        data/language/**/CharacterSpecList.tbl - localisation

        data/sound/voice/BTL/idset.tbl
        data/sound/voice/BTL/voice_table.tbl
        data/sound/voice/BTL/{guid}/*.HCA - audio lines for battle
        data/sound/voice/BTL/text/**/text.tbl - localised translations

    """

    file_list = [
        {
            "filename": "CharacterSpecList.pkd",
            "data_path": "resident",
            "archive": [
                "CharacterSpecList.cdb",
                "CharacterGrowthList.cdb",
                "SkillAcquisitionPatternList.cdb",
                "MyCharacterConfigurations.cdb",
            ],
        },
        {
            "filename": "CharacterConversionList.cdb",
            "data_path": "resident",
        },
    ]

    parse_list = [
        {
            "filename": "CharacterSpecList.cdb",
            "table": "CharacterSpecList",
            "parser_class": parsers.CharacterSpecList,
        },
        {
            "filename": "CharacterGrowthList.cdb",
            "table": "CharacterGrowthList",
            "parser_class": parsers.CharacterGrowthList,
        },
        {
            "filename": "SkillAcquisitionPatternList.cdb",
            "table": "SkillAcquisitionPatternList",
            "parser_class": parsers.SkillAcquisitionPatternList,
        },
        {
            "filename": "MyCharacterConfigurations.cdb",
            "table": "MyCharacterConfigurations",
            "parser_class": parsers.MyCharacterConfigurations,
        },
        {
            "filename": "CharacterConversionList.cdb",
            "table": "CharacterConversionList",
            "parser_class": parsers.CharacterConversionList,
        },
    ]

    localisations = [
        # Filename, tablename, data path
        {
            "filename": "CharacterSpecList.tbl",
            "table": "CharacterSpecList",
            "data_path": "language",
            "parser_class": Localisation,
        }
    ]

    string_maps = [
        {
            "table": "CharacterSpecList.characters",
            "field": "name",
            "strings": "CharacterSpecList",
        },
        {
            "table": "CharacterSpecList.characters",
            "field": "unique_name",
            "strings": "CharacterSpecList",
            "missing_value": -1,
        },
        {
            "table": "CharacterSpecList.npcs",
            "field": "name",
            "strings": "CharacterSpecList",
        },
        {
            "table": "CharacterSpecList.custom",
            "field": "name",
            "strings": "CharacterSpecList",
        },
        {
            "table": "MyCharacterConfigurations.outfits",
            "field": "name",
            "strings": "CharacterSpecList",
        },
        {
            "table": "MyCharacterConfigurations.voices",
            "field": "name",
            "strings": "CharacterSpecList",
        },
        {
            "table": "MyCharacterConfigurations.names",
            "field": "name",
            "strings": "CharacterSpecList",
        },
        {
            "table": "MyCharacterConfigurations.bgm",
            "field": "name",
            "strings": "CharacterSpecList",
        },
    ]

    index_maps = [
        {
            "table": "CharacterConversionList.characters",
            "table_field": "character",
            "index": "Characters.lookup",
            "index_field": "guid",
        },
        {
            "table": "CharacterConversionList.characters",
            "table_field": "conversion",
            "index": "Characters.lookup",
            "index_field": "guid",
        },
    ]

    def post_processing(
        self, localisations: dict[str, dict[int, dict]], records: dict[str, list[dict]]
    ) -> dict[str, list[dict]]:
        lookup_table = "Characters.lookup"
        lookup = {}
        for t in ["characters", "npcs", "custom"]:
            for r in records[f"CharacterSpecList.{t}"]:
                try:
                    lookup[r["guid"]] = r["unique_name"]["english"]
                except (AttributeError, KeyError, TypeError):
                    lookup[r["guid"]] = r["name"]["english"]
        records[lookup_table] = [{"guid": k, "name": v} for k, v in lookup.items()]

        return records


class MachineSpecList(Container):
    file_list = [
        {
            "filename": "MachineSpecList.pkd",
            "data_path": "resident",
            "archive": [
                "RangeDataList.cdb",
                "MachineGrowthList.cdb",
                "WeaponSpecList.cdb",
                "MachineSpecList.cdb",
                "MachineConversionList.cdb",
                "PersonalMachineList.cdb",
                "MachineDevelopmentList.cdb",
                "MachineDesignList.cdb",
            ],
        },
    ]

    parse_list = [
        {
            "filename": "RangeDataList.cdb",
            "table": "RangeDataList",
            "parser_class": parsers.RangeDataList,
        },
        {
            "filename": "MachineGrowthList.cdb",
            "table": "MachineGrowthList",
            "parser_class": parsers.MachineGrowthList,
        },
        {
            "filename": "WeaponSpecList.cdb",
            "table": "WeaponSpecList",
            "parser_class": parsers.WeaponSpecList,
        },
        {
            "filename": "MachineSpecList.cdb",
            "table": "MachineSpecList",
            "parser_class": parsers.MachineSpecList,
        },
        {
            "filename": "MachineConversionList.cdb",
            "table": "MachineConversionList",
            "parser_class": parsers.MachineConversionList,
        },
        {
            "filename": "PersonalMachineList.cdb",
            "table": "PersonalMachineList",
            "parser_class": parsers.PersonalMachineList,
        },
        {
            "filename": "MachineDevelopmentList.cdb",
            "table": "MachineDevelopmentList",
            "parser_class": parsers.MachineDevelopmentList,
        },
        {
            "filename": "MachineDesignList.cdb",
            "table": "MachineDesignList",
            "parser_class": parsers.MachineDesignList,
        },
    ]

    localisations = [
        # Filename, tablename, data path
        {
            "filename": "MachineSpecList.tbl",
            "table": "MachineSpecList",
            "data_path": "language",
            "parser_class": Localisation,
        },
    ]

    string_maps = [
        {
            "table": "MachineSpecList.units",
            "field": "name",
            "strings": "MachineSpecList",
        },
        {
            "table": "MachineSpecList.warships",
            "field": "name",
            "strings": "MachineSpecList",
        },
        {
            "table": "WeaponSpecList.weapons",
            "field": "name",
            "strings": "MachineSpecList",
        },
        {
            "table": "WeaponSpecList.mapWeapons",
            "field": "name",
            "strings": "MachineSpecList",
        },
        {
            "table": "WeaponSpecList.types",
            "field": "name",
            "strings": "MachineSpecList",
            "missing_value": 0,
        },
        {
            "table": "WeaponSpecList.effects",
            "field": "name",
            "strings": "MachineSpecList",
            "missing_value": 0,
        },
        {
            "table": "WeaponSpecList.effects",
            "field": "desc",
            "strings": "MachineSpecList",
        },
    ]

    index_maps = [
        {
            "table": "WeaponSpecList.weapons",
            "table_field": "type",
            "index": "WeaponSpecList.types",
            "index_field": "index",
        },
        {
            "table": "WeaponSpecList.weapons",
            "table_field": "effect",
            "index": "WeaponSpecList.effects",
            "index_field": "index",
            "missing_value": 0,
        },
        {
            "table": "WeaponSpecList.mapWeapons",
            "table_field": "type",
            "index": "WeaponSpecList.types",
            "index_field": "index",
        },
        {
            "table": "WeaponSpecList.mapWeapons",
            "table_field": "effect",
            "index": "WeaponSpecList.effects",
            "index_field": "index",
            "missing_value": 0,
        },
        {
            "table": "MachineConversionList.units",
            "table_field": "unit",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "MachineConversionList.units",
            "table_field": "transform",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "PersonalMachineList.units",
            "table_field": "unit",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "PersonalMachineList.units",
            "table_field": "custom",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "MachineDesignList.designs",
            "table_field": "first",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "MachineDesignList.designs",
            "table_field": "second",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "MachineDesignList.designs",
            "table_field": "result",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "MachineDevelopmentList.units",
            "table_field": "unit",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
        {
            "table": "MachineDevelopmentList.units",
            "table_field": "child",
            "index": "Machines.lookup",
            "index_field": "guid",
        },
    ]

    def post_processing(
        self, localisations: dict[str, dict[int, dict]], records: dict[str, list[dict]]
    ) -> dict[str, list[dict]]:
        table = "MachineDevelopmentList.units"
        exploded = []
        for r in records[table]:
            for c in r["children"]:
                exploded.append(
                    {
                        "index": r["index"],
                        "unit": r["unit"],
                        "child": c["guid"],
                        "level": c["level"],
                    }
                )
        records[table] = exploded

        records["Machines.lookup"] = []
        for t in ["MachineSpecList.units", "MachineSpecList.warships"]:
            records["Machines.lookup"].extend(
                [{"guid": r["guid"], "name": r["name"]["english"]} for r in records[t]]
            )

        return records


class AbilitySpecList(Container):
    file_list = [
        {"filename": "AbilitySpecList.cdb", "data_path": "resident"},
    ]

    parse_list = [
        {
            "filename": "AbilitySpecList.cdb",
            "table": "AbilitySpecList",
            "parser_class": parsers.AbilitySpecList,
        },
    ]

    localisations = [
        # Filename, tablename, data path
        {
            "filename": "AbilitySpecList.tbl",
            "table": "AbilitySpecList",
            "data_path": "language",
            "parser_class": Localisation,
        },
    ]

    string_maps = [
        {
            "table": "AbilitySpecList.unitAbilities",
            "field": "name",
            "strings": "AbilitySpecList",
        },
        {
            "table": "AbilitySpecList.unitModifications",
            "field": "name",
            "strings": "AbilitySpecList",
        },
        {
            "table": "AbilitySpecList.characterAbilities",
            "field": "name",
            "strings": "AbilitySpecList",
        },
        {
            "table": "AbilitySpecList.characterSkills",
            "field": "name",
            "strings": "AbilitySpecList",
        },
        {
            "table": "AbilitySpecList.effects",
            "field": "desc",
            "strings": "AbilitySpecList",
        },
    ]

    index_maps = []

    prefixes = [
        "unit_",
        "power_",
        "char_",
        "consumption_",
        "adjust_",
        "nullify_",
        "damage_",
        "bonus_",
    ]

    def pre_processing(self, records: dict[str, list[dict]]) -> dict[str, list[dict]]:
        # return zeroes
        for r in records["effects"]:
            for k in list(r.keys()):
                if r.get(k) is None:
                    r[k] = 0

        # Values between -1000 and 1000 are percents
        # everything else is an absolute value increased by 1000
        for r in records["effects"]:
            for k, v in r.items():
                for p in self.prefixes:
                    if k.startswith(p):
                        if v > 1:
                            r[k] = int(v + 1000)
                        elif v < -1:
                            r[k] = int(v - 1000)
                        else:
                            r[k] = int(v * 100)

        return records

    def post_processing(
        self, localisations: dict[str, dict[int, dict]], records: dict[str, list[dict]]
    ) -> dict[str, list[dict]]:
        effects = records["AbilitySpecList.effects"]
        # Values between -1000 and 1000 are percents
        # everything else is an absolute value increased by 1000
        for r in effects:
            for k, v in r.items():
                for p in self.prefixes:
                    if k.startswith(p):
                        if v >= 1000:
                            r[k] = int(v - 1000)
                        elif v <= -1000:
                            r[k] = int(v + 1000)
                        else:
                            r[k] = int(v / 100)

        # remove zeroes
        for r in effects:
            for k in list(r.keys()):
                if r[k] == 0:
                    r.pop(k)

        return records


class MiscData(Container):
    file_list = [
        {
            "filename": "MiscData.pkd",
            "data_path": "resident",
            "archive": [
                "DatabaseCaluclation.cdb",
                "SeriesList.cdb",
                "GroupSendingMissionList.cdb",
                "TutorialList.cdb",
            ],
        },
    ]

    parse_list = [
        {
            "filename": "DatabaseCaluclation.cdb",
            "table": "DatabaseCalculation",
            "parser_class": parsers.DatabaseCalculation,
        },
        {
            "filename": "SeriesList.cdb",
            "table": "SeriesList",
            "parser_class": parsers.SeriesList,
        },
        {
            "filename": "GroupSendingMissionList.cdb",
            "table": "GroupSendingMissionList",
            "parser_class": parsers.GroupSendingMissionList,
        },
        {
            "filename": "TutorialList.cdb",
            "table": "TutorialList",
            "parser_class": parsers.TutorialList,
        },
    ]

    localisations = [
        {
            "filename": "MiscData.tbl",
            "table": "MiscData",
            "data_path": "language",
            "parser_class": Localisation,
        },
    ]

    string_maps = [
        {"table": "SeriesList.series", "field": "name", "strings": "MiscData"},
        {
            "table": "GroupSendingMissionList.missions",
            "field": "name",
            "strings": "MiscData",
        },
        {
            "table": "GroupSendingMissionList.missions",
            "field": "description",
            "strings": "MiscData",
        },
    ]

    index_maps = []

    prefixes = [
        "unit_",
        "power_",
        "char_",
        "consumption_",
        "adjust_",
        "nullify_",
        "damage_",
        "bonus_",
    ]

    def index_strings(self, data: dict[str, list[dict]]) -> dict[str, dict[int, dict]]:
        localisations = super().index_strings(data)

        for record in data["GroupSendingMissionList.missions"]:
            for r in record["recommended"]:
                index = len(localisations["MiscData"])
                localisations["MiscData"][index] = r["name"]
                r["name"] = index

        return localisations

    def post_processing(
        self, localisations: dict[str, dict[int, dict]], records: dict[str, list[dict]]
    ) -> dict[str, list[dict]]:
        for record in records["GroupSendingMissionList.missions"]:
            for recommended in record["recommended"]:
                recommended["name"] = localisations["MiscData"][recommended["name"]]

        return records


class StageList(Container):
    file_list = [
        {
            "filename": "StageList.pkd",
            "data_path": "resident",
            "archive": ["StageList.cdb", "QuestList.cdb", "GetUnitList.cdb"],
        }
    ]

    parse_list = [
        {
            "filename": "StageList.cdb",
            "table": "StageList",
            "parser_class": parsers.StageList,
        },
        {
            "filename": "QuestList.cdb",
            "table": "QuestList",
            "parser_class": parsers.QuestList,
        },
        {
            "filename": "GetUnitList.cdb",
            "table": "GetUnitList",
            "parser_class": parsers.GetUnitList,
        },
    ]

    localisations = [
        {
            "filename": "StageList.tbl",
            "table": "StageList",
            "data_path": "language",
            "parser_class": Localisation,
        }
    ]

    string_maps = [
        {
            "table": "StageList.stages",
            "field": "name",
            "strings": "StageList",
        },
        {
            "table": "QuestList.quests",
            "field": "name",
            "strings": "StageList",
        },
        {
            "table": "QuestList.quests",
            "field": "desc2",
            "strings": "StageList",
        },
        {
            "table": "QuestList.quests",
            "field": "desc",
            "strings": "StageList",
        },
    ]

    index_maps = []


def apply_effects(records: dict) -> dict:
    tables = [
        "AbilitySpecList.unitAbilities",
        "AbilitySpecList.unitModifications",
        "AbilitySpecList.characterAbilities",
        "AbilitySpecList.characterSkills",
    ]
    for table in tables:
        for r in records[table]:
            r["effect"] = records["AbilitySpecList.effects"][r["effect"]]

    return records


def create_rewards(records: dict):
    table = "GroupSendingMissionList"
    sub_tables = [
        (
            "characterAbilities",
            "AbilitySpecList.characterAbilities",
            "characterAbility",
            "index",
        ),
        (
            "unitModifications",
            "AbilitySpecList.unitModifications",
            "unitModification",
            "index",
        ),
        (
            "units",
            "MachineSpecList.units",
            "unit",
            "guid",
        ),
    ]

    rewards = []
    print(f"Creating {table}.rewards")
    for record in records[f"{table}.missions"]:
        for sub_table, index_table, index, index_field in sub_tables:
            for reward in record[sub_table]:
                matched = Container.map_to_index(
                    reward[index], records[index_table], index_field
                )
                rewards.append(
                    {
                        "dispatch_id": record["dispatch_id"],
                        "name": record["name"]["english"],
                        "threshold": reward["threshold"],
                        "quantity": reward["quantity"],
                        "type": index,
                        "item": matched["name"]["english"],
                    }
                )

        if record["cooldowns"] > 0:
            rewards.append(
                {
                    "dispatch_id": record["dispatch_id"],
                    "name": record["name"]["english"],
                    "threshold": record["cooldown_threshold"],
                    "quantity": record["cooldowns"],
                    "type": "cooldown",
                    "item": "Dispatch Cooldown",
                }
            )
    rewards = sorted(
        rewards,
        key=lambda x: (x["dispatch_id"], x["threshold"], x["type"], x["quantity"]),
    )
    records[f"{table}.rewards"] = rewards

    return records


class_map = {
    "CharacterSpecList": CharacterSpecList,
    "MachineSpecList": MachineSpecList,
    "AbilitySpecList": AbilitySpecList,
    "MiscData": MiscData,
    "StageList": StageList,
}
