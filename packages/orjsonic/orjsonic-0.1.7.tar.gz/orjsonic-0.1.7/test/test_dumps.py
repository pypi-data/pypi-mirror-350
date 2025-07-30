import orjsonic as orjson
import pytest
from pathlib import Path


@pytest.fixture
def tmp_dir(tmp_path_factory):
    _tmp_dir = tmp_path_factory.mktemp('test_orjsonic')
    yield _tmp_dir


class TestDumps:
    def test_dumps_dict(self, tmp_dir):
        output = tmp_dir.joinpath('test_dumps.json')
        assert orjson.dumps({'a': 1, 'b': 2}, output=output) == b'{"a":1,"b":2}'
        assert output.exists()
