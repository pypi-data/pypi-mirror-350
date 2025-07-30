import akshare as ak
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List
from pandas import DataFrame
from datetime import datetime
import logging
import pickle
import time
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class KLineFetcher_EM:
    """A class for fetching and caching A-share stock market data with Python 3.13 standard library preferences."""
    
    def __init__(self, cache_dir: Optional[str] = "data_cache"):
        """Initialize the DataFetcher with optional caching.
        
        Args:
            cache_dir: Directory to store cached data. If None, caching is disabled.
        """
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _fetch_all_ashare_code(self) -> List[str]:
        """Fetch all A-share stock codes."""
        df = ak.stock_info_a_code_name()
        return df['code'].tolist()
    
    def _get_cache_path(self, code: str, start_date: str, end_date: str) -> Path:
        """Generate cache file path for given parameters."""
        return self.cache_dir / f"{code}_{start_date}_{end_date}.pkl"
    
    def _validate_date_format(self, date_str: str) -> bool:
        """Validate date format is YYYYMMDD."""
        try:
            datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False
    
    def _fetch_single_stock(self, code: str, start_date: str, end_date: str) -> Optional[DataFrame]:
        """Fetch data for a single stock with caching and error handling."""
        if not self._validate_date_format(start_date) or not self._validate_date_format(end_date):
            logger.error(f"Invalid date format for {code}. Expected YYYYMMDD.")
            return None
        
        # 尝试从缓存加载
        if self.cache_dir:
            cache_path = self._get_cache_path(code, start_date, end_date)
            if cache_path.exists():
                try:
                    with cache_path.open('rb') as f:
                        return pickle.load(f)
                except (pickle.PickleError, EOFError) as e:
                    logger.warning(f"Failed to load cache for {code}: {e}")
        
        # 从API获取数据
        try:
            start_time = time.monotonic()
            df = ak.stock_zh_a_hist(
                symbol=code, 
                period="daily", 
                start_date=start_date, 
                end_date=end_date, 
                adjust=""
            )
            
            if df.empty:
                logger.warning(f"No data returned for {code}")
                return None
            
            elapsed = time.monotonic() - start_time
            logger.info(f"Fetched {len(df)} records for {code} in {elapsed:.2f}s")
            
            # 缓存数据
            if self.cache_dir:
                try:
                    with cache_path.open('wb') as f:
                        pickle.dump(df, f)
                except (pickle.PickleError, IOError) as e:
                    logger.warning(f"Failed to cache data for {code}: {e}")
            
            return df
        except Exception as e:
            logger.error(f"Failed to fetch data for {code}: {str(e)}")
            return None
    
    def fetch_ashare_data(
        self, 
        start_date: str, 
        end_date: str, 
        max_workers: int = 5,
        batch_report: int = 100
    ) -> DataFrame:
        """Fetch historical A-share data for all stocks between dates.
        
        Args:
            start_date: Start date in format 'YYYYMMDD'
            end_date: End date in format 'YYYYMMDD'
            max_workers: Maximum number of threads for parallel fetching
            batch_report: Report progress every N stocks
            
        Returns:
            A concatenated DataFrame containing all fetched data
            
        Raises:
            ValueError: If input dates are invalid or no data was fetched
        """
        if not self._validate_date_format(start_date):
            raise ValueError(f"Invalid start_date format: {start_date}. Expected YYYYMMDD.")
        if not self._validate_date_format(end_date):
            raise ValueError(f"Invalid end_date format: {end_date}. Expected YYYYMMDD.")
        
        codes = self._fetch_all_ashare_code()
        total_codes = len(codes)
        logger.info(f"Starting to fetch data for {total_codes} stocks from {start_date} to {end_date}")
        
        data = []
        processed = 0
        failed_codes = []
        failure_reasons = defaultdict(list)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._fetch_single_stock, code, start_date, end_date): code
                for code in codes
            }
            
            for future in as_completed(futures):
                processed += 1
                code = futures[future]
                
                try:
                    df = future.result()
                    if df is not None:
                        data.append(df)
                    else:
                        failed_codes.append(code)
                        failure_reasons["No data returned"].append(code)
                except Exception as e:
                    failed_codes.append(code)
                    failure_reasons[str(e)].append(code)
                    logger.error(f"Unexpected error processing {code}: {e}")
                
                # 定期报告进度
                if processed % batch_report == 0 or processed == total_codes:
                    success = processed - len(failed_codes)
                    logger.info(
                        f"Progress: {processed}/{total_codes} "
                        f"({processed/total_codes:.1%}) | "
                        f"Success: {success} | Failed: {len(failed_codes)}"
                    )
        
        # 打印失败统计
        if failed_codes:
            logger.warning(f"\nFailed to fetch data for {len(failed_codes)} stocks:")
            
            # 按失败原因分组打印
            for reason, codes in failure_reasons.items():
                logger.warning(f"\nFailure reason: {reason}")
                logger.warning("Failed codes: " + ", ".join(codes[:10]))  # 只打印前10个避免日志过长
                if len(codes) > 10:
                    logger.warning(f"... and {len(codes)-10} more")
        
        if not data:
            raise ValueError("No data was fetched successfully")
        
        result = pd.concat(data, ignore_index=True)
        logger.info(
            f"\nCompleted. Total records: {len(result)} from {len(data)} stocks. "
            f"Failed to fetch {len(failed_codes)} stocks."
        )
        logging.warning("Failed codes: %s", failed_codes)
        
        # 返回结果和失败代码列表
        return result

if __name__ == "__main__":
    fetcher = KLineFetcher_EM(cache_dir=r"D:\pj-m\data\days\cache")
    try:
        data = fetcher.fetch_ashare_data("20150101", "20250331", max_workers=10, batch_report=50)
        print(data.head())
        print(data.info())
    except ValueError as e:
        logger.error(f"Error fetching data: {e}")