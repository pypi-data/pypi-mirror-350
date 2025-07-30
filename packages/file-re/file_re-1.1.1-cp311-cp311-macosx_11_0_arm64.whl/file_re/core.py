from pathlib import Path
from typing import Union, List
from ._file_re import (
    _search_single_line,
    _search_multi_line,
    _findall_single_line,
    _findall_multi_line,
    _search_with_num_lines,
    _findall_with_num_lines,
)
from .match import Match


class file_re_cls:

    @staticmethod
    def search(
        regex: str, file_path: Union[str, Path], multiline: bool = False, num_lines: int = None
    ) -> Match:
        """
        Search the first occurrence of the regex in the file.

        Args:
            regex (str): The regular expression pattern to search for. This should be
                a valid regex pattern supported by the `re` module.
            file_path (Union[str, Path]): The path to the file, provided as either a
                string or a Path object. The file will be read, and the regex applied
                to its content.
            multiline (bool, optional): If True, allows the regex to match across
                multiple lines. Defaults to False.
            num_lines (int, optional): Maximum number of lines the regex can span.
                When specified, uses a FIFO queue approach to find the last/longest match
                within the line limit. If None, uses standard multiline behavior.

        Returns:
            Match: A Match object containing information about the match, or None if
            no match is found.
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)

        if num_lines is not None:
            result = _search_with_num_lines(regex, file_path, num_lines)
        elif multiline is True:
            result = _search_multi_line(regex, file_path)
        else:
            result = _search_single_line(regex, file_path)

        match = None
        if result:

            match = Match(
                match_str=result.match_str,
                start=result.start,
                end=result.end,
                matchs_list=result.groups,
                matchs_dict=result.named_groups,
            )

        return match

    @staticmethod
    def findall(
        regex: str, file_path: Union[str, Path], multiline: bool = False, num_lines: int = None
    ) -> List:
        """
        Find all occurrences of the regex in the file.

        Args:
            regex (str): The regular expression pattern to search for. The pattern must be
                a valid regex expression supported by the `re` module.
            file_path (Union[str, Path]): The path to the file, as either a string or
                a Path object. The file will be read and the regex applied to its content.
            multiline (bool, optional): If True, allows the regex to match across
                multiple lines. Defaults to False.
            num_lines (int, optional): Maximum number of lines the regex can span.
                When specified, uses a FIFO queue approach to find all matches
                within the line limit. If None, uses standard multiline behavior.

        Returns:
            list: A list of tuples containing all matches found. If there are multiple
            capturing groups, each match is a tuple containing the groups. If there is
            only one capturing group, the list contains strings representing the matches.
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)

        if num_lines is not None:
            match_list = _findall_with_num_lines(regex, file_path, num_lines)
        elif multiline:
            match_list = _findall_multi_line(regex, file_path)
        else:
            match_list = _findall_single_line(regex, file_path)

        if match_list:
            if len(match_list[0]) == 1:
                match_list = [item for sublist in match_list for item in sublist]
            else:
                match_list = [tuple(sublist[1:]) for sublist in match_list]

        return match_list
