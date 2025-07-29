# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/7/1 09:44
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""
import os
import re
import urllib
from pathlib import Path

import clickhouse_df
import polars as pl
from dynaconf import Dynaconf

import ylog
from .parse import extract_table_names_from_sql

# 配置文件在 “~/.catdb/setting.toml”
USERHOME = os.path.expanduser('~')  # 用户家目录
NAME = "catdb"
CONFIG_PATH = os.path.join(USERHOME, f".{NAME}", "settings.toml")
if not os.path.exists(CONFIG_PATH):
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH))
    except FileExistsError as e:
        ...
    except Exception as e:
        ylog.error(f"配置文件生成失败: {e}")
    catdb_path = os.path.join(USERHOME, NAME)
    template_content = f"""[paths]
{NAME}="{catdb_path}"  # 本地数据库，默认家目录

## 数据库配置：
[database]
[database.ck]
# urls=["<host1>:<port1>", "<host2>:<port2>",]
# user="xxx"
# password="xxxxxx"
[database.jy]
# url="<host>:<port>"
# user="xxxx"
# password="xxxxxx"

## 视情况自由增加其他配置
    """
    with open(CONFIG_PATH, "w") as f:
        f.write(template_content)
    ylog.info(f"生成配置文件: {CONFIG_PATH}")


def get_settings():
    try:
        return Dynaconf(settings_files=[CONFIG_PATH])
    except Exception as e:
        ylog.error(f"读取配置文件失败: {e}")
        return {}


HOME = USERHOME
CATDB = os.path.join(HOME, NAME)
# 读取配置文件覆盖
SETTINGS = get_settings()
if SETTINGS is not None:
    CATDB = SETTINGS["PATHS"][NAME]
    if not CATDB.endswith(NAME):
        CATDB = os.path.join(CATDB, NAME)


# ======================== 本地数据库 catdb ========================
def tb_path(tb_name: str) -> Path:
    """
    返回指定表名 完整的本地路径
    Parameters
    ----------
    tb_name: str
       表名，路径写法: a/b/c
    Returns
    -------
        full_abs_path: pathlib.Path
        完整的本地绝对路径 $HOME/catdb/a/b/c
    """
    return Path(CATDB, tb_name)


def put(df: pl.DataFrame, tb_name: str, partitions: list[str] | None = None, abs_path: bool = False):
    if not abs_path:
        tbpath = tb_path(tb_name)
    else:
        tbpath = tb_name
    if not tbpath.exists():
        os.makedirs(tbpath, exist_ok=True)
    if partitions is not None:
        df.write_parquet(tbpath, partition_by=partitions)
    else:
        df.write_parquet(tbpath / "data.parquet")


def sql(query: str, abs_path: bool = False, lazy: bool = True):
    tbs = extract_table_names_from_sql(query)
    convertor = dict()
    for tb in tbs:
        if not abs_path:
            db_path = tb_path(tb)
        else:
            db_path = tb
        format_tb = f"read_parquet('{db_path}/**/*.parquet')"
        convertor[tb] = format_tb
    pattern = re.compile("|".join(re.escape(k) for k in convertor.keys()))
    new_query = pattern.sub(lambda m: convertor[m.group(0)], query)
    if not lazy:
        return pl.sql(new_query).collect()
    return pl.sql(new_query)


def read_mysql(query: str, db_conf: str = "database.mysql") -> pl.DataFrame:
    """
    读取 mysql 返回 polars.DataFrame
    :param query:
    :param db_conf: .catdb/settings.toml 中的 database 配置
    :return: polars.DataFrame
    """
    try:
        db_setting = get_settings().get(db_conf, {})
        if not isinstance(db_setting, dict):
            raise ValueError(f"Database configuration '{db_conf}' is not a dictionary.")

        required_keys = ['user', 'password', 'url']
        missing_keys = [key for key in required_keys if key not in db_setting]
        if missing_keys:
            raise KeyError(f"Missing required keys in database config: {missing_keys}")

        user = urllib.parse.quote_plus(db_setting['user'])
        password = urllib.parse.quote_plus(db_setting['password'])
        uri = f"mysql://{user}:{password}@{db_setting['url']}"
        return pl.read_database_uri(query, uri)

    except KeyError as e:
        raise RuntimeError("Database configuration error: missing required fields.") from e
    except Exception as e:
        raise RuntimeError(f"Failed to execute MySQL query: {e}") from e


def read_ck(query: str, db_conf: str = "database.ck") -> pl.DataFrame:
    """
    读取 clickhouse 集群 返回 polars.DataFrame
    :param query:
    :param db_conf: .catdb/settings.toml 中的 database 配置
    :return: polars.DataFrame
    """
    try:
        db_setting = get_settings().get(db_conf, {})
        if not isinstance(db_setting, dict):
            raise ValueError(f"Database configuration '{db_conf}' is not a dictionary.")

        required_keys = ['user', 'password', 'urls']
        missing_keys = [key for key in required_keys if key not in db_setting]
        if missing_keys:
            raise KeyError(f"Missing required keys in database config: {missing_keys}")

        user = urllib.parse.quote_plus(db_setting['user'])
        password = urllib.parse.quote_plus(db_setting['password'])

        with clickhouse_df.connect(db_setting['urls'], user=user, password=password):
            return clickhouse_df.to_polars(query)

    except KeyError as e:
        raise RuntimeError("Database configuration error: missing required fields.") from e
    except Exception as e:
        raise RuntimeError(f"Failed to execute ClickHouse query: {e}") from e
