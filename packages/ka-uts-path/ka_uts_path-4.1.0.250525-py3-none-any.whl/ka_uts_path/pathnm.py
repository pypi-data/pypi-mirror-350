from typing import Any

# import os

from ka_uts_log.log import LogEq
from ka_uts_path.path import Path

TyDic = dict[Any, Any]
TyPath = str

TnDic = None | TyDic
TnPath = None | TyPath


class PathNm:

    @staticmethod
    def sh_path(pathnm: str, kwargs: TyDic) -> TyPath:
        _path: TyPath = kwargs.get(pathnm, '')
        LogEq.debug("_path", _path)
        _path = Path.sh_path_by_tpl_and_d_pathnm2datetype(_path, pathnm, kwargs)
        return _path
