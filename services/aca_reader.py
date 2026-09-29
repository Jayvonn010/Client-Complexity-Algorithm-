import pandas as pd
from pathlib import Path
from services.aca_reader import ACAReader

aca_reader = ACAReader()

file_types = {
    "csv": aca_reader.read_csv,
    "xlsx": aca_reader.read_excel,
    "json": aca_reader.read_json,
}
''' This function checks if the file exists and is a file. If it does not exist or is not a file, it will raise a ValueError.'''
def file_exists(file_path: Path) -> bool:
    if not isinstance(file_path, Path):
        raise TypeError("file_path must be a pathlib.Path object.")
    return file_path.exists() and file_path.is_file()

''' This is check the file extension to make sure that it is the supported file type. If it is not supported, it will raise a ValueError.'''
def load_client_data(file_path: Path) -> pd.DataFrame:
    if not file_exists(file_path):
        raise ValueError("File does not exist or is not a file.")

    file_extension = file_path.suffix[1:].lower()
    if file_extension not in file_types:
        raise ValueError(f"Unsupported file type: {file_extension}")
    df = file_types[file_extension](file_path)
    return df

def read_file(file_path: Path) -> pd.DataFrame:
    """Read a file and return a DataFrame."""
    if not file_exists(file_path):
        raise ValueError("File does not exist or is not a file.")
    file_extension = file_path.suffix[1:].lower()
    if file_extension not in file_types:
        raise ValueError(f"Unsupported file type: {file_extension}")
    return file_types[file_extension](file_path)


