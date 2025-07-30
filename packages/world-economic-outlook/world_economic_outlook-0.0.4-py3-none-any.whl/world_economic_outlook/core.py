import urllib.request
import re
import io
import csv
from simple_sqlite3 import Database
from typing import Optional


def download_weo_data(year: int, month: str) -> bytes:
    url = f"https://www.imf.org/en/Publications/WEO/weo-database/{year}/{month}/download-entire-database"
    with urllib.request.urlopen(url) as response:
        html = response.read().decode()
    match = re.search(r'href="(/-/media/Files/Publications/WEO/WEO-Database[^"]+)"', html)
    if not match:
        raise ValueError("WEO data link not found on the IMF page.")
    file_url = "https://www.imf.org" + match.group(1)
    with urllib.request.urlopen(file_url) as file_response:
        data = file_response.read()
    return data


def push_weo_data(data: bytes, database_path: str, database_table: str, vintage: str) -> None:
    # Try utf-16-le first, then fallback to windows-1250
    try:
        file = io.TextIOWrapper(io.BytesIO(data), encoding="utf-16-le")
        reader = csv.reader(file, delimiter='\t')
        headers = next(reader)
    except UnicodeError:
        file = io.TextIOWrapper(io.BytesIO(data), encoding="windows-1250")
        reader = csv.reader(file, delimiter='\t')
        headers = next(reader)
    estimates_start_after_idx = headers.index("Estimates Start After")

    rows = []
    for row in reader:
        try:
            iso = row[1]
            weo_subject_code = row[2]
            country = row[3]
            subject_descriptor = row[4]
            units = row[6]
            scale = row[7] if len(row) > 7 else None
            estimates_start_after = int(row[estimates_start_after_idx]) if row[estimates_start_after_idx].isdigit() else None
            for col_idx in range(9, estimates_start_after_idx):
                year_col = ''.join(filter(str.isdigit, headers[col_idx]))
                try:
                    value = float(row[col_idx])
                except (ValueError, TypeError):
                    value = None
                if year_col:
                    rows.append((
                        iso, weo_subject_code, country, subject_descriptor, units, scale,
                        int(year_col), value, estimates_start_after,
                        int(estimates_start_after is not None and int(year_col) > estimates_start_after),
                        vintage
                    ))
        except IndexError:
            continue
    
    schema = """
        iso TEXT,
        weo_subject_code TEXT,
        country TEXT,
        subject_descriptor TEXT,
        units TEXT,
        scale TEXT,
        year INTEGER,
        value REAL,
        estimates_start_after INTEGER,
        estimate INTEGER,
        vintage TEXT
    """
    
    columns = tuple(col.strip().split()[0] for col in schema.strip().split(",\n"))

    db = Database(database_path)

    table = db.table(database_table)

    table.bulk_insert(rows=rows, columns=columns, schema=schema)


def save_weo_data(year: int, month: str, data: bytes, path: Optional[str] = None) -> None:
    """
    Saves the WEO data as an .xls file to the specified path.

    Args:
        year (int): The year of the WEO data.
        month (str): The month of the WEO data.
        data (bytes): The WEO data to save.
        path (str, optional): The file path to save the data. Defaults to '{year}_{month}.xls'.

    Raises:
        ValueError: If no data is provided.
        Exception: If file writing fails.
    """
    if not data:
        raise ValueError("No data to save. Please download the data first.")
    if path is None:
        path = f"{year}_{month}.xls"
    try:
        with open(path, 'wb') as file:
            file.write(data)
        print(f"WEO data saved to '{path}' successfully.")
    except Exception as e:
        print(f"Failed to save WEO data: {e}")
        raise


def download(vintage: str, save_path: str = None, database: str = None, table: str = None):
    """
    Downloads IMF WEO data for a given vintage and optionally saves to file or database.

    Args:
        vintage (str): The vintage string (e.g., '2025 April').
        save_path (str, optional): Path to save the WEO data as a file.
        database (str, optional): Path to the SQLite database file.
        table (str, optional): Name of the table to insert data into.

    Returns:
        bytes | None: The WEO data bytes if not saved or pushed, otherwise None.
    """
    year, month = vintage.split()
    year = int(year)
    data = download_weo_data(year, month)
    if save_path:
        save_weo_data(year, month, data, save_path)
        return None
    if database and table:
        push_weo_data(data, database, table, vintage)
        return None
    return data


class WEO:
    """
    Wrapper object for downloading, saving, and pushing IMF WEO data.
    """
    def __init__(self):
        """
        Initializes a WEO object. Vintage is now provided in download().
        """
        self.year = None
        self.month = None
        self.vintage = None
        self.data = None

    def download(self, vintage: str):
        """
        Downloads the WEO data for the specified vintage and stores it in the instance.

        Args:
            vintage (str): The vintage string (e.g., '2025 April').

        Returns:
            bytes: The downloaded WEO data.
        """
        self.year, self.month = vintage.split()
        self.year = int(self.year)
        self.vintage = vintage
        self.data = download_weo_data(self.year, self.month)
        return self.data

    def save(self, path: str = None):
        """
        Saves the downloaded data as an .xls file.

        Args:
            path (str, optional): The file path to save the data. Defaults to '{year}_{month}.xls'.

        Raises:
            ValueError: If no data has been downloaded yet.
        """
        if self.data is None:
            raise ValueError("No data downloaded. Call download() first.")
        save_weo_data(self.year, self.month, self.data, path)

    def push(self, database: str, table: str):
        """
        Pushes the downloaded data to a database as clean data.

        Args:
            database (str): Path to the SQLite database file.
            table (str): Name of the table to insert data into.

        Raises:
            ValueError: If no data has been downloaded yet.
        """
        if self.data is None:
            raise ValueError("No data downloaded. Call download() first.")
        push_weo_data(self.data, database, table, self.vintage)
