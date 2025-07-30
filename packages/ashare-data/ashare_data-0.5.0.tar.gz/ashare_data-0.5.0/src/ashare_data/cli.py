# src/ashare_data/cli.py

import click
import sys
import os
from pathlib import Path
from datetime import datetime

# 主命令组，对应 'ashare'
@click.group()
@click.version_option(package_name='ashare-data', prog_name='ashare') # 使用 ashare 作为程序名
def cli():
    """
    ASHARE: A command-line tool for A-share market data management.
    """
    # 这里可以进行全局初始化，或者传递上下文对象
    pass

# 创建 'data' 子命令组
@cli.group()
def data():
    """Commands for data initialization and updates."""
    pass # 这个函数本身不需要做任何事，它只是一个命令分组的容器

# 在 'data' 组下添加 'init' 命令
@data.command()
@click.option('--start-date', default='20150101', show_default=True,
              help='Start date for data consideration (YYYYMMDD format).')
@click.option('--end-date', default=None,
              help='End date for data consideration (YYYYMMDD format). Defaults to today.')
def init(start_date, end_date):
    """
    Initializes the required data storage structure based on ASHARE_DATA_ROOT.
    Checks for the ASHARE_DATA_ROOT environment variable, creates the directory
    if it doesn't exist, and warns if the directory is not empty.
    Example: ashare data init --start-date 20200101
    """
    # 1. 处理默认结束日期
    if end_date is None:
        end_date = datetime.today().strftime('%Y%m%d')
        click.echo(f"Info: No end date provided, using today's date: {end_date}")
    else:
        # (可选) 在这里可以添加日期格式校验
        pass
    click.echo(f"Effective data range: Start Date = {start_date}, End Date = {end_date}")
    click.echo("-" * 30) # 分隔线
    # 2. 读取并校验环境变量 ASHARE_DATA_ROOT
    data_root_env = __get()
    # 3. 处理目标目录路径
    try:
        data_root_path = Path(data_root_env).resolve() # 使用 Path 对象并解析为绝对路径
    except Exception as e:
        # 处理无效的路径字符串本身（虽然不太常见）
        click.secho(f"Error: The path specified in ASHARE_DATA_ROOT is invalid: {data_root_env}", fg='red')
        click.secho(f"Details: {e}", fg='red')
        sys.exit(1)
    # 4. 检查目录是否存在，并进行相应操作
    if data_root_path.exists():
        if not data_root_path.is_dir():
            # 路径存在但不是一个目录
            click.secho(f"Error: The specified path exists but is not a directory: {data_root_path}", fg='red')
            sys.exit(1)
        else:
            # 路径存在且是目录，检查是否为空
            click.echo(f"Directory already exists: {data_root_path}")
            try:
                # 使用生成器和next来检查是否为空，避免读取整个目录列表
                is_empty = next(data_root_path.iterdir(), None) is None
                if not is_empty:
                    click.secho("Warning: The directory is not empty. Existing data might be present.", fg='yellow')
                else:
                    click.echo("Directory is empty. Ready for initialization.")
            except PermissionError:
                click.secho(f"Error: Permission denied when trying to check contents of directory: {data_root_path}", fg='red')
                sys.exit(1)
            except Exception as e: # 其他可能的错误，如路径突然消失等
                 click.secho(f"Error: Could not check contents of directory {data_root_path}: {e}", fg='red')
                 sys.exit(1)
    else:
        # 目录不存在，尝试创建
        click.echo(f"Directory does not exist. Attempting to create: {data_root_path}")
        try:
            # parents=True: 创建任何必需的父目录 (类似 mkdir -p)
            # exist_ok=True: 如果目录在检查后、创建前被其他进程创建了，不要报错
            data_root_path.mkdir(parents=True, exist_ok=True)
            click.secho(f"Successfully created directory: {data_root_path}", fg='green')
        except PermissionError:
            click.secho(f"Error: Permission denied. Could not create directory: {data_root_path}", fg='red')
            sys.exit(1)
        except OSError as e:
            # 捕获其他可能的操作系统错误，例如路径名无效或磁盘满
            click.secho(f"Error: Failed to create directory {data_root_path}: {e}", fg='red')
            sys.exit(1)
        except Exception as e: # 捕获其他意外错误
            click.secho(f"An unexpected error occurred during directory creation: {e}", fg='red')
            sys.exit(1)
   
    # 这里可以添加将 start_date 和 end_date 写入配置文件的逻辑（如果需要）
    click.echo(f"Data directory set to: {data_root_path}")
    click.echo(f"Data range set from {start_date} to {end_date} (These values are currently not saved).")
    import ashare_data.utils as utils
    utils.create(data_root_path,start_date,end_date) 
     # 5. 结束提示
    click.echo("-" * 30) # 分隔线
    click.secho("Initialization setup complete.", fg='green')

# 在 'data' 组下添加 'update' 命令
@data.command()
# 如果 update 需要参数，可以在这里添加
# 例如：@click.option('--date', default='today', help='Update up to specified date (YYYY-MM-DD or "today").')
def update():
    """
    Updates the market data to the latest available or specified date.

    Example: ashare data update
    """
    # 2. 读取并校验环境变量 ASHARE_DATA_ROOT
    data_dir=__get()
    import ashare_data.utils as utils
    utils.update(data_dir)

# (可选) 你仍然可以添加顶层命令，不属于 'data' 组
# @cli.command()
# def status():
#    """Checks the status of the data."""
#    click.echo("Checking data status... (Placeholder)")


def __get()->str:
    data_root_env = os.getenv('ASHARE_DATA_ROOT')
    if not data_root_env:
        click.secho("Error: Environment variable 'ASHARE_DATA_ROOT' is not set.", fg='red')
        click.echo("Please set this variable to the directory where you want to store A-share data.")
        click.echo("Example (Linux/macOS): export ASHARE_DATA_ROOT=\"/path/to/your/data/directory\"")
        click.echo("Example (Windows CMD): set ASHARE_DATA_ROOT=\"C:\\path\\to\\your\\data\\directory\"")
        click.echo("Example (Windows PowerShell): $env:ASHARE_DATA_ROOT=\"C:\\path\\to\\your\\data\\directory\"")
        sys.exit(1) # 退出，指示错误
    click.echo(f"Found ASHARE_DATA_ROOT: {data_root_env}")
    return data_root_env
# 供直接运行脚本测试使用
if __name__ == "__main__":
    cli()

