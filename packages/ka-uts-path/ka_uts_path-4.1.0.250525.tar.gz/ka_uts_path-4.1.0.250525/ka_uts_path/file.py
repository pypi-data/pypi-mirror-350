# coding=utf-8
from collections.abc import Callable, Iterator

import glob
import os

from ka_uts_com.timer import Timer
from ka_uts_log.log import Log, LogEq
from ka_uts_obj.str import Str
from ka_uts_arr.aod import AoD

from typing import Any
TyAny = Any
TyArr = list[Any]
TyDic = dict[Any, Any]
TyAoD = list[TyDic]
TyDoD = dict[Any, TyDic]
TyFnc = Callable[..., Any]
TyIoS = Iterator[str]
TyObj = Any
TyPath = str
TnBool = None | bool
TnDic = None | TyDic
TnPath = None | TyPath
TnStr = None | str
TnFnc = None | TyFnc


class File:

    @staticmethod
    def count(path_pattern: TyPath) -> int:
        """
        count number of paths that match path pattern
        """
        return len(list(glob.iglob(path_pattern)))

    @staticmethod
    def ex_get_aod_by_fnc(
            path: TyPath, fnc: TyFnc, kwargs: TyDic) -> TyAoD:
        _mode = kwargs.get('mode', 'r')
        _aod: TyAoD = []
        with open(path, _mode) as _fd:
            for _line in _fd:
                _dic = Str.sh_dic(_line)
                _obj = fnc(_dic, kwargs)
                AoD.add(_aod, _obj)
        return _aod

    @staticmethod
    def ex_get_aod(path: TyPath, kwargs: TyDic) -> TyAoD:
        _mode = kwargs.get('mode', 'r')
        _aod: TyAoD = []
        with open(path, _mode) as _fd:
            for _line in _fd:
                _dic = Str.sh_dic(_line)
                AoD.add(_aod, _dic)
        return _aod

    @staticmethod
    def ex_get_dod_by_fnc(
            path: TyPath, fnc: TyFnc, key: str, kwargs: TyDic) -> TyDoD:
        """
        Create a dictionary of dictionaries by executing the following steps:
        1. read every line of the json file <path> into a dictionary
        2. If the function <obj_fnc> is not None:
             transform the dictionary by the function <obj_fnc>
             get value of the transformed dictionary for the key <key>
           else
             get value of the dictionary for the key <key>
        2. if the value is not None:
             insert the transformed dictionary into the new dictionary
             of dictionaries with the value as key.
        """
        _mode = kwargs.get('mode', 'r')
        _dod: TyDoD = {}
        with open(path, _mode) as _fd:
            for _line in _fd:
                _obj = Str.sh_dic(_line)
                _obj = fnc(_obj, kwargs)
                if _obj is not None:
                    _key = _obj.get(key)
                    if _key is not None:
                        _dod[_key] = _obj
        return _dod

    @staticmethod
    def ex_get_dod(
            path: TyPath, key: str, kwargs: TyDic) -> TyDoD:
        """
        Create a dictionary of dictionaries by executing the following steps:
        1. read every line of the json file <path> into a dictionary
        2. If the function <obj_fnc> is not None:
             transform the dictionary by the function <obj_fnc>
             get value of the transformed dictionary for the key <key>
           else
             get value of the dictionary for the key <key>
        2. if the value is not None:
             insert the transformed dictionary into the new dictionary
             of dictionaries with the value as key.
        """
        _mode = kwargs.get('mode', 'r')
        _dod: TyDoD = {}
        with open(path, _mode) as _fd:
            for _line in _fd:
                _obj = Str.sh_dic(_line)
                if _obj is not None:
                    _key = _obj.get(key)
                    _key = _obj[key]
                    if _key is not None:
                        _dod[_key] = _obj
        return _dod

    @classmethod
    def get_aod(cls, path: TyPath, fnc: TnFnc, kwargs: TyDic) -> TyAoD:
        Timer.start(cls.get_aod, f"{path}")
        if fnc is not None:
            _aod = cls.ex_get_aod_by_fnc(path, fnc, kwargs)
        else:
            _aod = cls.ex_get_aod(path, kwargs)
        Timer.end(cls.get_aod, f"{path}")
        return _aod

    @classmethod
    def get_dic(cls, path: TyPath, fnc: TnFnc, kwargs: TyDic) -> TyDic:
        Timer.start(cls.get_aod, f"{path}")
        aod = cls.get_aod(path, fnc, kwargs)
        if len(aod) > 1:
            msg = (f"File {path} contains {len(aod)} records; "
                   "it should contain only one record")
            raise Exception(msg)
        return aod[0]

    @classmethod
    def get_dod(
            cls, path: TyPath, fnc: TnFnc, key: str, kwargs: TyDic) -> TyDoD:
        """
        Create a dictionary of dictionaries by executing the following steps:
        1. read every line of the json file <path> into a dictionary
        2. If the function <obj_fnc> is not None:
             transform the dictionary by the function <obj_fnc>
             get value of the transformed dictionary for the key <key>
           else
             get value of the dictionary for the key <key>
        2. if the value is not None:
             insert the transformed dictionary into the new dictionary
             of dictionaries with the value as key.
        """
        Timer.start(cls.get_aod, f"{path}")
        if fnc is not None:
            _dod = cls.ex_get_dod_by_fnc(path, fnc, key, kwargs)
        else:
            _dod = cls.ex_get_dod(path, key, kwargs)
        Timer.end(cls.get_aod, f"{path}")
        return _dod

    @staticmethod
    def get_latest(path_pattern: TyPath) -> TnPath:
        """
        get latest path that match path pattern
        """
        _iter_path = glob.iglob(path_pattern)
        _a_path = list(_iter_path)
        if len(_a_path) > 0:
            return max(_a_path, key=os.path.getmtime)
        msg = f"No path exist for pattern: {path_pattern}"
        Log.error(msg)
        return None

    @staticmethod
    def get_paths(
            path_pattern: TyPath, sw_recursive: TnBool = None) -> TyIoS:
        """
        get all paths that match path_pattern
        """
        if sw_recursive is None:
            sw_recursive = False
        _paths: Iterator[str] = glob.iglob(path_pattern, recursive=sw_recursive)
        LogEq.debug("path_pattern", path_pattern)
        LogEq.debug("_paths", _paths)
        for _path in _paths:
            if os.path.isfile(_path):
                LogEq.debug("_path", _path)
                yield _path

    @staticmethod
    def io(obj: TyObj, path: TyPath, fnc: TyFnc) -> None:
        """
        execute io function
        """
        fnc(obj, path)
