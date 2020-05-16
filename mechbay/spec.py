import os
from io import BytesIO
from .parsers import *
from .pkd import PKDArchive
from .strings import Localisation


class CharacterSpecList:
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
        ("CharacterSpecList.cdb", CharacterSpecList),
        ("CharacterGrowthList.cdb", CharacterGrowthList),
        ("SkillAcquisitionPatternList.cdb", SkillAcquisitionPatternList),
        ("MyCharacterConfigurations.cdb", MyCharacterConfigurations),
    ]

    def __init__(self, read_data_path: str = "./data", write_data_path: str = "./mods"):
        self.read_path = read_data_path
        self.write_path = write_data_path

    def read_files(self) -> Dict:
        archive_file = "CharacterSpecList.pkd"
        string_file = "CharacterSpecList.tbl"

        archive = PKDArchive().read_file(
            os.path.join(self.read_path, "resident", archive_file)
        )
        data = {}

        for filename, cls in self.file_list:
            table_name = filename.split(".")[0]
            print(f"Reading {table_name}")
            obj = cls(self.read_path)
            records = obj.read(BytesIO(archive[filename]))
            if isinstance(records, dict):
                for sub_table, values in records.items():
                    data[f"{table_name}.{sub_table}"] = values
            else:
                data[table_name] = records

        strings = Localisation.read_files(
            os.path.join(self.read_path, "language"), string_file
        )

        fields = ["name", "unique_name"]
        for table_name, records in data.items():
            for r in records:
                for f in fields:
                    if f not in r:
                        continue
                    elif r.get(f) == -1:
                        r[f] = None
                    else:
                        try:
                            r[f] = strings[r[f]]
                        except IndexError:
                            r[f] = f"Bad string index {r[f]}"
        return data

    def write_files(self, data: Dict):
        archive_file = "CharacterSpecList.pkd"
        string_file = "CharacterSpecList.tbl"

        archive = {}
        strings = []

        fields = ["name", "unique_name"]
        for table_name, records in data.items():
            for f in fields:
                for r in records:
                    if f not in records:
                        continue
                    strings.append(r.pop(f))
                    r[f] = len(strings) - 1

        Localisation.write_files(
            strings, os.path.join(self.write_path, "language"), string_file
        )

        for filename, cls in self.file_list:
            obj = cls(self.write_path)
            archive[filename] = obj.write(data[filename.split(".")[0]])

        PKDArchive().write_file(
            archive, os.path.join(self.write_path, "resident", archive_file)
        )


class MiscData:
    file_list = [
        ("DatabaseCaluclation.cdb", DatabaseCalculation),
        ("SeriesList.cdb", SeriesList),
        ("GroupSendingMissionList.cdb", GroupSendingMissionList),
        ("TutorialList.cdb", TutorialList),
    ]

    data_sets = [
        ("SeriesList", "name"),
        ("GroupSendingMissionList", "name"),
        ("GroupSendingMissionList", "description"),
    ]

    def __init__(self, read_data_path: str = "./data", write_data_path: str = "./mods"):
        self.read_path = read_data_path
        self.write_path = write_data_path

    def read_files(self) -> Dict:
        archive_file = "MiscData.pkd"
        string_file = "MiscData.tbl"

        archive = PKDArchive().read_file(
            os.path.join(self.read_path, "resident", archive_file)
        )
        data = {}

        for filename, cls in self.file_list:
            table_name = filename.split(".")[0]
            print(f"Reading {table_name}")
            obj = cls(self.read_path)
            records = obj.read(BytesIO(archive[filename]))
            if isinstance(records, dict):
                for sub_table, values in records.items():
                    data[f"{table_name}.{sub_table}"] = values
            else:
                data[table_name] = records

        strings = Localisation.read_files(
            os.path.join(self.read_path, "language"), string_file
        )

        fields = ["name"]
        for table_name, records in data.items():
            for r in records:
                for f in fields:
                    if f not in r:
                        continue
                    try:
                        r[f] = strings[r[f]]
                    except IndexError:
                        r[f] = f"Bad string index {r[f]}"

        for record in data["GroupSendingMissionList"]:
            for r in record["recommended"]:
                r["name"] = strings[r["name"]]

        return data

    def write_files(self, data: Dict):
        archive_file = "MiscData.pkd"
        string_file = "MiscData.tbl"

        archive = {}
        strings = []

        fields = ["name", "unique_name"]
        for table_name, records in data.items():
            for f in fields:
                for r in records:
                    if f not in records:
                        continue
                    strings.append(r.pop(f))
                    r[f] = len(strings) - 1

        for record in data["GroupSendingMissionList"]:
            for r in record["recommended"]:
                strings.append(r["name"])
                r["name"] = len(strings) - 1

        Localisation.write_files(
            strings, os.path.join(self.write_path, "language"), string_file
        )

        for filename, cls in self.file_list:
            obj = cls(self.write_path)
            archive[filename] = obj.write(data[filename.split(".")[0]])

        PKDArchive().write_file(
            archive, os.path.join(self.write_path, "resident", archive_file)
        )
