from typing import Any, TypeAlias

import openpyxl as op

from ka_uts_path.pathnm import PathNm
from ka_uts_xls.op.ioipath import IoiPathWbOp

TyWbOp: TypeAlias = op.workbook.workbook.Workbook
TyWsOp: TypeAlias = op.worksheet.worksheet.Worksheet

TyArr = list[Any]
TyDic = dict[Any, Any]
TyAoA = list[TyArr]
TyAoD = list[TyDic]
TyDoAoD = dict[Any, TyAoD]
TyDoWsOp = dict[Any, TyWsOp]
TyAoD_DoAoD = TyAoD | TyDoAoD
TyPath = str
TyPathnm = str

TySheet = int | str
TySheets = int | str | list[int | str]
TySheetname = str
TySheetnames = list[TySheetname]

TnAoD = None | TyAoD
TnAoD_DoAoD = None | TyAoD_DoAoD
TnDoAoD = None | TyDoAoD
TnSheet = None | TySheet
TnSheets = None | TySheets
TnSheetname = None | TySheetname
TnSheetnames = None | TySheetnames
TnWbOp = None | TyWbOp
TnWsOp = None | TyWsOp
TnPath = None | TyPath


class IoiPathnmWbOp:

    @staticmethod
    def load(pathnm: TyPathnm, kwargs: TyDic, **kwargs_wb) -> TyWbOp:
        return IoiPathWbOp.load(
                PathNm.sh_path(pathnm, kwargs), **kwargs_wb)
