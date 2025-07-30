from typing import Any, TypeAlias

import pyexcelerate as pe

from ka_uts_xls.pe.ioc import IocWbPe

TyWbPe: TypeAlias = pe.Workbook

TyArr = list[Any]
TyAoA = list[TyArr]
TyAoAoA = list[TyAoA]
TyDic = dict[Any, Any]
TyAoD = list[TyDic]
TyDoD = dict[Any, TyDic]
TyDoAoA = dict[Any, TyAoA]
TyDoAoD = dict[Any, TyAoD]
TnArr = None | TyArr
TnAoA = None | TyAoA
TnDic = None | TyDic
TnDoAoA = None | TyDoAoA


class WbPe:

    @staticmethod
    def create_wb_from_doaod(doaod: TyDoAoD) -> TyWbPe:
        # if not doaod:
        #    raise Exception('doaod is empty')
        wb: TyWbPe = IocWbPe.get()
        if not doaod:
            return wb
        for sheet, aod in doaod.items():
            if not aod:
                continue
            a_header = [list(aod[0].keys())]
            a_data = [list(d.values()) for d in aod]
            a_row = a_header + a_data
            wb.new_sheet(sheet, data=a_row)
        return wb

    @staticmethod
    def create_wb_from_doaoa(doaoa: TyDoAoA) -> TyWbPe:
        # if not doaoa:
        #    raise Exception('doaoa is empty')
        wb: TyWbPe = IocWbPe.get()
        if not doaoa:
            return wb
        for sheet, aoa in doaoa.items():
            if not aoa:
                continue
            wb.new_sheet(sheet, data=aoa)
        return wb
