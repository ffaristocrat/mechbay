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
        archive_file = "MiscData.pkd"
        string_file = "MiscData.tbl"

        archive = PKDArchive().read_file(
            os.path.join(self.read_path, "resident", archive_file)
        )
        data = {}

        for filename, cls in self.file_list:
            obj = cls(self.read_path)
            data[filename.split(".")[0]] = obj.read(BytesIO(archive[filename]))

        strings = Localisation.read_files(
            os.path.join(self.read_path, "language"), string_file
        )

        for r in data["CharacterSpecList"]:
            r["name"] = strings[r["name"]]
            if "C" in r["guid"]:
                r["unique_name"] = (
                    strings[r["unique_name"]] if r["unique_name"] > 0 else {}
                )

        for dataset in data["MyCharacterConfigurations"].values():
            for r in dataset:
                r["name"] = strings[r["name"]]

        return data

    def write_files(self, data: Dict):
        archive_file = "MiscData.pkd"
        string_file = "MiscData.tbl"

        archive = {}
        strings = []

        for r in data["CharacterSpecList"]:
            strings.append(r["name"])
            r["name"] = len(strings) - 1
            if "C" in r["guid"]:
                if r["unique_name"]:
                    strings.append(r["unique_name"])
                    r["unique_name"] = len(strings) - 1
                else:
                    r["unique_name"] = -1

        for dataset in data["MyCharacterConfigurations"].values():
            for r in dataset:
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
            obj = cls(self.read_path)
            data[filename.split(".")[0]] = obj.read(BytesIO(archive[filename]))

        strings = Localisation.read_files(
            os.path.join(self.read_path, "language"), string_file
        )

        for data_set, field in self.data_sets:
            for r in data[data_set]:
                r[field] = strings[r[field]]

        for record in data["GroupSendingMissionList"]:
            for r in record["recommended"]:
                r["name"] = strings[r["name"]]

        return data

    def write_files(self, data: Dict):
        archive_file = "MiscData.pkd"
        string_file = "MiscData.tbl"

        archive = {}
        strings = []

        for data_set, field in self.data_sets:
            for r in data[data_set]:
                strings.append(r[field])
                r[field] = len(strings) - 1

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
