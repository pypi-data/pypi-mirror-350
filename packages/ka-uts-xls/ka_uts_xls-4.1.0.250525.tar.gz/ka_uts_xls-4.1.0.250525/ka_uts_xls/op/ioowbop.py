from typing import Any, TypeAlias

import openpyxl as op

from ka_uts_path.pathnm import PathNm
from ka_uts_xls.op.wbop import WbOp

TyWbOp: TypeAlias = op.workbook.workbook.Workbook

TyArr = list[Any]
TyDic = dict[Any, Any]
TyAoA = list[TyArr]
TyAoD = list[TyDic]
TyDoAoA = dict[Any, TyAoA]
TyDoAoD = dict[Any, TyAoD]
TyPath = str
TyPathnm = str
TySheet = int | str

TnWbOp = None | TyWbOp


class IooPathWbOp:

    @staticmethod
    def write(wb: TnWbOp, path: TyPath) -> None:
        if wb is not None:
            wb.save(path)

#   @staticmethod
#   def write_wb_from_doaoa(doaoa: TyDoAoA, path: str) -> None:
#       wb: TyWbOp = WbOp.create_wb_from_doaoa(doaoa)
#       wb.save(path)

    @staticmethod
    def write_wb_from_doaod(doaod: TyDoAoD, path: str) -> None:
        wb: TyWbOp = WbOp.create_wb_from_doaod(doaod)
        wb.save(path)


class IooPathnmWbOp:

    @staticmethod
    def write(
            wb: TnWbOp, pathnm: TyPathnm, **kwargs) -> None:
        _path: TyPath = PathNm.sh_path(pathnm, kwargs)
        IooPathWbOp.write(wb, _path)

    @staticmethod
    def write_wb_from_doaod(
            doaod: TyDoAoD, pathnm: str, **kwargs) -> None:
        _path: TyPath = PathNm.sh_path(pathnm, kwargs)
        IooPathWbOp.write_wb_from_doaod(doaod, _path)
