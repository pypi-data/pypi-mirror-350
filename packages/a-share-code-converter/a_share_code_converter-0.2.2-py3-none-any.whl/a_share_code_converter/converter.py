import numpy as np
import pandas as pd
import polars as pl
import re
from typing import Any


class CodeConverter:
    _short_name_map: dict[str, str] | None = None

    @staticmethod
    def _prepare_stripped(codes: Any) -> Any:
        """
        Strip market suffixes and whitespace using vectorized operations for pandas and Polars.
        Returns uppercase strings without suffix.
        """
        # pandas Series
        if isinstance(codes, pd.Series):
            s = codes.astype(str).str.strip().str.upper()
            return s.str.replace(r"\.(SZ|SH|BJ)$", "", regex=True)
        # Polars Series: fallback to Python list processing
        if isinstance(codes, pl.Series):
            raw = codes.cast(pl.Utf8).to_list()
            cleaned = [re.sub(r"\.(SZ|SH|BJ)$", "", str(v).strip(), flags=re.IGNORECASE).upper() for v in raw]
            return pl.Series(name=codes.name, values=cleaned, strict=False)
        # pandas DataFrame: apply to first column
        if isinstance(codes, pd.DataFrame):
            return CodeConverter._prepare_stripped(codes.iloc[:, 0])
        # Polars DataFrame: apply to first column
        if isinstance(codes, pl.DataFrame):
            return CodeConverter._prepare_stripped(codes[codes.columns[0]])
        # list or ndarray fallback
        try:
            raw = list(codes)
        except Exception:
            raw = [codes]
        return [re.sub(r"\.(SZ|SH|BJ)$", "", str(v).strip(), flags=re.IGNORECASE).upper() for v in raw]

    @staticmethod
    def _get_suffix_list(ints: np.ndarray) -> list[str]:
        """
        Generate market suffix list based on integer codes.
        """
        suffixes: list[str] = []
        for v in ints:
            if 0 <= v <= 399999:
                suffixes.append('.SZ')
            elif 600000 <= v <= 699999:
                suffixes.append('.SH')
            elif (400000 <= v <= 499999) or (800000 <= v <= 899999):
                suffixes.append('.BJ')
            else:
                suffixes.append('')
        return suffixes

    @classmethod
    def to_int(cls, codes: Any) -> Any:
        if isinstance(codes, pd.DataFrame):
            col = codes.columns[0]
            return pd.DataFrame({col: cls.to_int(codes[col])}, index=codes.index)
        if isinstance(codes, pl.DataFrame):
            col = codes.columns[0]
            arr = cls.to_int(codes[col])
            return pl.DataFrame({col: arr.to_list()}, strict=False)
        if isinstance(codes, pd.Series):
            stripped = cls._prepare_stripped(codes)
            return stripped.astype('float64').astype(int)
        if isinstance(codes, pl.Series):
            stripped = cls._prepare_stripped(codes)
            return stripped.cast(pl.Float64).cast(pl.Int64)
        if isinstance(codes, np.ndarray):
            return np.array([int(str(v).split('.')[0]) for v in codes], dtype=np.int64)
        return [int(str(v).split('.')[0]) for v in codes]

    @classmethod
    def to_str(cls, codes: Any) -> Any:
        if isinstance(codes, pd.DataFrame):
            col = codes.columns[0]
            return pd.DataFrame({col: cls.to_str(codes[col])}, index=codes.index)
        if isinstance(codes, pl.DataFrame):
            col = codes.columns[0]
            arr = cls.to_str(codes[col])
            return pl.DataFrame({col: arr.to_list()}, strict=False)
        if isinstance(codes, pd.Series):
            stripped = cls._prepare_stripped(codes)
            return stripped.str.zfill(6).str.slice(0,6)
        if isinstance(codes, pl.Series):
            stripped = cls._prepare_stripped(codes)
            return stripped.str.zfill(6).str.slice(0,6)
        ints = cls.to_int(codes)
        return [str(int(v)).zfill(6) for v in ints]

    @classmethod
    def to_suffix(cls, codes: Any) -> Any:
        if isinstance(codes, pd.DataFrame):
            col = codes.columns[0]
            return pd.DataFrame({col: cls.to_suffix(codes[col])}, index=codes.index)
        if isinstance(codes, pl.DataFrame):
            # delegate to Series version
            return cls.to_suffix(codes[codes.columns[0]])
        if isinstance(codes, pd.Series):
            s6 = cls.to_str(codes)
            suffixes = cls._get_suffix_list(s6.astype(int).values)
            return s6 + pd.Series(suffixes, index=codes.index)
        if isinstance(codes, pl.Series):
            s6_list = cls.to_str(codes).to_list()
            ints = [int(x) for x in s6_list]
            suffixes = cls._get_suffix_list(np.array(ints, dtype=np.int64))
            suffixed = [f"{c}{s}" for c, s in zip(s6_list, suffixes)]
            return pl.Series(name=codes.name, values=suffixed, strict=False)
        s6 = cls.to_str(codes)
        ints = cls.to_int(codes)
        suffixes = cls._get_suffix_list(np.array(ints, dtype=np.int64))
        return [f"{c}{s}" for c, s in zip(s6, suffixes)]

    @classmethod
    def convert(cls, codes: Any, to: str) -> Any:
        if to == 'int':
            return cls.to_int(codes)
        if to == 'str':
            return cls.to_str(codes)
        if to == 'suffix':
            return cls.to_suffix(codes)
        raise ValueError(f"Unsupported target format: {to}")

    @classmethod
    def to_name(
        cls,
        codes: Any,
        with_suffix: bool = False,
        with_code: bool = False,
        code_format: str = 'suffix'
    ) -> Any:
        if cls._short_name_map is None:
            cls._short_name_map = cls._load_short_name_map()
        # pandas DataFrame
        if isinstance(codes, pd.DataFrame):
            col = codes.columns[0]
            series = codes[col]
            df = cls.to_name(series, with_suffix, with_code, code_format)
            df.index = codes.index
            return df
        # polars DataFrame: delegate to Series
        if isinstance(codes, pl.DataFrame):
            return cls.to_name(codes[codes.columns[0]], with_suffix, with_code, code_format)
        # Series or list/array
        if code_format == 'int':
            rep = cls.to_int(codes)
        elif code_format == 'str':
            rep = cls.to_str(codes)
        else:
            rep = cls.to_suffix(codes)
        rep_list = rep.tolist() if hasattr(rep, 'tolist') else list(rep)
        keys = cls.to_str(codes)
        keys_list = keys.tolist() if hasattr(keys, 'tolist') else list(keys)
        names = [cls._short_name_map.get(k, '') for k in keys_list]
        if with_suffix:
            names = [f"{nm} ({cd})" if nm else str(cd) for nm, cd in zip(names, rep_list)]
        if with_code:
            result = list(zip(rep_list, names))
            if isinstance(codes, pd.Series):
                return pd.DataFrame({
                    f"{codes.name}_code": rep_list,
                    f"{codes.name}_short": names
                }, index=codes.index)
            if isinstance(codes, pl.Series):
                return pl.DataFrame({
                    f"{codes.name}_code": rep_list,
                    f"{codes.name}_short": names
                }, strict=False)
            return result
        if isinstance(codes, pd.Series):
            return pd.Series(names, index=codes.index)
        if isinstance(codes, pl.Series):
            return pl.Series(name='short_name', values=names, strict=False)
        if isinstance(codes, np.ndarray):
            return np.array(names)
        return names

    @staticmethod
    def _load_short_name_map() -> dict[str, str]:
        import polars as pl
        from sqlalchemy import create_engine
        conn_str = (
            'oracle+cx_oracle://thsdata:thsdata'
            '@10.200.10.77:1521/?service_name=touyan'
        )
        engine = create_engine(conn_str)
        df = pl.read_database(
            'select SEC_CODE,SEC_SHORT_NAME_CN '
            'from SEC_BASIC_INFO '
            'where SEC_TYPE_CODE=001001 and IS_LISTING=1 '
            'order by SEC_CODE',
            engine,
        )
        return {str(code).zfill(6): name for code, name in zip(df['SEC_CODE'], df['SEC_SHORT_NAME_CN'])}

