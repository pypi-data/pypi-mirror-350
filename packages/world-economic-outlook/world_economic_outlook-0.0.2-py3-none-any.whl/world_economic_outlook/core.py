"""
Core logic for downloading, saving, and pushing IMF World Economic Outlook (WEO) data.
"""
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import io
import csv
from typing import Optional, List, Dict
from simple_sqlite3 import Database
from charset_normalizer import detect


def download_weo_data(year: int, month: str) -> bytes:
    """
    Downloads WEO data for a specific year and month from the IMF website.

    Args:
        year (int): The year of the WEO data (e.g., 2025).
        month (str): The month of the WEO data (e.g., 'April').

    Returns:
        bytes: The raw bytes of the downloaded WEO data file.

    Raises:
        ValueError: If the download link is not found on the IMF page.
        requests.HTTPError: If the HTTP request fails.
    """
    IMF_URL = f"https://www.imf.org/en/Publications/WEO/weo-database/{year}/{month}/download-entire-database"
    response = requests.get(IMF_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('a', href=lambda href: href and "/-/media/Files/Publications/WEO/WEO-Database" in href)
    if not link:
        raise ValueError("WEO data link not found on the IMF page.")
    file_url = "https://www.imf.org" + link['href']
    file_response = requests.get(file_url, stream=True)
    file_response.raise_for_status()
    total_size = int(file_response.headers.get('content-length', 0))
    block_size = 1024
    t = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f"Downloading {month} {year} WEO data", colour='#004C97')
    data = bytearray()
    for chunk in file_response.iter_content(block_size):
        t.update(len(chunk))
        data.extend(chunk)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("Warning: Downloaded size does not match the expected size. Proceeding anyway.")
    return bytes(data)


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


def push_weo_data(data: bytes, database_path: str, database_table: str, vintage: str) -> None:
    """
    Pushes WEO data to a database table as structured records.

    Args:
        data (bytes): The WEO data to insert into the database.
        database_path (str): Path to the SQLite database file.
        database_table (str): Name of the table to insert data into.
        vintage (str): The vintage string (e.g., '2025 April') to annotate records.

    Raises:
        ValueError: If no data is provided.
        Exception: If database operations fail.
    """
    if not data:
        raise ValueError("No data to process. Please download the data first.")
    data_stream = io.BytesIO(data)
    def detect_encoding(data: bytes) -> str:
        sample_size = 10 * 1024
        sample_data = data[:sample_size]
        encoding = detect(sample_data)["encoding"]
        return "windows-1250" if encoding == "ascii" else "utf-16-le"
    db = Database(database_path)
    encoding = detect_encoding(data)
    try:
        with io.TextIOWrapper(data_stream, encoding=encoding) as file:
            reader = csv.reader(file, delimiter='\t')
            headers = next(reader)
            estimates_start_after_idx = headers.index("Estimates Start After")
            records: List[Dict] = []
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
                        # Accept negative values and floats
                        try:
                            value = float(row[col_idx])
                        except (ValueError, TypeError):
                            value = None
                        if year_col:
                            record = {
                                "iso": iso,
                                "weo_subject_code": weo_subject_code,
                                "country": country,
                                "subject_descriptor": subject_descriptor,
                                "units": units,
                                "scale": scale,
                                "year": int(year_col),
                                "value": value,
                                "estimates_start_after": estimates_start_after,
                                "estimate": estimates_start_after is not None and int(year_col) > estimates_start_after,
                                "vintage": vintage
                            }
                            records.append(record)
                except IndexError:
                    continue
            table = db.table(database_table)
            table.insert(records)
        print(f"WEO data pushed to database '{database_path}' (table: '{database_table}') successfully.")
    except Exception as e:
        print(f"Failed to push WEO data to database: {e}")
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
