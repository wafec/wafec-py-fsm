import unittest

from .list_utils import ListUtils


class ListUtilsTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_add_or_create(self):
        result = ListUtils.add_or_create(None, 10)
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result))
        self.assertEqual(10, result[0])

    def test_add_or_create_duplicate_allow_true(self):
        result = ListUtils.add_or_create(None, [10, 10], True)
        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))
        self.assertEqual(10, result[1])
        self.assertEqual(10, result[0])

    def test_add_or_create_duplicate_allow_false(self):
        result = ListUtils.add_or_create(None, [10, 10], False)
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result))
        self.assertEqual(10, result[0])

    def test_to_list(self):
        result = ListUtils.to_list(10)
        self.assertListEqual([10], result)

    def test_to_list_with_list(self):
        result = ListUtils.to_list([10, 11])
        self.assertListEqual([10, 11], result)
