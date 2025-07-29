import dataclasses
import unittest
from collections.abc import Iterable
from typing import Self

import ddt

from iker.common.utils.sequtils import Seq
from iker.common.utils.sequtils import batch_yield
from iker.common.utils.sequtils import chunk, chunk_between, chunk_with_key, merge_chunks
from iker.common.utils.sequtils import deduped, grouped
from iker.common.utils.sequtils import head, init, last, tail
from iker.common.utils.sequtils import seq


@ddt.ddt
class SeqUtilsTest(unittest.TestCase):
    data_head = [([1], 1), ([1, 2], 1)]

    @ddt.idata(data_head)
    @ddt.unpack
    def test_head(self, data, expect):
        self.assertEqual(expect, head(data))

    def test_head__empty(self):
        self.assertRaises(Exception, head, [])

    def test_head__none(self):
        self.assertRaises(Exception, head, None)

    data_last = [([1], 1), ([1, 2], 2)]

    @ddt.idata(data_last)
    @ddt.unpack
    def test_last(self, data, expect):
        self.assertEqual(expect, last(data))

    def test_last__empty(self):
        self.assertRaises(Exception, last, [])

    def test_last__none(self):
        self.assertRaises(Exception, last, None)

    data_init = [([1], []), ([1, 2], [1]), ([1, 2, 3], [1, 2])]

    @ddt.idata(data_init)
    @ddt.unpack
    def test_init(self, data, expect):
        self.assertEqual(expect, init(data))

    def test_init__empty(self):
        self.assertEqual([], init([]))

    def test_init__none(self):
        self.assertRaises(Exception, init, None)

    data_tail = [([1], []), ([1, 2], [2]), ([1, 2, 3], [2, 3])]

    @ddt.idata(data_tail)
    @ddt.unpack
    def test_tail(self, data, expect):
        self.assertEqual(expect, tail(data))

    def test_tail__empty(self):
        self.assertEqual([], tail([]))

    def test_tail__none(self):
        self.assertRaises(Exception, tail, None)

    data_grouped = [
        (None, lambda x: x, []),
        ([], lambda x: x, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                (0, [0]),
                (1, [1]),
                (2, [2]),
                (3, [3]),
                (4, [4]),
                (5, [5]),
                (6, [6]),
                (7, [7]),
                (8, [8]),
                (9, [9]),
                (10, [10]),
                (11, [11]),
                (12, [12]),
                (13, [13]),
                (14, [14]),
                (15, [15]),
                (16, [16]),
                (17, [17]),
                (18, [18]),
                (19, [19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 5,
            [
                (0, [0, 5, 10, 15]),
                (1, [1, 6, 11, 16]),
                (2, [2, 7, 12, 17]),
                (3, [3, 8, 13, 18]),
                (4, [4, 9, 14, 19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 2,
            [
                (0, [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]),
                (1, [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: None,
            [(None, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])],
        ),
        (
            [[0] * 5, [1] * 5, [2] * 4, [3] * 4, [4] * 3, [5] * 3],
            lambda x: len(x),
            [
                (5, [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]]),
                (4, [[2, 2, 2, 2], [3, 3, 3, 3]]),
                (3, [[4, 4, 4], [5, 5, 5]]),
            ],
        ),
    ]

    @ddt.idata(data_grouped)
    @ddt.unpack
    def test_grouped(self, data, key_func, expect):
        self.assertEqual(expect, grouped(data, key_func=key_func))

    data_grouped__values_only = [
        (None, lambda x: x, []),
        ([], lambda x: x, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 5,
            [
                [0, 5, 10, 15],
                [1, 6, 11, 16],
                [2, 7, 12, 17],
                [3, 8, 13, 18],
                [4, 9, 14, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 2,
            [
                [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
                [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: None,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [[0] * 5, [1] * 5, [2] * 4, [3] * 4, [4] * 3, [5] * 3],
            lambda x: len(x),
            [
                [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]],
                [[2, 2, 2, 2], [3, 3, 3, 3]],
                [[4, 4, 4], [5, 5, 5]],
            ],
        ),
    ]

    @ddt.idata(data_grouped__values_only)
    @ddt.unpack
    def test_grouped__values_only(self, data, key_func, expect):
        self.assertEqual(expect, grouped(data, key_func=key_func, values_only=True))

    data_deduped = [
        (None, lambda x: x, []),
        ([], lambda x, y: x == y, []),
        ([0, 0, 0, 0, 0], lambda x, y: x == y, [0]),
        ([None, None, None], lambda x, y: x == y, [None]),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x == y,
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        ),
        (
            [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
            lambda x, y: x == y,
            [0, 1, 2, 3, 4, 3, 2, 1, 0],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) < 2,
            [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
        ),
    ]

    @ddt.idata(data_deduped)
    @ddt.unpack
    def test_deduped(self, data, comp_func, expect):
        self.assertEqual(expect, deduped(data, comp_func=comp_func))

    data_batch_yield = [
        ([], 1, []),
        ([1], 1, [[1]]),
        ([1], 2, [[1]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3, 4, 5, 6], 2, [[1, 2], [3, 4], [5, 6]]),
        ([1, 2, 3, 4, 5, 6], 3, [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3], [4, 5, 6]], 1, [[[1, 2, 3]], [[4, 5, 6]]]),
        ([[1, 2, 3], [4, 5, 6]], 2, [[[1, 2, 3], [4, 5, 6]]]),
    ]

    @ddt.idata(data_batch_yield)
    @ddt.unpack
    def test_batch_yield(self, data, batch_size, expect):
        self.assertEqual(expect, list(batch_yield(data, batch_size)))

    data_chunk = [
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(head(x) - y) > 4,
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(last(x) - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 0,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 1,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    ]

    @ddt.idata(data_chunk)
    @ddt.unpack
    def test_chunk(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk(data, chunk_func=chunk_func))

    data_chunk__exclusive_end = [
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(head(x) - y) > 4,
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(last(x) - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 0,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 1,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    ]

    @ddt.idata(data_chunk__exclusive_end)
    @ddt.unpack
    def test_chunk__exclusive_end(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk(data, chunk_func=chunk_func, exclusive_end=True))

    data_chunk_between = [
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 0,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 1,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    ]

    @ddt.idata(data_chunk_between)
    @ddt.unpack
    def test_chunk_between(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk_between(data, chunk_func=chunk_func))

    data_chunk_between__exclusive_end = [
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 0,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 1,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    ]

    @ddt.idata(data_chunk_between__exclusive_end)
    @ddt.unpack
    def test_chunk_between__exclusive_end(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk_between(data, chunk_func=chunk_func, exclusive_end=True))

    data_chunk_with_key = [
        (None, lambda x: x, []),
        ([], lambda x: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: (x + 1) // 2,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x // 2,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    ]

    @ddt.idata(data_chunk_with_key)
    @ddt.unpack
    def test_chunk_with_key(self, data, key_func, expect):
        self.assertEqual(expect, chunk_with_key(data, key_func=key_func))

    data_chunk_with_key__exclusive_key = [
        (None, lambda x: x, []),
        ([], lambda x: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: (x + 1) // 2,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x // 2,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    ]

    @ddt.idata(data_chunk_with_key__exclusive_key)
    @ddt.unpack
    def test_chunk_with_key__exclusive_key(self, data, key_func, expect):
        self.assertEqual(expect, chunk_with_key(data, key_func=key_func, exclusive_end=True))

    data_merge_chunks = [
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
            lambda x, y: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: abs(head(x) - head(y)) < 10,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: last(x) % 10 == 4,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
    ]

    @ddt.idata(data_merge_chunks)
    @ddt.unpack
    def test_merge_chunks(self, data, merge_func, expect):
        self.assertEqual(expect, merge_chunks(data, merge_func=merge_func))

    data_merge_chunks__drop_exclusive_end = [
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
            lambda x, y: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: abs(head(x) - head(y)) < 10,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: last(init(x)) % 10 == 4,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
    ]

    @ddt.idata(data_merge_chunks__drop_exclusive_end)
    @ddt.unpack
    def test_merge_chunks__drop_exclusive_end(self, data, merge_func, expect):
        self.assertEqual(expect, merge_chunks(data, merge_func=merge_func, drop_exclusive_end=True))


@dataclasses.dataclass(frozen=True, eq=True, order=True)
class Naming(object):
    serial: int
    name: str
    gender: str


class NamingSeq(Seq[Naming]):

    def __init__(self, data: Iterable[Naming]):
        super(NamingSeq, self).__init__(data)
        self.serials = list(map(lambda x: x.serial, self.data))

    def identity(self) -> Self:
        return self

    def axis(self) -> list[int]:
        return self.serials


@ddt.ddt
class SeqTest(unittest.TestCase):
    data_builtin_init = [
        ([], []),
        (seq([]), []),
        (seq(seq([])), []),
        ([0], [0]),
        (seq([0]), [0]),
        (seq(seq([0])), [0]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        (seq([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5]),
        (seq(seq([1, 2, 3, 4, 5])), [1, 2, 3, 4, 5]),
        (range(1, 6), [1, 2, 3, 4, 5]),
        (seq(range(1, 6)), [1, 2, 3, 4, 5]),
        (seq(seq(range(1, 6))), [1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_builtin_init)
    @ddt.unpack
    def test_builtin_init(self, data, expect):
        self.assertEqual(seq(data).data, expect)

    def test_builtin_init__unsupported_data_type(self):
        with self.assertRaises(ValueError):
            seq(object())

    data_builtin_add = [
        ([], [], []),
        ([0], [], [0]),
        ([], [0], [0]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_builtin_add)
    @ddt.unpack
    def test_builtin_add(self, a, b, expect):
        actual = seq(a) + seq(b)
        self.assertEqual(actual.data, expect)

    data_builtin_getitem = [
        ([0], 0, [0]),
        ([1, 2, 3, 4, 5], 0, [1]),
        ([1, 2, 3, 4, 5], -1, [5]),
        ([1, 2, 3, 4, 5], slice(None, 1), [1]),
        ([1, 2, 3, 4, 5], slice(1, None), [2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], slice(None, -1), [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], slice(-1, None), [5]),
        ([1, 2, 3, 4, 5], slice(1, -1), [2, 3, 4]),
        ([1, 2, 3, 4, 5], slice(1, -1, 2), [2, 4]),
    ]

    @ddt.idata(data_builtin_getitem)
    @ddt.unpack
    def test_builtin_getitem(self, data, item, expect):
        actual = seq(data)[item]
        self.assertEqual(actual.data, expect)

    def test_builtin_getitem__unsupported_index_type(self):
        with self.assertRaises(ValueError):
            seq([])[object()]

    data_builtin_len = [
        ([], 0),
        ([0], 1),
        ([1, 2, 3, 4, 5], 5),
    ]

    @ddt.idata(data_builtin_len)
    @ddt.unpack
    def test_builtin_len(self, data, expect):
        actual = len(seq(data))
        self.assertEqual(actual, expect)

    data_builtin_contains = [
        ([], 0, False),
        ([0], 0, True),
        ([0], -1, False),
        ([1, 2, 3, 4, 5], 0, False),
        ([1, 2, 3, 4, 5], 1, True),
        ([1, 2, 3, 4, 5], -1, False),
    ]

    @ddt.idata(data_builtin_contains)
    @ddt.unpack
    def test_builtin_contains(self, data, item, expect):
        actual = item in seq(data)
        self.assertEqual(actual, expect)

    data_builtin_iter = [
        ([], []),
        ([0], [0]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_builtin_iter)
    @ddt.unpack
    def test_builtin_iter(self, data, expect):
        actual = list(x for x in seq(data))
        self.assertEqual(actual, expect)

    data_builtin_reversed = [
        ([], []),
        ([0], [0]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
    ]

    @ddt.idata(data_builtin_reversed)
    @ddt.unpack
    def test_builtin_reversed(self, data, expect):
        actual = list(x for x in reversed(seq(data)))
        self.assertEqual(actual, expect)

    data_count = [
        ([], 0, 0),
        ([0], 0, 1),
        ([0], -1, 0),
        ([0, 0, 0], 0, 3),
        ([0, 0, 0], -1, 0),
        ([1, 2, 3, 4, 5], 0, 0),
        ([1, 2, 3, 4, 5], 1, 1),
        ([1, 2, 3, 4, 5], -1, 0),
    ]

    @ddt.idata(data_count)
    @ddt.unpack
    def test_count(self, data, item, expect):
        actual = seq(data).count(item)
        self.assertEqual(actual, expect)

    data_count_if = [
        ([], lambda x: True, 0),
        ([0], lambda x: True, 1),
        ([0], lambda x: False, 0),
        ([0], lambda x: x % 2 == 0, 1),
        ([0], lambda x: x % 2 == 1, 0),
        ([0, 0, 0], lambda x: True, 3),
        ([0, 0, 0], lambda x: False, 0),
        ([0, 0, 0], lambda x: x % 2 == 0, 3),
        ([0, 0, 0], lambda x: x % 2 == 1, 0),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 0, 2),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 1, 3),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 0, 6),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 1, 9),
    ]

    @ddt.idata(data_count_if)
    @ddt.unpack
    def test_count_if(self, data, func, expect):
        actual = seq(data).count_if(func)
        self.assertEqual(actual, expect)

    data_take_left = [
        ([], 0, []),
        ([], 1, []),
        ([0], 0, []),
        ([0], 1, [0]),
        ([0], 2, [0]),
        ([1, 2, 3, 4, 5], 0, []),
        ([1, 2, 3, 4, 5], 1, [1]),
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 6, [1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_take_left)
    @ddt.unpack
    def test_take_left(self, data, n, expect):
        actual = seq(data).take_left(n)
        self.assertEqual(actual.data, expect)

    data_take_right = [
        ([], 0, []),
        ([], 1, []),
        ([0], 0, []),
        ([0], 1, [0]),
        ([0], 2, [0]),
        ([1, 2, 3, 4, 5], 0, []),
        ([1, 2, 3, 4, 5], 1, [5]),
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 6, [1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_take_right)
    @ddt.unpack
    def test_take_right(self, data, n, expect):
        actual = seq(data).take_right(n)
        self.assertEqual(actual.data, expect)

    data_reverse = [
        ([], []),
        ([0], [0]),
        ([0, 0, 0], [0, 0, 0]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
    ]

    @ddt.idata(data_reverse)
    @ddt.unpack
    def test_reverse(self, data, expect):
        actual = seq(data).reverse()
        self.assertEqual(actual.data, expect)

    data_distinct = [
        ([], []),
        ([0], [0]),
        ([0, 0, 0], [0]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5, 1, 2, 3, 4, 1, 2, 3, 1, 2, 1], [1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_distinct)
    @ddt.unpack
    def test_distinct(self, data, expect):
        actual = seq(data).distinct()
        self.assertEqual(actual.data, expect)

    data_scan_left = [
        ([], 0, lambda x, y: x, []),
        ([], None, lambda x, y: x, []),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [2, 4, 7, 11, 16]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [1, 2, 6, 24, 120]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [1, 12, 123, 1234, 12345]),
    ]

    @ddt.idata(data_scan_left)
    @ddt.unpack
    def test_scan_left(self, data, zero, func, expect):
        actual = seq(data).scan_left(zero, func)
        self.assertEqual(actual.data, expect)

    data_scan_right = [
        ([], 0, lambda x, y: x, []),
        ([], None, lambda x, y: x, []),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [16, 15, 13, 10, 6]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [120, 120, 60, 20, 5]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [54321, 5432, 543, 54, 5]),
    ]

    @ddt.idata(data_scan_right)
    @ddt.unpack
    def test_scan_right(self, data, zero, func, expect):
        actual = seq(data).scan_right(zero, func)
        self.assertEqual(actual.data, expect)

    data_map = [
        ([], lambda x: x, []),
        ([0], lambda x: x, [0]),
        ([1, 2, 3, 4, 5], lambda x: x * 2, [2, 4, 6, 8, 10]),
        ([1, 2, 3, 4, 5], lambda x: x ** 2, [1, 4, 9, 16, 25]),
    ]

    @ddt.idata(data_map)
    @ddt.unpack
    def test_map(self, data, func, expect):
        actual = seq(data).map(func)
        self.assertEqual(actual.data, expect)

    data_fold_left = [
        ([], 0, lambda x, y: x, [0]),
        ([], None, lambda x, y: x, []),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [16]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [120]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [12345]),
    ]

    @ddt.idata(data_fold_left)
    @ddt.unpack
    def test_fold_left(self, data, zero, func, expect):
        actual = seq(data).fold_left(zero, func)
        self.assertEqual(actual.data, expect)

    data_fold_right = [
        ([], 0, lambda x, y: x, [0]),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [16]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [120]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [54321]),
    ]

    @ddt.idata(data_fold_right)
    @ddt.unpack
    def test_fold_right(self, data, zero, func, expect):
        actual = seq(data).fold_right(zero, func)
        self.assertEqual(actual.data, expect)

    data_reduce = [
        ([], lambda x, y: x, []),
        ([0], lambda x, y: x + y, [0]),
        ([1, 2, 3, 4, 5], lambda x, y: x + y, [15]),
        ([1, 2, 3, 4, 5], lambda x, y: y, [5]),
    ]

    @ddt.idata(data_reduce)
    @ddt.unpack
    def test_reduce(self, data, func, expect):
        actual = seq(data).reduce(func)
        self.assertEqual(actual.data, expect)

    data_max = [
        ([], None, []),
        ([0], None, [0]),
        ([1, 2, 3, 4, 5], None, [5]),
        ([1, 2, 3, 4, 5], lambda x, y: True, [1]),
        ([1, 2, 3, 4, 5], lambda x, y: False, [5]),
    ]

    @ddt.idata(data_max)
    @ddt.unpack
    def test_max(self, data, func, expect):
        actual = seq(data).max(func)
        self.assertEqual(actual.data, expect)

    data_min = [
        ([], None, []),
        ([0], None, [0]),
        ([1, 2, 3, 4, 5], None, [1]),
        ([1, 2, 3, 4, 5], lambda x, y: True, [1]),
        ([1, 2, 3, 4, 5], lambda x, y: False, [5]),
    ]

    @ddt.idata(data_min)
    @ddt.unpack
    def test_min(self, data, func, expect):
        actual = seq(data).min(func)
        self.assertEqual(actual.data, expect)

    data_group = [
        ([], lambda x: x % 2, []),
        ([0], lambda x: x % 2, [(0, [0])]),
        ([1, 2, 3, 4, 5], lambda x: x % 2, [(0, [2, 4]), (1, [1, 3, 5])]),
        ([1, 2, 3, 4, 5], lambda x: x * 2, [(2, [1]), (4, [2]), (6, [3]), (8, [4]), (10, [5])]),
    ]

    @ddt.idata(data_group)
    @ddt.unpack
    def test_group(self, data, func, expect):
        actual = seq(data).group(func)
        self.assertEqual(actual.data, expect)

    data_keys = [
        ([], []),
        ([(0, "")], [0]),
        ([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")], [1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_keys)
    @ddt.unpack
    def test_keys(self, data, expect):
        actual = seq(data).keys()
        self.assertEqual(actual.data, expect)

    data_values = [
        ([], []),
        ([(0, "")], [""]),
        ([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")], ["a", "b", "c", "d", "e"]),
    ]

    @ddt.idata(data_values)
    @ddt.unpack
    def test_values(self, data, expect):
        actual = seq(data).values()
        self.assertEqual(actual.data, expect)

    data_swap = [
        ([], []),
        ([(0, "")], [("", 0)]),
        ([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")], [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]),
    ]

    @ddt.idata(data_swap)
    @ddt.unpack
    def test_swap(self, data, expect):
        actual = seq(data).swap()
        self.assertEqual(actual.data, expect)

    data_map_keys = [
        ([], lambda x: x, []),
        ([(0, "0")], lambda x: x * 2, [(0, "0")]),
        ([(0, "0")], str, [("0", "0")]),
        (
            [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
            lambda x: x * 2,
            [(2, "1"), (4, "2"), (6, "3"), (8, "4"), (10, "5")],
        ),
        (
            [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
            str,
            [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
        ),
    ]

    @ddt.idata(data_map_keys)
    @ddt.unpack
    def test_map_keys(self, data, func, expect):
        actual = seq(data).map_keys(func)
        self.assertEqual(actual.data, expect)

    data_map_values = [
        ([], lambda x: x, []),
        ([(0, "0")], lambda x: x * 2, [(0, "00")]),
        ([(0, "0")], int, [(0, 0)]),
        (
            [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
            lambda x: x * 2,
            [(1, "11"), (2, "22"), (3, "33"), (4, "44"), (5, "55")],
        ),
        (
            [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
            int,
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        ),
    ]

    @ddt.idata(data_map_values)
    @ddt.unpack
    def test_map_values(self, data, func, expect):
        actual = seq(data).map_values(func)
        self.assertEqual(actual.data, expect)

    data_flat_map = [
        ([], lambda x: x, []),
        ([[]], lambda x: x, []),
        ([[0]], lambda x: x, [0]),
        ([[1, 2, 3, 4, 5]], lambda x: x, [1, 2, 3, 4, 5]),
        ([[], [1], [2], [3], [4], [5], []], lambda x: x, [1, 2, 3, 4, 5]),
        ([[], [1, 2, 3, 4, 5], []], lambda x: x, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], lambda x: list(range(x)), [0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 4]),
    ]

    @ddt.idata(data_flat_map)
    @ddt.unpack
    def test_flat_map(self, data, func, expect):
        actual = seq(data).flat_map(func)
        self.assertEqual(actual.data, expect)

    data_flatten = [
        ([], []),
        ([[]], []),
        ([[0]], [0]),
        ([[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5]),
        ([[], [1], [2], [3], [4], [5], []], [1, 2, 3, 4, 5]),
        ([[], [1, 2, 3, 4, 5], []], [1, 2, 3, 4, 5]),
    ]

    @ddt.idata(data_flatten)
    @ddt.unpack
    def test_flatten(self, data, expect):
        actual = seq(data).flatten()
        self.assertEqual(actual.data, expect)

    data_group_map = [
        ([], lambda x: x % 2, lambda x: x ** 2, []),
        ([0], lambda x: x % 2, lambda x: x ** 2, [(0, [0])]),
        ([1, 2, 3, 4, 5], lambda x: x % 2, lambda x: x ** 2, [(0, [4, 16]), (1, [1, 9, 25])]),
        ([1, 2, 3, 4, 5], lambda x: x, lambda x: x ** 2, [(1, [1]), (2, [4]), (3, [9]), (4, [16]), (5, [25])]),
    ]

    @ddt.idata(data_group_map)
    @ddt.unpack
    def test_group_map(self, data, group_func, map_func, expect):
        actual = seq(data).group_map(group_func, map_func)
        self.assertEqual(actual.data, expect)

    data_filter = [
        ([], lambda x: True, []),
        ([0], lambda x: True, [0]),
        ([0], lambda x: False, []),
        ([0], lambda x: x % 2 == 0, [0]),
        ([0], lambda x: x % 2 == 1, []),
        ([0, 0, 0], lambda x: True, [0, 0, 0]),
        ([0, 0, 0], lambda x: False, []),
        ([0, 0, 0], lambda x: x % 2 == 0, [0, 0, 0]),
        ([0, 0, 0], lambda x: x % 2 == 1, []),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 0, [2, 4]),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 1, [1, 3, 5]),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 0, [2, 2, 4, 4, 4, 4]),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 1, [1, 3, 3, 3, 5, 5, 5, 5, 5]),
    ]

    @ddt.idata(data_filter)
    @ddt.unpack
    def test_filter(self, data, func, expect):
        actual = seq(data).filter(func)
        self.assertEqual(actual.data, expect)

    data_filter_not = [
        ([], lambda x: True, []),
        ([0], lambda x: True, []),
        ([0], lambda x: False, [0]),
        ([0], lambda x: x % 2 == 0, []),
        ([0], lambda x: x % 2 == 1, [0]),
        ([0, 0, 0], lambda x: True, []),
        ([0, 0, 0], lambda x: False, [0, 0, 0]),
        ([0, 0, 0], lambda x: x % 2 == 0, []),
        ([0, 0, 0], lambda x: x % 2 == 1, [0, 0, 0]),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 0, [1, 3, 5]),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 1, [2, 4]),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 0, [1, 3, 3, 3, 5, 5, 5, 5, 5]),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 1, [2, 2, 4, 4, 4, 4]),
    ]

    @ddt.idata(data_filter_not)
    @ddt.unpack
    def test_filter_not(self, data, func, expect):
        actual = seq(data).filter_not(func)
        self.assertEqual(actual.data, expect)

    data_sort = [
        ([], lambda x: x, []),
        ([0], lambda x: x, [0]),
        ([0, 0, 0], lambda x: x, [0, 0, 0]),
        ([1, 2, 3, 4, 5], lambda x: x, [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], lambda x: x, [1, 2, 3, 4, 5]),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x, [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]),
        ([1, 2, 3, 4, 5, 2, 3, 4, 5, 3, 4, 5, 4, 5, 5], lambda x: x, [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]),
        ([1, 2, 3, 4, 5, 2, 3, 4, 5, 3, 4, 5, 4, 5, 5], lambda x: -x, [5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 2, 2, 1]),
    ]

    @ddt.idata(data_sort)
    @ddt.unpack
    def test_sort(self, data, func, expect):
        actual = (seq(data).sort(func))
        self.assertEqual(actual.data, expect)

    data_zip = [
        ([], [], []),
        ([0], [], []),
        ([], [0], []),
        ([0], [0], [(0, 0)]),
        ([0, 0], [0], [(0, 0)]),
        ([0], [0, 0], [(0, 0)]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1)]),
        ([1, 2, 3, 4, 5], ["a", "b", "c", "d", "e"], [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]),
        (["a", "b", "c", "d", "e"], [1, 2, 3, 4, 5], [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]),
    ]

    @ddt.idata(data_zip)
    @ddt.unpack
    def test_zip(self, a, b, expect):
        actual = seq(a).zip(seq(b))
        self.assertEqual(actual.data, expect)

    data_zip_fill = [
        ([], [], 0, []),
        ([0], [], None, [(0, None)]),
        ([0], [], 1, [(0, 1)]),
        ([], [0], None, [(None, 0)]),
        ([], [0], 1, [(1, 0)]),
        ([0], [0], 0, [(0, 0)]),
        ([0, 0], [0], None, [(0, 0), (0, None)]),
        ([0, 0], [0], 1, [(0, 0), (0, 1)]),
        ([0], [0, 0], None, [(0, 0), (None, 0)]),
        ([0], [0, 0], 1, [(0, 0), (1, 0)]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], None, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], None, [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1)]),
        ([1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5], 0, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 0), (7, 0)]),
        ([1, 2, 3, 4, 5, 6, 7], [5, 4, 3, 2, 1], 0, [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0), (7, 0)]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7], 0, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (0, 6), (0, 7)]),
        ([1, 2, 3, 4, 5], [7, 6, 5, 4, 3, 2, 1], 0, [(1, 7), (2, 6), (3, 5), (4, 4), (5, 3), (0, 2), (0, 1)]),
        ([1, 2, 3, 4, 5], ["a", "b", "c", "d", "e"], None, [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]),
        (["a", "b", "c", "d", "e"], [1, 2, 3, 4, 5], None, [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]),
        (
            [1, 2, 3, 4, 5],
            ["a", "b", "c", "d", "e", "f", "g"],
            0,
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), (0, "f"), (0, "g")],
        ),
        (
            [1, 2, 3, 4, 5],
            ["a", "b", "c", "d", "e", "f", "g"],
            "-",
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), ("-", "f"), ("-", "g")],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            ["a", "b", "c", "d", "e"],
            "-",
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), (6, "-"), (7, "-")],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            ["a", "b", "c", "d", "e"],
            0,
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), (6, 0), (7, 0)],
        ),
    ]

    @ddt.idata(data_zip_fill)
    @ddt.unpack
    def test_zip_fill(self, a, b, fill, expect):
        actual = seq(a).zip_fill(seq(b), fill)
        self.assertEqual(actual.data, expect)

    def test_naming_seq(self):
        names = [
            ("Andrew", "M"),
            ("Alice", "W"),
            ("Benjamin", "M"),
            ("Bella", "W"),
            ("Charles", "M"),
            ("Charlotte", "W"),
            ("Daniel", "M"),
            ("Diana", "W"),
            ("Ethan", "M"),
            ("Emily", "W"),
            ("Felix", "M"),
            ("Fiona", "W"),
            ("George", "M"),
            ("Grace", "W"),
            ("Henry", "M"),
            ("Hannah", "W"),
            ("Isaac", "M"),
            ("Isabella", "W"),
            ("Jacob", "M"),
            ("Julia", "W"),
            ("Kevin", "M"),
            ("Katherine", "W"),
            ("Liam", "M"),
            ("Lily", "W"),
            ("Michael", "M"),
            ("Madison", "W"),
            ("Nathan", "M"),
            ("Natalie", "W"),
            ("Oliver", "M"),
            ("Olivia", "W"),
            ("Patrick", "M"),
            ("Penelope", "W"),
            ("Quentin", "M"),
            ("Quinn", "W"),
            ("Ryan", "M"),
            ("Rebecca", "W"),
            ("Samuel", "M"),
            ("Sophia", "W"),
            ("Thomas", "M"),
            ("Tiffany", "W"),
            ("Ulysses", "M"),
            ("Ursula", "W"),
            ("Victor", "M"),
            ("Victoria", "W"),
            ("William", "M"),
            ("Wendy", "W"),
            ("Xavier", "M"),
            ("Xenia", "W"),
            ("Yosef", "M"),
            ("Yvonne", "W"),
            ("Zachary", "M"),
            ("Zoe", "W"),
        ]
        naming_seq = NamingSeq(Naming(serial, name, gender) for serial, (name, gender) in enumerate(names))

        self.assertEqual(naming_seq, naming_seq)
        self.assertEqual(naming_seq.concat(naming_seq).axis(), list(range(0, 52)) + list(range(0, 52)))
        self.assertEqual(naming_seq.take_left(26).axis(), list(range(0, 26)))
        self.assertEqual(naming_seq.take_right(26).axis(), list(range(26, 52)))
        self.assertEqual(naming_seq.reverse().axis(), list(reversed(range(0, 52))))
        self.assertEqual(naming_seq.distinct().axis(), list(range(0, 52)))
        self.assertEqual(naming_seq.reduce(lambda x, y: x).axis(), [0])
        self.assertEqual(naming_seq.reduce(lambda x, y: y).axis(), [51])
        self.assertEqual(naming_seq.min(lambda x, y: x.serial < y.serial).axis(), [0])
        self.assertEqual(naming_seq.max(lambda x, y: x.serial > y.serial).axis(), [51])
        self.assertEqual(naming_seq.filter(lambda x: x.gender == "M").axis(), list(range(0, 52, 2)))
        self.assertEqual(naming_seq.filter(lambda x: x.gender == "W").axis(), list(range(1, 52, 2)))
        self.assertEqual(naming_seq.filter_not(lambda x: x.gender == "M").axis(),
                         naming_seq.filter(lambda x: x.gender == "W").axis())
        self.assertEqual(naming_seq.filter_not(lambda x: x.gender == "W").axis(),
                         naming_seq.filter(lambda x: x.gender == "M").axis())
        self.assertEqual(naming_seq.sort(lambda x: -x.serial).axis(), naming_seq.reverse().axis())
        self.assertEqual(naming_seq.head().axis(), [0])
        self.assertEqual(naming_seq.last().axis(), [51])
        self.assertEqual(naming_seq.init().axis(), list(range(0, 51)))
        self.assertEqual(naming_seq.tail().axis(), list(range(1, 52)))
        self.assertEqual(naming_seq.foreach(lambda x: x).data, naming_seq.data)
        self.assertEqual(naming_seq.union(naming_seq).data, naming_seq.data)
        self.assertEqual(naming_seq.intersect(naming_seq).data, naming_seq.data)

        self.assertEqual(naming_seq.scan_left(0, lambda x, y: x + y.serial).data,
                         seq(range(0, 52)).scan_left(0, lambda x, y: x + y).data)
        self.assertEqual(naming_seq.scan_right(0, lambda x, y: x + y.serial).data,
                         seq(range(0, 52)).scan_right(0, lambda x, y: x + y).data)
        self.assertEqual(naming_seq.map(lambda x: x.serial).data, list(range(0, 52)))

        self.assertEqual(naming_seq.fold_left(0, lambda x, y: x + y.serial).data,
                         seq(range(0, 52)).fold_left(0, lambda x, y: x + y).data)
        self.assertEqual(naming_seq.fold_right(0, lambda x, y: x + y.serial).data,
                         seq(range(0, 52)).fold_right(0, lambda x, y: x + y).data)

        self.assertEqual(naming_seq.group(lambda x: x.serial % 2).size, 2)
        self.assertEqual(naming_seq.group(lambda x: x.gender).size, 2)
        self.assertEqual(naming_seq.group(lambda x: x.name[0]).size, 26)
