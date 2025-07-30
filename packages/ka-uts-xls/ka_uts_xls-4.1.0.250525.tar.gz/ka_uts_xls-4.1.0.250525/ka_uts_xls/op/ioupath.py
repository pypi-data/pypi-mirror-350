from typing import Any, TypeAlias

import openpyxl as op
import pandas as pd

from ka_uts_path.path import Path
from ka_uts_xls.ioipath import IoiPathWbOp
from ka_uts_xls.op.wbop import WbOp

TyWbOp: TypeAlias = op.workbook.workbook.Workbook
TyPdDf: TypeAlias = pd.DataFrame

TyDic = dict[Any, Any]
TyDoPdDf = dict[Any, TyPdDf]
TyPath = str
TnWbOp = None | TyWbOp


class IouPathWbOp:

    @staticmethod
    def update_wb_with_dodf_by_tpl(
            dodf: TyDoPdDf, path_tpl: TyPath, path: TyPath, **kwargs) -> None:
        _wb_tpl: TyWbOp = IoiPathWbOp.load(path_tpl)
        wb: TnWbOp = WbOp.update_wb_with_dodf(_wb_tpl, dodf, **kwargs)
        if wb is None:
            return
        Path.mkdir_from_path(path)
        wb.save(path)
