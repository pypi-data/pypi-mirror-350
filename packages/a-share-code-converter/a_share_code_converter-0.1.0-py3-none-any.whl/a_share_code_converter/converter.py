import numpy as np
import pandas as pd
import polars as pl
import numbers
from typing import Any

class CodeConverter:
    @staticmethod
    def _to_int_array(codes: Any) -> np.ndarray:
        if isinstance(codes, pd.Series) :
            raw_vals = codes.tolist()
        elif isinstance(codes, np.ndarray):
            raw_vals = codes.tolist()
        elif isinstance(codes, pl.Series):
            raw_vals = codes.to_list()
        else:
            raw_vals = list(codes)
        # Build list of normalized strings
        str_list = []
        for v in raw_vals:
            if isinstance(v, numbers.Number):
                # Cast floats and ints to int first to drop any decimal
                v_int = int(v)
                str_list.append(str(v_int))
            else:
                # Keep string as-is
                str_list.append(str(v))
        # Convert to numpy array of unicode for vectorized ops
        arr = np.array(str_list, dtype=str)
        # Strip suffixes (.SZ, .SH, .BJ) and any leading/trailing whitespace
        for suf in ['.SZ', '.SH', '.BJ']:
            arr = np.char.replace(arr, suf, '')
        arr = np.char.strip(arr)
        # Convert to int64
        return arr.astype(np.int64)

    @staticmethod
    def _get_suffix_array(ints: np.ndarray) -> np.ndarray:
        """Return market suffix array based on code ranges."""
        suffix = np.full(ints.shape, '', dtype='<U3')
        mask_sz = (ints >= 0) & (ints <= 399999)
        suffix[mask_sz] = '.SZ'
        mask_sh = (ints >= 600000) & (ints <= 699999)
        suffix[mask_sh] = '.SH'
        mask_bj = ((ints >= 400000) & (ints <= 499999)) | ((ints >= 800000) & (ints <= 899999))
        suffix[mask_bj] = '.BJ'
        return suffix

    @classmethod
    def to_int(cls, codes: Any) -> Any:
        """Convert to integer codes, preserving input type."""
        arr = cls._to_int_array(codes)
        if isinstance(codes, pd.Series):
            return pd.Series(arr, index=codes.index, name=codes.name)
        if isinstance(codes, pl.Series):
            return pl.Series(name=codes.name, values=arr)
        if isinstance(codes, np.ndarray):
            return arr
        return arr.tolist()

    @classmethod
    def to_str(cls, codes: Any) -> Any:
        """Convert to zero-padded 6-digit strings."""
        ints = cls._to_int_array(codes)
        str6 = np.char.zfill(ints.astype(str), 6)
        if isinstance(codes, pd.Series):
            return pd.Series(str6, index=codes.index, name=codes.name)
        if isinstance(codes, pl.Series):
            return pl.Series(name=codes.name, values=str6.tolist())
        if isinstance(codes, np.ndarray):
            return str6
        return str6.tolist()

    @classmethod
    def to_suffix(cls, codes: Any) -> Any:
        """Convert to suffixed format, e.g., '600519.SH'."""
        ints = cls._to_int_array(codes)
        str6 = np.char.zfill(ints.astype(str), 6)
        suffix = cls._get_suffix_array(ints)
        suffixed = np.char.add(str6, suffix)
        if isinstance(codes, pd.Series):
            return pd.Series(suffixed, index=codes.index, name=codes.name)
        if isinstance(codes, pl.Series):
            return pl.Series(name=codes.name, values=suffixed.tolist())
        if isinstance(codes, np.ndarray):
            return suffixed
        return suffixed.tolist()

    @classmethod
    def convert(cls, codes: Any, to: str) -> Any:

        if to == 'int':
            return cls.to_int(codes)
        elif to == 'str':
            return cls.to_str(codes)
        elif to == 'suffix':
            return cls.to_suffix(codes)
        else:
            raise ValueError(f"Unsupported target format: {to}")

