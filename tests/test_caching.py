# -*- coding: utf-8; -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Flavien Charlon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bitcoin.core.script
import colorcore.caching
import openassets.protocol
import unittest


class SqliteCacheTests(unittest.TestCase):
    def test_colored_output(self):
        target = colorcore.caching.SqliteCache(':memory:')

        output = openassets.protocol.TransactionOutput(
            150,
            bitcoin.core.script.CScript(b'abcd'),
            b'1234',
            75,
            openassets.protocol.OutputType.issuance
        )

        target.put(b'transaction', 5, output)
        result = target.get(b'transaction', 5)

        self.assert_output(result, 150, b'abcd', b'1234', 75, openassets.protocol.OutputType.issuance)

    def test_commit(self):
        target = colorcore.caching.SqliteCache(':memory:')

        output = openassets.protocol.TransactionOutput(
            150,
            bitcoin.core.script.CScript(b'abcd'),
            b'1234',
            75,
            openassets.protocol.OutputType.issuance
        )

        target.put(b'transaction', 5, output)
        target.commit()
        result = target.get(b'transaction', 5)

        self.assert_output(result, 150, b'abcd', b'1234', 75, openassets.protocol.OutputType.issuance)

    def test_uncolored_output(self):
        target = colorcore.caching.SqliteCache(':memory:')

        output = openassets.protocol.TransactionOutput(
            150,
            bitcoin.core.script.CScript(b'abcd'),
            None,
            0,
            openassets.protocol.OutputType.uncolored
        )

        target.put(b'transaction', 5, output)
        result = target.get(b'transaction', 5)

        self.assert_output(result, 150, b'abcd', None, 0, openassets.protocol.OutputType.uncolored)

    def test_max_values(self):
        target = colorcore.caching.SqliteCache(':memory:')

        output = openassets.protocol.TransactionOutput(
            2 ** 63 - 1,
            bitcoin.core.script.CScript(b'a' * 16384),
            b'1234',
            2 ** 63 - 1,
            openassets.protocol.OutputType.issuance
        )

        target.put(b'transaction', 5, output)
        result = target.get(b'transaction', 5)

        self.assert_output(
            result, 2 ** 63 - 1, b'a' * 16384, b'1234', 2 ** 63 - 1, openassets.protocol.OutputType.issuance)

    def test_cache_miss(self):
        target = colorcore.caching.SqliteCache(':memory:')

        result = target.get(b'transaction', 5)

        self.assertIsNone(result)

    def assert_output(self, output, nValue, scriptPubKey, asset_address, asset_quantity, output_type):
        self.assertEqual(nValue, output.nValue)
        self.assertEqual(scriptPubKey, bytes(output.scriptPubKey))
        self.assertEqual(asset_address, output.asset_address)
        self.assertEqual(asset_quantity, output.asset_quantity)
        self.assertEqual(output_type, output.output_type)