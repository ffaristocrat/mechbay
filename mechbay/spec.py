import os
from io import BytesIO
from .parsers import *
from .pkd import PKDArchive
from .strings import Localisation


class Characters:
    """
        Character data is composed of
            data/resident/CharacterSpecList.pkd
                CharacterSpecList.cdb - Stats of all characters
                CharacterGrowthList.cdb - Stat growth profiles
                SkillAcquisitionPatternList.cdb - Skill gain profiles
                MyCharacterConfigurations.cdb - Custom character configs

            data/resident/CellAttributeList.pkd - Container for
                BattleBgList.cdb - Maps BGM music to files

            data/language/**/CharacterSpecList.tbl - localisation

            data/sound/voice/BTL/idset.tbl
            data/sound/voice/BTL/voice_table.tbl
            data/sound/voice/BTL/{guid}/*.HCA - audio lines for battle
            data/sound/voice/BTL/text/**/text.tbl - localised translations

    """

    character_spec_list_files = [
        ("CharacterSpecList.cdb", CharacterSpecList),
        ("CharacterGrowthList.cdb", CharacterGrowthList),
        ("SkillAcquisitionPatternList.cdb", SkillAcquisitionPatternList),
        ("MyCharacterConfigurations.cdb", MyCharacterConfigurations),
    ]

    def __init__(self, read_data_path: str = "./data", write_data_path: str = "./mods"):
        self.read_path = read_data_path
        self.write_path = write_data_path

    def read_files(self) -> Dict:
        archive = PKDArchive().read_file(
            os.path.join(self.read_path, "resident", "CharacterSpecList.pkd")
        )
        data = {}

        for filename, cls in self.character_spec_list_files:
            obj = cls(self.read_path)
            data[filename.split(".")[0]] = obj.read(BytesIO(archive[filename]))

        strings = Localisation.read_files(
            os.path.join(self.read_path, "language"), "CharacterSpecList.tbl"
        )

        for r in data["CharacterSpecList"]:
            r["name"] = strings[r["name"]]
            if "C" in r["guid"]:
                r["unique_name"] = (
                    strings[r["unique_name"]] if r["unique_name"] > 0 else {}
                )

        name_fields = [
            ("outfits", "name"),
            ("voices", "voice_actor"),
            ("names", "name"),
            ("bgm", "song_name"),
        ]
        for dataset, field in name_fields:
            for r in data["MyCharacterConfigurations"][dataset]:
                r[field] = strings[r[field]]

        return data

    def write_files(self, data: Dict):
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

        name_fields = [
            ("outfits", "name"),
            ("voices", "voice_actor"),
            ("names", "name"),
            ("bgm", "song_name"),
        ]

        for dataset, field in name_fields:
            for r in data["MyCharacterConfigurations"][dataset]:
                strings.append(r[field])
                r[field] = len(strings) - 1

        Localisation.write_files(
            strings, os.path.join(self.write_path, "language"), "CharacterSpecList.tbl"
        )

        for filename, cls in self.character_spec_list_files:
            obj = cls(self.write_path)
            archive[filename] = obj.write(data[filename.split(".")[0]])

        PKDArchive().write_file(
            archive, os.path.join(self.write_path, "resident", "CharacterSpecList.pkd")
        )
