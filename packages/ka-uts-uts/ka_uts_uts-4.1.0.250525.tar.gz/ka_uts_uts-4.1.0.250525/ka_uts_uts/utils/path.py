# coding=utf-8
from typing import Any

import os

# from ka_uts_uts.utils.pac import Pac

TyArr = list[Any]
TyDic = dict[Any, Any]
TyPath = str
TyStr = str
TyTup = tuple[Any, Any]


class File:
    """
    Package Module Management
    """
    @staticmethod
    def sh_app_data_path_by_type_and_file_pattern(
            filename, type_: str, suffix: str, kwargs: TyDic) -> TyPath:
        """
        show type specific path
        """
        _app_com = kwargs.get('app_com')
        _app_data = kwargs.get('app_data', '')
        _tenant = kwargs.get('tenant', '')
        _a_pacmod: TyArr = _app_com.__module__.split(".")
        _package = _a_pacmod[0]
        _module = _a_pacmod[1]
        _path = os.path.join(_app_data, _tenant, _package, _module, type_)
        return os.path.join(_path, f"{filename}*.{suffix}")


class XPath:
    """
    Package Module Management
    """
    @staticmethod
    def sh_app_data_path_by_type_and_file_pattern(
            kwargs: TyDic, filename, type_: str, suffix: str) -> TyPath:
        """
        show type specific path
        """
        _app_com = kwargs.get('app_com')
        _app_data = kwargs.get('app_data', '')
        _tenant = kwargs.get('tenant', '')
        _a_pacmod: TyArr = _app_com.__module__.split(".")
        _package = _a_pacmod[0]
        _module = _a_pacmod[1]
        _path = os.path.join(_app_data, _tenant, _package, _module, type_)
        return os.path.join(_path, f"{filename}*.{suffix}")
