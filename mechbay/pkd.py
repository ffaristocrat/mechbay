import os
from typing import List, Dict, BinaryIO, NamedTuple

from .data import GundamDataFile


RESIDENT = {
    "CharacterSpecList.pkd": [
        "CharacterSpecList.cdb",
        "CharacterGrowthList.cdb",
        "SkillAcquisitionPatternList.cdb",
        "MyCharacterConfigurations.cdb",
    ],
    "MachineSpecList.pkd": [
        "RangeDataList.cdb",
        "MachineGrowthList.cdb",
        "WeaponSpecList.cdb",
        "MachineSpecList.cdb",
        "MachineConversionList.cdb",
        "PersonalMachineList.cdb",
        "MachineDevelopmentList.cdb",
        "MachineDesignList.cdb",
    ],
    "MiscData.pkd": [
        "DatabaseCaluclation.cdb",
        "SeriesList.cdb",
        "GroupSendingMissionList.cdb",
        "TutorialList.cdb",
    ],
    "StageList.pkd": ["StageList.cdb", "QuestList.cdb", "GetUnitList.cdb"],
    "CellAttributeList.pkd": ["CellAttributeList.cdb", "BattleBgList.cdb"],
}


class PkdInfo(NamedTuple):
    name: str
    size: int


class PkdFile:
    __header = b"\x20\x44\x4B\x50\x00\x01\x03\x00"

    def __init__(self, file, mode: str = "x"):
        self._file = file
        self._mode = mode

        self._handle = None

    def close(self):
        pass

    def getinfo(self, name: str):
        pass

    def infolist(self) -> List:
        pass

    def namelist(self) -> List[str]:
        pass

    def open(self, name: str, mode="r"):
        pass

    def extract(self, member, path=None):
        pass

    def extractall(self, path=None, members=None):
        pass

    def printdir(self):
        pass

    def read(self):
        pass

    def testpkd(self):
        pass

    def write(self, filename, arcname=None):
        pass

    def writestr(self, zinfo_or_arcname, data):
        pass

    @property
    def filename(self):
        return

    @property
    def mode(self):
        return self._mode


class PKDArchive(GundamDataFile):
    signature = b"\x20\x44\x4B\x50\x00\x01\x03\x00"
    definitions = {
        "main": {
            "file_pointer": "uint:4",
            "file_size": "uint:4",
            "name_pointer": "uint:4",
        }
    }

    def write(self, records: Dict[str, bytes]) -> bytes:
        padding = 64
        string_bytes = bytes()

        string_bytes += self.signature
        record_count = len(records)
        string_bytes += self.write_int(record_count, 4)
        # Maybe number of bits for padding? long? Always seems to 0x40000000
        string_bytes += self.write_int(padding, 4)

        # index size
        index_size = (record_count * 12) + sum(
            [len(filename.encode("utf-8")) + 1 for filename in records.keys()]
        )
        string_bytes += self.write_int(index_size, 4)

        # initial pointers
        name_start = record_count * 12
        file_start = index_size + 20
        file_start += padding - (file_start % padding)
        for filename, data in records.items():
            # File pointer
            string_bytes += self.write_int(file_start, 4)

            # File size
            string_bytes += self.write_int(len(data), 4)
            file_start += len(data)
            # Pad to 64 byte increments
            file_start += padding - (file_start % padding)

            # name pointer
            string_bytes += self.write_int(name_start, 4)
            name_start += len(filename.encode("utf-8")) + 1

        for filename in records.keys():
            string_bytes += filename.encode("utf-8") + b"\x00"
        string_bytes += (padding - (len(string_bytes) % padding)) * b"\x00"

        for filename, data in records.items():
            string_bytes += data
            string_bytes += (padding - (len(string_bytes) % padding)) * b"\x00"

        return string_bytes

    @classmethod
    def read_header(cls, buffer: BinaryIO) -> Dict[str, Dict[str, int]]:
        signature = buffer.read(len(cls.signature))
        assert signature == cls.signature

        header = {
            "counts": {"main": cls.read_int(buffer.read(cls.record_count_length))},
            "pointers": {},
        }
        # Maybe number of bits for long? Always seems to 0x40000000
        cls.read_int(buffer.read(4))
        # Size of the index block which we don't care about tbh
        cls.read_int(buffer.read(4))
        header["pointers"]["main"] = buffer.tell()

        return header

    def read(self, buffer: BinaryIO) -> Dict[str, bytes]:
        header = self.read_header(buffer)
        files = self.read_records(
            self.definitions["main"], buffer, header["counts"]["main"]
        )

        for file in files:
            file["filename"] = self.read_string_null_term(
                buffer, file["name_pointer"] + 20
            )

        archive = {}
        for file in files:
            buffer.seek(file["file_pointer"])
            archive[file["filename"]] = buffer.read(file["file_size"])

        return archive

    def pack_files(self, filenames: List[str]) -> bytes:
        records = {}
        for filename in filenames:
            with open(filename, "rb") as file:
                records[os.path.split(filename)[1]] = file.read()

        return self.write(records)

    def read_file(self, filename: str = None) -> Dict[str, bytes]:
        with open(filename, "rb") as buffer:
            archive = self.read(buffer)

        return archive

    def write_file(self, records: Dict[str, bytes], filename: str):
        os.makedirs(os.path.split(filename)[0], exist_ok=True)
        with open(filename, "wb") as buffer:
            buffer.write(self.write(records))
