import os
from io import BytesIO
from pathlib import Path
from typing import List, Dict, BinaryIO

from .data import GundamDataFile

LANGUAGES = ["english", "japanese", "korean", "schinese", "tchinese/hk", "tchinese/tw"]


def write_byte_dict(data: Dict[str, bytes], base_path: str):
    for file_path, byte_string in data.items():
        full_path = Path(os.path.join(base_path, file_path))
        full_path.mkdir(parents=True, exist_ok=True)
        with full_path.open("wb") as f:
            f.write(byte_string)


def read_byte_dict(file_list: List[str], base_path: str) -> Dict[str, bytes]:
    data = {}
    for file_path in file_list:
        full_path = Path(os.path.join(base_path, file_path))
        try:
            with full_path.open("rb") as f:
                data[file_path] = f.read()
        except FileNotFoundError:
            data[file_path] = {}

    return data


class StringTBL(GundamDataFile):
    signature = b"\x54\x52\x54\x53\x00\x01\x01\x00"

    definitions = {"strings": {"index": "uint:4", "string": "uint:4"}}

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        pad_length = 16
        string_bytes = bytes()
        string_bytes += self.signature
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)

        string_start = len(string_bytes) + (record_count * 8)

        # We pad out a 16 byte row with null bytes
        # after the index
        padding = pad_length - (string_start % pad_length)
        string_start += padding

        for record in records["strings"]:
            string_bytes += self.write_int(record.get("index", 0), 4)
            string_bytes += self.write_int(string_start, 4)

            string_start += len(record["string"].encode("utf-8")) + 1

        string_bytes += b"\x00" * padding

        for record in records["strings"]:
            string_bytes += self.write_string_null_term(record["string"])

        return string_bytes

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = super().read(buffer)

        for record in records["strings"]:
            # Pointers in StringTBLs work slightly differently
            record["string"] = self.read_string_null_term(buffer, record.pop("string"))

        return records


class Localisation:
    @classmethod
    def read_files(
        cls, input_data_path: str, filename: str
    ) -> Dict[int, Dict[str, str]]:
        data = {}
        for language in LANGUAGES:
            full_path = os.path.join(input_data_path, language, filename)
            try:
                with open(full_path, "rb") as f:
                    data[language] = f.read()
            except FileNotFoundError:
                print(f"{full_path} not found!")
                data[language] = None

        records = cls.read_bytes(data)

        return records

    @classmethod
    def read_bytes(cls, data: Dict[str, bytes]) -> Dict[int, Dict[str, str]]:
        records = []
        for language, byte_string in data.items():
            if not byte_string:
                continue

            localisation = StringTBL().read(BytesIO(byte_string))["strings"]

            if not records:
                records = localisation[:]

            if len(records) != len(localisation):
                raise ValueError(f"Length of {language} string table does not match")

            for r, l in zip(records, localisation):
                r[language] = l["string"]

        record_dict = {}
        for i, r in enumerate(records):
            del r["string"]
            del r["index"]
            record_dict[i] = r

        return record_dict

    @classmethod
    def write_files(
        cls, records: Dict[int, Dict[str, str]], output_data_path: str, filename: str
    ):
        data = cls.write_bytes(records)

        for language, byte_string in data.items():
            full_path = os.path.join(output_data_path, language, filename)
            os.makedirs(os.path.split(full_path)[0], exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(byte_string)

    @classmethod
    def write_bytes(cls, records: Dict[int, Dict[str, str]]) -> Dict[str, bytes]:
        data = {}
        for language in LANGUAGES:
            localisation = {"strings": [
                {"string": records[i].get(language, ""), "index": 0}
                for i in range(len(records))
            ]}
            data[language] = StringTBL().write(localisation)

        return data


class LocalisationIndexed(Localisation):
    """ The stage versions have meaningful indexes
        And not all localisations have the strings present
    """

    @classmethod
    def read_bytes(cls, data: Dict[str, bytes]) -> Dict[int, Dict[str, str]]:
        records = {}
        for language, byte_string in data.items():
            if not byte_string:
                continue
            localisation = StringTBL().read(BytesIO(byte_string))["strings"]
            for line in localisation:
                index = int(line["index"])
                if index not in records:
                    records[index] = {}
                records[index][language] = line["string"]

        return records

    @classmethod
    def write_bytes(cls, records: Dict[int, Dict[str, str]]) -> Dict[str, bytes]:
        data = {}
        for language in LANGUAGES:
            localisation = {"strings": [
                {"string": record[language], "index": index}
                for index, record in records.items()
                if record.get(language) is not None
            ]}
            data[language] = StringTBL().write(localisation)

        return data


class StageLocalisation:
    stage_tables = {
        0: {
            "dir": "data/stageComment",
            "voice": "StageCommentVoiceTable.tbl",
            "string": "StageCommentStringTable.tbl",
        },
        1: {
            "dir": "data/tmap/stage",
            "voice": "VoiceTable.tbl",
            "string": "TMapStringTable.tbl",
        },
        2: {
            "dir": "data/tmap/stage",
            "voice": "VoiceTable2.tbl",
            "string": "TMapStringTable2.tbl",
        },
        3: {
            "dir": "data/stageComment",
            "voice": "SeriesEndingVoiceTable.tbl",
            "string": "SeriesEndingStringTable.tbl",
        },
    }

    @classmethod
    def read_files(cls, input_data_path: str, stage_id: int) -> Dict[int, Dict]:
        parts = {}
        campaign = str(stage_id).zfill(5)[0:3]
        stage = str(stage_id).zfill(5)[3:5]

        for part, tables in cls.stage_tables.items():
            stage_path = os.path.join(
                input_data_path,
                tables["dir"],
                f"{campaign}_{stage}{part}",
                "StringTable",
            )
            parts[part] = LocalisationIndexed.read_files(stage_path, tables["string"])
            voice_path = os.path.join(
                input_data_path,
                tables["dir"],
                f"{campaign}_{stage}{part}",
                tables["voice"],
            )
            try:
                voice = VoiceTable().read_file(voice_path)["strings"]
            except FileNotFoundError:
                voice = []

            for v in voice:
                index = int(v["index"])
                for vf in VoiceTable.fields:
                    parts[part][index][vf] = v[vf]

        return parts

    @classmethod
    def write_files(
        cls, records: Dict[int, Dict], output_data_path: str, stage_id: int
    ):
        campaign = str(stage_id).zfill(5)[0:3]
        stage = str(stage_id).zfill(5)[3:5]

        for part, tables in cls.stage_tables.items():
            stage_path = os.path.join(
                output_data_path,
                tables["dir"],
                f"{campaign}_{stage}{part}",
                "StringTable",
            )
            LocalisationIndexed.write_files(records[part], output_data_path, stage_path)

            voice_path = os.path.join(
                output_data_path,
                tables["dir"],
                f"{campaign}_{stage}{part}",
                tables["voice"],
            )
            voices = []
            for index, v in records[part].items():
                voice = {"index": index}
                for vf in VoiceTable.fields:
                    voice[vf] = records[part][index][vf]
                voices.append(voice)
            VoiceTable().write_file({"strings": voices}, voice_path)


class VoiceTable(StringTBL):
    signature = b"\x54\x52\x54\x53\x00\x01\x01\x00"
    fields = ["voice_id", "unk1", "unk1", "unk1"]

    def write(self, records: Dict[str, List[Dict]]) -> bytes:
        for r in records["main"]:
            r["string"] = ",".join([str(r[f]) for f in self.fields])
        byte_string = super().write(records)

        return byte_string

    def read(self, buffer: BinaryIO) -> Dict[str, List[Dict]]:
        records = super().read(buffer)

        for record in records["main"]:
            for field, value in zip(self.fields, record.pop("string").split(",")):
                record[field] = value if field == "voice_id" else int(value)

        return records
