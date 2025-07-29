#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This module implements a hexadecimal reader.
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

r"""
This module implements a hexadecimal reader.

~# python3 -m doctest -v HexaReader.py

2 items had no tests:
    HexaReader.HexaReader.__init__
    HexaReader.main
4 items passed all tests:
   3 tests in HexaReader
   3 tests in HexaReader.HexaReader
   2 tests in HexaReader.HexaReader.get_line
   3 tests in HexaReader.HexaReader.reader
11 tests in 6 items.
11 passed and 0 failed.
Test passed.

>>> from io import BytesIO
>>> hexareader = HexaReader(BytesIO(bytes(range(256))))
>>> for line in hexareader.reader(): print(line)
00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f   ................
10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f   ................
20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f    !"#$%&'()*+,-./
30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f   0123456789:;<=>?
40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f   @ABCDEFGHIJKLMNO
50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f   PQRSTUVWXYZ[\]^_
60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f   `abcdefghijklmno
70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f   pqrstuvwxyz{|}~.
80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f   ................
90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f   ................
a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af   ................
b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf   ................
c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf   ................
d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df   ................
e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef   ................
f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff   ................
>>> 
"""

__version__ = "3.0.4"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This module implements a hexadecimal reader.
"""
__url__ = "https://github.com/mauricelambert/BinaryFileReader"

__all__ = ["HexaReader", "colors", "main"]

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

from typing import Iterator, Dict, Callable
from sys import argv, exit, stderr
from _io import _BufferedIOBase
from binascii import hexlify
from os.path import exists

from PythonToolsKit.WindowsTerminal import (
    active_virtual_terminal,
    desactive_virtual_terminal,
)
from PythonToolsKit.Terminal import char_ANSI, COLORS_MODES, colors_map, COLORS

base_color = char_ANSI + COLORS_MODES.FGCOLOR1.value


colors: Dict[str, str] = {
    "abcdefghijklmnopqrstuvwxyzABCDEFIJKLMNOPQRSTUVWXYZ": "GREEN",
    "0123456789": "CYAN",
    " !\"#$%&'()*+,-./:;<=>?[\\]^_{|}~`": "YELLOW",
    "\0": "BLUE",
}


class HexaReader:
    r"""
    This class implements a hexadecimal reader.

    >>> from io import BytesIO
    >>> hexareader = HexaReader(BytesIO(bytes(range(256))))
    >>> for line in hexareader.reader(): print(line)
    00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f   ................
    10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f   ................
    20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f    !"#$%&'()*+,-./
    30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f   0123456789:;<=>?
    40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f   @ABCDEFGHIJKLMNO
    50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f   PQRSTUVWXYZ[\]^_
    60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f   `abcdefghijklmno
    70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f   pqrstuvwxyz{|}~.
    80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f   ................
    90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f   ................
    a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af   ................
    b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf   ................
    c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf   ................
    d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df   ................
    e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef   ................
    f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff   ................
    >>>
    """

    def __init__(
        self,
        file: _BufferedIOBase,
        size: int = 16,
        ascii: bool = True,
        colors: Dict[str, str] = None,
    ):
        self.file = file
        self.size = size
        self.ascii = ascii
        self.colors = (
            {
                x: color.upper()
                for chars, color in colors.items()
                for x in chars.encode()
            }
            if colors
            else None
        )
        self.default_color = base_color + COLORS.RED.value
        self.reset = char_ANSI + COLORS.BLACK.value

    def reader(self) -> Iterator[str]:
        r"""
        This method read file 16 chars by 16 chars and yield lines.

        >>> from io import BytesIO
        >>> hexareader = HexaReader(BytesIO(bytes(range(256))))
        >>> for line in hexareader.reader(): print(line)
        00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f   ................
        10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f   ................
        20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f    !"#$%&'()*+,-./
        30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f   0123456789:;<=>?
        40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f   @ABCDEFGHIJKLMNO
        50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f   PQRSTUVWXYZ[\]^_
        60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f   `abcdefghijklmno
        70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f   pqrstuvwxyz{|}~.
        80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f   ................
        90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f   ................
        a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af   ................
        b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf   ................
        c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf   ................
        d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df   ................
        e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef   ................
        f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff   ................
        >>>
        """

        data = True
        process_line = self.get_line_processor()
        read = self.file.read
        size = self.size

        while data:
            if data := read(size):
                yield process_line(data)

    def get_line_processor(self) -> Callable:
        """
        This method return hexareader line from bytes.

        >>> hexareader = HexaReader(None)
        >>> hexareader.get_line_processor()(bytes(range(50, 66)))
        '32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f 40 41   23456789:;<=>?@A'
        >>>
        """

        if self.colors is None and not self.ascii:
            return (
                lambda x: hexlify(x, " ").ljust((self.size * 3) + 2).decode()
            )

        def process_line_color(data):
            hex_out = ""
            ascii_out = ""
            for char in data:
                if char in self.colors:
                    color = colors_map[self.colors[char]].value
                    hex_out += f"{base_color}{color}{char:0>2X}{self.reset} "
                    ascii_out += (
                        base_color
                        + color
                        + (chr(char) if 32 <= char <= 126 else ".")
                        + self.reset
                    )
                else:
                    hex_out += f"{self.default_color}{char:0>2X}{self.reset} "
                    ascii_out += self.default_color + "." + self.reset
            return (
                hex_out
                + " " * (((self.size - int(len(hex_out) / 12)) * 3) + 2)
                + ascii_out
            )

        def process_line(data):
            hexa = hexlify(data, " ").ljust((self.size * 3) + 2)
            ascii_ = bytes([x if 32 <= x <= 126 else 46 for x in data])
            return (hexa + ascii_).decode()

        return process_line_color if self.colors else process_line


def main() -> int:
    """
    This function runs the module from command line.
    """

    print_usages = lambda: print(
        "USAGE: python3 HexaReader.py filename [-c/--color/--no-color]"
        " ([-s/--size/--line-size] size)",
        file=stderr,
    )

    def get_size(position):
        del argv[position]
        if len(argv) <= position or not argv[position].isdigit():
            print("invalid size")
            print_usages()
            return 3
        value = int(argv[position])
        del argv[position]
        return value

    color = True
    if "-c" in argv:
        argv.remove("-c")
        color = False
    elif "--color" in argv:
        argv.remove("--color")
        color = False
    elif "--no-color" in argv:
        argv.remove("--no-color")
        color = False

    size = 16
    if "-s" in argv:
        size = get_size(argv.index("-s"))
    elif "--size" in argv:
        size = get_size(argv.index("--size"))
    elif "--line-size" in argv:
        size = get_size(argv.index("--line-size"))

    if len(argv) != 2:
        print_usages()
        return 1
    elif not exists(argv[1]):
        print(f"ERROR: file {argv[1]} doesn't exist.", file=stderr)
        return 2

    active_virtual_terminal()

    with open(argv[1], "rb") as file:
        hexareader = HexaReader(file, size, True, colors if color else None)
        for line in hexareader.reader():
            print(line)

    desactive_virtual_terminal()
    return 0


if __name__ == "__main__":
    exit(main())
