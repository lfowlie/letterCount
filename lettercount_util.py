"""
Generic util file for functions that may be used in disparate parts of the application.
"""


def calculate_substring_count_in_string_list(substr, str_list):
    """
    Calculates and returns the number of times a substring appears in a list of strings.
    :param str substr: substring to search list for
    :param list str_list: list of strings
    :rtype int
    """
    if substr == '' or str_list == []:
        return 0

    count = 0
    for item in str_list:
        count += item.count(substr)

    return count
