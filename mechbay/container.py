import os
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
            if isinstance(file["archive"], list):
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
                try:
                    record[mapping["field"]] = localisations[record[mapping["field"]]]
                except IndexError:
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

    def read(self) -> Dict[str, List[Dict]]:
        # first read in the raw bytes of all the files
        raw_data = self.read_files()

        # now parse them with their specific classes
        data = self.parse_data(raw_data)

        # read in localisations
        localisations = self.read_localisations()

        # map localisation strings onto data
        self.map_strings(localisations, data)

        return data

    def write(self, data: Dict[str, List[Dict]]):
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
            "missing_value": None,
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
            "missing_value": None,
        },
        {
            "table": "MyCharacterConfigurations.outfits",
            "field": "name",
            "strings": "CharacterSpecList",
            "missing_value": None,
        },
        {
            "table": "MyCharacterConfigurations.voices",
            "field": "name",
            "strings": "CharacterSpecList",
            "missing_value": None,
        },
        {
            "table": "MyCharacterConfigurations.names",
            "field": "name",
            "strings": "CharacterSpecList",
            "missing_value": None,
        },
        {
            "table": "MyCharacterConfigurations.bgm",
            "field": "name",
            "strings": "CharacterSpecList",
            "missing_value": None,
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
        # Filename, tablename, data path
        {
            "filename": "MiscData.tbl",
            "table": "MiscData",
            "data_path": "language",
            "parser_class": Localisation,
        }
    ]

    string_maps = [
        {
            "table": "SeriesList",
            "field": "name",
            "strings": "MiscData",
            "missing_value": None,
        },
        {
            "table": "GroupSendingMissionList",
            "field": "name",
            "strings": "MiscData",
            "missing_value": None,
        },
        {
            "table": "GroupSendingMissionList",
            "field": "description",
            "strings": "MiscData",
            "missing_value": None,
        },
    ]

    def map_strings(
        self, localisations: Dict[str, Dict[int, Dict]], data: Dict[str, List[Dict]]
    ) -> None:
        super().map_strings(localisations, data)

        for record in data["GroupSendingMissionList"]:
            for recommended in record["recommended"]:
                recommended["name"] = localisations["MiscData"][recommended["name"]]

    def index_strings(self, data: Dict[str, List[Dict]]) -> Dict[str, Dict[int, Dict]]:
        localisations = super().index_strings(data)

        for record in data["GroupSendingMissionList"]:
            for r in record["recommended"]:
                index = len(localisations["MiscData"])
                localisations["MiscData"][index] = r["name"]
                r["name"] = index

        return localisations


class AbilitySpecList(Container):
    read_list = [
        {"filename": "AbilitySpecList.cdb", "data_path": "resident", "archive": None}
    ]

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
            "strings": "MiscData",
            "missing_value": None,
        },
        {
            "table": "AbilitySpecList.unitModifications",
            "field": "name",
            "strings": "MiscData",
            "missing_value": None,
        },
        {
            "table": "AbilitySpecList.characterAbilities",
            "field": "name",
            "strings": "MiscData",
            "missing_value": None,
        },
        {
            "table": "AbilitySpecList.characterSkills",
            "field": "name",
            "strings": "MiscData",
            "missing_value": None,
        },
        {
            "table": "AbilitySpecList.effects",
            "field": "name",
            "strings": "MiscData",
            "missing_value": None,
        },
    ]
