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
    header = b"\x54\x52\x54\x53\x00\x01\x01\x00"

    definition = {"index": "uint:4", "string": "uint:4"}

    def write(self, records: List[Dict]) -> bytes:
        record_count = len(records)
        string_bytes = self.write_header(record_count)

        string_start = len(string_bytes) + (record_count * 8)

        # We pad out a 16 byte row with null bytes
        # after the index
        padding = 16 - (string_start % 16)
        string_start += padding

        for record in records:
            string_bytes += self.write_int(record.get("index", 0), 4)
            string_bytes += self.write_int(string_start, 4)

            string_start += len(record["string"].encode("utf-8")) + 1

        string_bytes += b"\x00" * padding

        for record in records:
            string_bytes += self.write_string_null_term(record["string"])

        return string_bytes

    def read(self, buffer: BinaryIO) -> List[Dict]:
        record_count = self.read_header(buffer)
        records = self.read_records(self.definition, buffer, record_count)

        for record in records:
            # Pointers in StringTBLs work slightly differently
            record["string"] = self.read_string_null_term(buffer, record["string"])

        return records


class Localisation:
    @classmethod
    def read_files(cls, input_data_path: str, filename: str):
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
    def read_bytes(cls, data: Dict[str, bytes]) -> List[Dict]:
        records = []
        for language, byte_string in data.items():
            if not byte_string:
                continue

            localisation = StringTBL().read(BytesIO(byte_string))

            if not records:
                records = localisation[:]

            if len(records) != len(localisation):
                raise ValueError(f"Length of {language} string table does not match")

            for r, l in zip(records, localisation):
                r[language] = l["string"]

        for r in records:
            del r["string"]
            del r["index"]

        return records

    @classmethod
    def write_files(cls, records: List[Dict], output_data_path: str, filename: str):
        data = cls.write_bytes(records)

        for language, byte_string in data.items():
            full_path = os.path.join(output_data_path, language, filename)
            os.makedirs(os.path.split(full_path)[0], exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(byte_string)

    @classmethod
    def write_bytes(cls, records: List[Dict]) -> Dict[str, bytes]:
        data = {}
        for language in LANGUAGES:
            localisation = [
                {"string": r.get(language, ""), "index": 0}
                for r in records
            ]
            data[language] = StringTBL().write(localisation)

        return data


class LocalisationIndexed(Localisation):
    """ The stage versions have meaningful indexes
        And not all localisations have the strings present
    """

    @classmethod
    def read_bytes(cls, data: Dict[str, bytes]) -> Dict[int, Dict]:
        records = {}
        for language, byte_string in data.items():
            if not byte_string:
                continue
            localisation = StringTBL().read(BytesIO(byte_string))
            for line in localisation:
                index = int(line["index"])
                if index not in records:
                    records[index] = {}
                records[index][language] = line["string"]

        return records

    @classmethod
    def read_files(cls, input_data_path: str, filename: str) -> Dict[int, Dict]:
        data = {}
        for language in LANGUAGES:
            full_path = os.path.join(input_data_path, language, filename)
            try:
                with open(full_path, "rb") as f:
                    data[language] = f.read()
            except FileNotFoundError:
                data[language] = None

        records = cls.read_bytes(data)

        return records

    @classmethod
    def write_bytes(cls, records: Dict[int, Dict]) -> Dict[str, bytes]:
        data = {}
        for language in LANGUAGES:
            localisation = [
                {"string": r[language], "index": index}
                for index, r in records.items()
                if r.get(language) is not None
            ]
            data[language] = StringTBL().write(localisation)

        return data

    @classmethod
    def write_files(
        cls, records: Dict[int, Dict], output_data_path: str, filename: str
    ):
        data = cls.write_bytes(records)

        for language, byte_string in data.items():
            full_path = os.path.join(output_data_path, language, filename)
            os.makedirs(os.path.split(full_path)[0], exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(byte_string)


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
    voice_fields = ["voice_id", "val1", "val2", "val3"]

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
                voice = VoiceTable().read_file(voice_path)
            except FileNotFoundError:
                voice = []

            for v in voice:
                index = int(v["index"])
                parts[part][index]["voice_id"] = v["voice_id"]
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
                voice = {"index": index, "voice_id": records[part][index]["voice_id"]}
                for vf in VoiceTable.fields:
                    voice[vf] = records[part][index][vf]
                voices.append(voice)

            VoiceTable().write_file(voices, voice_path)


class VoiceTable(StringTBL):
    header = b"\x54\x52\x54\x53\x00\x01\x01\x00"
    # TODO: What do these values mean?
    fields = ["val1", "val2", "val3"]

    def write(self, records: List[Dict]) -> bytes:
        for r in records:
            r["string"] = ",".join([r["voice_id"]] + [r[f] for f in self.fields])
        byte_string = super().write(records)

        return byte_string

    def read(self, buffer: BinaryIO) -> List[Dict]:
        records = super().read(buffer)

        for record in records:
            unpack = record.pop("string").split(",")
            record["voice_id"] = unpack[0]
            for i, f in enumerate(self.fields):
                record[f] = int(unpack[i + 1])

        return records
