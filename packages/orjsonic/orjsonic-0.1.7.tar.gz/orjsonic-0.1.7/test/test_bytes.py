# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from base64 import b64decode, b64encode

import orjsonic as orjson


class TestBytes:
    def test_bytes_obj(self):
        """
        dumps() simple bytes obj
        """
        obj = b'hello'
        assert b64decode(orjson.dumps(obj)) == obj
        assert orjson.dumps(obj).decode() == '"{}"'.format(b64encode(obj).decode())

        obj = b'\x00\xff'
        assert b64decode(orjson.dumps(obj)) == obj
        assert orjson.dumps(obj).decode() == '"{}"'.format(b64encode(obj).decode())

    def test_dict_with_bytes(self):
        """
        dumps() dict with bytes
        """
        val = b'hello'
        obj = {'data': val}
        assert b64decode(orjson.loads(orjson.dumps(obj))['data']) == val
