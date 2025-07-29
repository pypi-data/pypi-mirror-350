#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file exports strings from binary file.
#    Copyright (C) 2021, 2025  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This file exports strings from binary file.

~# python3 -m doctest -v Strings.py

2 items had no tests:
    Strings.Strings.__init__
    Strings.main
4 items passed all tests:
   5 tests in Strings
   5 tests in Strings.Strings
  22 tests in Strings.Strings.analyse_character
   5 tests in Strings.Strings.reader
37 tests in 6 items.
37 passed and 0 failed.
Test passed.

>>> from io import BytesIO
>>> strings = Strings(BytesIO(b"\\x00\\x01abcde\\x00ghijk\\x01lmnopqrst\\x00"))
>>> for line in strings.reader(): print(line)
abcde
lmnopqrst
>>> strings = Strings(BytesIO(b"\\x00\\x01abcde\\x00ghijk\\x01lmnopqrst\\x00"), null_terminated=False)
>>> for line in strings.reader(): print(line)
abcde
ghijk
lmnopqrst
>>> 
"""

__version__ = "3.0.4"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This file exports strings from binary file.
"""
__url__ = "https://github.com/mauricelambert/BinaryFileReader"

__all__ = ["Strings", "main"]

__license__ = "GPL-3.0 License"
__copyright__ = """
BinaryFileReader  Copyright (C) 2021, 2025  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
copyright = __copyright__
license = __license__

print(copyright)

from argparse import ArgumentParser, Namespace
from typing import Iterator, Tuple
from _io import _BufferedIOBase


class Strings:
    """
    This class exports strings from binary file.

    >>> from io import BytesIO
    >>> strings = Strings(BytesIO(b"\\x00\\x01abcde\\x00ghijk\\x01lmnopqrst\\x00"))
    >>> for line in strings.reader(): print(line)
    abcde
    lmnopqrst
    >>> strings = Strings(BytesIO(b"\\x00\\x01abcde\\x00ghijk\\x01lmnopqrst\\x00"), null_terminated=False)
    >>> for line in strings.reader(): print(line)
    abcde
    ghijk
    lmnopqrst
    >>>
    """

    def __init__(
        self,
        file: _BufferedIOBase,
        minimum_length: int = 5,
        null_terminated: bool = True,
    ):
        self.file = file
        self.minimum_length = minimum_length
        self.current_string: str = ""
        self.current_unicode_string: str = ""
        self.null_terminated = null_terminated
        self._temp_unicode_char = None

    def reader(self) -> Iterator[str]:
        """
        This method reads character after character and yield strings.

        >>> from io import BytesIO
        >>> strings = Strings(BytesIO(b"\\x00\\x01abcde\\x00ghijk\\x01lmnopqrst\\x00"))
        >>> for line in strings.reader(): print(line)
        abcde
        lmnopqrst
        >>> strings = Strings(BytesIO(b"\\x00\\x01abcde\\x00ghijk\\x01lmnopqrst\\x00"), null_terminated=False)
        >>> for line in strings.reader(): print(line)
        abcde
        ghijk
        lmnopqrst
        >>>
        """

        char = self.file.read(1)

        while char:
            unicode_terminated, terminated = self.analyse_character(char)

            if terminated:
                if len(self.current_string) >= self.minimum_length:
                    yield self.current_string
                self.current_string = ""

            if unicode_terminated:
                if len(self.current_unicode_string) >= self.minimum_length:
                    yield self.current_unicode_string
                self.current_unicode_string = ""

            char = self.file.read(1)

        if len(self.current_string) >= self.minimum_length:
            yield self.current_string

        if len(self.current_unicode_string) >= self.minimum_length:
            yield self.current_unicode_string

    def analyse_character(self, char: bytes) -> Tuple[bool, bool]:
        """
        This method analyses a byte and returns boolean to know when a
        string is terminated.

        >>> strings = Strings(None)
        >>> strings.analyse_character(b'a')
        (False, False)
        >>> strings.analyse_character(b'\\0')
        (False, True)
        >>> strings.current_string
        'a'
        >>> strings.analyse_character(b'\\0')
        (False, True)
        >>> strings.analyse_character(b'\\0')
        (True, True)
        >>> strings.current_unicode_string
        'a'
        >>> strings.analyse_character(b'\\1')
        (False, False)
        >>> strings.current_string
        ''
        >>> strings.current_unicode_string
        ''
        >>> strings = Strings(None, null_terminated=False)
        >>> strings.analyse_character(b'a')
        (False, False)
        >>> strings.analyse_character(b'\\0')
        (False, True)
        >>> strings.current_string
        'a'
        >>> strings.analyse_character(b'\\0')
        (False, True)
        >>> strings.analyse_character(b'\\0')
        (True, True)
        >>> strings.current_unicode_string
        'a'
        >>> strings.analyse_character(b'a')
        (False, False)
        >>> strings.analyse_character(b'\\1')
        (False, True)
        >>> strings.analyse_character(b'a')
        (False, False)
        >>> strings.analyse_character(b'\\0')
        (False, True)
        >>> strings.analyse_character(b'\\1')
        (True, True)
        >>>
        """

        char = char[0]

        if 32 <= char <= 126:
            self.current_string += chr(char)
            self._temp_unicode_char = char
            return False, False
        elif not char:

            if self._temp_unicode_char:
                self.current_unicode_string += chr(self._temp_unicode_char)
                self._temp_unicode_char = None
                return False, True
            elif self._temp_unicode_char is None:
                if self.current_unicode_string:
                    self._temp_unicode_char = char
                return False, True
            return True, True

        elif self.null_terminated:
            self.current_string = ""
            self.current_unicode_string = ""
            return False, False
        else:
            if self._temp_unicode_char:
                self._temp_unicode_char = None
                return False, True
            return True, True


def parse_arguments(parser: ArgumentParser = None) -> Namespace:
    """
    This function parses command line arguments.
    """

    if parser is None:
        parser = ArgumentParser(
            description="This script exports strings from binary file."
        )

    parser.add_argument("filename", help="Filename of binary file.")
    parser.add_argument(
        "--minimum-length",
        "--length",
        "-l",
        "-n",
        type=int,
        default=5,
        help="Minimum length to extract a string.",
    )
    parser.add_argument(
        "--non-null-terminated",
        "-t",
        default=False,
        action="store_true",
        help="Non null terminated.",
    )
    return parser.parse_args()


def main() -> int:
    """
    This function runs the module from the command line.
    """

    arguments = parse_arguments()

    with open(arguments.filename, "rb") as file:
        strings = Strings(
            file,
            minimum_length=arguments.minimum_length,
            null_terminated=not arguments.non_null_terminated,
        )

        for line in strings.reader():
            print(line)

    return 0


if __name__ == "__main__":
    exit(main())
