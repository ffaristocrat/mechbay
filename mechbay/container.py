import os
from copy import deepcopy
from io import BytesIO
from typing import Dict, List
import mechbay.parsers as parsers
from .pkd import PKDArchive
from .strings import Localisation


class Container:
    read_list: List[Dict] = []
    parse_list: List[Dict] = []
    localisations: List[Dict] = []
    string_maps: List[Dict] = []

    def __init__(self, read_data_path: str = "./data", write_data_path: str = "./mods"):
        self.read_path = read_data_path
        self.write_path = write_data_path

    def read_files(self) -> Dict[str, bytes]:
        # first read in the raw bytes of all the files
        raw_data = {}
        for file in self.read_list:
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

    def write_files(self, raw_data: Dict[str, bytes]):
        for file in self.read_list:
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

    def parse_data(self, raw_data: Dict[str, bytes]) -> Dict[str, List[Dict]]:
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

    def compose_data(self, data: Dict[str, List[Dict]]) -> Dict[str, bytes]:
        # now compose them with their specific classes
        raw_data = {}
        for file in self.parse_list:
            records = {}
            for table, table_data in data.items():
                if table == file["table"]:
                    records = table_data
                    break
                elif table.startswith(file["table"]):
                    sub_table = table.rpartition(".")
                    records[sub_table] = table_data
            print(f"Composing {file['table']}")
            raw_data[file["filename"]] = file["parser_class"]().write(records)

        return raw_data

    def read_localisations(self) -> Dict[str, Dict[int, Dict]]:
        # read in localisations
        strings = {}
        for file in self.localisations:
            strings[file["table"]] = file["parser_class"].read_files(
                os.path.join(self.read_path, file["data_path"]), file["filename"]
            )
        return strings

    def write_localisations(self, localisations: Dict[str, Dict[int, Dict]]):
        for file in self.localisations:
            file["parser_class"].write_files(
                records=localisations[file["table"]],
                output_data_path=os.path.join(self.read_path, file["data_path"]),
                filename=file["filename"],
            )

    def map_strings(
        self, localisations: Dict[str, Dict[int, Dict]], data: Dict[str, List[Dict]]
    ) -> None:
        for mapping in self.string_maps:
            for record in data[mapping["table"]]:
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

    def index_strings(self, data: Dict[str, List[Dict]]) -> Dict[str, Dict[int, Dict]]:
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

    def post_processing(
        self, localisations: Dict[str, Dict[int, Dict]], data: Dict[str, List[Dict]]
    ) -> Dict[str, List[Dict]]:
        return data

    def pre_processing(self, data: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        return data

    def read(self) -> Dict[str, List[Dict]]:
        # first read in the raw bytes of all the files
        raw_data = self.read_files()

        # now parse them with their specific classes
        data = self.parse_data(raw_data)

        # read in localisations
        localisations = self.read_localisations()

        # map localisation strings onto data
        self.map_strings(localisations, data)

        data = self.post_processing(localisations, data)

        return data

    def write(self, data: Dict[str, List[Dict]]):
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

    read_list = [
        {
            "filename": "CharacterSpecList.pkd",
            "data_path": "resident",
            "archive": [
                "CharacterSpecList.cdb",
                "CharacterGrowthList.cdb",
                "SkillAcquisitionPatternList.cdb",
                "MyCharacterConfigurations.cdb",
            ],
        }
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


class MiscData(Container):
    read_list = [
        {
            "filename": "MiscData.pkd",
            "data_path": "resident",
            "archive": [
                "DatabaseCaluclation.cdb",
                "SeriesList.cdb",
                "GroupSendingMissionList.cdb",
                "TutorialList.cdb",
            ],
        }
    ]

    parse_list = [
        # {
        #     "filename": "DatabaseCaluclation.cdb",
        #     "table": "DatabaseCalculation",
        #     "parser_class": parsers.DatabaseCalculation,
        # },
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
        # Filename, tablename, data path
        {
            "filename": "MiscData.tbl",
            "table": "MiscData",
            "data_path": "language",
            "parser_class": Localisation,
        }
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

    def post_processing(
        self, localisations: Dict[str, Dict[int, Dict]], data: Dict[str, List[Dict]]
    ) -> Dict[str, List[Dict]]:
        for record in data["GroupSendingMissionList.missions"]:
            for recommended in record["recommended"]:
                recommended["name"] = localisations["MiscData"][recommended["name"]]

        return data

    def index_strings(self, data: Dict[str, List[Dict]]) -> Dict[str, Dict[int, Dict]]:
        localisations = super().index_strings(data)

        for record in data["GroupSendingMissionList.missions"]:
            for r in record["recommended"]:
                index = len(localisations["MiscData"])
                localisations["MiscData"][index] = r["name"]
                r["name"] = index

        return localisations


class AbilitySpecList(Container):
    read_list = [{"filename": "AbilitySpecList.cdb", "data_path": "resident"}]

    parse_list = [
        {
            "filename": "AbilitySpecList.cdb",
            "table": "AbilitySpecList",
            "parser_class": parsers.AbilitySpecList,
        }
    ]

    localisations = [
        # Filename, tablename, data path
        {
            "filename": "AbilitySpecList.tbl",
            "table": "AbilitySpecList",
            "data_path": "language",
            "parser_class": Localisation,
        }
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
            "field": "name",
            "strings": "AbilitySpecList",
        },
    ]


class MachineSpecList(Container):
    read_list = [
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
        }
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
        }
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
            "missing_value": -1,
        },
        {
            "table": "WeaponSpecList.effects",
            "field": "name",
            "strings": "MachineSpecList",
        },
        {
            "table": "WeaponSpecList.effects",
            "field": "desc",
            "strings": "MachineSpecList",
        },

    ]
