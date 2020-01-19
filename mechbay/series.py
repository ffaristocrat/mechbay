import os
from itertools import zip_longest
from .cdb import SeriesList, SeriesProfileList
from .tbl import StringTBL

LANGUAGES = [
    "english",
    "japanese",
    "korean",
    "schinese",
    "tchinese/hk",
    "tchinese/tw",
]


class Series:
    def read(self, base_path: str):
        series_list = SeriesList().read_file(
            os.path.join(base_path, "data/resident/SeriesList.cdb")
        )
        series_profile_list = SeriesProfileList().read_file(
            os.path.join(base_path, "data/resident/SeriesProfileList.cdb")
        )

        series_profile_strings = {}
        misc_data_strings = {}

        for l in LANGUAGES:
            series_profile_strings[l] = StringTBL().read_file(
                os.path.join(base_path, f"data/language/{l}/SeriesProfileList.tbl")
            )
            misc_data_strings[l] = StringTBL().read_file(
                os.path.join(base_path, f"data/language/{l}/MiscData.tbl")
            )
        
        series = []
        for s, sp in zip_longest(series_list, series_profile_list, fillvalue={}):
            combined = {
                "logo_l": s["series_logo_l"],
                "logo_s": s["series_logo_s"],
                "gallery": sp.get("gallery"),
                "era": s["era"],
                "profile_value": sp.get("value"),
                "flag": s["flag"],
                "name": {
                    l: misc_data_strings[l][s["string_index"]]["string"]
                    for l in LANGUAGES
                },
                "profile": {
                    l: series_profile_strings[l][sp["string_index"]]["string"] if sp else None
                    for l in LANGUAGES
                },
            }
            series.append(combined)

        return series
