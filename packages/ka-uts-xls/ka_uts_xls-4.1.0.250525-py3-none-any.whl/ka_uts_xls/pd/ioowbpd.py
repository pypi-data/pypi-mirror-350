from typing import Any, TypeAlias

import pandas as pd

# from ka_uts_com.log import Log
from ka_uts_dic.dic import Dic
from ka_uts_path.path import Path

TyPdDf: TypeAlias = pd.DataFrame

TyArr = list[Any]
TyDic = dict[Any, Any]
TyAoA = list[TyArr]
TyAoD = list[TyDic]
TyDoAoA = dict[Any, TyAoA]
TyDoAoD = dict[Any, TyAoD]
TyDoPdDf = dict[Any, TyPdDf]


class IooPathPdDf:

    @staticmethod
    def write_pd_from_dopdf(dodf: TyDoPdDf, path: str) -> None:
        # def write_xls(d_df: TyDoPdDf, path: str, **kwargs) -> None:
        Path.mkdir_from_path(path)
        writer = pd.ExcelWriter(path, engine='openpyxl')
        _a_key: TyArr = Dic.show_sorted_keys(dodf)
        for _key in _a_key:
            _df: TyPdDf = dodf[_key]
            _df.to_excel(writer, sheet_name=_key)
        writer.close()
