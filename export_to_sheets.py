import pandas as pd
from gspread_pandas import Spread, Client

import mechbay.parsers as parsers
import mechbay.container as container


def main():
    spread = Spread("Gundam G Generation Cross Rays Data")

    game_path = "./ggcr/data"

    classes = [
        parsers.ActAbilityEffectList,
        parsers.SeriesProfileList,
        parsers.MapTypes,
        parsers.CellAttributeList,
        parsers.SpecProfileList,
        parsers.PowerUpList,
        parsers.BattleBgList,
    ]

    data = {}

    for cls in classes:
        class_name, _, _ = cls.default_filename.rpartition(".")
        print("Reading", class_name)
        try:
            data.update(
                **{
                    f"{class_name}.{table}": records
                    for table, records in cls(game_path).read_file().items()
                }
            )
        except Exception as E:
            print("Error reading", class_name, ":", E)
            continue

    data.update(**container.CharacterSpecList(read_data_path=game_path).read())
    data.update(**container.AbilitySpecList(read_data_path=game_path).read())
    data.update(**container.MachineSpecList(read_data_path=game_path).read())
    data.update(**container.StageList(read_data_path=game_path).read())
    data.update(**container.MiscData(read_data_path=game_path).read())

    data = container.apply_effects(data)

    for sheet_name, records in data.items():
        print("Exporting", sheet_name)

        df = pd.json_normalize(records)
        spread.df_to_sheet(df, sheet=sheet_name, replace=True, index=False)
        spread.freeze(rows=1, sheet=sheet_name)


if __name__ == "__main__":
    main()
