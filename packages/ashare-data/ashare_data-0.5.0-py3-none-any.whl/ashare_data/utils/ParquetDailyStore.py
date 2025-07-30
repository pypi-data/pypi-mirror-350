import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import logging
from pathlib import Path
from typing import Dict, List, Set  # 导入 用于类型提示
import akshare as ak

# --- Configuration ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

COLUMN_MAPPING: Dict[str, str] = {
    "日期": "date",
    "股票代码": "code",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "振幅": "amplitude",
    "涨跌幅": "pct_change",
    "涨跌额": "change",
    "换手率": "turnover_rate",
}
EXPECTED_ENG_COLUMNS: List[str] = list(COLUMN_MAPPING.values())
UNIQUE_KEY_COLUMNS: List[str] = ["date", "code"]


class ParquetDailyStore:
    """
    工具类，用于将日线数据的 Pandas DataFrame 高效地存储到 Parquet 文件中。
    数据按年份分区存储，并支持增量更新（合并、去重、覆盖）。
    使用 pathlib 进行路径操作。
    """

    def __init__(
        self,
        data_folder: str|Path,
        column_mapping: Dict[str, str] = COLUMN_MAPPING,
        unique_key_columns: List[str] = UNIQUE_KEY_COLUMNS,
    ):
        self._data_folder = Path(data_folder)
        self._column_mapping = column_mapping
        self._unique_key_columns = unique_key_columns
        self._expected_eng_columns = list(column_mapping.values())
        logging.info("ParquetDailyStore initialized.")

    def _validate_and_prepare_df(self, df: pd.DataFrame) -> pd.DataFrame | None:
        if not isinstance(df, pd.DataFrame):
            logging.error("Input 'df' is not a Pandas DataFrame.")
            return None
        if df.empty:
            logging.warning("Input DataFrame 'df' is empty. Nothing to store.")
            return None

        df_processed = df.copy()

        # 1. 重命名列
        try:
            missing_cols = [
                col
                for col in self._column_mapping.keys()
                if col not in df_processed.columns
            ]
            if missing_cols:
                logging.error(
                    f"Input DataFrame is missing required columns: {missing_cols}"
                )
                return None
            df_processed.rename(columns=self._column_mapping, inplace=True)
        except Exception as e:
            logging.error(f"Error renaming columns: {e}")
            return None

        # 2. 检查重命名后的列是否完整
        if not all(col in df_processed.columns for col in self._expected_eng_columns):
            missing_eng_cols = [
                col
                for col in self._expected_eng_columns
                if col not in df_processed.columns
            ]
            logging.error(
                f"DataFrame missing expected English columns after rename: {missing_eng_cols}"
            )
            return None

        # 3. 转换 'date' 列为 datetime 对象
        if "date" not in df_processed.columns:
            logging.error("Critical error: 'date' column not found after renaming.")
            return None
        try:
            df_processed["date"] = pd.to_datetime(df_processed["date"], errors="coerce")
            if df_processed["date"].isnull().any():
                logging.warning(
                    "Some 'date' values could not be parsed and were set to NaT."
                )
                df_processed.dropna(subset=["date"], inplace=True)
                if df_processed.empty:
                    logging.warning(
                        "DataFrame became empty after removing rows with invalid dates."
                    )
                    return None
        except Exception as e:
            logging.error(f"Error converting 'date' column to datetime: {e}")
            return None


        # 5. 添加 'year' 列用于分组
        try:
            df_processed["year"] = df_processed["date"].dt.year
        except AttributeError:
            logging.error(
                "Cannot extract year because 'date' column is not in datetime format."
            )
            return None
        except Exception as e:
            logging.error(f"Error adding 'year' column: {e}")
            return None

        # 6. 检查用于去重的列是否存在
        if not all(col in df_processed.columns for col in self._unique_key_columns):
            missing_key_cols = [
                col
                for col in self._unique_key_columns
                if col not in df_processed.columns
            ]
            logging.error(
                f"DataFrame missing columns needed for deduplication: {missing_key_cols}"
            )
            return None

        return df_processed

    def store_daily_data(self, df: pd.DataFrame) -> None:
        root_path = self._data_folder
        logging.info(f"Starting data storage process for path: {root_path}")

        df_prepared = self._validate_and_prepare_df(df)
        if df_prepared is None:
            logging.error("Data preparation failed. Aborting storage process.")
            return

        try:
            root_path.mkdir(parents=True, exist_ok=True)
            logging.debug(f"Ensured directory exists: {root_path}")
        except OSError as e:
            logging.error(f"Failed to create or access directory {root_path}: {e}")
            return

        grouped_by_year = df_prepared.groupby("year")
        total_years = len(grouped_by_year)
        processed_years = 0
        logging.info(f"Processing data for {total_years} year(s).")

        for year, group_df in grouped_by_year:
            processed_years += 1
            year_str = str(year)
            file_path: Path = root_path / f"{year_str}.parquet"
            logging.info(
                f"[{processed_years}/{total_years}] Processing year: {year_str} -> {file_path}"
            )

            try:
                current_year_data = group_df.drop_duplicates(
                    subset=self._unique_key_columns, keep="last"
                ).copy()

                final_df_to_write = None

                if file_path.exists():
                    logging.debug(f"File exists: {file_path}. Reading existing data.")
                    try:
                        existing_table = pq.read_table(file_path)
                        existing_df = existing_table.to_pandas()
                        logging.info(
                            f"Read {len(existing_df)} rows from existing file {file_path}."
                        )
                        combined_df = pd.concat(
                            [existing_df, current_year_data], ignore_index=True
                        )
                        logging.debug(
                            f"Combined data size before deduplication: {len(combined_df)}"
                        )
                        final_df_to_write = combined_df.drop_duplicates(
                            subset=self._unique_key_columns, keep="last"
                        )
                        logging.info(
                            f"Combined data size after deduplication: {len(final_df_to_write)}"
                        )
                    except pa.ArrowIOError as e:
                        logging.error(
                            f"Error reading existing Parquet file {file_path}: {e}. Skipping update for this year."
                        )
                        raise
                    except Exception as e:
                        logging.error(
                            f"Unexpected error processing existing file {file_path}: {e}. Skipping update for this year."
                        )
                        raise
                else:
                    logging.debug(
                        f"File does not exist: {file_path}. Preparing to write new data."
                    )
                    final_df_to_write = current_year_data

                if final_df_to_write is not None and not final_df_to_write.empty:
                    try:
                        final_df_to_write = final_df_to_write.drop(columns=['year'])
                        arrow_table = pa.Table.from_pandas(
                            final_df_to_write, preserve_index=False
                        )
                        pq.write_table(arrow_table, file_path, compression="snappy")
                        logging.info(
                            f"Successfully wrote {len(final_df_to_write)} rows to {file_path}"
                        )
                    except pa.ArrowInvalid as e:
                        logging.error(
                            f"Data type issue writing to {file_path}: {e}. DataFrame head:\n{final_df_to_write.head()}"
                        )
                    except Exception as e:
                        logging.error(f"Error writing Parquet file {file_path}: {e}")
                elif final_df_to_write is not None and final_df_to_write.empty:
                    logging.warning(
                        f"Final DataFrame for year {year_str} is empty after processing. No file written or updated for {file_path}."
                    )
                else:
                    logging.error(
                        f"Internal logic error: final_df_to_write is None for year {year_str}"
                    )

            except Exception as e:
                logging.error(
                    f"An unexpected error occurred while processing year {year_str}: {e}"
                )
                raise

        logging.info("Data storage process finished.")

    def cleanup_all_parquet_files(self, remove_empty_folders: bool = False) -> None:
        """
        删除数据文件夹中的所有Parquet文件
        
        参数:
            remove_empty_folders: 是否在删除Parquet文件后删除空文件夹
            
        返回:
            None
        """
        deleted_files = 0
        deleted_folders = 0
        
        # 删除所有.parquet文件
        for parquet_file in self._data_folder.rglob('*.parquet'):
            try:
                parquet_file.unlink()  # 删除文件
                deleted_files += 1
                logging.debug(f"Deleted Parquet file: {parquet_file}")
            except Exception as e:
                logging.warning(f"Failed to delete {parquet_file}: {str(e)}")
        
        logging.info(f"Deleted {deleted_files} Parquet files from {self._data_folder}")
        
        # 如果需要，删除空文件夹
        if remove_empty_folders:
            for folder in list(self._data_folder.rglob('*')):
                if folder.is_dir() and not any(folder.iterdir()):
                    try:
                        folder.rmdir()  # 删除空文件夹
                        deleted_folders += 1
                        logging.debug(f"Removed empty folder: {folder}")
                    except Exception as e:
                        logging.warning(f"Failed to remove folder {folder}: {str(e)}")
            
            logging.info(f"Removed {deleted_folders} empty folders from {self._data_folder}")

# --- Helper Function for Example ---
def __get_unique_years_from_df(df: pd.DataFrame, date_col_name: str = "日期") -> Set[int]:
    """
    从 DataFrame 的日期列中安全地提取唯一的年份。

    Args:
        df (pd.DataFrame): 输入的 DataFrame。
        date_col_name (str): 包含日期的列名 (原始名称)。

    Returns:
        Set[int]: 包含不重复年份的集合。如果列不存在或无法处理，返回空集合。
    """
    if df is None or df.empty or date_col_name not in df.columns:
        return set()
    try:
        # 转换为 datetime，无法转换的变为 NaT
        dates = pd.to_datetime(df[date_col_name], errors="coerce")
        # 移除 NaT 并提取年份，去重
        return set(dates.dropna().dt.year)
    except Exception as e:
        logging.warning(f"Could not extract years from column '{date_col_name}': {e}")
        return set()


# --- Example Usage (Dynamic Year Verification) ---
if __name__ == "__main__":
    # 1. 创建示例数据
    df1 = ak.stock_zh_a_hist(
        symbol="600000",
        period="daily",
        start_date="20150101",
        end_date="20240130",
        adjust="",
    )
    df2 = ak.stock_zh_a_hist(
        symbol="600000",
        period="daily",
        start_date="20240101",
        end_date="20250331",
        adjust="",
    )

    # 2. 指定存储目录
    # storage_path = Path(r"D:\pj-m\data\days\parquet\test")
    # 3. 创建存储工具实例
    store = ParquetDailyStore(r"D:\pj-m\data\days\parquet\test")

    # 4. 动态获取输入数据的年份
    years_in_df1 = __get_unique_years_from_df(df1, "日期")
    years_in_df2 = __get_unique_years_from_df(df2, "日期")
    all_involved_years = years_in_df1.union(years_in_df2)

    print(f"Years found in df1: {sorted(list(years_in_df1))}")
    print(f"Years found in df2: {sorted(list(years_in_df2))}")
    print(f"All unique years across df1 & df2: {sorted(list(all_involved_years))}")

    # --- 第一次存储 ---
    print("\n--- First Store Operation ---")
    store.store_daily_data(df1 )
    storage_path = Path(r"D:\pj-m\data\days\parquet\test")
    # 验证第一次存储的结果
    print(
        f"\n--- Verifying files after first store (Expected years: {sorted(list(years_in_df1))}) ---"
    )
    if storage_path.exists() and storage_path.is_dir():
        print(
            f"Files found in {storage_path}: {[p.name for p in storage_path.iterdir()]}"
        )
        verified_count = 0
        for year in sorted(list(years_in_df1)):
            file_path_to_check = storage_path / f"{year}.parquet"
            print(f"\nChecking for: {file_path_to_check.name}")
            if file_path_to_check.exists():
                try:
                    df_read = pd.read_parquet(file_path_to_check)
                    print(
                        f"Content of {file_path_to_check.name} (rows: {len(df_read)}):"
                    )
                    print(df_read.head(3))  # 打印前几行看看
                    verified_count += 1
                except Exception as e:
                    print(f"Error reading {file_path_to_check.name}: {e}")
            else:
                # 这通常不应该发生，因为我们只检查 df1 中存在的年份
                print(
                    f"File {file_path_to_check.name} NOT FOUND (Unexpected for first store)."
                )
        print(
            f"\nVerified {verified_count} out of {len(years_in_df1)} expected files from df1."
        )
    else:
        print(f"Directory {storage_path} was not created.")

    # --- 第二次存储 ---
    print("\n--- Second Store Operation (Append/Update) ---")
    store.store_daily_data(df2)

    # 验证第二次存储的结果 (检查所有涉及的年份)
    print(
        f"\n--- Verifying files after second store (Expected years: {sorted(list(all_involved_years))}) ---"
    )
    if storage_path.exists() and storage_path.is_dir():
        print(
            f"Files found in {storage_path}: {[p.name for p in storage_path.iterdir()]}"
        )
        verified_count = 0
        for year in sorted(list(all_involved_years)):
            file_path_to_check = storage_path / f"{year}.parquet"
            print(f"\nChecking for: {file_path_to_check.name}")
            if file_path_to_check.exists():
                try:
                    df_read = pd.read_parquet(file_path_to_check)
                    print(
                        f"Content of {file_path_to_check.name} (rows: {len(df_read)}):"
                    )
                    print(df_read.head(3))  # 打印前几行
                    # 特别检查更新效果 (df2 中 2015-01-05 000001 的 open 应该是 10.1)
                    if year == 2015:
                        record = df_read[
                            (df_read["date"] == "2015-01-05")
                            & (df_read["code"] == "000001")
                        ]
                        if not record.empty:
                            print(
                                f"  Check updated record (2015-01-05, 000001): Open = {record['open'].iloc[0]}"
                            )
                        else:
                            print(
                                "  Record (2015-01-05, 000001) not found in 2015 file after update."
                            )

                    verified_count += 1
                except Exception as e:
                    print(f"Error reading {file_path_to_check.name}: {e}")
            else:
                # 这可能发生，如果 df2 中的某个年份数据处理失败
                print(f"File {file_path_to_check.name} NOT FOUND.")
        print(
            f"\nVerified {verified_count} out of {len(all_involved_years)} expected files after second store."
        )
    else:
        print(f"Directory {storage_path} does not exist.")
