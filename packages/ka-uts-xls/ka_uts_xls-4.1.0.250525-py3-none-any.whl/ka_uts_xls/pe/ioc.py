import pyexcelerate as pe

from typing import Any, TypeAlias
TyWbPe: TypeAlias = pe.Workbook


class IocWbPe:

    @staticmethod
    def get(**kwargs: Any) -> TyWbPe:
        wb: TyWbPe = pe.Workbook(**kwargs)
        return wb
