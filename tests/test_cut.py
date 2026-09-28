import unittest

from mincut.cut import CutError, global_min_cut, parse_edges


class ParseTest(unittest.TestCase):
    def test_two_edges(self):
        self.assertEqual(parse_edges("a-b:1,b-c:2"), [("a", "b", 1), ("b", "c", 2)])

    def test_missing_capacity(self):
        with self.assertRaises(CutError):
            parse_edges("a-b")

    def test_missing_dash(self):
        with self.assertRaises(CutError):
            parse_edges("ab:1")


class CutTest(unittest.TestCase):
    def test_two_nodes(self):
        capacity, side = global_min_cut(parse_edges("a-b:3"))
        self.assertEqual(capacity, 3)
        self.assertEqual(len(side), 1)

    def test_single_node(self):
        capacity, side = global_min_cut(parse_edges("a-a:9"))
        self.assertEqual(capacity, 0)
        self.assertEqual(side, [])

    def test_triangle(self):
        capacity, side = global_min_cut(parse_edges("a-b:4,b-c:4,c-a:4"))
        self.assertEqual(capacity, 8)
        self.assertEqual(len(side), 1)

    def test_side_is_sorted(self):
        _, side = global_min_cut(parse_edges("b-a:1,c-b:1"))
        self.assertEqual(side, sorted(side))

    def test_empty(self):
        self.assertEqual(global_min_cut([]), (0, []))


if __name__ == "__main__":
    unittest.main()
