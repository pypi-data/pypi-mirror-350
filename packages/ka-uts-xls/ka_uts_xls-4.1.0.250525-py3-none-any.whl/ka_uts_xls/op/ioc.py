import openpyxl as op

from typing import Any, TypeAlias
TyWbOp: TypeAlias = op.workbook.workbook.Workbook
TnWbOp = None | TyWbOp


class IocWbOp:

    @staticmethod
    def get(**kwargs: Any) -> TyWbOp:
        wb: TyWbOp = op.Workbook(**kwargs)
        return wb
