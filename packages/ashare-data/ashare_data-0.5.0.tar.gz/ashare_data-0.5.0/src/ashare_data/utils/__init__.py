import logging
from pathlib import Path
from .ParquetDailyStore import ParquetDailyStore
from .KLineFetcher_EM import KLineFetcher_EM
from .DailyDataReader import DailyDataReader

log = logging.getLogger(__name__)
__store=None
__fetcher=None
__reader=None

def create(data_dir:str, start_date:str, end_date:str)->None:
    __init(data_dir)
    __store.cleanup_all_parquet_files()
    df=__fetcher.fetch_ashare_data(start_date, end_date)
    __store.store_daily_data(df)

def update(data_dir:str)->None:
    __init(data_dir)
    start_date, end_date = __reader.get_missing_period()
    df = __fetcher.fetch_ashare_data(start_date, end_date,max_workers=1)
    __store.store_daily_data(df)

def __init(data_dir:str) -> None:
    global __store, __fetcher, __reader
    if(__ensure_data_subdirs(data_dir)):
        log.info("Data subdirectories ensured successfully.")
        base_path = Path(data_dir)
        store_path= base_path / "days" / "parquet"
        cache_path= base_path / "days" / "cache"
        __store=__store or ParquetDailyStore(data_folder=store_path)
        __fetcher=__fetcher or KLineFetcher_EM(cache_dir=cache_path)
        __reader=__reader or DailyDataReader(data_folder=store_path)

def __ensure_data_subdirs(data_dir: str) -> bool:
    """
    Ensures the necessary subdirectory structure ('days/parquet', 'days/cache')
    exists within the specified data directory.
    Args:
        data_dir: The root data directory path (string).
    Returns:
        True if the directories were successfully ensured (created or already existed),
        False if an error occurred during directory creation.
    """
    base_path = Path(data_dir)
    # Define the target subdirectories relative to the base path
    subdirs_to_create = [
        base_path / "days" / "parquet",
        base_path / "days" / "cache",
    ]
    log.info(f"Ensuring required subdirectories exist in: {base_path}")
    try:
        for subdir_path in subdirs_to_create:
            # Check if the specific path already exists but is a file
            if subdir_path.exists() and not subdir_path.is_dir():
                 log.error(f"Error: A file exists at the location where a directory is needed: {subdir_path}")
                 return False # Indicate failure
            # Create the directory
            # parents=True: Creates any necessary parent directories (like 'days')
            # exist_ok=True: Doesn't raise an error if the directory already exists
            subdir_path.mkdir(parents=True, exist_ok=True)
            log.debug(f"Directory ensured: {subdir_path}") # Use debug level for successful checks
        log.info("Required subdirectory structure is ready.")
        return True # Indicate success
    except PermissionError:
        log.error(f"Permission denied: Could not create subdirectories in {data_dir}.")
        return False # Indicate failure
    except OSError as e:
        # Catch other potential OS errors during directory creation
        log.error(f"Failed to create subdirectories in {data_dir}: {e}")
        return False # Indicate failure
    except Exception as e:
        # Catch any other unexpected errors
        log.error(f"An unexpected error occurred while ensuring directory structure: {e}")
        return False # Indicate failure