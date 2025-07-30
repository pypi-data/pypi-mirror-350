import datetime
import os
import pathlib
import sys
from base64 import b64encode
from functools import partial
from typing import Any, Callable, Literal

import chardet
import numpy as np
import orjson
import pandas as pd

orjsonic = orjson
Fragment = orjson.Fragment
JSONDecodeError = orjson.JSONDecodeError
JSONEncodeError = orjson.JSONEncodeError
OPT_APPEND_NEWLINE = orjson.OPT_APPEND_NEWLINE
OPT_INDENT_2 = orjson.OPT_INDENT_2
OPT_NAIVE_UTC = orjson.OPT_NAIVE_UTC
OPT_NON_STR_KEYS = orjson.OPT_NON_STR_KEYS
OPT_OMIT_MICROSECONDS = orjson.OPT_OMIT_MICROSECONDS
OPT_PASSTHROUGH_DATACLASS = orjson.OPT_PASSTHROUGH_DATACLASS
OPT_PASSTHROUGH_DATETIME = orjson.OPT_PASSTHROUGH_DATETIME
OPT_PASSTHROUGH_SUBCLASS = orjson.OPT_PASSTHROUGH_SUBCLASS
OPT_SERIALIZE_DATACLASS = orjson.OPT_SERIALIZE_DATACLASS
OPT_SERIALIZE_NUMPY = orjson.OPT_SERIALIZE_NUMPY
OPT_SERIALIZE_UUID = orjson.OPT_SERIALIZE_UUID
OPT_SORT_KEYS = orjson.OPT_SORT_KEYS
OPT_STRICT_INTEGER = orjson.OPT_STRICT_INTEGER
OPT_UTC_Z = orjson.OPT_UTC_Z


def __custom_default(
    obj: Any, datetime_fmt: str = None, date_fmt: str = None, time_fmt: str = None, option: int = 0
) -> Any:
    """
    Custom default function for serializing objects that are not natively serializable by orjson.

    Parameters:
    obj (Any): The object to be serialized.
    datetime_fmt (str, optional): The format string for datetime objects. Defaults to '%Y-%m-%d %H:%M:%S'.
    date_fmt (str, optional): The format string for date objects. Defaults to '%Y-%m-%d'.
    time_fmt (str, optional): The format string for time objects. Defaults to '%H:%M:%S'.
    **kwargs: Additional keyword arguments that might be passed but are not used in this function.

    Returns:
    Any: The serialized object as a string or list, depending on the type of the input object.

    This function handles the serialization of the following types:
    - datetime.datetime: Converts to a string using the specified datetime format.
    - datetime.date: Converts to a string using the specified date format.
    - datetime.time: Converts to a string using the specified time format.
    - np.datetime64: Converts to a string using the specified datetime or date format, depending on whether it includes time information.
    - np.datetime64('NaT'): Converts to null.
    - np.ndarray: Converts to a list.
    - bytes | bytearray | memoryview: Use base64 to encode bytes object and convert to string.
    """
    datetime_fmt = datetime_fmt or '%Y-%m-%d %H:%M:%S'
    date_fmt = date_fmt or '%Y-%m-%d'
    time_fmt = time_fmt or '%H:%M:%S'
    if isinstance(obj, datetime.datetime):
        if obj is pd.NaT:
            return None
        return obj.strftime(datetime_fmt)
    if isinstance(obj, datetime.date):
        return obj.strftime(date_fmt)
    if isinstance(obj, datetime.time):
        # tzinfo only valid for datetime.datetime, not datetime.time
        # orjson will raise a TypeError if tzinfo is present
        # orjsonic will ignore the tzinfo whether %z or %Z is present in time_fmt or not
        return obj.strftime(time_fmt)
    if isinstance(obj, np.datetime64):
        if np.isnat(obj):
            return None
        time_us = obj - obj.astype('datetime64[D]')
        if time_us:
            return obj.item().strftime(datetime_fmt)
        else:
            return obj.item().strftime(date_fmt)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, pd.Series):
        return obj.to_list()
    if isinstance(obj, bytes | bytearray):
        return b64encode(obj).decode('utf-8')
    if isinstance(obj, memoryview):
        return b64encode(obj.tobytes()).decode('utf-8')
    return orjson.dumps(obj, option=option)


def dumps(
    __obj: Any,
    /,
    default: Callable[[Any], Any] = None,
    option: int = None,
    datetime_fmt: str = None,
    date_fmt: str = None,
    time_fmt: str = None,
    output: str | os.PathLike | pathlib.Path = None,
    return_str: bool = False,
) -> str:
    """
    Serialize an object to a JSON-formatted string using orjson with custom options and formatting.

    Parameters:
    __obj (Any): The object to be serialized.
    default (Callable[[Any], Any], optional): A callable to handle non-serializable objects. Defaults to None.
    option (int, optional): Options to customize the serialization behavior. Defaults to 0.
    datetime_fmt (str, optional): The format string for datetime objects. Defaults to None.
    date_fmt (str, optional): The format string for date objects. Defaults to None.
    time_fmt (str, optional): The format string for time objects. Defaults to None.
    output (str | os.PathLike | pathlib.Path, optional): A file path to write the serialized JSON data. Defaults to None.
    return_str (bool, optional): If True, return the JSON data as a string. If False, return the JSON data as bytes. Defaults to False.

    Returns:
    str | bytes: The JSON-formatted string or bytes of the serialized object, depending on the `return_str` parameter.

    The function uses orjson to serialize the object. If a custom format is provided for datetime, date, or time objects
    and no default callable is specified, it uses a custom default function with the specified formats.
    If serialization fails with a TypeError, it falls back to using the custom default function.
    If an output path is provided, the serialized JSON data is written to the specified file.
    """
    if option is None:
        option = 0
    if type(option) is not int:
        raise TypeError('option must be an integer or orjonic.OPT_* or None')
    if default is None and any((datetime_fmt is not None, date_fmt is not None, time_fmt is not None)):
        custom_default = partial(
            __custom_default, datetime_fmt=datetime_fmt, date_fmt=date_fmt, time_fmt=time_fmt, option=option
        )
        option = option | OPT_PASSTHROUGH_DATETIME
        data = orjson.dumps(__obj, default=custom_default, option=option)
    else:
        try:
            data = orjson.dumps(__obj, default=default, option=option | OPT_SERIALIZE_NUMPY)
        except TypeError:
            custom_default = partial(
                __custom_default, datetime_fmt=datetime_fmt, date_fmt=date_fmt, time_fmt=time_fmt, option=option
            )
            data = orjson.dumps(__obj, default=custom_default, option=option | OPT_PASSTHROUGH_DATETIME)

    if output is not None:
        with open(output, 'wb') as f:
            f.write(data)

    if not return_str:
        return data
    else:
        return data.decode(sys.getdefaultencoding())


def __is_valid_file_path(s: str | os.PathLike | pathlib.Path):
    """check if a string is a valid file path and exists"""
    return isinstance(s, (str, os.PathLike, pathlib.Path)) and os.path.isfile(s) and os.path.exists(s)


def __read_file(file_path: str | os.PathLike | pathlib.Path) -> bytes:
    """read a file and return its contents as bytes"""
    with open(file_path, 'rb') as f:
        data = f.read()
        return data


def __convert_to_utf8(
    data: bytes | bytearray | memoryview,
    encoding: Literal['utf-8-sig', 'gbk', 'gb18030'] = None,
    errors: Literal['strict', 'ignore', 'replace', 'backslashreplace', 'surrogateescape'] = None,
) -> bytes:
    """
    Convert input data to UTF-8 encoding, suitable for orjson to load.

    Parameters:
    - data: The input data to be converted. Can be of type bytes, bytearray, or memoryview.
    - encoding: The encoding to use for decoding the input data. Defaults to 'utf-8' if not specified.
                Supported encodings are 'utf-8-sig', 'gbk', and 'gb18030'.
    - errors: The error handling scheme to use for decoding. Defaults to 'strict' if not specified.
              Supported options are 'strict', 'ignore', 'replace', 'backslashreplace', and 'surrogateescape'.

    Returns:
    - bytes: The input data encoded in UTF-8.

    If the specified encoding fails to decode the data, the function attempts to detect the encoding using chardet.
    However, since chardet can be computationally expensive, providing the correct encoding or using a non-strict
    error handling scheme can improve performance while maintaining correctness.
    """
    if isinstance(data, memoryview):
        data = data.tobytes()
    if encoding is None:
        encoding = 'utf-8'
    if errors is None:
        errors = 'strict'
    try:
        data = data.decode(encoding=encoding, errors=errors)
        return data.encode('utf-8')
    except UnicodeDecodeError:
        encoding = chardet.detect(data)['encoding']
        data = data.decode(encoding=encoding, errors=errors)
        return data.encode('utf-8')


def loads(
    __obj: bytes | bytearray | memoryview | str | os.PathLike | pathlib.Path,
    encoding: Literal['utf-8-sig', 'gbk', 'gb18030', 'ascii'] = None,
    errors: Literal['strict', 'ignore', 'replace', 'backslashreplace', 'surrogateescape'] = None,
) -> dict | list | str | int | float | bool | None:
    """
    Parse JSON data from various input types and handle encoding issues.

    Parameters:
    - __obj: The input data to be parsed. Can be of type bytes, bytearray, memoryview, str, os.PathLike, or pathlib.Path.
    - encoding: The encoding to use for decoding the input data if it is not already in UTF-8. Defaults to None.
                Supported encodings are 'utf-8-sig', 'gbk', 'gb18030', and 'ascii'.
    - errors: The error handling scheme to use for decoding. Defaults to None.
              Supported options are 'strict', 'ignore', 'replace', 'backslashreplace', and 'surrogateescape'.

    Returns:
    - The parsed JSON data, which can be a dict, list, str, int, float, bool, or None.

    If the input data is of type bytes, bytearray, or memoryview, the function attempts to parse it directly using orjson.
    If a JSONDecodeError occurs, it converts the data to UTF-8 using the specified encoding and errors handling scheme,
    then attempts to parse it again.

    If the input data is a string, the function checks if it represents a valid file path:
    - If it is a valid file path, it reads the file and recursively calls `loads` with the file content.
    - If it is not a valid file path, it encodes the string to UTF-8 and then recursively calls `loads` with the encoded bytes.
    """
    if isinstance(__obj, (bytes, bytearray, memoryview)):
        try:
            return orjson.loads(__obj)
        except JSONDecodeError:
            data = __convert_to_utf8(__obj, encoding=encoding, errors=errors)
            return orjson.loads(data)

    if isinstance(__obj, (str, os.PathLike, pathlib.Path)):
        if __is_valid_file_path(__obj):
            data = __read_file(__obj)
            return loads(data, encoding=encoding, errors=errors)
        else:
            try:
                data = __obj.encode('utf-8')
                return loads(data, encoding=encoding, errors=errors)
            except UnicodeEncodeError as err:
                if 'surrogates not allowed' in str(err):
                    try:
                        data = __obj.encode('unicode_escape')
                        return loads(data, encoding=encoding, errors=errors)
                    except JSONDecodeError as sub_err:
                        if 'no low surrogate in string' in str(sub_err) or 'invalid high surrogate in string' in str(sub_err):
                            data = __obj.encode('utf-8', errors='replace')
                            return loads(data, encoding=encoding, errors=errors)
                else:
                    raise err

    return orjson.loads(__obj)
