# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import Path

import orjsonic as orjson

data_dir = os.path.join(os.path.dirname(__file__), "../data")


class TestFile:
    def test_file(self):
        file = Path(data_dir, 'file', 'file_utf8.json')
        assert orjson.loads(file) == dict(a=1, b=2)
