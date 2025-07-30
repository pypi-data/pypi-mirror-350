# A-Share Code Converter

`a-share-code-converter` is a lightweight Python utility that helps you normalize and convert Chinese A-share stock codes between various formats. It supports:

- Conversion to pure integer codes (e.g., `600519`)
- Conversion to zero-padded string codes (e.g., `"600519"`)
- Conversion to suffixed formats indicating exchanges (e.g., `"600519.SH"`)

The converter supports multiple input types, including:
- Python `list`
- NumPy arrays
- `pandas.Series`
- `polars.Series`

## 📦 Installation

```bash
pip install a-share-code-converter

```

## 🚀 Usage

The `CodeConverter` class provides the following key methods:

### 1. `CodeConverter.to_int(codes)`

Converts various code formats (e.g. `"600519.SH"`, `"000001"`, `430047`) into **pure 6-digit integers**.

- ✅ Strips suffixes like `.SH`, `.SZ`, `.BJ`
- ✅ Works with `list`, `numpy.ndarray`, `pandas.Series`, `polars.Series`

```python
from a_share_code_converter import CodeConverter

codes = ["600519", "000001.SZ", "430047.BJ", 2415]

CodeConverter.to_int(codes)
# Output: [600519, 1, 430047, 2415]
```

### `2. CodeConverter.to_str(codes)`

Converts input to zero-padded 6-digit string format without any suffix.

✅ Ensures all codes are 6-character strings like '000001', '600519'

```python
CodeConverter.to_str(codes)
# Output: ['600519', '000001', '430047', '002415']
```

### 3. `CodeConverter.to_suffix(codes)`

Converts codes to full format with market suffix, e.g., '600519.SH'.

- ✅ Based on numeric code ranges:

  - .SZ: 000000–399999

  - .SH: 600000–699999

  - .BJ: 400000–499999, 800000–899999

```python
CodeConverter.to_suffix(codes)
# Output: ['600519.SH', '000001.SZ', '430047.BJ', '002415.SZ']
```

### 4. `CodeConverter.convert(codes, to)`

A unified entry point to perform conversion. Choose target format via to parameter:

| `to` value | Result                                |
| ---------- | ------------------------------------- |
| `'int'`    | Integer codes (`int` or `np.int64`)   |
| `'str'`    | 6-digit zero-padded string codes      |
| `'suffix'` | 6-digit string with `.SH`/`.SZ`/`.BJ` |

```python
CodeConverter.convert(codes, to='int')
# Output: [600519, 1, 430047, 2415]

CodeConverter.convert(codes, to='str')
# Output: ['600519', '000001', '430047', '002415']

CodeConverter.convert(codes, to='suffix')
# Output: ['600519.SH', '000001.SZ', '430047.BJ', '002415.SZ']
```


## 🧪 Supported Input Types

- list[str | int | float]

- numpy.ndarray

- pandas.Series

- polars.Series

All methods will preserve the original type (e.g., return a pandas.Series if input is a pandas.Series).