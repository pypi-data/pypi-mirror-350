#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file process exported strings recursively from binary file.
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
This file process exported strings recursively from binary file.
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

__all__ = ["MagicStrings", "Result", "main"]

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

try:
    from .Strings import Strings, parse_arguments
except ImportError:
    from Strings import Strings, parse_arguments

from PythonToolsKit.PrintF import printf
from RC6Encryption import RC6Encryption
from RC4Encryption import RC4Encryption
from PegParser import formats, Format

from typing import Iterator, Tuple, List, Union, Dict, Generator
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from os.path import getsize, exists
from sys import stderr, exit
from io import BytesIO


@dataclass
class Step:
    """
    This dataclass contains a decrypting or decoding step.
    """

    mode: str
    operation: str

    def __str__(self):
        return self.operation

    def __repr__(self):
        return f"{self.mode}:{self.operation}"


@dataclass
class Result:
    """
    This dataclass contains the result for each
    exported and processed strings and matchs.
    """

    string: bytes
    format: Format
    process_level: int
    steps: List[Step] = field(default_factory=list)
    last_step_decrypt: bool = False

    def __str__(self):
        steps = ", ".join(str(x) for x in self.steps)
        return (
            f"[{self.process_level} {self.format.name}: {steps}] "
            + self.string.decode("ascii")
        )

    def __repr__(self):
        steps = ", ".join(str(x) for x in self.steps)
        return f"[{self.process_level} {self.format.name}: {steps}] " + repr(
            self.string.decode("ascii")
        )


format_string = Format(
    "string", lambda x: x, lambda x: x, lambda x: True, lambda x: False
)
step_string = Step("string", "string")
step_crypto_data = Step("crypto", "crypto data")
step_string_truncated = Step("string", "truncated")
step_crypto_string = Step("crypto", "crypto string")


class MagicStrings(Strings):
    """
    This class process exported strings recursively from binary file.
    """

    lasts: Dict[str, bytes] = {}

    def __init__(
        self,
        *args,
        process_level: int = 0,
        keys: List[Tuple[bytes, Union[None, str]]] = [],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.process_level = process_level
        self.this_lasts = {}
        self.keys = keys

    def magic(self) -> Iterator[Result]:
        """
        This method process the file.
        """

        self.steps = [step_string]
        self.last_step_decrypt = False

        yield from self.process_strings()
        return

        if not hasattr(self.file, "tell") or not hasattr(self.file, "seek"):
            return None

        if self.file.tell() <= 153600:
            self.file.seek(0)
            yield from self.process_data(self.file.read())

    def process_strings(self) -> Iterator[Result]:
        """
        This method sends each string to recursive function.
        """

        for string in self.reader():
            result = Result(
                string.encode("ascii"),
                format_string,
                self.process_level,
                self.steps,
                self.last_step_decrypt,
            )
            yield result
            yield from self.process_string(result)

    def process_string(self, result: Result) -> Iterator[Result]:
        """
        The recursive method to process each string.
        """

        first = True
        steps_crypto = result.steps.copy()
        steps_crypto.append(step_crypto_string)
        steps_truncated = result.steps.copy()
        steps_truncated.append(step_string_truncated)
        self.this_lasts.clear()

        while len(result.string) >= self.minimum_length:
            this_formats = formats.copy()
            yield from self.decode_string(
                result.string,
                result.steps,
                result.last_step_decrypt,
                this_formats,
                True,
            )

            for temp_string in self.decrypt_string(result):
                yield from self.decode_string(
                    temp_string, steps_crypto, True, this_formats
                )

            result = Result(
                result.string[1:],
                format_string,
                self.process_level,
                steps_truncated,
                result.last_step_decrypt,
            )
            if first:
                steps_crypto = result.steps.copy()
                steps_crypto.append(step_crypto_string)
                self.process_level += 1
                first = False

        if not first:
            self.process_level -= 1

    def decrypt_string(self, result: Result) -> Iterator[bytes]:
        """
        This method bruteforces a string.
        """

        if result.last_step_decrypt:
            return None

        self.process_level += 1

        for function in letters_bruteforcer:
            for key in range(1, 26):
                yield function(result.string, key)

        self.process_level -= 1

    def decode_string(
        self,
        string_encoded: bytes,
        steps: List[Step],
        last_step_decrypt: bool,
        this_formats: Dict[str, Format],
        first: bool = False,
    ) -> Iterator[Result]:
        """
        The method checks the string for all formats.
        """

        keys = set()
        for name, format in this_formats.items():
            match = format.match(string_encoded)

            if match is None or len(match) < self.minimum_length:
                continue

            try:
                data = format.decode(match)
            except Exception as e:
                continue

            if first:
                keys.add(name)

            if match in self.lasts.get(name, b"") or match in self.this_lasts.get(name, b""):
                continue

            result = Result(
                match,
                format,
                self.process_level,
                steps,
                last_step_decrypt,
            )
            yield result
            self.lasts[name] = match
            self.this_lasts[name] = match

            if data != match:
                self.process_level += 1
                temp_steps = result.steps.copy()
                temp_steps.append(Step("decode", name))
                yield from self.process_data(data, temp_steps, False)
                self.process_level -= 1

        for name in keys:
            del this_formats[name]

    @staticmethod
    def yield_if_next(
        generator: Generator, result: Result
    ) -> Iterator[Result]:
        """
        This function yields results and yields from generator
        if there is a yield in the generator.
        """

        try:
            first_element = next(generator)
        except StopIteration:
            return None

        yield result
        yield first_element
        yield from generator

    def process_data(
        self, data: bytes, steps: List[Step], last_step_decrypt: bool
    ) -> Iterator[Result]:
        """
        This method sends each data to recursive function.
        """

        first = True
        steps_crypto = steps.copy()
        steps_crypto.append(step_crypto_data)

        while len(data) >= self.minimum_length:
            yield from self.new(data, steps, last_step_decrypt)
            for decrypted in self.process_crypto(data, last_step_decrypt):
                yield from self.new(decrypted, steps_crypto, True)

            data = data[1:]
            if first:
                self.process_level += 1
                steps.append(step_string_truncated)
                steps_crypto = steps.copy()
                steps_crypto.append(step_crypto_data)
                first = False

        if not first:
            self.process_level -= 1

    def new(
        self, data: bytes, steps: List[Step], last_step_decrypt: bool
    ) -> Iterator[Result]:
        """
        This method makes a new instance of MagicStrings
        for a in depth string search.
        """

        instance = self.__class__(
            BytesIO(data),
            self.minimum_length,
            False,
            process_level=self.process_level + 1,
            keys=self.keys,
        )

        steps = steps.copy()
        steps.append(step_string)
        instance.steps = steps
        instance.last_step_decrypt = last_step_decrypt

        yield from instance.process_strings()

    def process_crypto(
        self, data: bytes, last_step_decrypt: bool
    ) -> Iterator[bytes]:
        """
        This method process data with crypto functions.
        """

        if last_step_decrypt:
            return None

        self.process_level += 1
        for key, cypher in self.keys:
            if cypher is not None:
                yield from decryptors[cypher](key)
                continue
            for decryptor in decryptors.values():
                yield from decryptor(key)

        yield from self.bruteforces(data)
        self.process_level -= 1

    def bruteforces(
        self, data: bytes, is_string: bool = False
    ) -> Iterator[bytes]:
        """
        This method bruteforces one character keys
        for small crypto functions.
        """

        for function in bytes_bruteforcer:
            for key in range(1, 256):
                yield function(data, key)


def single_add_bytes(data: bytes, key: int) -> bytes:
    """
    This function encrypts or decrypts single key
    character substitution cypher on all bytes.
    """

    if len(data) > 14:
        return bytes([(x + key) & 0xFF for x in data])

    new_data = []
    for char in data:
        decrypted_char = (char + key) & 0xFF
        if (
            decrypted_char != 10 and 32 > decrypted_char
        ) or decrypted_char > 126:
            return None
        new_data.append(decrypted_char)

    return bytes(new_data)


def single_add_letters(data: bytes, key: int) -> bytes:
    """
    This function encrypts or decrypts single key
    character substitution cypher on letters only.
    """
    return bytes(
        [
            (
                (
                    (((x + key - 97) % 26) + 97)
                    if x >= 97
                    else (((x + key - 65) % 26)) + 65
                )
                if 97 <= x <= 122 or 65 <= x <= 90
                else x
            )
            for x in data
        ]
    )


def single_xor_bytes(data: bytes, key: int) -> bytes:
    """
    This function encrypts or decrypts single key
    character xor cypher.
    """

    if len(data) > 14:
        return bytes([(x ^ key) for x in data])

    new_data = []
    for char in data:
        decrypted_char = char ^ key
        if (
            decrypted_char != 10 and 32 > decrypted_char
        ) or decrypted_char > 126:
            return None
        new_data.append(decrypted_char)

    return bytes(new_data)


def rc4_decryptor(data: bytes, key: bytes) -> bytes:
    """
    This function is the decryptor for RC4 cypher.
    """

    rc4 = RC4Encryption(key)
    rc4.make_key()
    return rc4.crypt(data)


def rc6_ecb_decryptor(data: bytes, key: bytes) -> bytes:
    """
    This function is the decryptor for RC6 cypher
    (mode ECB, no IV, not secure).
    """

    rc6 = RC6Encryption(key)
    return rc6.data_decryption_ECB(data)


bytes_bruteforcer = [single_xor_bytes, single_add_bytes]
letters_bruteforcer = [single_add_letters]
decryptors = {
    "rc4": rc4_decryptor,
    "RC4": rc4_decryptor,
    "rc6": rc6_ecb_decryptor,
    "RC6": rc6_ecb_decryptor,
}


def specific_argument_parser() -> Namespace:
    """
    This function adds specific arguments to Strings argument parser
    and return parsed arguments.
    """

    parser = ArgumentParser(
        description=(
            "This script exports strings from binary file, "
            "try to identify format, decode it and decrypt it."
        )
    )
    filters_process = parser.add_mutually_exclusive_group()
    filters_process.add_argument(
        "--process-only",
        "-p",
        default=[],
        action="extend",
        nargs="+",
        help="Process only specified formats to get match.",
    )
    filters_process.add_argument(
        "--do-not-process",
        "-d",
        default=[],
        action="extend",
        nargs="+",
        help="Don't process specified formats to get match.",
    )
    filters_print = parser.add_mutually_exclusive_group()
    filters_print.add_argument(
        "--print-only",
        "-i",
        default=[],
        action="extend",
        nargs="+",
        help="Process formats but print only specified formats.",
    )
    filters_print.add_argument(
        "--do-not-print",
        "-o",
        default=[],
        action="extend",
        nargs="+",
        help="Process formats but don't print specified formats.",
    )

    parser.add_argument(
        "--strict",
        "-s",
        action="store_true",
        help="Only probable true positive, by default only probable false positive are not printed.",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Based on all formats (by default multiples formats are disabled for optimization).",
    )

    return parse_arguments(parser)


def init_formats(arguments: Namespace) -> int:
    """
    This function initialize formats.
    """

    global formats

    if not arguments.all:
        formats = {
            x: y
            for x, y in formats.items()
            if x
            not in (
                "base85",
                "base32_lower",
                "base32_insensitive",
                "base64_urlsafe",
                "string_null_terminated",
                "csv",
                "unicode_null_terminated",
                "ipvfuture",
                "http_response",
                "http_request",
            )
        }
        arguments.do_not_print.append("hex")
        arguments.do_not_print.append("base32")
        arguments.do_not_print.append("base64")

    for format in (
        arguments.process_only
        + arguments.do_not_process
        + arguments.print_only
        + arguments.do_not_print
    ):
        if format not in formats:
            print(
                "Invalid format:",
                format + ", formats:",
                ", ".join(formats),
                file=stderr,
            )
            return 3

    arguments.process_only = set(arguments.process_only)
    arguments.do_not_process = set(arguments.do_not_process)
    arguments.print_only = set(arguments.print_only)
    arguments.do_not_print = set(arguments.do_not_print)

    formats = {
        x: y
        for x, y in formats.items()
        if not (
            (arguments.process_only and x not in arguments.process_only)
            or (arguments.do_not_process and x in arguments.do_not_process)
        )
    }


def main() -> int:
    """
    This function runs the module from the command line.
    """

    arguments = specific_argument_parser()
    if code := init_formats(arguments):
        return code

    if not exists(arguments.filename):
        print("File:", arguments.filename, "does not exists.", file=stderr)
        return 2

    size = getsize(arguments.filename)
    with open(arguments.filename, "rb") as file:
        strings = MagicStrings(
            file,
            minimum_length=arguments.minimum_length,
            null_terminated=not arguments.non_null_terminated,
        )

        for result in strings.magic():
            if (
                (result.format.name == "string" and result.process_level)
                or (
                    arguments.strict
                    and not result.format.probable_true_positive(result.string)
                )
                or (
                    not arguments.strict
                    and result.format.probable_false_positive(result.string)
                )
                or (
                    arguments.print_only
                    and result.format.name not in arguments.print_only
                )
                or (
                    arguments.do_not_print
                    and result.format.name in arguments.do_not_print
                )
            ):
                continue
            printf(result, pourcent=round(file.tell() / size * 100))

    return 0


if __name__ == "__main__":
    exit(main())
