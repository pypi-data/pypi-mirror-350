"""
CLI for the World Economic Outlook (WEO) Data Module.
Provides commands to download, save, and push WEO data.
"""
import argparse
import sys
from .core import download


def main():
    parser = argparse.ArgumentParser(
        description="WEO Data Module CLI: Download, save, or push IMF WEO data.")
    subparsers = parser.add_subparsers(dest="command")

    download_parser = subparsers.add_parser(
        "download", help="Download WEO data from IMF and optionally save or push to a database.")
    download_parser.add_argument(
        "year_month", type=str,
        help="Year and month of the WEO data (format: 'YYYY Month', e.g., '2025 April')")
    download_parser.add_argument(
        "-save", type=str,
        help="Path to save WEO data as a .xls file (e.g., -save data.xls)")
    download_parser.add_argument(
        "-database", type=str,
        help="Path to the SQLite database file (e.g., -database weo.db)")
    download_parser.add_argument(
        "-table", type=str,
        help="Database table name to store the data (e.g., -table weo_data)")

    args = parser.parse_args()

    if args.command == "download":
        # Validate year_month format
        try:
            year, month = args.year_month.split()
            int(year)
        except ValueError:
            parser.error("Invalid year_month format. Use 'YYYY Month' (e.g., '2025 April').")

        # Validate database and table arguments
        if args.database and not args.table:
            parser.error("If you specify a database, you must also specify a table using -table.")
        if args.table and not args.database:
            parser.error("If you specify a table, you must also specify a database using -database.")

        if not (args.save or (args.database and args.table)):
            print("Please specify either -save to save to a file or both -database and -table to push to a database.")
            sys.exit(1)
        try:
            download(
                vintage=args.year_month,
                save_path=args.save,
                database=args.database,
                table=args.table
            )
            print("Operation completed successfully.")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()