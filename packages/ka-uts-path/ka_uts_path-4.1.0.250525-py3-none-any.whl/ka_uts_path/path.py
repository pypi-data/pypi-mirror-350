# coding=utf-8
from collections.abc import Callable, Iterator
from typing import Any

import datetime
import glob
import importlib
import os
import pathlib
import re
from string import Template

from ka_uts_log.log import Log, LogEq
from ka_uts_uts.utils.pac import Pac

TyAny = Any
TyArr = list[Any]
TyAoS = list[str]
TyAoA = list[TyArr]
TyCallable = Callable[..., Any]
TyDic = dict[Any, Any]
TyAoD = list[TyDic]
TyDoA = dict[Any, TyArr]
TyDoAoA = dict[Any, TyAoA]
TyDoInt = dict[str, int]
TyDoDoInt = dict[str, TyDoInt]
TyIntStr = int | str
TyPath = str
TyPathLike = os.PathLike
TyAoPath = list[TyPath]
TyBasename = str
TyTup = tuple[Any, ...]
TyIterAny = Iterator[Any]
TyIterPath = Iterator[TyPath]
TyIterTup = Iterator[TyTup]
TyStr = str
TyToS = tuple[str, ...]

TnAny = None | TyAny
TnArr = None | TyArr
TnAoA = None | TyAoA
TnDic = None | TyDic
TnInt = None | int
TnPath = None | TyPath
TnStr = None | str
TnTup = None | TyTup


class Path:

    @staticmethod
    def verify(path: TyPath) -> None:
        if path is None:
            raise Exception("path is None")
        elif path == '':
            raise Exception("path is empty")

    @classmethod
    def edit_path(cls, path: TyPath, kwargs: TyDic) -> TyPath:
        _d_edit = kwargs.get('d_out_path_edit', {})
        _prefix = kwargs.get('dl_out_file_prefix', '')
        _suffix = kwargs.get('dl_out_file_suffix', '.csv')
        _edit_from = _d_edit.get('from')
        _edit_to = _d_edit.get('to')
        if _edit_from is not None and _edit_to is not None:
            _path_out = path.replace(_edit_from, _edit_to)
        else:
            _path_out = path
        _dir_out = os.path.dirname(_path_out)
        cls.mkdir_from_path(_dir_out)
        _basename_out = os.path.basename(_path_out)
        if _prefix:
            _basename_out = str(f"{_prefix}{_basename_out}")
        if _suffix:
            _basename_out = os.path.splitext(_basename_out)[0]
            _basename_out = str(f"{_basename_out}{_suffix}")
        _path_out = os.path.join(_dir_out, _basename_out)
        return _path_out

    @staticmethod
    def mkdir(path: TyPath) -> None:
        if not os.path.exists(path):
            # Create the directory
            os.makedirs(path)

    @staticmethod
    def mkdir_from_path(path: TyPath) -> None:
        _dir = os.path.dirname(path)
        if not os.path.exists(_dir):
            # Create the directory
            os.makedirs(_dir)

    @staticmethod
    def sh_aopath_mtime_gt_threshold(path: TyPath, mtime_threshhold) -> TyArr:
        if not path:
            raise Exception("Argument 'path' is empty")
        _a_path: TyArr = glob.glob(path)
        return AoPath.sh_aopath_mtime_gt_threshold(_a_path, mtime_threshhold)

    @staticmethod
    def sh_basename(path: TyPath) -> TyBasename:
        """
        Extracts basename of a given path.
        Should Work with any OS Path on any OS
        """
        raw_string = r'[^\\/]+(?=[\\/]?$)'
        basename = re.search(raw_string, path)
        if basename:
            return basename.group(0)
        return path

    @classmethod
    def sh_components(
            cls, path: TyPath, d_ix: TyDic, separator: str = "-") -> TnStr:
        ix_start = d_ix.get("start")
        ix_add = d_ix.get("add", 0)
        if not ix_start:
            return None
        _a_dir: TyArr = cls.split_to_array(path)
        _ix_end = ix_start + ix_add + 1
        _component = separator.join(_a_dir[ix_start:_ix_end])
        _a_component = os.path.splitext(_component)
        return _a_component[0]

    @classmethod
    def sh_component_by_field_name(
        # def sh_component_at_start(
            cls, path: TyPath, d_path_ix: TyDoDoInt, field_name: str) -> TyStr:
        _d_ix: TyDoInt = d_path_ix.get(field_name, {})
        if not _d_ix:
            msg = f"field_name: {field_name} is not defined in dictionary: {d_path_ix}"
            raise Exception(msg)
        _start = _d_ix.get('start')
        if not _start:
            msg = f"'start' is not defined in dictionary: {_d_ix}"
            raise Exception(msg)
        _a_dir: TyAoS = cls.split_to_array(path)
        if _start < len(_a_dir):
            return _a_dir[_start]
        msg = f"index: {_start} is out of range of list: {_a_dir}"
        raise Exception(msg)

    @staticmethod
    def sh_fnc_name_by_pathlib(path: TyPath) -> str:
        # def sh_fnc_name(path: TyPath) -> str:
        _purepath = pathlib.PurePath(path)
        dir_: str = _purepath.parent.name
        stem_: str = _purepath.stem
        return f"{dir_}-{stem_}"

    @staticmethod
    def sh_fnc_name_by_os_path(path: TyPath) -> str:
        # def sh_os_fnc_name(path: TyPath) -> str:
        split_ = os.path.split(path)
        dir_ = os.path.basename(split_[0])
        stem_ = os.path.splitext(split_[1])[0]
        return f"{dir_}-{stem_}"

    @classmethod
    def sh_last_part(cls, path: TyPath) -> Any:
        # def sh_last_component(cls, path: TyPath) -> TyPath:
        a_dir: TyArr = cls.split_to_array(path)
        return a_dir[-1]

    @staticmethod
    def sh_path_by_d_path(path: TyPath, kwargs: TyDic) -> TyPath:
        _d_path = kwargs.get('d_path', {})
        if not _d_path:
            return path
        return Template(path).safe_substitute(_d_path)

    @staticmethod
    def sh_path_by_tpl(path: TyPath, kwargs: TyDic) -> TyPath:
        # Extract variables starting with '$'
        _a_key = re.findall(r'\$(\w+)', path)
        LogEq.debug("_a_key", _a_key)
        _dic = {}
        for _key in _a_key:
            _val = kwargs.get(_key)
            if _val:
                _dic[_key] = _val
        LogEq.debug("_dic", _dic)
        if not _dic:
            return path
        LogEq.debug("path", path)
        _template = Template(path)
        _path = _template.safe_substitute(**_dic)
        # _path = _template.substitute(**_dic)
        LogEq.debug("_path", _path)
        return _path

    @classmethod
    def sh_path_by_tpl_and_pac(cls, path: TyPath, kwargs: TyDic) -> TyPath:
        if not path:
            msg = "The parameter 'path' is udefined or empty"
            raise Exception(msg)
        _a_part: TyArr = list(pathlib.Path(path).parts)
        LogEq.debug("_a_part", _a_part)
        if not _a_part:
            return ''
        _a_path = AoPath.sh_aopath_by_pac(_a_part, kwargs)
        return AoPath.sh_path_by_tpl_first_exist(_a_path, kwargs)

    @classmethod
    def sh_path_by_tpl_and_d_pathnm2datetype(
           cls,  path: TyPath, pathnm: str, kwargs: TyDic) -> TyPath:
        LogEq.debug("path", path)
        _path: TyPath = cls.sh_path_by_tpl(path, kwargs)
        LogEq.debug("_path", _path)
        _path = cls.sh_path_by_d_pathnm2datetype(_path, pathnm, kwargs)
        return _path

    @classmethod
    def sh_path_by_d_pathnm2datetype(
            cls, path: TyPath, pathnm: str, kwargs: TyDic) -> TyPath:
        LogEq.debug("pathnm", pathnm)
        _d_pathnm2datetype: TyDic = kwargs.get('d_pathnm2datetype', {})
        LogEq.debug("_d_pathnm2datetype", _d_pathnm2datetype)
        if not _d_pathnm2datetype:
            return path
        _datetype: TyStr = _d_pathnm2datetype.get(pathnm, '')
        _path = cls.sh_path_by_datetype(path, _datetype, kwargs)
        LogEq.debug("_path", _path)
        return _path

    @classmethod
    def sh_path_by_datetype(
            cls, path: TyPath, datetype: str, kwargs: TyDic) -> TyPath:
        LogEq.debug("path", path)
        LogEq.debug("datetype", datetype)
        match datetype:
            case 'last':
                path_new = cls.sh_path_last(path)
            case 'first':
                path_new = cls.sh_path_first(path)
            case 'now':
                path_new = cls.sh_path_now(path, **kwargs)
            case _:
                path_new = cls.sh_path(path)
        LogEq.debug("path_new", path_new)
        return path_new

    @staticmethod
    def sh_path(path: TyPath) -> TyPath:
        LogEq.debug("path", path)
        if not path:
            raise Exception("Argument 'path' is empty")
        _a_path: TyArr = glob.glob(path)
        if not _a_path:
            msg = f"glob.glob find no paths for template: {path}"
            raise Exception(msg)
        path_new: str = sorted(_a_path)[0]
        return path_new

    @staticmethod
    def sh_path_first(path: TyPath) -> TyPath:
        if not path:
            raise Exception("Argument 'path' is empty")
        _a_path: TyArr = glob.glob(path)
        if not _a_path:
            msg = f"glob.glob find no paths for template: {path}"
            raise Exception(msg)
        path_new: str = sorted(_a_path)[0]
        return path_new

    @staticmethod
    def sh_path_last(path: TyPath) -> TyPath:
        if not path:
            raise Exception("Argument 'path' is empty")
        _a_path: TyArr = glob.glob(path)
        if not _a_path:
            msg = f"glob.glob find no paths for template: {path}"
            raise Exception(msg)
        path_new: str = sorted(_a_path)[-1]
        return path_new

    @staticmethod
    def sh_path_now(path: TyPath, **kwargs) -> TyPath:
        now_var = kwargs.get('now_var', 'now')
        now_fmt = kwargs.get('now_fmt', '%Y%m%d')
        if not path:
            raise Exception("Argument 'path' is empty")
        _current_date: str = datetime.datetime.now().strftime(now_fmt)
        _dic = {now_var: _current_date}
        _path_new: str = Template(path).safe_substitute(_dic)
        return _path_new

    @staticmethod
    def split_to_array(path: TyPath) -> TyArr:
        """ Convert path to normalized pyth
            Should Work with any OS Path on any OS
        """
        _normalized_path = os.path.normpath(path)
        _a_path: TyArr = _normalized_path.split(os.sep)
        return _a_path


class AoPath:

    @staticmethod
    def join(aopath: TyAoPath) -> TyPath:
        _sep = os.sep
        return ''.join([_sep+_path.strip(_sep) for _path in aopath if _path])

    @staticmethod
    def mkdirs(aopath: TyAoPath, **kwargs) -> None:
        if not aopath:
            return
        for _path in aopath:
            os.makedirs(_path, **kwargs)

    @staticmethod
    def sh_a_path(
            path: TyPath) -> TyAoPath:
        a_path: TyAoPath = glob.glob(path)
        return a_path

    @classmethod
    def sh_a_path_by_tpl(
            cls, a_path_tpl_key: TyAoPath, kwargs: TyDic) -> TyAoPath:
        _a_path_tpl: TyAoPath = cls.sh_items_in_dic(a_path_tpl_key, kwargs)
        _path_tpl: TyPath = cls.join(_a_path_tpl)
        return cls.sh_a_path(_path_tpl)

    @staticmethod
    def sh_aopath_by_glob(aopath: TyAoPath) -> TyArr:
        if not aopath:
            return []
        _aopath: TyArr = []
        for _path in aopath:
            _aopath = _aopath + glob.glob(_path)
        return _aopath

    @staticmethod
    def sh_aopart_by_pac(a_part: TyArr, kwargs: TyDic) -> TyAoPath:
        LogEq.debug("a_part", a_part)
        _a_part: TyArr = []
        for _part in a_part:
            LogEq.debug("_part", _part)
            if _part == 'package':
                _package = kwargs.get('package', '')
                _dir_package: TyPath = str(importlib.resources.files(_package))
                _a_part.append(_dir_package)
            else:
                _a_part.append(_part)
        LogEq.debug("_a_part", _a_part)
        return _a_part

    @classmethod
    def sh_aopath_by_pac(cls, a_part: TyArr, kwargs: TyDic) -> TyAoPath:
        if a_part[0] == os.sep:
            _a_part = a_part[1:]
        else:
            _a_part = a_part
        _part0 = a_part[0]
        LogEq.debug("_part0", _part0)
        _a_part0 = _part0.split("|")
        _a_part0_new = cls.sh_aopart_by_pac(_a_part0, kwargs)
        LogEq.debug("_a_part0_new", _a_part0_new)

        _a_path: TyArr = []
        for _part in _a_part0_new:
            _a_part_new = [os.sep, _part] + _a_part[1:]
            _path_new = str(pathlib.Path(*_a_part_new))
            _a_path.append(_path_new)
        return _a_path

    @staticmethod
    def sh_aopath_mtime_gt_threshold(aopath: TyAoPath, mtime_threshold) -> TyArr:
        if not aopath:
            return []
        _aopath: TyArr = []
        for _path in aopath:
            _mtime = os.path.getmtime(_path)  # Get file's last modified time
            LogEq.debug("_path", _path)
            LogEq.debug("_mtime", _mtime)
            LogEq.debug("mtime_threshold", mtime_threshold)
            if _mtime > mtime_threshold:
                Log.debug(f"mtime: {_mtime} of _path: {_path} is greater than: {mtime_threshold}")
                _aopath.append(_path)
        LogEq.debug("_aopath", _aopath)
        return _aopath

    @staticmethod
    def sh_items_in_dic(arr: TnArr, dic: TnDic) -> TyArr:
        # def sh_values(arr: TnArr, dic: TnDic) -> TyArr:
        a_new: TyArr = []
        if not arr:
            return a_new
        if not dic:
            return a_new
        for _key in arr:
            if _key in dic:
                a_new.append(dic[_key])
        return a_new

    @staticmethod
    def sh_path_by_tpl_first_exist(a_path: TyArr, kwargs: TyDic) -> TyPath:
        LogEq.debug("_a_path", a_path)
        for _path in a_path:
            LogEq.debug("_path", _path)
            _path_new: TyPath = Path.sh_path_by_tpl(_path, kwargs)
            if os.path.exists(_path_new):
                return _path_new
        msg = f"No path of the path-list {a_path} exists"
        raise Exception(msg)

    @classmethod
    def yield_path_kwargs_over_path(
        # def yield_over_a_path(
            cls, a_path_tpl_key: TyAoPath, kwargs: TyDic
    ) -> TyIterTup:
        _a_path: TyAoPath = cls.sh_a_path_by_tpl(a_path_tpl_key, kwargs)
        for _path in _a_path:
            yield (_path, kwargs)

    @classmethod
    def yield_path_kwargs_over_dir_path(
        # def yield_path_kwargs_new(
        # def yield_over_a_dir_a_path(
            cls,
            a_dir_tpl_key: TyAoPath,
            a_path_tpl_key: TyAoPath,
            sh_kwargs_new: TyCallable,
            kwargs: TyDic
    ) -> TyIterTup:
        _a_dir: TyAoPath = cls.sh_a_path_by_tpl(a_dir_tpl_key, kwargs)
        for _dir in _a_dir:
            _kwargs_new: TyDic = sh_kwargs_new([_dir, kwargs])
            _a_path: TyAoPath = cls.sh_a_path_by_tpl(
                    a_path_tpl_key, _kwargs_new)
            for _path in _a_path:
                yield (_path, _kwargs_new)

    @classmethod
    def yield_path_item_kwargs_over_path_arr(
        # def yield_path_item_kwargs(
        # def yield_over_a_path_arr(
            cls, a_path_tpl_key: TyAoPath, arr_key: str, kwargs: TyDic
    ) -> TyIterTup:
        _a_path: TyAoPath = cls.sh_a_path_by_tpl(a_path_tpl_key, kwargs)
        _arr: TyAoPath = kwargs.get(arr_key, [])
        for _path in _a_path:
            for _item in _arr:
                yield (_path, _item, kwargs)

    @classmethod
    def yield_path_item_kwargs_over_dir_path_arr(
        # def yield_path_item_kwargs_new(
        # def yield_over_a_dir_a_path_arr(
            cls,
            a_dir_tpl_key: TyAoPath,
            a_path_tpl_key: TyAoPath,
            arr_key: str,
            sh_kwargs_new: TyCallable,
            kwargs: TyDic
    ) -> TyIterTup:
        _a_dir: TyAoPath = cls.sh_a_path_by_tpl(a_dir_tpl_key, kwargs)
        _arr: TyAoPath = kwargs.get(arr_key, [])
        for _dir in _a_dir:
            _kwargs_new: TyDic = sh_kwargs_new([_dir, kwargs])
            _a_path: TyAoPath = cls.sh_a_path_by_tpl(
                    a_path_tpl_key, _kwargs_new)
            for _path in _a_path:
                for _item in _arr:
                    yield (_path, _item, _kwargs_new)


class AoDoDoPath:
    """
    Manage Array of Path-Dictionaries
    """
    @staticmethod
    def sh_aopath(aodod_path: TyAoD, kwargs: TyDic) -> TyAoPath:
        _aopath: TyAoPath = []
        LogEq.debug("aodod_path", aodod_path)
        if not aodod_path:
            LogEq.debug("_aopath", _aopath)
            return _aopath
        for _dod_path in aodod_path:
            _path: TyPath = DoDoPath.sh_path(_dod_path, kwargs)
            _aopath.append(_path)
        LogEq.debug("_aopath", _aopath)
        return _aopath


class DoDoPath:

    @classmethod
    def sh_path(cls, dodopath: TyDic, kwargs: TyDic) -> TyPath:
        LogEq.debug("dodopath", dodopath)
        if not dodopath:
            return ''
        _d_path: TyDic = dodopath.get('d_path', {})
        LogEq.debug("_d_path", _d_path)
        _path: TyPath = DoPath.sh_path(_d_path, kwargs)
        LogEq.debug("_path", _path)

        _datetype = dodopath.get('datetype')
        LogEq.debug("_datetype", _datetype)

        if _datetype:
            _path = Path.sh_path_by_datetype(_path, _datetype, kwargs)
        return _path


class DoPath:

    @staticmethod
    def sh_path(d_path: TyDic, kwargs: TyDic) -> TyPath:
        LogEq.debug("d_path", d_path)
        _a_part: TyArr = []
        _package: TyStr = kwargs.get('package', '')
        for _k, _v in d_path.items():
            LogEq.debug("_k", _k)
            LogEq.debug("_v", _v)
            match _v:
                case 'key':
                    _val = kwargs.get(_k)
                    if _val:
                        _a_part.append(_val)
                case 'pac':
                    _val = Pac.sh_path_by_path(_package, _k, Log.log)
                    if _val:
                        _a_part.append(_val)
                case _:
                    _a_part.append(_k)
        LogEq.debug("_a_part", _a_part)
        if not _a_part:
            msg = f"a_part for d_path = {d_path} is undefined or empty"
            raise Exception(msg)
        return os.path.join(*_a_part)
