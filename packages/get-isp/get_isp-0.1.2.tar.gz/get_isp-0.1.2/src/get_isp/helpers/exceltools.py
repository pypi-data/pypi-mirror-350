from concurrent.futures import ThreadPoolExecutor
import os
import re
import pandas as pd
from tqdm import tqdm

from get_isp.helpers.ispchecker import get_isp_info


def get_isp_from_api(input_file, telephone_column):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")

        tqdm.pandas()
        df = pd.read_excel(input_file, dtype=str)
        if telephone_column not in df.columns:
            raise ValueError(
                f"Column '{telephone_column}' not found in the Excel file."
            )

        df[telephone_column] = (
            df[telephone_column]
            .fillna("")
            .str.strip()
            .apply(lambda x: re.sub(r"\D", "", x))
        )

        mask = (df[telephone_column].str.len() == 10) & df[
            telephone_column
        ].str.startswith("0")

        # TODO: for limit testing
        # filtered_df = df[mask].copy().head(100)
        filtered_df = df[mask].copy()

        with ThreadPoolExecutor(max_workers=10) as executor:
            filtered_df["ISP"] = list(
                tqdm(
                    executor.map(get_isp_info, filtered_df[telephone_column]),
                    total=len(filtered_df),
                )
            )
        return filtered_df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
