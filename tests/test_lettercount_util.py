from unittest import TestCase

import lettercount_util


class TestLettercountUtil(TestCase):
    def test_calculate_substring_count_in_string_list(self):
        str_list = ['pizza', 'papa john\'s', 'dog', 'cat']
        self.assertEqual(lettercount_util.calculate_substring_count_in_string_list('p', str_list), 3)

    def test_calculate_substring_count_in_string_list_empty_list(self):
        str_list = []
        self.assertEqual(lettercount_util.calculate_substring_count_in_string_list('p', str_list), 0)

    def test_calculate_substring_count_in_string_list_empty_substr(self):
        str_list = ['pizza', 'papa john\'s', 'dog', 'cat']
        self.assertEqual(lettercount_util.calculate_substring_count_in_string_list('', str_list), 0)
