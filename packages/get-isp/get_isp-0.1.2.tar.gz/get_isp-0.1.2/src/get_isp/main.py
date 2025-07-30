import argparse
import datetime
import logging

from get_isp.helpers.exceltools import get_isp_from_api

logging.basicConfig(
    # filename='app.log',
    # filemode='a',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    starting_datestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description="GET ISP Info")
    parser.add_argument(
        "-i", "--input_path", type=str, required=True, help="5C file path"
    )
    parser.add_argument(
        "-c",
        "--column_name",
        default="เบอร์โทร-ที่ขอข้อมูล",
        type=str,
        required=False,
        help="Telephone number column name in the input file",
    )
    args = parser.parse_args()
    input_path = args.input_path
    column_name = args.column_name

    filtered_df = get_isp_from_api(input_path, column_name)
    result_filename = f"{starting_datestamp}_fetched_isp.xlsx"
    filtered_df.to_excel(result_filename, index=False)

    logging.info(f"ISP Record {len(filtered_df)} rows saved to {result_filename}.")
if __name__ == "__main__":
    main()
