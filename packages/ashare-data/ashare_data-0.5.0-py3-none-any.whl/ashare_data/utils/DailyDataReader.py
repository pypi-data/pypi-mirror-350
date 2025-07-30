import pandas as pd
import pyarrow.dataset as ds
from pathlib import Path
import logging
from typing import List, Optional, Union
from datetime import datetime, date, timedelta

# 配置基础日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义预期的数据列（保证空DataFrame的结构一致性）
EXPECTED_COLUMNS = [
    'date', 'code', 'open', 'close', 'high', 'low', 'volume',
    'amount', 'amplitude', 'pct_change', 'change', 'turnover_rate'
]

class DailyDataReader:
    """
    用于从按年份分区的Parquet文件中读取股票日线数据的工具类

    假设Parquet文件按年份命名（例如2023.parquet），
    每个文件包含某年多个股票代码的日线数据

    属性：
        data_folder (Path): Parquet文件存储根目录路径
    """

    def __init__(self, data_folder: str):
        """
        初始化数据读取器

        参数：
            data_folder (str): Parquet文件存储目录路径

        异常：
            FileNotFoundError: 当指定目录不存在时抛出
        """
        self.data_folder = Path(data_folder)
        if not self.data_folder.is_dir():
            raise FileNotFoundError(f"数据目录不存在或不是文件夹: {data_folder}")
        logging.info(f"数据读取器已初始化，数据目录: {self.data_folder}")

    def _validate_dates(self, start_date_str: str, end_date_str: str) -> Optional[tuple[datetime, datetime]]:
        """验证日期格式及顺序有效性"""
        try:
            start_dt = datetime.strptime(start_date_str, '%Y%m%d')
            end_dt = datetime.strptime(end_date_str, '%Y%m%d')
        except ValueError:
            logging.error(f"日期格式错误，请使用'YYYYMMDD'格式。输入 start='{start_date_str}', end='{end_date_str}'")
            return None

        if start_dt > end_dt:
            logging.error(f"开始日期'{start_date_str}'不能晚于结束日期'{end_date_str}'")
            return None
        return start_dt, end_dt

    def _get_relevant_years(self, start_dt: datetime, end_dt: datetime) -> List[int]:
        """根据起止日期确定相关年份范围"""
        start_year = start_dt.year
        end_year = end_dt.year
        return list(range(start_year, end_year + 1))

    def _create_empty_df(self) -> pd.DataFrame:
        """创建符合预期结构的空DataFrame"""
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    def read_data(self, code: Union[str, List[str]], start_date: str, end_date: str) -> pd.DataFrame:
        """
        读取指定股票代码（单个/多个/全部）在日期范围内的日线数据

        参数：
            code (Union[str, List[str]]):
                - 单个股票代码（例如'000001'）
                - 股票代码列表（例如['000001', '600000']）
                - 字符串'all'表示读取所有股票代码
            start_date (str): 开始日期（格式'YYYYMMDD'）
            end_date (str): 结束日期（格式'YYYYMMDD'）

        返回：
            pd.DataFrame: 按日期排序的日线数据，无数据时返回空DataFrame
        """
        # --- 校验股票代码输入类型 ---
        is_single_code = isinstance(code, str) and code.lower() != 'all'
        is_multiple_codes = isinstance(code, list) and len(code) > 0 and all(isinstance(c, str) for c in code)
        is_all_codes = isinstance(code, str) and code.lower() == 'all'

        if not (is_single_code or is_multiple_codes or is_all_codes):
            logging.error(f"无效的股票代码参数。应为非空字符串（非'all'）、"
                          f"非空字符串列表或'all'。当前输入: {code}")
            return self._create_empty_df()

        validated_dates = self._validate_dates(start_date, end_date)
        if not validated_dates:
            return self._create_empty_df()  # 验证失败返回空DataFrame
        start_dt, end_dt = validated_dates

        relevant_years = self._get_relevant_years(start_dt, end_dt)

        # --- 根据代码类型调整日志信息 ---
        if is_single_code:
            log_code_repr = f"股票代码'{code}'"
        elif is_multiple_codes:
            # 截断过长的代码列表
            log_code_repr = f"代码列表 {code[:5]}{'...' if len(code) > 5 else ''}"
        else:  # 全部代码
            log_code_repr = "所有股票代码"
            logging.warning("正在读取全部股票代码数据，大日期范围可能导致内存消耗过高")

        logging.info(f"正在读取{log_code_repr}从{start_date}到{end_date}的数据，涉及年份: {relevant_years}")

        all_data_frames = []

        for year in relevant_years:
            file_path = self.data_folder / f"{year}.parquet"
            if not file_path.is_file():
                logging.warning(f"年份文件不存在: {year} - {file_path}，跳过")
                continue

            # --- 根据代码类型确定过滤条件 ---
            pyarrow_filter = None
            pandas_filter = None
            if is_single_code:
                pyarrow_filter = (ds.field('code') == code)
                pandas_filter = [('code', '==', code)]
            elif is_multiple_codes:
                pyarrow_filter = ds.field('code').isin(code)
                pandas_filter = [('code', 'in', code)]
            # 全部代码不需要过滤条件

            try:
                # --- 性能优化：使用PyArrow Dataset进行谓词下推 ---
                dataset = ds.dataset(file_path, format="parquet")
                table = dataset.to_table(filter=pyarrow_filter)  # 应用过滤条件

                if table.num_rows > 0:
                    df_year = table.to_pandas()
                    all_data_frames.append(df_year)
                    logging.debug(f"从{file_path}读取到{table.num_rows}行{log_code_repr}的数据")
                else:
                    logging.debug(f"{file_path}中未找到{log_code_repr}的匹配数据")

            except ImportError:
                logging.warning("检测到PyArrow不可用，回退至pd.read_parquet")
                try:
                    df_year = pd.read_parquet(
                        file_path,
                        engine='pyarrow',
                        filters=pandas_filter  # 应用过滤条件
                    )
                    if not df_year.empty:
                        all_data_frames.append(df_year)
                        logging.debug(f"使用pd.read_parquet从{file_path}读取到{len(df_year)}行数据")
                except Exception as e:
                    logging.error(f"读取文件{file_path}失败: {e}", exc_info=True)

            except Exception as e:
                logging.error(f"处理文件{file_path}时发生错误: {e}", exc_info=True)

        if not all_data_frames:
            logging.warning(f"在指定年份中未找到{log_code_repr}的数据")
            return self._create_empty_df()

        # 合并所有年度数据
        try:
            combined_df = pd.concat(all_data_frames, ignore_index=True)
        except Exception as e:
            logging.error(f"合并DataFrame时发生错误: {e}", exc_info=True)
            return self._create_empty_df()

        if 'date' not in combined_df.columns or 'code' not in combined_df.columns:
            logging.error("合并后的DataFrame缺少'date'或'code'列")
            # 确保最终返回包含预期列
            for col in EXPECTED_COLUMNS:
                if col not in combined_df.columns:
                    combined_df[col] = None
            if 'date' not in combined_df.columns or 'code' not in combined_df.columns:
                return self._create_empty_df()

        # 最终日期范围过滤
        try:
            final_df = combined_df[
                (combined_df['date'] >= start_dt) &
                (combined_df['date'] <= end_dt)
            ].copy()  # 避免SettingWithCopyWarning
        except Exception as e:
            logging.error(f"执行最终日期过滤时发生错误: {e}", exc_info=True)
            return self._create_empty_df()

        # 按日期排序（多代码时增加代码排序）
        sort_columns = ['date', 'code'] if (is_multiple_codes or is_all_codes) else ['date']
        actual_sort_columns = [col for col in sort_columns if col in final_df.columns]
        if actual_sort_columns:
            final_df.sort_values(by=actual_sort_columns, inplace=True)
        else:
            logging.warning(f"无法排序，缺少必要列: {sort_columns}")

        # 重置索引
        final_df.reset_index(drop=True, inplace=True)

        logging.info(f"成功获取{len(final_df)}行{log_code_repr}从{start_date}到{end_date}的数据")
        # 补全缺失列
        missing_cols = [col for col in EXPECTED_COLUMNS if col not in final_df.columns]
        if missing_cols:
            logging.warning(f"最终DataFrame缺失预期列: {missing_cols}，已填充为NaN")
            for col in missing_cols:
                final_df[col] = pd.NA

        # 按预期列顺序排列
        final_df = final_df.reindex(columns=EXPECTED_COLUMNS)

        return final_df
    def get_missing_period(self) -> tuple[str, str]:
        """
        获取需要补录的数据期间
        返回：
            tuple[str, str]: (start_date, end_date) 日期字符串，格式为 YYYYMMDD
                            表示需要补录的开始日期和结束日期
        逻辑：
            1. 获取当前日期
            2. 根据当前年份确定应读取的Parquet文件
            3. 从文件中找到最大日期
            4. 如果需要补录：
               - start_date = 最大日期 + 1天
               - end_date = 当前日期
            5. 如果没有数据或不需要补录，返回适当的空值
        """
        current_date = date.today()
        current_year = current_date.year
        file_path = self.data_folder / f"{current_year}.parquet"
        # 如果当前年份文件不存在，返回全年范围
        if not file_path.exists():
            logging.info(f"当前年份数据文件不存在: {file_path}")
            start_date = date(current_year, 1, 1)
            end_date = current_date
            return (
                start_date.strftime("%Y%m%d"),
                end_date.strftime("%Y%m%d")
            )
        try:
            # 读取Parquet文件
            df = pd.read_parquet(file_path)
            
            # 假设日期列名为'date'或其他标准名称
            date_column = 'date' if 'date' in df.columns else 'trade_date'
            
            if date_column not in df.columns:
                raise ValueError(f"文件 {file_path} 中找不到日期列")
            
            # 找到最大日期
            max_date = pd.to_datetime(df[date_column]).max().date()
            
            # 计算需要补录的期间
            if max_date >= current_date:
                logging.info("数据已是最新，无需补录")
                return None, None
                
            start_date = max_date + timedelta(days=1)
            end_date = current_date
            
            logging.info(
                f"需要补录的数据期间: {start_date.strftime('%Y%m%d')} "
                f"至 {end_date.strftime('%Y%m%d')}"
            )
            
            return (
                start_date.strftime("%Y%m%d"),
                end_date.strftime("%Y%m%d")
            )
            
        except Exception as e:
            logging.error(f"获取补录期间时出错: {str(e)}")
            raise RuntimeError(f"无法确定补录期间: {str(e)}")

# --- 示例用法 ---
if __name__ == "__main__":
    try:
        reader = DailyDataReader(data_folder=r"D:\pj-m\data\days\parquet\test")
        
        # --- 测试用例1: 单个股票代码（已有测试） ---
        print("\n测试用例1: 代码'000001'，日期'20221229'至'20230103'")
        df1 = reader.read_data(code='000001', start_date='20221229', end_date='20230103')
        print(df1)
        print("-" * 30)

        # --- 测试用例2: 多个股票代码 ---
        print("\n测试用例2: 代码['000001', '600000']，日期'20221230'至'20230101'")
        df2 = reader.read_data(code=['000001', '600000'], start_date='20221230', end_date='20230101')
        print(df2)
        print("-" * 30)

        # --- 测试用例3: 全部代码 ---
        print("\n测试用例3: 代码'all'，日期'20230101'至'20230102'")
        df3 = reader.read_data(code='all', start_date='20230101', end_date='20230102')
        print(df3)
        print("-" * 30)

        # --- 测试用例4: 不存在的代码（多个） ---
        print("\n测试用例4: 代码['999999', '888888']，日期'20230101'至'20230131'")
        df4 = reader.read_data(code=['999999', '888888'], start_date='20230101', end_date='20230131')
        print(df4)
        print("-" * 30)

        # --- 测试用例5: 无效日期范围 ---
        print("\n测试用例5: 代码'000001'，日期'20230201'至'20230101'")
        df5 = reader.read_data(code='000001', start_date='20230201', end_date='20230101')
        print(df5)
        print("-" * 30)

        # --- 测试用例6: 空代码列表 ---
        print("\n测试用例6: 代码[]，日期'20230101'至'20230105'")
        df6 = reader.read_data(code=[], start_date='20230101', end_date='20230105')
        print(df6)
        print("-" * 30)

        # --- 测试用例7: 混合类型代码列表 ---
        print("\n测试用例7: 代码['000001', 123]，日期'20230101'至'20230105'")
        df7 = reader.read_data(code=['000001', 123], start_date='20230101', end_date='20230105')  # type: ignore
        print(df7)
        print("-" * 30)

        # --- 测试用例8: 全部代码跨年查询 ---
        print("\n测试用例8: 代码'all'，日期'20221231'至'20230101'")
        df8 = reader.read_data(code='all', start_date='20221231', end_date='20230101')
        print(df8)
        print("-" * 30)
        print(reader.get_missing_period()) 
    except FileNotFoundError as e:
        print(f"初始化读取器失败: {e}")
    except Exception as e:
        print(f"发生未预期错误: {e}")
    finally:
        # 清理临时数据
        pass