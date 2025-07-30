from typing import Any, TypeAlias

import pyexcelerate as pe

from ka_uts_path.pathnm import PathNm
from ka_uts_xls.pe.ioc import IocWbPe
from ka_uts_xls.pe.wbpe import WbPe

TyWbPe: TypeAlias = pe.Workbook

TyArr = list[Any]
TyDic = dict[Any, Any]
TyAoA = list[TyArr]
TyAoD = list[TyDic]
TyDoAoA = dict[Any, TyAoA]
TyDoAoD = dict[Any, TyAoD]
TyPath = str
TyPathnm = str
TySheet = int | str

TnWbPe = None | TyWbPe


class IooPathWbPe:

    @staticmethod
    def write(wb: TnWbPe, path: TyPath) -> None:
        if wb is not None:
            wb.save(path)

    @staticmethod
    def write_wb_from_doaoa(doaoa: TyDoAoA, path: str) -> None:
        # def write_xls_wb_from_doaoa(doaoa: TyDoAoA, path: str) -> None:
        wb: TyWbPe = WbPe.create_wb_from_doaoa(doaoa)
        wb.save(path)

    @staticmethod
    def write_wb_from_doaod(doaod: TyDoAoD, path: str) -> None:
        # def write_xls_wb_from_doaod(doaod: TyDoAoD, path: str) -> None:
        wb: TyWbPe = WbPe.create_wb_from_doaod(doaod)
        wb.save(path)

    @staticmethod
    def write_wb_from_aod(
            aod: TyAoD, path: str, sheet: TySheet) -> None:
        # def write_xls_wb_from_aod(aod: TyAoD, path: str, sheet_id: str) -> None:
        wb: TyWbPe = IocWbPe.get()
        a_header: TyArr = [list(aod[0].keys())]
        a_data: TyArr = [list(d.values()) for d in aod]
        a_row: TyArr = a_header + a_data
        wb.new_sheet(sheet, data=a_row)
        wb.save(path)


class IooPathnmWbPe:

    @staticmethod
    def write(
            wb: TnWbPe, pathnm: TyPathnm, **kwargs) -> None:
        _path: TyPath = PathNm.sh_path(pathnm, kwargs)
        if wb is not None:
            wb.save(_path)

    @staticmethod
    def write_wb_from_doaoa(
            doaoa: TyDoAoA, pathnm: str, **kwargs) -> None:
        _path: TyPath = PathNm.sh_path(pathnm, kwargs)
        IooPathWbPe.write_wb_from_doaoa(doaoa, _path)

    @staticmethod
    def write_wb_from_doaod(
            doaod: TyDoAoD, pathnm: str, **kwargs) -> None:
        _path: TyPath = PathNm.sh_path(pathnm, kwargs)
        IooPathWbPe.write_wb_from_doaod(doaod, _path)

    @staticmethod
    def write_wb_from_aod(
            aod: TyAoD, pathnm: str, sheet: TySheet, **kwargs) -> None:
        _path: TyPath = PathNm.sh_path(pathnm, kwargs)
        IooPathWbPe.write_wb_from_aod(aod, _path, sheet)
