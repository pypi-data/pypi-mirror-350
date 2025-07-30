# orjsonic
A fleixible and fast wrapper around orjson for custom JSON encoding/decoding.

It basically copies the `orjson` API with some customized default behaviors.

## Usage & Differences

### loads

- ##### 🎯 support to load file path from `str`, `os.PathLike`, `pathlib.Path`

<table>
<tr>
<th>orjson</th>
<th>orjsonic</th>
</tr>
<tr>
<td valign="top">
<div style="width: 377px;">

```python
>>> import orjson
>>> orjson.loads('data/file/file_utf8.json')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
orjson.JSONDecodeError: unexpected character:
  line 1 column 1 (char 0)
```

</div>
</td>
<td valign="top">
<div style="width: 370px;">

```python
>>> import orjsonic
>>> orjsonic.loads('data/file/file_utf8.json')
{'a': 1, 'b': 2}
```

</div>
</td>
</tr>
</table>

- ##### 🎯 support to set encoding arbitrarily or detect encoding automatically (although precision is in doubt)

<table>
<tr>
<th>orjson</th>
<th>orjsonic</th>
</tr>
<tr>
<td valign="top">
<div style="width: 377px;">

```python
>>> import orjson
>>> data = '{"name": "小明"}'.encode('gbk')
>>> orjson.loads(data)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
orjson.JSONDecodeError: str is not valid UTF-8:
  surrogates not allowed:
    line 1 column 1 (char 0)
```

</div>
</td>
<td valign="top">
<div style="width: 370px;">

```python
>>> import orjsonic
>>> data = '{"name": "小明"}'.encode('gbk')
>>> orjsonic.loads(data)
{'name': 'ะกร๗'}
>>> orjsonic.loads(data, encoding='gbk')
{'name': '小明'}
```

</div>
</td>
</tr>
</table>

- ##### 🎯 it also try best to resolve errors during loads different wrong encoded data, you can set `orjsonic.loads(data, errors='ignore')` or other encoding error handling methods, to avoid break your code, in case the wrong encoding is not critical.

<table>
<tr>
<th>orjson</th>
<th>orjsonic</th>
</tr>
<tr>
<td valign="top">
<div style="width: 377px;">

```python
>>> import orjson
>>> data = '{"name": "小明"}'.encode('gbk')
>>> orjson.loads(data)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
orjson.JSONDecodeError: str is not valid UTF-8:
  surrogates not allowed:
    line 1 column 1 (char 0)
```

</div>
</td>
<td valign="top">
<div style="width: 370px;">

```python
>>> import orjsonic
>>> data = '{"name": "小明"}'.encode('gbk')
>>> orjsonic.loads(data, errors='replace')
{'name': 'С��'}
```

</div>
</td>
</tr>
</table>


### dumps

- ##### 🎯 added datetime_fmt, date_fmt and time_fmt to support customize datetime format. If set OPT_PASSTHROUGH_DATETIME without specify `default`, changed default format from iso format `%Y-%m-%dT%H:%M:%S.%f` to `%Y-%m-%d %H:%M:%S`

<table>
<tr>
<th>orjson</th>
<th>orjsonic</th>
</tr>
<tr>
<td valign="top">
<div style="width: 377px;">

```python
>>> import datetime
>>> import orjson
>>> data = dict(
>>>     datetime=datetime.datetime(
>>>         2025, 1, 2, 3, 4, 5, 678900
>>>     ),
>>>     date=datetime.date(2025, 1, 2),
>>>     time=datetime.time(3, 4, 5, 678900),
>>> )
>>> orjson.dumps(data)
b'{"datetime":"2025-01-02T03:04:05.678900",
"date":"2025-01-02","time":"03:04:05.678900"}'

>>> orjson.dumps(
>>>     data,
>>>     option=orjson.OPT_PASSTHROUGH_DATETIME
>>> )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Type is not JSON serializable:
  datetime.datetime
```

</div>
</td>
<td valign="top">
<div style="width: 370px;">

```python
>>> import datetime
>>> import orjsonic
>>> data = dict(
>>>     datetime=datetime.datetime(
>>>         2025, 1, 2, 3, 4, 5, 678900
>>>     ),
>>>     date=datetime.date(2025, 1, 2),
>>>     time=datetime.time(3, 4, 5, 678900),
>>> )
>>> orjsonic.dumps(data)
b'{"datetime":"2025-01-02T03:04:05.678900",
"date":"2025-01-02","time":"03:04:05.678900"}'

>>> orjsonic.dumps(
>>>     data,
>>>     option=orjson.OPT_PASSTHROUGH_DATETIME
>>> )
b'{"datetime":"2025-01-02 03:04:05",
"date":"2025-01-02","time":"03:04:05"}'

>>> orjsonic.dumps(
>>>     data,
>>>     datetime_fmt='%Y%m%d%H%M%S',
>>>     date_fmt='%Y-%m-%d %H:%M:%S.%f',
>>>     time_fmt='%H:%M:%S.%f',
>>> )
b'{"datetime":"20250102030405",
"date":"2025-01-02 00:00:00.000000",
"time":"03:04:05."}'
```

</div>
</td>
</tr>
</table>

- ##### 🎯 add support to numpy and pandas series

<table>
<tr>
<th>orjson</th>
<th>orjsonic</th>
</tr>
<tr>
<td valign="top">
<div style="width: 377px;">

```python
>>> import datetime
>>> import numpy as np
>>> import pandas as pd
>>> import orjson
>>> arr = np.array([
>>>     1,
>>>     np.datetime64('2025-01-02'),
>>>     np.datetime64('nat')
>>> ])
>>> s = pd.Series(arr).convert_dtypes()

>>> orjson.dumps(arr)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Type is not JSON serializable:
  numpy.ndarray

>>> orjson.dumps(
>>>     arr,
>>>     option=orjson.OPT_SERIALIZE_NUMPY
>>> )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported datatype in numpy array

>>> orjson.dumps(s)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Type is not JSON serializable:
  Series
```

</div>
</td>
<td valign="top">
<div style="width: 370px;">

```python
>>> import datetime
>>> import numpy as np
>>> import pandas as pd
>>> import orjsonic
>>> arr = np.array([
>>>     1,
>>>     np.datetime64('2025-01-02'),
>>>     np.datetime64('nat')
>>> ])
>>> s = pd.Series(arr).convert_dtypes()

>>> orjsonic.dumps(arr)
b'[1,"2025-01-02",null]'

>>> orjson.dumps(s)
b'[1,"2025-01-02",null]'
```

</div>
</td>
</tr>
</table>

- ##### 🎯 support argument `output` to dump to json file, also support argument `return_str` to return json string rather than bytes.

<table>
<tr>
<th>orjson</th>
<th>orjsonic</th>
</tr>
<tr>
<td valign="top">
<div style="width: 377px;">

```python
>>> import orjson
>>> ret_bytes = orjson.dumps(
>>>     {'a': 1, 'b': 2}
>>> )
>>> ret_bytes.decode()
'{"a":1,"b":2}'
>>> with open('output.json', 'wb') as f:
>>>     f.write(ret_bytes)
>>> with open('output.json', 'r') as f:
>>>     print(f.read())
{"a":1,"b":2}
```

</div>
</td>
<td valign="top">
<div style="width: 370px;">

```python
>>> import orjsonic
>>> ret_str = orjsonic.dumps(
>>>     {'a': 1, 'b': 2},
>>>     output='output.json',
>>>     return_str=True
>>> )
>>> ret_str
'{"a":1,"b":2}'
>>> with open('output.json', 'r') as f:
>>>     print(f.read())
{"a":1,"b":2}
```

</div>
</td>
</tr>
</table>
