#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements a PEG (Parsing Expression Grammar) to parse
#    syntax, i add rules to parse URL, HTTP request and response easily
#    with security and some format like hexadecimal, base32, base64,
#    base85, CSV, JSON (strict and permissive), system file path...
#    Copyright (C) 2025  PegParser

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
This package implements a PEG (Parsing Expression Grammar) to parse
syntax, i add rules to parse URL, HTTP request and response easily
with security and some format like hexadecimal, base32, base64,
base85, CSV, JSON (strict and permissive), system file path...

Tests:
~# python3 -m doctest PegParser.py
~# python3 -m doctest -v PegParser.py

53 items had no tests:
    PegParser
    PegParser.Format
    PegParser.Format.__eq__
    PegParser.Format.__init__
    PegParser.Format.__repr__
    PegParser.Format.probable_false_positive
    PegParser.Format.probable_true_positive
    PegParser.HttpRequest
    PegParser.HttpRequest.__eq__
    PegParser.HttpRequest.__init__
    PegParser.HttpRequest.__repr__
    PegParser.HttpResponse
    PegParser.HttpResponse.__eq__
    PegParser.HttpResponse.__init__
    PegParser.HttpResponse.__repr__
    PegParser.MatchList
    PegParser.MatchList.__init__
    PegParser.PegParser
    PegParser.PegParser.and_predicate
    PegParser.PegParser.not_predicate
    PegParser.PegParser.one_or_more
    PegParser.PegParser.ordered_choice
    PegParser.PegParser.sequence
    PegParser.PegParser.zero_or_more
    PegParser.StandardMatch
    PegParser.StandardMatch.check_char
    PegParser.StandardMatch.or_check_chars
    PegParser.StandardRules
    PegParser.StandardRules.Csv
    PegParser.StandardRules.Format
    PegParser.StandardRules.Http
    PegParser.StandardRules.Json
    PegParser.StandardRules.Json._end_dict
    PegParser.StandardRules.Json._end_list
    PegParser.StandardRules.Json._start_dict
    PegParser.StandardRules.Json._start_list
    PegParser.StandardRules.Network
    PegParser.StandardRules.Path
    PegParser.StandardRules.Path._directories_file
    PegParser.StandardRules.Path._directories_or_file
    PegParser.StandardRules.Path._directory_file
    PegParser.StandardRules.Types
    PegParser.StandardRules.Url
    PegParser.StandardRules.Url._base_path
    PegParser.StandardRules.Url._character_subdelims_colon_commat
    PegParser.StandardRules.Url._character_subdelims_colon_commat_slot_quest
    PegParser.StandardRules.Url._characters
    PegParser.StandardRules.Url._characters_subdelims_colon
    PegParser.StandardRules.Url._characters_subdelims_colon_commat
    PegParser.StandardRules.Url._optional_characters_subdelims_colon_commat
    PegParser.StandardRules.Url._optional_characters_subdelims_colon_commat_slot_quest
    PegParser.get_http_content
    PegParser.match_getter
116 items passed all tests:
   3 tests in PegParser.HttpRequest.__bytes__
   3 tests in PegParser.HttpResponse.__bytes__
   3 tests in PegParser.StandardMatch.is_blank
   4 tests in PegParser.StandardMatch.is_digit
   5 tests in PegParser.StandardMatch.is_hex
   4 tests in PegParser.StandardMatch.is_letter
   4 tests in PegParser.StandardMatch.is_lower
   5 tests in PegParser.StandardMatch.is_octal
   6 tests in PegParser.StandardMatch.is_printable
   4 tests in PegParser.StandardMatch.is_special
   4 tests in PegParser.StandardMatch.is_upper
   7 tests in PegParser.StandardRules.Csv.full
   7 tests in PegParser.StandardRules.Csv.line
   4 tests in PegParser.StandardRules.Csv.line_delimiter
   1 tests in PegParser.StandardRules.Csv.multi
   4 tests in PegParser.StandardRules.Csv.quoted_value
   2 tests in PegParser.StandardRules.Csv.value
   6 tests in PegParser.StandardRules.Csv.values
   9 tests in PegParser.StandardRules.Format.base32
   9 tests in PegParser.StandardRules.Format.base32_insensitive
   9 tests in PegParser.StandardRules.Format.base32_lower
   8 tests in PegParser.StandardRules.Format.base64
   9 tests in PegParser.StandardRules.Format.base64_urlsafe
   6 tests in PegParser.StandardRules.Format.base85
   4 tests in PegParser.StandardRules.Format.blanks
   6 tests in PegParser.StandardRules.Format.hex
   6 tests in PegParser.StandardRules.Format.hexadecimal
   6 tests in PegParser.StandardRules.Format.integer
   6 tests in PegParser.StandardRules.Format.octal
   4 tests in PegParser.StandardRules.Format.optional_blanks
   4 tests in PegParser.StandardRules.Format.string_null_terminated_length
   4 tests in PegParser.StandardRules.Format.unicode_null_terminated_length
   5 tests in PegParser.StandardRules.Format.word
   2 tests in PegParser.StandardRules.Http.field_name
   2 tests in PegParser.StandardRules.Http.field_value
   2 tests in PegParser.StandardRules.Http.header
   1 tests in PegParser.StandardRules.Http.headers
   5 tests in PegParser.StandardRules.Http.is_text_char
   2 tests in PegParser.StandardRules.Http.magic
   2 tests in PegParser.StandardRules.Http.protocol_version
   2 tests in PegParser.StandardRules.Http.reason
   2 tests in PegParser.StandardRules.Http.request
   1 tests in PegParser.StandardRules.Http.response
   2 tests in PegParser.StandardRules.Http.response_start
   2 tests in PegParser.StandardRules.Http.status_code
   2 tests in PegParser.StandardRules.Http.text
   2 tests in PegParser.StandardRules.Http.token
   8 tests in PegParser.StandardRules.Http.verb
   2 tests in PegParser.StandardRules.Http.version
   7 tests in PegParser.StandardRules.Json.dict
   3 tests in PegParser.StandardRules.Json.false
   9 tests in PegParser.StandardRules.Json.full
   7 tests in PegParser.StandardRules.Json.list
   8 tests in PegParser.StandardRules.Json.null
  10 tests in PegParser.StandardRules.Json.permissive_dict
   3 tests in PegParser.StandardRules.Json.permissive_false
   9 tests in PegParser.StandardRules.Json.permissive_full
   7 tests in PegParser.StandardRules.Json.permissive_list
   8 tests in PegParser.StandardRules.Json.permissive_null
   8 tests in PegParser.StandardRules.Json.permissive_simple_value
   3 tests in PegParser.StandardRules.Json.permissive_true
   8 tests in PegParser.StandardRules.Json.simple_value
   3 tests in PegParser.StandardRules.Json.true
   7 tests in PegParser.StandardRules.Network.fqdn
   9 tests in PegParser.StandardRules.Network.host
   9 tests in PegParser.StandardRules.Network.host_port
   7 tests in PegParser.StandardRules.Network.hostname
  12 tests in PegParser.StandardRules.Network.ipv4
  16 tests in PegParser.StandardRules.Network.ipv6
   8 tests in PegParser.StandardRules.Network.ipv6_zoneid
   7 tests in PegParser.StandardRules.Network.ipvfuture
   3 tests in PegParser.StandardRules.Network.user_info
   4 tests in PegParser.StandardRules.Path.base_filename
   3 tests in PegParser.StandardRules.Path.drive_path
   4 tests in PegParser.StandardRules.Path.extensions
   4 tests in PegParser.StandardRules.Path.filename
   4 tests in PegParser.StandardRules.Path.filename_extension
   4 tests in PegParser.StandardRules.Path.linux_path
   3 tests in PegParser.StandardRules.Path.nt_path
  13 tests in PegParser.StandardRules.Path.path
   3 tests in PegParser.StandardRules.Path.relative_path
   9 tests in PegParser.StandardRules.Path.windows_path
   6 tests in PegParser.StandardRules.Types.bool
   6 tests in PegParser.StandardRules.Types.digits
   6 tests in PegParser.StandardRules.Types.float
   5 tests in PegParser.StandardRules.Types.hex_integer
   8 tests in PegParser.StandardRules.Types.octal_integer
  10 tests in PegParser.StandardRules.Types.string
   8 tests in PegParser.StandardRules.Url.form_data
   4 tests in PegParser.StandardRules.Url.fragment
  10 tests in PegParser.StandardRules.Url.full
   9 tests in PegParser.StandardRules.Url.parameters
  11 tests in PegParser.StandardRules.Url.path
   4 tests in PegParser.StandardRules.Url.path_rootless
   9 tests in PegParser.StandardRules.Url.query
   6 tests in PegParser.StandardRules.Url.scheme
   3 tests in PegParser.csv_file_parse
   2 tests in PegParser.csv_files_parse
   1 tests in PegParser.csv_parse
   2 tests in PegParser.filename_false_positive
   2 tests in PegParser.get_json
   1 tests in PegParser.get_json_from_ordered_matchs
   2 tests in PegParser.get_matchs
   2 tests in PegParser.get_ordered_matchs
   2 tests in PegParser.host_port_false_positive
   2 tests in PegParser.host_port_true_positive
   2 tests in PegParser.linux_path_false_positive
   2 tests in PegParser.linux_path_true_positive
   4 tests in PegParser.match
   3 tests in PegParser.mjson_file_parse
   1 tests in PegParser.parse_http_request
   1 tests in PegParser.parse_http_response
   2 tests in PegParser.uri_false_positive
   2 tests in PegParser.uri_true_positive
   2 tests in PegParser.word_false_positive
   2 tests in PegParser.word_true_positive
574 tests in 169 items.
574 passed and 0 failed.
Test passed.
"""

__version__ = "1.1.5"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This package implements a PEG (Parsing Expression Grammar) to parse
syntax, i add rules to parse URL, HTTP request and response easily
with security and some format like hexadecimal, base32, base64,
base85, CSV, JSON (strict and permissive), system file path...
"""
__url__ = "https://github.com/mauricelambert/PegParser"

# __all__ = []

__license__ = "GPL-3.0 License"
__copyright__ = """
PegParser  Copyright (C) 2025  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
copyright = __copyright__
license = __license__

print(copyright)

from typing import Callable, List, Iterable, Union, Tuple, Dict
from base64 import b32decode, b64decode, b85decode
from collections import defaultdict
from dataclasses import dataclass
from _io import _BufferedIOBase
from binascii import unhexlify
from functools import partial
from codecs import decode


@dataclass
class Format:
    """
    Format is a dataclass used in formats dict to list, check,
    decode and verify probable validity for all formats.

    Formats was defined to check untrusted/identified strings,
    there are probably lot of False positive because multiples formats
    were very flexible. The `probable_true_positive` is used to identify
    a probable real value for the format (by default return False),
    and `probable_false_positive` is used to identify a probable false
    value for the format (by default return True.)
    """

    name: str
    match: Callable
    decode: Callable
    probable_true_positive: Callable = lambda x: False
    probable_false_positive: Callable = lambda x: True


@dataclass
class HttpResponse:
    magic: bytes
    version: float
    code: int
    reason: str
    headers: List[Tuple[str, str]]
    body: bytes
    content_length: int = 0
    content_type: str = None

    def __bytes__(self) -> bytes:
        r"""
        This magic method returns bytes for the full response
        in the HTTP format.

        >>> bytes(HttpResponse(b'HTTP', 1.0, 200, 'OK', [], b'body content'))
        b"HTTP/1.0 200 OK\r\nContent-Length: 12\r\nServer: Maurice Lambert's HTTP server\r\n\r\nbody content"
        >>> bytes(HttpResponse(b'HTTP', 1.1, 201, 'Created', [('Content-Length', '12'), ('Content-Type', 'application/json'), ('Server', 'TestServer')], b'', 10, 'plain/text'))
        b'HTTP/1.1 201 Created\r\nContent-Length: 12\r\nContent-Type: application/json\r\nServer: TestServer\r\n\r\n'
        >>> bytes(HttpResponse(b'HTTP', 1.0, 202, 'Accepted', [], b'body content', 10, 'plain/text'))
        b"HTTP/1.0 202 Accepted\r\nContent-Type: plain/text\r\nContent-Length: 10\r\nServer: Maurice Lambert's HTTP server\r\n\r\nbody content"
        >>>
        """

        content_length = len(self.body)
        set_content_length = False
        set_content_type = False
        set_server = False
        headers = bytearray()

        for header, value in self.headers:
            header = header.title().encode("ascii")
            if header == b"Content-Length":
                set_content_length = True
            elif header == b"Content-Type":
                set_content_type = True
            elif header == b"Server":
                set_server = True
            headers.extend(header + b": " + value.encode("ascii") + b"\r\n")

        if self.body and not set_content_type and self.content_type:
            headers.extend(
                b"Content-Type: " + self.content_type.encode("ascii") + b"\r\n"
            )

        if content_length and not set_content_length:
            if self.content_length:
                headers.extend(
                    b"Content-Length: "
                    + str(self.content_length).encode("ascii")
                    + b"\r\n"
                )
            else:
                headers.extend(
                    b"Content-Length: "
                    + str(content_length).encode("ascii")
                    + b"\r\n"
                )

        if not set_server:
            headers.extend(
                b"Server: "
                + __author__.encode("ascii")
                + b"'s HTTP server\r\n"
            )

        return (
            self.magic
            + b"/"
            + str(self.version).encode("ascii")
            + b" "
            + str(self.code).encode("ascii")
            + b" "
            + self.reason.encode("ascii")
            + b"\r\n"
            + headers
            + b"\r\n"
            + self.body
        )


@dataclass
class HttpRequest:
    verb: str
    uri: str
    magic: bytes
    version: float
    headers: List[Tuple[str, str]]
    body: bytes
    content_length: int = 0
    content_type: str = None
    host: str = None

    def __bytes__(self) -> bytes:
        r"""
        This magic method returns bytes for the full request
        in the HTTP format.

        >>> bytes(HttpRequest('GET', '/', b'HTTP', 1.0, [], b'body content'))
        b"GET / HTTP/1.0\r\nContent-Length: 12\r\nUser-Agent: Maurice Lambert's HTTP client\r\n\r\nbody content"
        >>> bytes(HttpRequest('POST', '/upload', b'HTTP', 1.1, [('Content-Length', '12'), ('Content-Type', 'application/json'), ('User-Agent', 'TestClient')], b'', 10, 'plain/text'))
        b'POST /upload HTTP/1.1\r\nContent-Length: 12\r\nContent-Type: application/json\r\nUser-Agent: TestClient\r\n\r\n'
        >>> bytes(HttpRequest('HEAD', '/wp-admin?user=admin', b'HTTP', 1.0, [], b'body content', 10, 'plain/text'))
        b"HEAD /wp-admin?user=admin HTTP/1.0\r\nContent-Type: plain/text\r\nContent-Length: 10\r\nUser-Agent: Maurice Lambert's HTTP client\r\n\r\nbody content"
        >>>
        """

        content_length = len(self.body)
        set_content_length = False
        set_content_type = False
        set_user_agent = False
        headers = bytearray()

        for header, value in self.headers:
            header = header.title().encode("ascii")
            if header == b"Content-Length":
                set_content_length = True
            elif header == b"Content-Type":
                set_content_type = True
            elif header == b"User-Agent":
                set_user_agent = True
            headers.extend(header + b": " + value.encode("ascii") + b"\r\n")

        if self.body and not set_content_type and self.content_type:
            headers.extend(
                b"Content-Type: " + self.content_type.encode("ascii") + b"\r\n"
            )

        if content_length and not set_content_length:
            if self.content_length:
                headers.extend(
                    b"Content-Length: "
                    + str(self.content_length).encode("ascii")
                    + b"\r\n"
                )
            else:
                headers.extend(
                    b"Content-Length: "
                    + str(content_length).encode("ascii")
                    + b"\r\n"
                )

        if not set_user_agent:
            headers.extend(
                b"User-Agent: "
                + __author__.encode("ascii")
                + b"'s HTTP client\r\n"
            )

        return (
            self.verb.encode("ascii")
            + b" "
            + self.uri.encode("ascii")
            + b" "
            + self.magic
            + b"/"
            + str(self.version).encode("ascii")
            + b"\r\n"
            + headers
            + b"\r\n"
            + self.body
        )


class MatchList(list):
    """
    Simple list with hidden argument to identify match.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._match_name = None


class PegParser:
    """
    This class implements methods for a PEG parser.
    """

    def sequence(
        rules: Iterable[Callable], data: bytes, position: int
    ) -> Tuple[int, Union[None, List[bytes]]]:
        """
        This method implements the PEG `sequence`
        ("match 2 elements").
        """

        backup_position = position
        results = MatchList()

        for rule in rules:
            position, result = rule(data, position)
            if result is None:
                return backup_position, None
            results.append(result)

        return position, results

    def ordered_choice(
        rules: Iterable[Callable], data: bytes, position: int
    ) -> Tuple[int, Union[None, bytes]]:
        """
        This method implements the PEG `ordered choice`
        ("OR" operator, like "|" in regex).
        """

        backup_position = position

        for rule in rules:
            position, result = rule(data, position)
            if result is not None:
                return position, result

        return backup_position, None

    def and_predicate(
        first: Callable, data: bytes, position: int
    ) -> Tuple[int, Union[None, bytes]]:
        """
        This method implements the PEG `and predicate`
        ("match without consume data" | position is always the same).
        """

        return position, first(data, position)[1] is not None or None

    def not_predicate(
        first: Callable, data: bytes, position: int
    ) -> Tuple[int, Union[None, bool]]:
        """
        This method implements the PEG `not predicate`
        ("don't match without consume data" | position is always the same).
        """

        return position, first(data, position)[1] is None or None

    def zero_or_more(
        first: Callable, data: bytes, position: int
    ) -> Tuple[int, List[bytes]]:
        """
        This method implements the PEG `zero or more` or `optional`
        (like "*" in regex).
        """

        results = MatchList()
        position_first, result_first = first(data, position)

        while result_first:
            position = position_first
            results.append(result_first)
            position_first, result_first = first(data, position)

        return position, results

    def one_or_more(
        first: Callable, data: bytes, position: int
    ) -> Tuple[int, Union[None, List[bytes]]]:
        """
        This method implements the PEG `one or more`
        (like "+" in regex).
        """

        position, result = PegParser.zero_or_more(first, data, position)
        return (position, result or None)


class StandardMatch:
    """
    This class implements methods to match standard characters groups.
    """

    def is_letter(
        data: bytes, position: int
    ) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII letter
        (upper or lower case).

        >>> StandardMatch.is_letter(b"a1Bc", 0)
        (1, b'a')
        >>> StandardMatch.is_letter(b"a1Bc", 1)
        (1, None)
        >>> StandardMatch.is_letter(b"a1Bc", 2)
        (3, b'B')
        >>> len([x for x in range(256) if StandardMatch.is_letter(bytes((x,)), 0)[1] is not None])
        52
        >>>
        """

        result = StandardMatch.is_lower(data, position)

        if result[1] is None:
            return StandardMatch.is_upper(data, position)

        return result

    def is_lower(data: bytes, position: int) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII lower case letter.

        >>> StandardMatch.is_lower(b"a1Bc", 0)
        (1, b'a')
        >>> StandardMatch.is_lower(b"a1Bc", 1)
        (1, None)
        >>> StandardMatch.is_lower(b"a1Bc", 2)
        (2, None)
        >>> len([x for x in range(256) if StandardMatch.is_lower(bytes((x,)), 0)[1] is not None])
        26
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if 97 <= char <= 122:
            return position + 1, bytes((char,))
        return position, None

    def is_upper(data: bytes, position: int) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII upper case letter.

        >>> StandardMatch.is_upper(b"a1Bc", 0)
        (0, None)
        >>> StandardMatch.is_upper(b"a1Bc", 1)
        (1, None)
        >>> StandardMatch.is_upper(b"a1Bc", 2)
        (3, b'B')
        >>> len([x for x in range(256) if StandardMatch.is_upper(bytes((x,)), 0)[1] is not None])
        26
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if 65 <= char <= 90:
            return position + 1, bytes((char,))
        return position, None

    def is_digit(data: bytes, position: int) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII digit character.

        >>> StandardMatch.is_digit(b"a1Bc", 0)
        (0, None)
        >>> StandardMatch.is_digit(b"a1Bc", 1)
        (2, b'1')
        >>> StandardMatch.is_digit(b"a1Bc", 2)
        (2, None)
        >>> len([x for x in range(256) if StandardMatch.is_digit(bytes((x,)), 0)[1] is not None])
        10
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if 48 <= char <= 57:
            return position + 1, bytes((char,))
        return position, None

    def is_hex(data: bytes, position: int) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII hexadecimal character.

        >>> StandardMatch.is_hex(b"a1Bc", 0)
        (1, b'a')
        >>> StandardMatch.is_hex(b"a1Bc", 1)
        (2, b'1')
        >>> StandardMatch.is_hex(b"a1Bc", 2)
        (3, b'B')
        >>> StandardMatch.is_hex(b"a1Bg", 3)
        (3, None)
        >>> len([x for x in range(256) if StandardMatch.is_hex(bytes((x,)), 0)[1] is not None])
        22
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if 48 <= char <= 57 or 65 <= char <= 70 or 97 <= char <= 102:
            return position + 1, bytes((char,))
        return position, None

    def is_octal(data: bytes, position: int) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII octal character.

        >>> StandardMatch.is_octal(b"01234567", 0)
        (1, b'0')
        >>> StandardMatch.is_octal(b"789", 0)
        (1, b'7')
        >>> StandardMatch.is_octal(b"a123", 0)
        (0, None)
        >>> StandardMatch.is_octal(b";+123", 0)
        (0, None)
        >>> len([x for x in range(256) if StandardMatch.is_octal(bytes((x,)), 0)[1] is not None])
        8
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if 48 <= char <= 55:
            return position + 1, bytes((char,))
        return position, None

    def is_printable(
        data: bytes, position: int
    ) -> Tuple[int, Union[None, bytes]]:
        r"""
        This method checks a position for an ASCII printable character.

        >>> StandardMatch.is_printable(b"a1Bc", 0)
        (1, b'a')
        >>> StandardMatch.is_printable(b"a1Bc", 1)
        (2, b'1')
        >>> StandardMatch.is_printable(b"a1Bc", 2)
        (3, b'B')
        >>> StandardMatch.is_printable(b"a1B\0", 3)
        (3, None)
        >>> from string import printable
        >>> len([x for x in range(256) if StandardMatch.is_printable(bytes((x,)), 0)[1] is not None]) == len(printable)
        True
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if 32 <= char <= 126 or 9 <= char <= 13:
            return position + 1, bytes((char,))
        return position, None

    def is_blank(data: bytes, position: int) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII special character.

        >>> StandardMatch.is_blank(b" 1Bc", 0)
        (1, b' ')
        >>> StandardMatch.is_blank(b" 1Bc", 1)
        (1, None)
        >>> len([x for x in range(256) if StandardMatch.is_blank(bytes((x,)), 0)[1] is not None])
        6
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if 9 <= char <= 13 or char == 32:
            return position + 1, bytes((char,))
        return position, None

    def is_special(
        data: bytes, position: int
    ) -> Tuple[int, Union[None, bytes]]:
        """
        This method checks a position for an ASCII special character.

        >>> StandardMatch.is_special(b";1Bc", 0)
        (1, b';')
        >>> StandardMatch.is_special(b" 1Bc", 1)
        (1, None)
        >>> from string import printable
        >>> len([x for x in range(256) if StandardMatch.is_special(bytes((x,)), 0)[1] is not None]) == len(printable) - 26 * 2 - 10 - 6
        True
        >>>
        """

        if len(data) == position:
            return position, None

        char = data[position]
        if (
            33 <= char <= 47
            or 58 <= char <= 64
            or 91 <= char <= 96
            or 123 <= char <= 126
        ):
            return position + 1, bytes((char,))
        return position, None

    def check_char(char: int) -> Callable:
        """
        Generic method to generate a check for a specific character.
        """

        def check(
            data: bytes, position: int
        ) -> Tuple[int, Union[None, bytes]]:
            if len(data) == position:
                return position, None

            checked_char = data[position]
            if checked_char == char:
                return position + 1, bytes((char,))
            return position, None

        return check

    def or_check_chars(*chars: int) -> Callable:
        """
        Generic method to generate wrapper for `check_char`
        with `ordered_choice`.
        """

        def checks(
            data: bytes, position: int
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            return PegParser.ordered_choice(
                [StandardMatch.check_char(x) for x in chars],
                data,
                position,
            )

        return checks


class StandardRules:
    """
    This class implements standard rules.
    """

    class Types:
        """
        This class implements standard types parsing rules.
        """

        def digits(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks multiples digits.

            >>> StandardRules.Types.digits(b"0123456789")
            (10, [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9'])
            >>> StandardRules.Types.digits(b"abc0123")
            (0, None)
            >>> StandardRules.Types.digits(b"0123abc")
            (4, [b'0', b'1', b'2', b'3'])
            >>> StandardRules.Types.digits(b"+123")
            (0, None)
            >>> StandardRules.Types.digits(b"0B2;")
            (1, [b'0'])
            >>> StandardRules.Types.digits(b"a ")
            (0, None)
            >>>
            """

            result = PegParser.one_or_more(
                StandardMatch.is_digit,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "digits"

            return result

        def float(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks multiples digits.

            >>> StandardRules.Types.float(b"1.525")
            (5, [[b'1'], b'.', [b'5', b'2', b'5']])
            >>> StandardRules.Types.float(b"4521.5")
            (6, [[b'4', b'5', b'2', b'1'], b'.', [b'5']])
            >>> StandardRules.Types.float(b"0.2356")
            (6, [[b'0'], b'.', [b'2', b'3', b'5', b'6']])
            >>> StandardRules.Types.float(b"5624.0")
            (6, [[b'5', b'6', b'2', b'4'], b'.', [b'0']])
            >>> StandardRules.Types.float(b".0256")
            (0, None)
            >>> StandardRules.Types.float(b"0256.")
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Types.digits,
                    StandardMatch.check_char(46),
                    StandardRules.Types.digits,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "float"

            return result

        def bool(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks multiples digits.

            >>> StandardRules.Types.bool(b"true")
            (4, [b't', b'r', b'u', b'e'])
            >>> StandardRules.Types.bool(b"false")
            (5, [b'f', b'a', b'l', b's', b'e'])
            >>> StandardRules.Types.bool(b"True")
            (0, None)
            >>> StandardRules.Types.bool(b"False")
            (0, None)
            >>> StandardRules.Types.bool(b"test")
            (0, None)
            >>> StandardRules.Types.bool(b"tru")
            (0, None)
            >>>
            """

            result = PegParser.ordered_choice(
                [
                    lambda d, p: PegParser.sequence(
                        [
                            StandardMatch.check_char(116),
                            StandardMatch.check_char(114),
                            StandardMatch.check_char(117),
                            StandardMatch.check_char(101),
                        ],
                        d,
                        p,
                    ),
                    lambda d, p: PegParser.sequence(
                        [
                            StandardMatch.check_char(102),
                            StandardMatch.check_char(97),
                            StandardMatch.check_char(108),
                            StandardMatch.check_char(115),
                            StandardMatch.check_char(101),
                        ],
                        d,
                        p,
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "bool"

            return result

        def hex_integer(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks hexadecimal integer.

            >>> StandardRules.Types.hex_integer(b"0x123")
            (5, [b'0', b'x', [b'1', b'2', b'3']])
            >>> StandardRules.Types.hex_integer(b"0Xa1c")
            (5, [b'0', b'X', [b'a', b'1', b'c']])
            >>> StandardRules.Types.hex_integer(b"0xg23")
            (0, None)
            >>> StandardRules.Types.hex_integer(b"0x1;")
            (3, [b'0', b'x', [b'1']])
            >>> StandardRules.Types.hex_integer(b"0x 1")
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(48),
                    StandardMatch.or_check_chars(88, 120),
                    StandardRules.Format.hex,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "hex_integer"

            return result

        def octal_integer(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks hexadecimal integer.

            >>> StandardRules.Types.octal_integer(b"0o123")
            (5, [b'0', b'o', [b'1', b'2', b'3']])
            >>> StandardRules.Types.octal_integer(b"0O123")
            (5, [b'0', b'O', [b'1', b'2', b'3']])
            >>> StandardRules.Types.octal_integer(b"0o891")
            (0, None)
            >>> StandardRules.Types.octal_integer(b"0O891")
            (0, None)
            >>> StandardRules.Types.octal_integer(b"0Oabc")
            (0, None)
            >>> StandardRules.Types.octal_integer(b"0Oabc")
            (0, None)
            >>> StandardRules.Types.octal_integer(b"123")
            (0, None)
            >>> StandardRules.Types.octal_integer(b"+0o123")
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(48),
                    StandardMatch.or_check_chars(79, 111),
                    StandardRules.Format.octal,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "octal_integer"

            return result

        def string(data: bytes, position: int = 0):
            """
            This method checks for string.

            >>> StandardRules.Types.string(b'"test"')
            (6, [b'"', [b't', b'e', b's', b't'], b'"'])
            >>> StandardRules.Types.string(b"'test2.,'")
            (9, [b"'", [b't', b'e', b's', b't', b'2', b'.', b','], b"'"])
            >>> StandardRules.Types.string(b"'\\\\x56\\\\t\\\\r\\\\7\\\\45\\\\111'")
            (0, None)
            >>> StandardRules.Types.string(b"test")
            (0, None)
            >>> StandardRules.Types.string(b"'\\\\98'")
            (0, None)
            >>> StandardRules.Types.string(b"'\\\\xgf'")
            (0, None)
            >>> StandardRules.Types.string(b"'\\\\N{NAME -TEST1}'")
            (17, [b"'", [[b'\\\\', b'N', b'{', [b'N', b'A', b'M', b'E', b' ', b'-', b'T', b'E', b'S', b'T', b'1'], b'}']], b"'"])
            >>> StandardRules.Types.string(b"'\\\\u0020'")
            (0, None)
            >>> StandardRules.Types.string(b"'\\\\U00000020'")
            (0, None)
            >>> StandardRules.Types.string(b'"test')
            (0, None)
            >>>
            """

            def wrapper_simple_character(x: int):
                def simple_character(data: bytes, position: int):
                    if len(data) == position:
                        return position, None

                    char = data[position]
                    if (
                        32 <= char <= 126 and char != 92 and char != x
                    ) or 9 <= char <= 10:
                        return position + 1, bytes((char,))
                    return position, None

                return simple_character

            def hex_special(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(92),
                        StandardMatch.or_check_chars(88, 120),
                        StandardMatch.is_hex,
                        StandardMatch.is_hex,
                    ],
                    data,
                    position,
                )

            def octal3_special(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.is_octal,
                        StandardMatch.is_octal,
                        StandardMatch.is_octal,
                    ],
                    data,
                    position,
                )

            def octal2_special(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.is_octal,
                        StandardMatch.is_octal,
                    ],
                    data,
                    position,
                )

            def octal_number_special(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        octal3_special,
                        octal2_special,
                        StandardMatch.is_octal,
                    ],
                    data,
                    position,
                )

            def octal_special(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(92),
                        StandardMatch.or_check_chars(79, 111),
                        octal_number_special,
                    ],
                    data,
                    position,
                )

            def unicode4(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(92),
                        StandardMatch.check_char(117),
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                    ],
                    data,
                    position,
                )

            def unicode8(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(92),
                        StandardMatch.check_char(85),
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                        StandardRules.Format.hex,
                    ],
                    data,
                    position,
                )

            def named_unicode(data: bytes, position: int):
                def name_char(data: bytes, position: int):
                    return PegParser.ordered_choice(
                        [
                            StandardMatch.is_letter,
                            StandardMatch.is_digit,
                            StandardMatch.or_check_chars(0x20, 0x2D),
                        ],
                        data,
                        position,
                    )

                def name_chars(data: bytes, position: int):
                    return PegParser.zero_or_more(name_char, data, position)

                return PegParser.sequence(
                    [
                        StandardMatch.check_char(92),
                        StandardMatch.check_char(78),
                        StandardMatch.check_char(123),
                        name_chars,
                        StandardMatch.check_char(125),
                    ],
                    data,
                    position,
                )

            def letter_special(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(92),
                        StandardMatch.or_check_chars(
                            34, 39, 92, 97, 98, 102, 110, 114, 116, 118
                        ),
                    ],
                    data,
                    position,
                )

            def special_character(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        hex_special,
                        octal_special,
                        unicode4,
                        unicode8,
                        named_unicode,
                        letter_special,
                    ],
                    data,
                    position,
                )

            def wrapper_character(x: int):
                def character(data: bytes, position: int):
                    return PegParser.ordered_choice(
                        [
                            wrapper_simple_character(x),
                            special_character,
                        ],
                        data,
                        position,
                    )

                return character

            def wrapper_characters(x: int):
                def characters(data: bytes, position: int):
                    return PegParser.zero_or_more(
                        wrapper_character(x),
                        data,
                        position,
                    )

                return characters

            def string_format1(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(34),
                        wrapper_characters(34),
                        StandardMatch.check_char(34),
                    ],
                    data,
                    position,
                )

            def string_format2(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(39),
                        wrapper_characters(39),
                        StandardMatch.check_char(39),
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    string_format1,
                    string_format2,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "strings"

            return result

    class Format:
        """
        This class implements standard data formats parsing rules.
        """

        def integer(
            data: bytes, position: int = 0
        ) -> Tuple[
            int, Union[None, Iterable[Union[bool, bytes, Iterable[bytes]]]]
        ]:
            """
            This method checks signed integer.

            >>> StandardRules.Format.integer(b"+1")
            (2, [b'+', [b'1']])
            >>> StandardRules.Format.integer(b"-123")
            (4, [b'-', [b'1', b'2', b'3']])
            >>> StandardRules.Format.integer(b"123")
            (3, [True, [b'1', b'2', b'3']])
            >>> StandardRules.Format.integer(b"1a3")
            (1, [True, [b'1']])
            >>> StandardRules.Format.integer(b"+a")
            (0, None)
            >>> StandardRules.Format.integer(b"-abc")
            (0, None)
            >>>
            """

            def check_sign(data, position):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.check_char(45),
                        StandardMatch.check_char(43),
                        lambda data, position: PegParser.and_predicate(
                            StandardMatch.is_digit, data, position
                        ),
                    ],
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    check_sign,
                    StandardRules.Types.digits,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "sign_integer"

            return result

        def optional_blanks(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            r"""
            This method checks for optional multiples blank characters.

            >>> StandardRules.Format.optional_blanks(b"\n \n\r\n  ")
            (7, [b'\n', b' ', b'\n', b'\r', b'\n', b' ', b' '])
            >>> StandardRules.Format.optional_blanks(b"\r\t+")
            (2, [b'\r', b'\t'])
            >>> StandardRules.Format.optional_blanks(b" ;")
            (1, [b' '])
            >>> StandardRules.Format.optional_blanks(b"a ")
            (0, [])
            >>>
            """

            return PegParser.zero_or_more(
                StandardMatch.is_blank,
                data,
                position,
            )

        def blanks(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            r"""
            This method checks for multiples blank characters.

            >>> StandardRules.Format.blanks(b"\n \n\r\n  ")
            (7, [b'\n', b' ', b'\n', b'\r', b'\n', b' ', b' '])
            >>> StandardRules.Format.blanks(b"\r\t+")
            (2, [b'\r', b'\t'])
            >>> StandardRules.Format.blanks(b" ;")
            (1, [b' '])
            >>> StandardRules.Format.blanks(b"a ")
            (0, None)
            >>>
            """

            return PegParser.one_or_more(
                StandardMatch.is_blank,
                data,
                position,
            )

        def word(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks for a word.

            >>> StandardRules.Format.word(b"abc")
            (3, [b'a', b'b', b'c'])
            >>> StandardRules.Format.word(b"abc;")
            (3, [b'a', b'b', b'c'])
            >>> StandardRules.Format.word(b"+123")
            (0, None)
            >>> StandardRules.Format.word(b"1abc")
            (0, None)
            >>> StandardRules.Format.word(b"a ")
            (1, [b'a'])
            >>>
            """

            result = PegParser.one_or_more(
                StandardMatch.is_letter,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "word"

            return result

        def hex(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks for hexadecimal characters.

            >>> StandardRules.Format.hex(b"abcdef")
            (6, [b'a', b'b', b'c', b'd', b'e', b'f'])
            >>> StandardRules.Format.hex(b"abc0123")
            (7, [b'a', b'b', b'c', b'0', b'1', b'2', b'3'])
            >>> StandardRules.Format.hex(b"0123abc")
            (7, [b'0', b'1', b'2', b'3', b'a', b'b', b'c'])
            >>> StandardRules.Format.hex(b"+123")
            (0, None)
            >>> StandardRules.Format.hex(b"0B2;")
            (3, [b'0', b'B', b'2'])
            >>> StandardRules.Format.hex(b"a ")
            (1, [b'a'])
            >>>
            """

            result = PegParser.one_or_more(
                StandardMatch.is_hex,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "hex"

            return result

        def hexadecimal(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Iterable[bytes]]]]:
            """
            This method checks for multiples pairs of hexadecimal characters.

            >>> StandardRules.Format.hexadecimal(b"abcdef")
            (6, [[b'a', b'b'], [b'c', b'd'], [b'e', b'f']])
            >>> StandardRules.Format.hexadecimal(b"abc0123")
            (6, [[b'a', b'b'], [b'c', b'0'], [b'1', b'2']])
            >>> StandardRules.Format.hexadecimal(b"0123abc")
            (6, [[b'0', b'1'], [b'2', b'3'], [b'a', b'b']])
            >>> StandardRules.Format.hexadecimal(b"+123")
            (0, None)
            >>> StandardRules.Format.hexadecimal(b"0B2;")
            (2, [[b'0', b'B']])
            >>> StandardRules.Format.hexadecimal(b"a ")
            (0, None)
            >>>
            """

            result = PegParser.one_or_more(
                lambda d, p: PegParser.sequence(
                    [StandardMatch.is_hex, StandardMatch.is_hex],
                    d,
                    p,
                ),
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "hex"

            return result

        def octal(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method checks for a word.

            >>> StandardRules.Format.octal(b"01234567")
            (8, [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7'])
            >>> StandardRules.Format.octal(b"789")
            (1, [b'7'])
            >>> StandardRules.Format.octal(b"abc123")
            (0, None)
            >>> StandardRules.Format.octal(b"+123")
            (0, None)
            >>> StandardRules.Format.octal(b"0;B2;")
            (1, [b'0'])
            >>> StandardRules.Format.octal(b"a ")
            (0, None)
            >>>
            """

            result = PegParser.one_or_more(
                StandardMatch.is_octal,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "octal"

            return result

        def base32_insensitive(
            data: bytes, position: int = 0
        ) -> Tuple[
            int, Iterable[Union[bool, Iterable[Union[bytes, Iterable[bytes]]]]]
        ]:
            """
            This method checks for insensitive base32 format.

            >>> StandardRules.Format.base32_insensitive(b"aB======")
            (8, [[], [b'a', b'B', b'=', b'=', b'=', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32_insensitive(b"aBc2====")
            (8, [[], [b'a', b'B', b'c', b'2', b'=', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32_insensitive(b"aBc23===")
            (8, [[], [b'a', b'B', b'c', b'2', b'3', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32_insensitive(b"aBc23zt=")
            (8, [[], [b'a', b'B', b'c', b'2', b'3', b'z', b't', b'=']])
            >>> StandardRules.Format.base32_insensitive(b"aBc23zt7")
            (8, [[[b'a', b'B', b'c', b'2', b'3', b'z', b't', b'7']], True])
            >>> StandardRules.Format.base32_insensitive(b"ab")
            (0, [[], True])
            >>> StandardRules.Format.base32_insensitive(b"a1======")
            (0, [[], True])
            >>> StandardRules.Format.base32_insensitive(b"a ======")
            (0, [[], True])
            >>> StandardRules.Format.base32_insensitive(b"aBc23zt7kf======")
            (16, [[[b'a', b'B', b'c', b'2', b'3', b'z', b't', b'7']], [b'k', b'f', b'=', b'=', b'=', b'=', b'=', b'=']])
            >>>
            """

            return StandardRules.Format.base32(data, position, False, True)

        def base32_lower(
            data: bytes, position: int = 0
        ) -> Tuple[
            int, Iterable[Union[bool, Iterable[Union[bytes, Iterable[bytes]]]]]
        ]:
            """
            This method checks for lower base32 format.

            >>> StandardRules.Format.base32_lower(b"ab======")
            (8, [[], [b'a', b'b', b'=', b'=', b'=', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32_lower(b"abc2====")
            (8, [[], [b'a', b'b', b'c', b'2', b'=', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32_lower(b"abc23===")
            (8, [[], [b'a', b'b', b'c', b'2', b'3', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32_lower(b"abc23zt=")
            (8, [[], [b'a', b'b', b'c', b'2', b'3', b'z', b't', b'=']])
            >>> StandardRules.Format.base32_lower(b"abc23zt7")
            (8, [[[b'a', b'b', b'c', b'2', b'3', b'z', b't', b'7']], True])
            >>> StandardRules.Format.base32_lower(b"ab")
            (0, [[], True])
            >>> StandardRules.Format.base32_lower(b"a1======")
            (0, [[], True])
            >>> StandardRules.Format.base32_lower(b"a ======")
            (0, [[], True])
            >>> StandardRules.Format.base32_lower(b"abc23zt7kf======")
            (16, [[[b'a', b'b', b'c', b'2', b'3', b'z', b't', b'7']], [b'k', b'f', b'=', b'=', b'=', b'=', b'=', b'=']])
            >>>
            """

            return StandardRules.Format.base32(data, position, True)

        def base32(
            data: bytes,
            position: int = 0,
            lower: bool = False,
            insensitive: bool = False,
        ) -> Tuple[
            int, Iterable[Union[bool, Iterable[Union[bytes, Iterable[bytes]]]]]
        ]:
            """
            This method checks for base32 format.

            >>> StandardRules.Format.base32(b"AB======")
            (8, [[], [b'A', b'B', b'=', b'=', b'=', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32(b"ABC2====")
            (8, [[], [b'A', b'B', b'C', b'2', b'=', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32(b"ABC23===")
            (8, [[], [b'A', b'B', b'C', b'2', b'3', b'=', b'=', b'=']])
            >>> StandardRules.Format.base32(b"ABC23ZT=")
            (8, [[], [b'A', b'B', b'C', b'2', b'3', b'Z', b'T', b'=']])
            >>> StandardRules.Format.base32(b"ABC23ZT7")
            (8, [[[b'A', b'B', b'C', b'2', b'3', b'Z', b'T', b'7']], True])
            >>> StandardRules.Format.base32(b"AB")
            (0, [[], True])
            >>> StandardRules.Format.base32(b"A1======")
            (0, [[], True])
            >>> StandardRules.Format.base32(b"A ======")
            (0, [[], True])
            >>> StandardRules.Format.base32(b"ABC23ZT7KF======")
            (16, [[[b'A', b'B', b'C', b'2', b'3', b'Z', b'T', b'7']], [b'K', b'F', b'=', b'=', b'=', b'=', b'=', b'=']])
            >>>
            """

            def base32_char(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        (
                            StandardMatch.is_letter
                            if insensitive
                            else (
                                StandardMatch.is_lower
                                if lower
                                else StandardMatch.is_upper
                            )
                        ),
                        StandardMatch.or_check_chars(50, 51, 52, 53, 54, 55),
                    ],
                    data,
                    position,
                )

            def base32_chars(data: bytes, position: int):
                return PegParser.sequence(
                    [base32_char] * 8,
                    data,
                    position,
                )

            def sequence(data: bytes, position: int):
                return PegParser.zero_or_more(
                    base32_chars,
                    data,
                    position,
                )

            def wrapper_padding(x: int):
                def end_padding(data: bytes, position: int):
                    return PegParser.sequence(
                        [base32_char] * (8 - x)
                        + [StandardMatch.check_char(61)] * x,
                        data,
                        position,
                    )

                return end_padding

            def end(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        wrapper_padding(1),
                        wrapper_padding(3),
                        wrapper_padding(4),
                        wrapper_padding(6),
                        lambda d, p: PegParser.not_predicate(
                            base32_chars, d, p
                        ),
                    ],
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    sequence,
                    end,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "base32"

            return result

        def base64_urlsafe(
            data: bytes, position: int = 0
        ) -> Tuple[
            int, Iterable[Union[bool, Iterable[Union[bytes, Iterable[bytes]]]]]
        ]:
            """
            This method checks for base64 urlsafe format.

            >>> StandardRules.Format.base64_urlsafe(b'Y5==')
            (4, [[], [b'Y', b'5', b'=', b'=']])
            >>> StandardRules.Format.base64_urlsafe(b'Y5-=')
            (4, [[], [b'Y', b'5', b'-', b'=']])
            >>> StandardRules.Format.base64_urlsafe(b"Y5-_")
            (4, [[[b'Y', b'5', b'-', b'_']], True])
            >>> StandardRules.Format.base64_urlsafe(b"09AZaz-_")
            (8, [[[b'0', b'9', b'A', b'Z'], [b'a', b'z', b'-', b'_']], True])
            >>> StandardRules.Format.base64_urlsafe(b"--==")
            (4, [[], [b'-', b'-', b'=', b'=']])
            >>> StandardRules.Format.base64_urlsafe(b"___=")
            (4, [[], [b'_', b'_', b'_', b'=']])
            >>> StandardRules.Format.base64_urlsafe(b"a=")
            (0, [[], True])
            >>> StandardRules.Format.base64_urlsafe(b"a+==")
            (0, [[], True])
            >>> StandardRules.Format.base64_urlsafe(b"a/==")
            (0, [[], True])
            >>>
            """

            return StandardRules.Format.base64(data, position, True)

        def base64(
            data: bytes, position: int = 0, urlsafe: bool = False
        ) -> Tuple[
            int, Iterable[Union[bool, Iterable[Union[bytes, Iterable[bytes]]]]]
        ]:
            """
            This method checks for base64 format.

            >>> StandardRules.Format.base64(b'Y5==')
            (4, [[], [b'Y', b'5', b'=', b'=']])
            >>> StandardRules.Format.base64(b'Y5+=')
            (4, [[], [b'Y', b'5', b'+', b'=']])
            >>> StandardRules.Format.base64(b"Y5+/")
            (4, [[[b'Y', b'5', b'+', b'/']], True])
            >>> StandardRules.Format.base64(b"09AZaz+/")
            (8, [[[b'0', b'9', b'A', b'Z'], [b'a', b'z', b'+', b'/']], True])
            >>> StandardRules.Format.base64(b"++==")
            (4, [[], [b'+', b'+', b'=', b'=']])
            >>> StandardRules.Format.base64(b"///=")
            (4, [[], [b'/', b'/', b'/', b'=']])
            >>> StandardRules.Format.base64(b"a=")
            (0, [[], True])
            >>> StandardRules.Format.base64(b"a ==")
            (0, [[], True])
            >>>
            """

            def base64_char(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.is_letter,
                        StandardMatch.is_digit,
                        (
                            StandardMatch.or_check_chars(45, 95)
                            if urlsafe
                            else StandardMatch.or_check_chars(43, 47)
                        ),
                    ],
                    data,
                    position,
                )

            def base64_chars(data: bytes, position: int):
                return PegParser.sequence(
                    [base64_char] * 4,
                    data,
                    position,
                )

            def sequence(data: bytes, position: int):
                return PegParser.zero_or_more(
                    base64_chars,
                    data,
                    position,
                )

            def wrapper_padding(x: int):
                def end_padding(data: bytes, position: int):
                    return PegParser.sequence(
                        [base64_char] * (4 - x)
                        + [StandardMatch.check_char(61)] * x,
                        data,
                        position,
                    )

                return end_padding

            def end(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        wrapper_padding(1),
                        wrapper_padding(2),
                        lambda d, p: PegParser.not_predicate(
                            base64_chars, d, p
                        ),
                    ],
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    sequence,
                    end,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "base64"

            return result

        def base85(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Iterable[bytes]]]]:
            """
            This method checks for base85 format.

            >>> StandardRules.Format.base85(b'VPRomVE')
            (5, [[b'V', b'P', b'R', b'o', b'm']])
            >>> StandardRules.Format.base85(b'VPRomVPO')
            (5, [[b'V', b'P', b'R', b'o', b'm']])
            >>> StandardRules.Format.base85(b"VPRomVPRn")
            (5, [[b'V', b'P', b'R', b'o', b'm']])
            >>> StandardRules.Format.base85(b"VPRomVPRom")
            (10, [[b'V', b'P', b'R', b'o', b'm'], [b'V', b'P', b'R', b'o', b'm']])
            >>> StandardRules.Format.base85(b"VPRomVPRom``+|}{;<=>")
            (20, [[b'V', b'P', b'R', b'o', b'm'], [b'V', b'P', b'R', b'o', b'm'], [b'`', b'`', b'+', b'|', b'}'], [b'{', b';', b'<', b'=', b'>']])
            >>> StandardRules.Format.base85(b"VPRo mVPRom``+|}{;<=>")
            (0, None)
            >>>
            """

            def base85_char(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.is_letter,
                        StandardMatch.is_digit,
                        StandardMatch.or_check_chars(
                            33,
                            35,
                            36,
                            37,
                            38,
                            40,
                            41,
                            42,
                            43,
                            45,
                            59,
                            60,
                            61,
                            62,
                            63,
                            64,
                            94,
                            95,
                            96,
                            123,
                            124,
                            125,
                            126,
                        ),
                    ],
                    data,
                    position,
                )

            def base85_chars(data: bytes, position: int):
                return PegParser.sequence(
                    [base85_char] * 5,
                    data,
                    position,
                )

            result = PegParser.one_or_more(
                base85_chars,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "base85"

            return result

        def string_null_terminated_length(minimum_length: int = 3) -> Callable:
            r"""
            This function matchs null terminated string
            (like in C char* = "...") with `length` characters.

            >>> StandardRules.Format.string_null_terminated_length()(b"abcdef\0")
            (7, [b'a', b'b', b'c', [b'd', b'e', b'f'], b'\x00'])
            >>> StandardRules.Format.string_null_terminated_length(3)(b"abc\0")
            (4, [b'a', b'b', b'c', [], b'\x00'])
            >>> StandardRules.Format.string_null_terminated_length(5)(b"abc\0")
            (0, None)
            >>> StandardRules.Format.string_null_terminated_length(5)(b"a\1bcdef\0")
            (0, None)
            >>>
            """

            def string_null_terminated(
                data: bytes, position: int = 0
            ) -> Tuple[
                int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]
            ]:
                """
                This function matchs null terminated string
                (like in C char* = "...").
                """

                return PegParser.sequence(
                    [
                        *[StandardMatch.is_printable] * minimum_length,
                        lambda d, p: PegParser.zero_or_more(
                            StandardMatch.is_printable, d, p
                        ),
                        StandardMatch.check_char(0),
                    ],
                    data,
                    position,
                )

            return string_null_terminated

        def unicode_null_terminated_length(
            minimum_length: int = 3,
        ) -> Callable:
            r"""
            This function matchs null terminated string
            (like in C char* = "...") with `length` characters.

            >>> StandardRules.Format.unicode_null_terminated_length()(b"a\0b\0c\0d\0e\0f\0\0\0")
            (14, [[b'a', b'\x00'], [b'b', b'\x00'], [b'c', b'\x00'], [[b'd', b'\x00'], [b'e', b'\x00'], [b'f', b'\x00']], b'\x00', b'\x00'])
            >>> StandardRules.Format.unicode_null_terminated_length(3)(b"a\0b\0c\0\0\0")
            (8, [[b'a', b'\x00'], [b'b', b'\x00'], [b'c', b'\x00'], [], b'\x00', b'\x00'])
            >>> StandardRules.Format.unicode_null_terminated_length(5)(b"a\0b\0c\0\0\0")
            (0, None)
            >>> StandardRules.Format.unicode_null_terminated_length(5)(b"a\1b\0c\0d\0e\0f\0\0\0")
            (0, None)
            >>>
            """

            def unicode_null_terminated(
                data: bytes, position: int = 0
            ) -> Tuple[
                int,
                Union[
                    None,
                    Iterable[
                        Union[bytes, Iterable[Union[bytes, Iterable[bytes]]]]
                    ],
                ],
            ]:
                """
                This function matchs unicode terminated string
                (like in C LPWSTR = L"...").
                """

                def unicode_character(data: bytes, position: int):
                    return PegParser.sequence(
                        [
                            StandardMatch.is_printable,
                            StandardMatch.check_char(0),
                        ],
                        data,
                        position,
                    )

                return PegParser.sequence(
                    [
                        *[unicode_character] * minimum_length,
                        lambda d, p: PegParser.zero_or_more(
                            unicode_character, d, p
                        ),
                        StandardMatch.check_char(0),
                        StandardMatch.check_char(0),
                    ],
                    data,
                    position,
                )

            return unicode_null_terminated

    class Url:
        """
        This class implements methods to parse an URL.
        """

        def _characters(data, position):
            def check_url_encoding(data, position):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(37),
                        StandardMatch.is_hex,
                        StandardMatch.is_hex,
                    ],
                    data,
                    position,
                )

            def check_url_char(data, position):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.is_letter,
                        StandardMatch.is_digit,
                        StandardMatch.check_char(126),
                        StandardMatch.check_char(95),
                        StandardMatch.check_char(45),
                        StandardMatch.check_char(46),
                        StandardMatch.check_char(43),
                        check_url_encoding,
                    ],
                    data,
                    position,
                )

            return PegParser.zero_or_more(
                check_url_char,
                data,
                position,
            )

        def _characters_subdelims_colon(data, position):
            return PegParser.ordered_choice(
                [
                    StandardMatch.or_check_chars(
                        33, 36, 38, 39, 40, 41, 42, 43, 44, 58, 59, 61
                    ),
                    StandardRules.Url._characters,
                ],
                data,
                position,
            )

        def _character_subdelims_colon_commat(data, position):
            return PegParser.ordered_choice(
                [
                    StandardMatch.or_check_chars(
                        33, 36, 38, 39, 40, 41, 42, 43, 44, 58, 61, 64
                    ),
                    StandardRules.Url._characters,
                ],
                data,
                position,
            )

        def _character_subdelims_colon_commat_slot_quest(data, position):
            return PegParser.ordered_choice(
                [
                    StandardMatch.or_check_chars(
                        33,
                        36,
                        38,
                        39,
                        40,
                        41,
                        42,
                        43,
                        44,
                        58,
                        59,
                        61,
                        64,
                        47,
                        63,
                    ),
                    StandardRules.Url._characters,
                ],
                data,
                position,
            )

        def _characters_subdelims_colon_commat(data, position):
            return PegParser.one_or_more(
                StandardRules.Url._character_subdelims_colon_commat,
                data,
                position,
            )

        def _optional_characters_subdelims_colon_commat(data, position):
            return PegParser.zero_or_more(
                StandardRules.Url._character_subdelims_colon_commat,
                data,
                position,
            )

        def _optional_characters_subdelims_colon_commat_slot_quest(
            data, position
        ):
            return PegParser.zero_or_more(
                StandardRules.Url._character_subdelims_colon_commat_slot_quest,
                data,
                position,
            )

        def _base_path(data: int, position: int):
            return PegParser.sequence(
                [
                    StandardMatch.check_char(47),
                    StandardRules.Url._optional_characters_subdelims_colon_commat,
                ],
                data,
                position,
            )

        def path_rootless(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Iterable[Iterable[Union[bytes, Iterable[Iterable[bytes]]]]]
                ],
            ],
        ]:
            """
            This method checks path root-less.

            >>> StandardRules.Url.path_rootless(b"abc/def.")
            (8, [[[b'a', b'b', b'c']], [[b'/', [[b'd', b'e', b'f', b'.']]]]])
            >>> StandardRules.Url.path_rootless(b"abc?/def")
            (3, [[[b'a', b'b', b'c']], []])
            >>> StandardRules.Url.path_rootless(b"a-bc#/def")
            (4, [[[b'a', b'-', b'b', b'c']], []])
            >>> StandardRules.Url.path_rootless(b"a_bc%25/def")
            (11, [[[b'a', b'_', b'b', b'c', [b'%', b'2', b'5']]], [[b'/', [[b'd', b'e', b'f']]]]])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Url._characters_subdelims_colon_commat,
                    lambda d, p: PegParser.zero_or_more(
                        StandardRules.Url._base_path, d, p
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "path"

            return result

        def path(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Iterable[
                        Union[
                            bytes,
                            Iterable[
                                Union[
                                    bytes,
                                    Iterable[Union[bytes, Iterable[bytes]]],
                                ]
                            ],
                        ]
                    ]
                ],
            ],
        ]:
            """
            This method checks URL path.

            >>> StandardRules.Url.path(b"/abc/def.")
            (9, [[b'/', [[b'a', b'b', b'c']]], [b'/', [[b'd', b'e', b'f', b'.']]]])
            >>> StandardRules.Url.path(b"/abc?/def")
            (4, [[b'/', [[b'a', b'b', b'c']]]])
            >>> StandardRules.Url.path(b"/a-bc#/def")
            (5, [[b'/', [[b'a', b'-', b'b', b'c']]]])
            >>> StandardRules.Url.path(b"/a_bc%25/def")
            (12, [[b'/', [[b'a', b'_', b'b', b'c', [b'%', b'2', b'5']]]], [b'/', [[b'd', b'e', b'f']]]])
            >>> StandardRules.Url.path(b"/a~bc%2F/def")
            (12, [[b'/', [[b'a', b'~', b'b', b'c', [b'%', b'2', b'F']]]], [b'/', [[b'd', b'e', b'f']]]])
            >>> StandardRules.Url.path(b"//def")
            (5, [[b'/', []], [b'/', [[b'd', b'e', b'f']]]])
            >>> StandardRules.Url.path(b"/abc%2/def")
            (4, [[b'/', [[b'a', b'b', b'c']]]])
            >>> StandardRules.Url.path(b"/abc%/def")
            (4, [[b'/', [[b'a', b'b', b'c']]]])
            >>> StandardRules.Url.path(b"/")
            (1, [[b'/', []]])
            >>> StandardRules.Url.path(b"/c=test")
            (7, [[b'/', [[b'c'], b'=', [b't', b'e', b's', b't']]]])
            >>> StandardRules.Url.path(b"")
            (0, None)
            >>>
            """

            result = PegParser.one_or_more(
                StandardRules.Url._base_path,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "path"

            return result

        def form_data(data: bytes, position: int = 0) -> Tuple[
            int,
            Iterable[
                Iterable[Union[bytes, Iterable[Union[bytes, Iterable[bytes]]]]]
            ],
        ]:
            """
            This method checks the form data format used in POST
            body and GET query.

            >>> StandardRules.Url.form_data(b"abc=def&def=abc")
            (15, [[[b'a', b'b', b'c'], b'=', [b'd', b'e', b'f']], [[b'&', [[b'd', b'e', b'f'], b'=', [b'a', b'b', b'c']]]]])
            >>> StandardRules.Url.form_data(b"abc")
            (3, [[b'a', b'b', b'c'], []])
            >>> StandardRules.Url.form_data(b"abc&def")
            (7, [[b'a', b'b', b'c'], [[b'&', [b'd', b'e', b'f']]]])
            >>> StandardRules.Url.form_data(b"&def=abc")
            (8, [[], [[b'&', [[b'd', b'e', b'f'], b'=', [b'a', b'b', b'c']]]]])
            >>> StandardRules.Url.form_data(b"&def?=abc")
            (4, [[], [[b'&', [b'd', b'e', b'f']]]])
            >>> StandardRules.Url.form_data(b"&def;")
            (4, [[], [[b'&', [b'd', b'e', b'f']]]])
            >>> StandardRules.Url.form_data(b"/abc%/def")
            (0, [[], []])
            >>> StandardRules.Url.form_data(b"+")
            (1, [[b'+'], []])
            >>>
            """

            def named_value(data, position):
                return PegParser.sequence(
                    [
                        StandardRules.Url._characters,
                        StandardMatch.check_char(61),
                        StandardRules.Url._characters,
                    ],
                    data,
                    position,
                )

            def value_or_named_value(data, position):
                return PegParser.ordered_choice(
                    [
                        named_value,
                        StandardRules.Url._characters,
                    ],
                    data,
                    position,
                )

            def separator_and_value(data, position):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(38),
                        value_or_named_value,
                    ],
                    data,
                    position,
                )

            def separators_and_values(data, position):
                return PegParser.zero_or_more(
                    separator_and_value,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    value_or_named_value,
                    separators_and_values,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "form_data"

            return result

        def query(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                bool,
                Iterable[
                    Union[
                        bytes,
                        Iterable[
                            Union[
                                bytes, Iterable[Union[bytes, Iterable[bytes]]]
                            ]
                        ],
                    ]
                ],
            ],
        ]:
            """
            This method checks URL query.

            >>> StandardRules.Url.query(b"?abc=def&def=abc")
            (16, [b'?', [[b'a', b'b', b'c'], b'=', [b'd', b'e', b'f'], b'&', [b'd', b'e', b'f'], b'=', [b'a', b'b', b'c']]])
            >>> StandardRules.Url.query(b"?abc%25")
            (7, [b'?', [[b'a', b'b', b'c', [b'%', b'2', b'5']]]])
            >>> StandardRules.Url.query(b"?abc&def")
            (8, [b'?', [[b'a', b'b', b'c'], b'&', [b'd', b'e', b'f']]])
            >>> StandardRules.Url.query(b"?")
            (1, [b'?', []])
            >>> StandardRules.Url.query(b"?&def=abc")
            (9, [b'?', [b'&', [b'd', b'e', b'f'], b'=', [b'a', b'b', b'c']]])
            >>> StandardRules.Url.query(b"?&def?=abc")
            (10, [b'?', [b'&', [b'd', b'e', b'f'], b'?', b'=', [b'a', b'b', b'c']]])
            >>> StandardRules.Url.query(b"&def;")
            (0, True)
            >>> StandardRules.Url.query(b"/abc%/def")
            (0, True)
            >>> StandardRules.Url.query(b"+")
            (0, True)
            >>>
            """

            def check_query(data, position):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(63),
                        StandardRules.Url._optional_characters_subdelims_colon_commat_slot_quest,
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    check_query,
                    lambda d, p: PegParser.not_predicate(
                        StandardMatch.check_char(63), d, p
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "query"

            return result

        def parameters(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                bool,
                Iterable[
                    Union[
                        bytes,
                        Iterable[
                            Iterable[
                                Union[
                                    bytes,
                                    Iterable[
                                        Union[
                                            bytes,
                                            Iterable[
                                                Union[bytes, Iterable[bytes]]
                                            ],
                                        ]
                                    ],
                                ]
                            ]
                        ],
                    ]
                ],
            ],
        ]:
            """
            This method checks URL parameters.

            >>> StandardRules.Url.parameters(b";abc=def&def=abc")
            (16, [b';', [[[b'a', b'b', b'c'], b'=', [b'd', b'e', b'f']], [[b'&', [[b'd', b'e', b'f'], b'=', [b'a', b'b', b'c']]]]]])
            >>> StandardRules.Url.parameters(b";abc")
            (4, [b';', [[b'a', b'b', b'c'], []]])
            >>> StandardRules.Url.parameters(b";abc&def")
            (8, [b';', [[b'a', b'b', b'c'], [[b'&', [b'd', b'e', b'f']]]]])
            >>> StandardRules.Url.parameters(b";")
            (1, [b';', [[], []]])
            >>> StandardRules.Url.parameters(b";&def=abc")
            (9, [b';', [[], [[b'&', [[b'd', b'e', b'f'], b'=', [b'a', b'b', b'c']]]]]])
            >>> StandardRules.Url.parameters(b";&def;=abc")
            (5, [b';', [[], [[b'&', [b'd', b'e', b'f']]]]])
            >>> StandardRules.Url.parameters(b"&def;")
            (0, True)
            >>> StandardRules.Url.parameters(b"/abc%/def")
            (0, True)
            >>> StandardRules.Url.parameters(b"+")
            (0, True)
            >>>
            """

            def check_parameters(data, position):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(59),
                        StandardRules.Url.form_data,
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    check_parameters,
                    lambda d, p: PegParser.not_predicate(
                        StandardMatch.check_char(59), d, p
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "parameters"

            return result

        def fragment(
            data: bytes, position: int = 0
        ) -> Tuple[
            int, Union[bool, Iterable[Union[bytes, Iterable[Iterable[bytes]]]]]
        ]:
            """
            This method checks URL fragment.

            >>> StandardRules.Url.fragment(b"#AZaz09-_.~+")
            (12, [b'#', [[b'A', b'Z', b'a', b'z', b'0', b'9', b'-', b'_', b'.', b'~', b'+']]])
            >>> StandardRules.Url.fragment(b"AZaz09-_.~")
            (0, True)
            >>> StandardRules.Url.fragment(b"!$&'()*,;=:@/?")
            (0, True)
            >>> StandardRules.Url.fragment(b"#")
            (1, [b'#', []])
            >>>
            """

            def check_fragment(data, position):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(35),
                        StandardRules.Url._optional_characters_subdelims_colon_commat_slot_quest,
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    check_fragment,
                    lambda d, p: PegParser.not_predicate(
                        StandardMatch.check_char(35), d, p
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "fragment"

            return result

        def full(data: bytes, position: int = 0):
            """
            This method parses the full URL.

            >>> StandardRules.Url.full(b"https://my.full.url/with/path;and=parameters?query=too#fragment")
            (63, [[b'h', [b't', b't', b'p', b's']], b':', [b'/', b'/', [[b'm', [b'y']], [[b'.', [b'f', [b'u', b'l', b'l']]], [b'.', [b'u', [b'r', b'l']]]]], [[b'/', [[b'w', b'i', b't', b'h']]], [b'/', [[b'p', b'a', b't', b'h']]]]], [b';', [[[b'a', b'n', b'd'], b'=', [b'p', b'a', b'r', b'a', b'm', b'e', b't', b'e', b'r', b's']], []]], [b'?', [[b'q', b'u', b'e', b'r', b'y'], b'=', [b't', b'o', b'o']]], [b'#', [[b'f', b'r', b'a', b'g', b'm', b'e', b'n', b't']]]])
            >>> StandardRules.Url.full(b"http://www.ics.uci.edu/pub/ietf/uri/#Related")
            (44, [[b'h', [b't', b't', b'p']], b':', [b'/', b'/', [[b'w', [b'w', b'w']], [[b'.', [b'i', [b'c', b's']]], [b'.', [b'u', [b'c', b'i']]], [b'.', [b'e', [b'd', b'u']]]]], [[b'/', [[b'p', b'u', b'b']]], [b'/', [[b'i', b'e', b't', b'f']]], [b'/', [[b'u', b'r', b'i']]], [b'/', []]]], True, True, [b'#', [[b'R', b'e', b'l', b'a', b't', b'e', b'd']]]])
            >>> StandardRules.Url.full(b"ftp://ftp.is.co.za/rfc/rfc1808.txt")
            (34, [[b'f', [b't', b'p']], b':', [b'/', b'/', [[b'f', [b't', b'p']], [[b'.', [b'i', [b's']]], [b'.', [b'c', [b'o']]], [b'.', [b'z', [b'a']]]]], [[b'/', [[b'r', b'f', b'c']]], [b'/', [[b'r', b'f', b'c', b'1', b'8', b'0', b'8', b'.', b't', b'x', b't']]]]], True, True, True])
            >>> StandardRules.Url.full(b"http://www.ietf.org/rfc/rfc2396.txt")
            (35, [[b'h', [b't', b't', b'p']], b':', [b'/', b'/', [[b'w', [b'w', b'w']], [[b'.', [b'i', [b'e', b't', b'f']]], [b'.', [b'o', [b'r', b'g']]]]], [[b'/', [[b'r', b'f', b'c']]], [b'/', [[b'r', b'f', b'c', b'2', b'3', b'9', b'6', b'.', b't', b'x', b't']]]]], True, True, True])
            >>> StandardRules.Url.full(b"ldap://[2001:db8::7]/c=GB?objectClass?one")
            (41, [[b'l', [b'd', b'a', b'p']], b':', [b'/', b'/', [b'[', [[[b'2', b'0', b'0', b'1'], b':'], [b'd', b'b', b'8'], b':', b':', b'7'], b']'], [[b'/', [[b'c'], b'=', [b'G', b'B']]]]], True, [b'?', [[b'o', b'b', b'j', b'e', b'c', b't', b'C', b'l', b'a', b's', b's'], b'?', [b'o', b'n', b'e']]], True])
            >>> StandardRules.Url.full(b"mailto:John.Doe@example.com")
            (27, [[b'm', [b'a', b'i', b'l', b't', b'o']], b':', [[[b'J', b'o', b'h', b'n', b'.', b'D', b'o', b'e'], b'@', [b'e', b'x', b'a', b'm', b'p', b'l', b'e', b'.', b'c', b'o', b'm']], []], True, True, True])
            >>> StandardRules.Url.full(b"news:comp.infosystems.www.servers.unix")
            (38, [[b'n', [b'e', b'w', b's']], b':', [[[b'c', b'o', b'm', b'p', b'.', b'i', b'n', b'f', b'o', b's', b'y', b's', b't', b'e', b'm', b's', b'.', b'w', b'w', b'w', b'.', b's', b'e', b'r', b'v', b'e', b'r', b's', b'.', b'u', b'n', b'i', b'x']], []], True, True, True])
            >>> StandardRules.Url.full(b"tel:+1-816-555-1212")
            (19, [[b't', [b'e', b'l']], b':', [[b'+', [b'1', b'-', b'8', b'1', b'6', b'-', b'5', b'5', b'5', b'-', b'1', b'2', b'1', b'2']], []], True, True, True])
            >>> StandardRules.Url.full(b"telnet://192.0.2.16:80/")
            (23, [[b't', [b'e', b'l', b'n', b'e', b't']], b':', [b'/', b'/', [[[b'1', [b'9', b'2']], [[b'.', [b'0', []]], [b'.', [b'2', []]], [b'.', [b'1', [b'6']]]]], b':', [b'8', b'0']], [[b'/', []]]], True, True, True])
            >>> StandardRules.Url.full(b"urn:oasis:names:specification:docbook:dtd:xml:4.1.2")
            (51, [[b'u', [b'r', b'n']], b':', [[[b'o', b'a', b's', b'i', b's'], b':', [b'n', b'a', b'm', b'e', b's'], b':', [b's', b'p', b'e', b'c', b'i', b'f', b'i', b'c', b'a', b't', b'i', b'o', b'n'], b':', [b'd', b'o', b'c', b'b', b'o', b'o', b'k'], b':', [b'd', b't', b'd'], b':', [b'x', b'm', b'l'], b':', [b'4', b'.', b'1', b'.', b'2']], []], True, True, True])
            >>>
            """

            def autority(data, position):
                return PegParser.ordered_choice(
                    [
                        lambda d, p: PegParser.sequence(
                            [
                                StandardRules.Network.user_info,
                                StandardMatch.check_char(64),
                                StandardRules.Network.host_port,
                            ],
                            d,
                            p,
                        ),
                        lambda d, p: PegParser.sequence(
                            [
                                StandardRules.Network.user_info,
                                StandardMatch.check_char(64),
                                StandardRules.Network.host,
                            ],
                            d,
                            p,
                        ),
                        StandardRules.Network.host_port,
                        StandardRules.Network.host,
                    ],
                    data,
                    position,
                )

            def autority_path(data, position):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(47),
                        StandardMatch.check_char(47),
                        autority,
                        StandardRules.Url.path,
                    ],
                    data,
                    position,
                )

            def hier_part(data, position):
                return PegParser.ordered_choice(
                    [
                        autority_path,
                        StandardRules.Url.path,
                        StandardRules.Url.path_rootless,
                        lambda d, p: PegParser.not_predicate(
                            StandardMatch.check_char(47), d, p
                        ),
                    ],
                    data,
                    position,
                )

            def _full_choice(*methods):
                def choice(data, position):
                    return PegParser.sequence(
                        [
                            StandardRules.Url.scheme,
                            StandardMatch.check_char(58),
                            hier_part,
                            *methods,
                        ],
                        data,
                        position,
                    )

                return choice

            result = PegParser.ordered_choice(
                [
                    _full_choice(
                        StandardRules.Url.parameters,
                        StandardRules.Url.query,
                        StandardRules.Url.fragment,
                    ),
                    _full_choice(
                        StandardRules.Url.parameters, StandardRules.Url.query
                    ),
                    _full_choice(
                        StandardRules.Url.parameters,
                        StandardRules.Url.fragment,
                    ),
                    _full_choice(StandardRules.Url.parameters),
                    _full_choice(
                        StandardRules.Url.query, StandardRules.Url.fragment
                    ),
                    _full_choice(StandardRules.Url.query),
                    _full_choice(StandardRules.Url.fragment),
                    _full_choice(),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "url"

            return result

        def scheme(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]]:
            """
            This method checks URL scheme.

            >>> StandardRules.Url.scheme(b"http")
            (4, [b'h', [b't', b't', b'p']])
            >>> StandardRules.Url.scheme(b"git+ssh")
            (7, [b'g', [b'i', b't', b'+', b's', b's', b'h']])
            >>> StandardRules.Url.scheme(b"gopher")
            (6, [b'g', [b'o', b'p', b'h', b'e', b'r']])
            >>> StandardRules.Url.scheme(b"itms-services")
            (13, [b'i', [b't', b'm', b's', b'-', b's', b'e', b'r', b'v', b'i', b'c', b'e', b's']])
            >>> StandardRules.Url.scheme(b"TEST.0tEst9")
            (11, [b'T', [b'E', b'S', b'T', b'.', b'0', b't', b'E', b's', b't', b'9']])
            >>> StandardRules.Url.scheme(b"TEST,0tEst9")
            (4, [b'T', [b'E', b'S', b'T']])
            >>>
            """

            def character(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.is_letter,
                        StandardMatch.is_digit,
                        StandardMatch.or_check_chars(43, 45, 46),
                    ],
                    data,
                    position,
                )

            def characters(data: bytes, position: int):
                return PegParser.zero_or_more(
                    character,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    StandardMatch.is_letter,
                    characters,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "scheme"

            return result

    class Network:
        """
        This class implements methods to parse Network formats and data.
        """

        def hostname(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Union[
                        bytes,
                        Iterable[
                            Union[
                                bytes, Iterable[Union[bytes, Iterable[bytes]]]
                            ]
                        ],
                    ]
                ],
            ],
        ]:
            """
            This method parses hostnames value.

            >>> StandardRules.Network.hostname(b"test")
            (4, [b't', [b'e', b's', b't']])
            >>> StandardRules.Network.hostname(b"test-abc")
            (8, [b't', [b'e', b's', b't', [[b'-'], b'a'], b'b', b'c']])
            >>> StandardRules.Network.hostname(b"a")
            (1, [b'a', []])
            >>> StandardRules.Network.hostname(b"test-ABC456")
            (11, [b't', [b'e', b's', b't', [[b'-'], b'A'], b'B', b'C', b'4', b'5', b'6']])
            >>> StandardRules.Network.hostname(b"6test")
            (5, [b'6', [b't', b'e', b's', b't']])
            >>> StandardRules.Network.hostname(b"6test-")
            (5, [b'6', [b't', b'e', b's', b't']])
            >>> StandardRules.Network.hostname(b"-6test")
            (0, None)
            >>>
            """

            def first_last(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.is_letter,
                        StandardMatch.is_digit,
                    ],
                    data,
                    position,
                )

            def minus(data: bytes, position: int):
                return PegParser.one_or_more(
                    StandardMatch.check_char(45),
                    data,
                    position,
                )

            def minus_match(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        minus,
                        first_last,
                    ],
                    data,
                    position,
                )

            def character(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        first_last,
                        minus_match,
                    ],
                    data,
                    position,
                )

            def characters(data: bytes, position: int):
                return PegParser.zero_or_more(
                    character,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    first_last,
                    characters,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "hostname"

            return result

        def fqdn(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Iterable[
                        Union[
                            bytes,
                            Iterable[
                                Union[
                                    bytes,
                                    Iterable[
                                        Union[
                                            bytes,
                                            Iterable[
                                                Union[
                                                    bytes,
                                                    Iterable[
                                                        Union[
                                                            bytes,
                                                            Iterable[bytes],
                                                        ]
                                                    ],
                                                ]
                                            ],
                                        ]
                                    ],
                                ]
                            ],
                        ]
                    ]
                ],
            ],
        ]:
            """
            This method parses the FQDN format.

            >>> StandardRules.Network.fqdn(b"test012.abc.com")
            (15, [[b't', [b'e', b's', b't', b'0', b'1', b'2']], [[b'.', [b'a', [b'b', b'c']]], [b'.', [b'c', [b'o', b'm']]]]])
            >>> StandardRules.Network.fqdn(b"test012.abc-def.com")
            (19, [[b't', [b'e', b's', b't', b'0', b'1', b'2']], [[b'.', [b'a', [b'b', b'c', [[b'-'], b'd'], b'e', b'f']]], [b'.', [b'c', [b'o', b'm']]]]])
            >>> StandardRules.Network.fqdn(b".test012.abc-def.com")
            (0, None)
            >>> StandardRules.Network.fqdn(b"test012.abc-def.com.")
            (19, [[b't', [b'e', b's', b't', b'0', b'1', b'2']], [[b'.', [b'a', [b'b', b'c', [[b'-'], b'd'], b'e', b'f']]], [b'.', [b'c', [b'o', b'm']]]]])
            >>> StandardRules.Network.fqdn(b"-test012.abc-def.com")
            (0, None)
            >>> StandardRules.Network.fqdn(b"test012.abc-def.com-")
            (19, [[b't', [b'e', b's', b't', b'0', b'1', b'2']], [[b'.', [b'a', [b'b', b'c', [[b'-'], b'd'], b'e', b'f']]], [b'.', [b'c', [b'o', b'm']]]]])
            >>> StandardRules.Network.fqdn(b"012test.abc-def.com-")
            (19, [[b'0', [b'1', b'2', b't', b'e', b's', b't']], [[b'.', [b'a', [b'b', b'c', [[b'-'], b'd'], b'e', b'f']]], [b'.', [b'c', [b'o', b'm']]]]])
            >>>
            """

            def dot_hostname(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(46),
                        StandardRules.Network.hostname,
                    ],
                    data,
                    position,
                )

            def dot_hostnames(data: bytes, position: int):
                return PegParser.one_or_more(
                    dot_hostname,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    StandardRules.Network.hostname,
                    dot_hostnames,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "fqdn"

            return result

        def ipv6(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Union[bytes, Iterable[Union[bytes, Iterable[bytes]]]]
                ],
            ],
        ]:
            """
            This method parses IPv6 formats.

            >>> StandardRules.Network.ipv6(b":1:")
            (0, None)
            >>> StandardRules.Network.ipv6(b"2:1:3")
            (0, None)
            >>> StandardRules.Network.ipv6(b"5:4:2:1:3")
            (0, None)
            >>> StandardRules.Network.ipv6(b"::")
            (2, [b':', b':'])
            >>> StandardRules.Network.ipv6(b"::1")
            (3, [b':', b':', b'1'])
            >>> StandardRules.Network.ipv6(b"::1:2")
            (5, [b':', b':', [b'1', b':'], b'2'])
            >>> StandardRules.Network.ipv6(b"::1:2:3")
            (7, [b':', b':', [b'1', b':'], [b'2', b':'], b'3'])
            >>> StandardRules.Network.ipv6(b"1::2:3:4:5")
            (10, [b'1', b':', b':', [b'2', b':'], [b'3', b':'], [b'4', b':'], b'5'])
            >>> StandardRules.Network.ipv6(b"1:2::3:4:5")
            (10, [[b'1', b':'], b'2', b':', b':', [b'3', b':'], [b'4', b':'], b'5'])
            >>> StandardRules.Network.ipv6(b"1:2:3::4:5")
            (10, [[b'1', b':'], [b'2', b':'], b'3', b':', b':', [b'4', b':'], b'5'])
            >>> StandardRules.Network.ipv6(b"1:2:3:4::5")
            (10, [[b'1', b':'], [b'2', b':'], [b'3', b':'], b'4', b':', b':', b'5'])
            >>> StandardRules.Network.ipv6(b"1:2:3:4:5::")
            (11, [[b'1', b':'], [b'2', b':'], [b'3', b':'], [b'4', b':'], b'5', b':', b':'])
            >>> StandardRules.Network.ipv6(b"f09f:9af9:a09a::0af0:0b2c")
            (25, [[[b'f', b'0', b'9', b'f'], b':'], [[b'9', b'a', b'f', b'9'], b':'], [b'a', b'0', b'9', b'a'], b':', b':', [[b'0', b'a', b'f', b'0'], b':'], [b'0', b'b', b'2', b'c']])
            >>> StandardRules.Network.ipv6(b"0090:9009:0090::0000:0000")
            (25, [[[b'0', b'0', b'9', b'0'], b':'], [[b'9', b'0', b'0', b'9'], b':'], [b'0', b'0', b'9', b'0'], b':', b':', [[b'0', b'0', b'0', b'0'], b':'], [b'0', b'0', b'0', b'0']])
            >>> StandardRules.Network.ipv6(b"0:9:0::0:0")
            (10, [[b'0', b':'], [b'9', b':'], b'0', b':', b':', [b'0', b':'], b'0'])
            >>> StandardRules.Network.ipv6(b"2001:0db8:0000:0000:0000:ff00:0042:8329")
            (39, [[[b'2', b'0', b'0', b'1'], b':'], [[b'0', b'd', b'b', b'8'], b':'], [[b'0', b'0', b'0', b'0'], b':'], [[b'0', b'0', b'0', b'0'], b':'], [[b'0', b'0', b'0', b'0'], b':'], [[b'f', b'f', b'0', b'0'], b':'], [[b'0', b'0', b'4', b'2'], b':'], [b'8', b'3', b'2', b'9']])
            >>>
            """

            def hex_generator(x: int):
                def hex(data: bytes, position: int):
                    return PegParser.sequence(
                        [StandardMatch.is_hex] * x,
                        data,
                        position,
                    )

                return hex

            def hex_group(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        hex_generator(4),
                        hex_generator(3),
                        hex_generator(2),
                        StandardMatch.is_hex,
                    ],
                    data,
                    position,
                )

            def hex_dots(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        hex_group,
                        StandardMatch.check_char(58),
                    ],
                    data,
                    position,
                )

            def groups_generator(x: int, y: int):
                def groups(data: bytes, position: int):
                    return PegParser.sequence(
                        (([hex_dots] * (x - 1) + [hex_group]) if x else [])
                        + (
                            []
                            if x == 8
                            else [
                                StandardMatch.check_char(58),
                                StandardMatch.check_char(58),
                            ]
                        )
                        + (([hex_dots] * (y - 1) + [hex_group]) if y else []),
                        data,
                        position,
                    )

                return groups

            def generate_groups():
                groups = [groups_generator(8, 0)]
                for a in range(7, -1, -1):
                    b = 7 - a
                    while b >= 0:
                        groups.append(groups_generator(a, b))
                        # groups.append(groups_generator(b, a))
                        b -= 1
                return groups

            result = PegParser.ordered_choice(
                generate_groups(),
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "ipv6"

            return result

        def ipv6_zoneid(data: bytes, position: int = 0) -> Tuple[
            int,
            Iterable[
                Union[
                    bytes,
                    Iterable[
                        Union[bytes, Iterable[Union[bytes, Iterable[bytes]]]]
                    ],
                ]
            ],
        ]:
            """
            This method parses IPv6 with Zone ID.

            >>> StandardRules.Network.ipv6_zoneid(b"::1%eth0")
            (8, [[b':', b':', b'1'], b'%', [[b'e', b't', b'h', b'0']]])
            >>> StandardRules.Network.ipv6_zoneid(b"::1%0")
            (5, [[b':', b':', b'1'], b'%', [[b'0']]])
            >>> StandardRules.Network.ipv6_zoneid(b"::1%9")
            (5, [[b':', b':', b'1'], b'%', [[b'9']]])
            >>> StandardRules.Network.ipv6_zoneid(b"::1%259")
            (7, [[b':', b':', b'1'], [b'%', b'2', b'5'], [[b'9']]])
            >>> StandardRules.Network.ipv6_zoneid(b"::1%250")
            (7, [[b':', b':', b'1'], [b'%', b'2', b'5'], [[b'0']]])
            >>> StandardRules.Network.ipv6_zoneid(b"::1%25eth0")
            (10, [[b':', b':', b'1'], [b'%', b'2', b'5'], [[b'e', b't', b'h', b'0']]])
            >>> StandardRules.Network.ipv6_zoneid(b"::1%eth0-_~.test")
            (16, [[b':', b':', b'1'], b'%', [[b'e', b't', b'h', b'0', b'-', b'_', b'~', b'.', b't', b'e', b's', b't']]])
            >>> StandardRules.Network.ipv6_zoneid(b"::1%eth0-_~.#test")
            (12, [[b':', b':', b'1'], b'%', [[b'e', b't', b'h', b'0', b'-', b'_', b'~', b'.']]])
            >>>
            """

            def start(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        lambda d, p: PegParser.sequence(
                            [
                                StandardMatch.check_char(37),
                                StandardMatch.check_char(50),
                                StandardMatch.check_char(53),
                            ],
                            d,
                            p,
                        ),
                        StandardMatch.check_char(37),
                    ],
                    data,
                    position,
                )

            def character(data: bytes, position: int):
                return PegParser.one_or_more(
                    StandardRules.Url._characters,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    StandardRules.Network.ipv6,
                    start,
                    character,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "ipv6_zoneid"

            return result

        def ipv4(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]]:
            """
            This method parses IPv4 format.

            >>> StandardRules.Network.ipv4(b"256.256.256.256")
            (0, None)
            >>> StandardRules.Network.ipv4(b"310.200.200.200")
            (0, None)
            >>> StandardRules.Network.ipv4(b"255.255.255.255")
            (15, [[b'2', b'5', b'5'], b'.', [b'2', b'5', b'5'], b'.', [b'2', b'5', b'5'], b'.', [b'2', b'5', b'5']])
            >>> StandardRules.Network.ipv4(b"249.230.225.212")
            (15, [[b'2', b'4', b'9'], b'.', [b'2', b'3', b'0'], b'.', [b'2', b'2', b'5'], b'.', [b'2', b'1', b'2']])
            >>> StandardRules.Network.ipv4(b"199.130.125.112")
            (15, [[b'1', b'9', b'9'], b'.', [b'1', b'3', b'0'], b'.', [b'1', b'2', b'5'], b'.', [b'1', b'1', b'2']])
            >>> StandardRules.Network.ipv4(b"1.1.1.1")
            (7, [b'1', b'.', b'1', b'.', b'1', b'.', b'1'])
            >>> StandardRules.Network.ipv4(b"0.0.0.0")
            (7, [b'0', b'.', b'0', b'.', b'0', b'.', b'0'])
            >>> StandardRules.Network.ipv4(b"10.20.80.90")
            (11, [[b'1', b'0'], b'.', [b'2', b'0'], b'.', [b'8', b'0'], b'.', [b'9', b'0']])
            >>> StandardRules.Network.ipv4(b".20.80.90")
            (0, None)
            >>> StandardRules.Network.ipv4(b"10.20.80.")
            (0, None)
            >>> StandardRules.Network.ipv4(b"10.20..80.90")
            (0, None)
            >>> StandardRules.Network.ipv4(b"10.20.80.1110")
            (12, [[b'1', b'0'], b'.', [b'2', b'0'], b'.', [b'8', b'0'], b'.', [b'1', b'1', b'1']])
            >>>
            """

            def digit250(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(50),
                        StandardMatch.check_char(53),
                        StandardMatch.or_check_chars(48, 49, 50, 51, 52, 53),
                    ],
                    data,
                    position,
                )

            def digit200(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(50),
                        StandardMatch.or_check_chars(48, 49, 50, 51, 52),
                        StandardMatch.is_digit,
                    ],
                    data,
                    position,
                )

            def digit100(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(49),
                        StandardMatch.is_digit,
                        StandardMatch.is_digit,
                    ],
                    data,
                    position,
                )

            def digit3(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        digit250,
                        digit200,
                        digit100,
                    ],
                    data,
                    position,
                )

            def digit2(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.is_digit,
                        StandardMatch.is_digit,
                    ],
                    data,
                    position,
                )

            def digits(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        digit3,
                        digit2,
                        StandardMatch.is_digit,
                    ],
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    digits,
                    StandardMatch.check_char(46),
                    digits,
                    StandardMatch.check_char(46),
                    digits,
                    StandardMatch.check_char(46),
                    digits,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "ipv4"

            return result

        def ipvfuture(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]]:
            """
            This method parses the IPvFuture.

            >>> StandardRules.Network.ipvfuture(b"v0123456789abcdef.any_characters-including&$(exploit)'&&exploit")
            (63, [b'v', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'a', b'b', b'c', b'd', b'e', b'f'], b'.', [[b'a', b'n', b'y', b'_', b'c', b'h', b'a', b'r', b'a', b'c', b't', b'e', b'r', b's', b'-', b'i', b'n', b'c', b'l', b'u', b'd', b'i', b'n', b'g'], b'&', b'$', b'(', [b'e', b'x', b'p', b'l', b'o', b'i', b't'], b')', b"'", b'&', b'&', [b'e', b'x', b'p', b'l', b'o', b'i', b't']]])
            >>> StandardRules.Network.ipvfuture(b"0123456789abcdef.any_characters-including&$(exploit)'&&exploit")
            (0, None)
            >>> StandardRules.Network.ipvfuture(b"v.any_characters-including&$(exploit)'&&exploit")
            (0, None)
            >>> StandardRules.Network.ipvfuture(b"v0123456789abcdefany_characters-including&$(exploit)'&&exploit")
            (0, None)
            >>> StandardRules.Network.ipvfuture(b"v0123456789abcdef.?any_characters-including&$(exploit)'&&exploit")
            (0, None)
            >>> StandardRules.Network.ipvfuture(b"v0123456789abcdef.%25")
            (21, [b'v', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'a', b'b', b'c', b'd', b'e', b'f'], b'.', [[[b'%', b'2', b'5']]]])
            >>> StandardRules.Network.ipvfuture(b"v0123456789abcdef.%2")
            (0, None)
            >>>
            """

            def characters(data, position):
                return PegParser.one_or_more(
                    StandardRules.Url._characters_subdelims_colon,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(118),
                    StandardRules.Format.hex,
                    StandardMatch.check_char(46),
                    characters,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "ipvfuture"

            return result

        def host(data: bytes, position: int = 0) -> Tuple[
            int,
            Iterable[
                Union[
                    bytes,
                    Iterable[
                        Iterable[
                            Union[
                                bytes, Iterable[Union[bytes, Iterable[bytes]]]
                            ]
                        ]
                    ],
                ]
            ],
        ]:
            """
            This method parses the network host value.

            >>> StandardRules.Network.host(b"test-hostname")
            (13, [b't', [b'e', b's', b't', [[b'-'], b'h'], b'o', b's', b't', b'n', b'a', b'm', b'e']])
            >>> StandardRules.Network.host(b"test.fqdn")
            (9, [[b't', [b'e', b's', b't']], [[b'.', [b'f', [b'q', b'd', b'n']]]]])
            >>> StandardRules.Network.host(b"127.0.0.1")
            (9, [[b'1', [b'2', b'7']], [[b'.', [b'0', []]], [b'.', [b'0', []]], [b'.', [b'1', []]]]])
            >>> StandardRules.Network.host(b"[::1]")
            (5, [b'[', [b':', b':', b'1'], b']'])
            >>> StandardRules.Network.host(b"[::dead:beef%eth1]")
            (18, [b'[', [[b':', b':', [[b'd', b'e', b'a', b'd'], b':'], [b'b', b'e', b'e', b'f']], b'%', [[b'e', b't', b'h', b'1']]], b']'])
            >>> StandardRules.Network.host(b"[v0123456789abcdef.%25]")
            (23, [b'[', [b'v', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'a', b'b', b'c', b'd', b'e', b'f'], b'.', [[[b'%', b'2', b'5']]]], b']'])
            >>> StandardRules.Network.host(b"dead::beef")
            (4, [b'd', [b'e', b'a', b'd']])
            >>> StandardRules.Network.host(b"dead::beef%25test|")
            (4, [b'd', [b'e', b'a', b'd']])
            >>> StandardRules.Network.host(b"v0123456789abcdef.%25")
            (17, [b'v', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'a', b'b', b'c', b'd', b'e', b'f']])
            >>>
            """

            def address_literal(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardRules.Network.ipvfuture,
                        StandardRules.Network.ipv6_zoneid,
                        StandardRules.Network.ipv6,
                    ],
                    data,
                    position,
                )

            def ip_literal(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(91),
                        address_literal,
                        StandardMatch.check_char(93),
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    ip_literal,
                    StandardRules.Network.fqdn,
                    StandardRules.Network.ipv4,
                    StandardRules.Network.hostname,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "host"

            return result

        def host_port(data: bytes, position: int = 0) -> Tuple[
            int,
            Iterable[
                Union[
                    bytes,
                    Iterable[
                        Union[
                            bytes,
                            Iterable[
                                Iterable[
                                    Union[
                                        bytes,
                                        Iterable[
                                            Union[bytes, Iterable[bytes]]
                                        ],
                                    ]
                                ]
                            ],
                        ]
                    ],
                ]
            ],
        ]:
            """
            This method parses the network host value with a port.

            >>> StandardRules.Network.host_port(b"test-hostname:4545")
            (18, [[b't', [b'e', b's', b't', [[b'-'], b'h'], b'o', b's', b't', b'n', b'a', b'm', b'e']], b':', [b'4', b'5', b'4', b'5']])
            >>> StandardRules.Network.host_port(b"test.fqdn:8080")
            (14, [[[b't', [b'e', b's', b't']], [[b'.', [b'f', [b'q', b'd', b'n']]]]], b':', [b'8', b'0', b'8', b'0']])
            >>> StandardRules.Network.host_port(b"127.0.0.1:65535")
            (15, [[[b'1', [b'2', b'7']], [[b'.', [b'0', []]], [b'.', [b'0', []]], [b'.', [b'1', []]]]], b':', [b'6', b'5', b'5', b'3', b'5']])
            >>> StandardRules.Network.host_port(b"[::1]:1234")
            (10, [[b'[', [b':', b':', b'1'], b']'], b':', [b'1', b'2', b'3', b'4']])
            >>> StandardRules.Network.host_port(b"[::dead:beef%eth1]:7845")
            (23, [[b'[', [[b':', b':', [[b'd', b'e', b'a', b'd'], b':'], [b'b', b'e', b'e', b'f']], b'%', [[b'e', b't', b'h', b'1']]], b']'], b':', [b'7', b'8', b'4', b'5']])
            >>> StandardRules.Network.host_port(b"[v0123456789abcdef.%25]:8989")
            (28, [[b'[', [b'v', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'a', b'b', b'c', b'd', b'e', b'f'], b'.', [[[b'%', b'2', b'5']]]], b']'], b':', [b'8', b'9', b'8', b'9']])
            >>> StandardRules.Network.host_port(b"[dead::beef]:abc")
            (0, None)
            >>> StandardRules.Network.host_port(b"[dead::beef%25t]:+4578")
            (0, None)
            >>> StandardRules.Network.host_port(b"[v0123456789abcdef.%25]4542")
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Network.host,
                    StandardMatch.check_char(58),
                    StandardRules.Types.digits,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "host_port"

            return result

        def user_info(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]]:
            """
            This method parses the network host value with a port.

            >>> StandardRules.Network.user_info(b"toto:123")
            (8, [[b't', b'o', b't', b'o'], b':', [b'1', b'2', b'3']])
            >>> StandardRules.Network.user_info(b"test:p@ssword")
            (6, [[b't', b'e', b's', b't'], b':', [b'p']])
            >>> StandardRules.Network.user_info(b"test123:p+~._-ssword%25")
            (23, [[b't', b'e', b's', b't', b'1', b'2', b'3'], b':', [b'p', b'+', b'~', b'.', b'_', b'-', b's', b's', b'w', b'o', b'r', b'd', [b'%', b'2', b'5']]])
            >>>
            """

            result = PegParser.one_or_more(
                StandardRules.Url._characters_subdelims_colon,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "user_info"

            return result

    class Http:
        """
        This class implements a complete parser for http.
        """

        def verb(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method returns `verb` bytes for the protocol.

            >>> StandardRules.Http.verb(b'GET')
            (3, [b'G', b'E', b'T'])
            >>> StandardRules.Http.verb(b'POST')
            (4, [b'P', b'O', b'S', b'T'])
            >>> StandardRules.Http.verb(b'put')
            (3, [b'p', b'u', b't'])
            >>> StandardRules.Http.verb(b'delete')
            (6, [b'd', b'e', b'l', b'e', b't', b'e'])
            >>> StandardRules.Http.verb(b'Options')
            (7, [b'O', b'p', b't', b'i', b'o', b'n', b's'])
            >>> StandardRules.Http.verb(b'hEAD')
            (4, [b'h', b'E', b'A', b'D'])
            >>> StandardRules.Http.verb(b'PaTcH')
            (5, [b'P', b'a', b'T', b'c', b'H'])
            >>> StandardRules.Http.verb(b'tRaCe')
            (5, [b't', b'R', b'a', b'C', b'e'])
            >>>
            """

            result = StandardRules.Http.token(data, position)

            if isinstance(result[1], MatchList):
                result[1]._match_name = "verb"

            return result

        def magic(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method returns `magic` bytes for the protocol.

            >>> StandardRules.Http.magic(b'http')
            (4, [b'h', b't', b't', b'p'])
            >>> StandardRules.Http.magic(b'HTTP')
            (4, [b'H', b'T', b'T', b'P'])
            >>>
            """

            result = StandardRules.Format.word(data, position)

            if isinstance(result[1], MatchList):
                result[1]._match_name = "magic"

            return result

        def version(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]]:
            """
            This method returns `version` bytes for the protocol.

            >>> StandardRules.Http.version(b'1.0')
            (3, [[b'1'], b'.', [b'0']])
            >>> StandardRules.Http.version(b'1.1')
            (3, [[b'1'], b'.', [b'1']])
            >>>
            """

            result = StandardRules.Types.float(data, position)

            if isinstance(result[1], MatchList):
                result[1]._match_name = "version"

            return result

        def protocol_version(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Union[bytes, Iterable[Union[bytes, Iterable[bytes]]]]
                ],
            ],
        ]:
            """
            This method returns `version` bytes for the protocol.

            >>> StandardRules.Http.protocol_version(b'HTTP/1.0')
            (8, [[b'H', b'T', b'T', b'P'], b'/', [[b'1'], b'.', [b'0']]])
            >>> StandardRules.Http.protocol_version(b'http/1.1')
            (8, [[b'h', b't', b't', b'p'], b'/', [[b'1'], b'.', [b'1']]])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Http.magic,
                    StandardMatch.check_char(47),
                    StandardRules.Http.version,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "http_version"

            return result

        def status_code(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method returns `status code` bytes for the response.

            >>> StandardRules.Http.status_code(b'200')
            (3, [b'2', b'0', b'0'])
            >>> StandardRules.Http.status_code(b'404')
            (3, [b'4', b'0', b'4'])
            >>>
            """

            result = StandardRules.Types.digits(data, position)

            if isinstance(result[1], MatchList):
                result[1]._match_name = "status_code"

            return result

        def is_text_char(
            data: bytes, position: int
        ) -> Tuple[int, Union[None, bytes]]:
            r"""
            This method checks a position for an HTTP TEXT character.

            >>> StandardRules.Http.is_text_char(b"a1Bc", 0)
            (1, b'a')
            >>> StandardRules.Http.is_text_char(b"a1Bc", 1)
            (2, b'1')
            >>> StandardRules.Http.is_text_char(b"a1Bc", 2)
            (3, b'B')
            >>> StandardRules.Http.is_text_char(b"a1B\0", 3)
            (3, None)
            >>> len([x for x in range(256) if StandardRules.Http.is_text_char(bytes((x,)), 0)[1] is not None])
            96
            >>>
            """

            if len(data) == position:
                return position, None

            char = data[position]
            if 32 <= char <= 126 or char == 9:
                return position + 1, bytes((char,))
            return position, None

        def text(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method parses HTTP TEXT format.

            >>> StandardRules.Http.text(b'HTTp Text 200 !')
            (15, [b'H', b'T', b'T', b'p', b' ', b'T', b'e', b'x', b't', b' ', b'2', b'0', b'0', b' ', b'!'])
            >>> StandardRules.Http.text(b'Another text to test 5.5, other things ?":@#')
            (44, [b'A', b'n', b'o', b't', b'h', b'e', b'r', b' ', b't', b'e', b'x', b't', b' ', b't', b'o', b' ', b't', b'e', b's', b't', b' ', b'5', b'.', b'5', b',', b' ', b'o', b't', b'h', b'e', b'r', b' ', b't', b'h', b'i', b'n', b'g', b's', b' ', b'?', b'"', b':', b'@', b'#'])
            >>>
            """

            return PegParser.one_or_more(
                StandardRules.Http.is_text_char,
                data,
                position,
            )

        def reason(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method returns `reason` bytes for the response status.

            >>> StandardRules.Http.reason(b'OK')
            (2, [b'O', b'K'])
            >>> StandardRules.Http.reason(b'Internal Server Error')
            (21, [b'I', b'n', b't', b'e', b'r', b'n', b'a', b'l', b' ', b'S', b'e', b'r', b'v', b'e', b'r', b' ', b'E', b'r', b'r', b'o', b'r'])
            >>>
            """

            result = StandardRules.Http.text(data, position)

            if isinstance(result[1], MatchList):
                result[1]._match_name = "reason"

            return result

        def field_value(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method returns `field_value` bytes for HTTP.

            >>> StandardRules.Http.field_value(b'application/json; charset="utf8"')
            (32, [b'a', b'p', b'p', b'l', b'i', b'c', b'a', b't', b'i', b'o', b'n', b'/', b'j', b's', b'o', b'n', b';', b' ', b'c', b'h', b'a', b'r', b's', b'e', b't', b'=', b'"', b'u', b't', b'f', b'8', b'"'])
            >>> StandardRules.Http.field_value(b'Fri, 02 May 2025 14:02:56 GMT')
            (29, [b'F', b'r', b'i', b',', b' ', b'0', b'2', b' ', b'M', b'a', b'y', b' ', b'2', b'0', b'2', b'5', b' ', b'1', b'4', b':', b'0', b'2', b':', b'5', b'6', b' ', b'G', b'M', b'T'])
            >>>
            """

            result = StandardRules.Http.text(data, position)

            if isinstance(result[1], MatchList):
                result[1]._match_name = "field_value"

            return result

        def response_start(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Union[
                        bytes,
                        Iterable[
                            Union[
                                bytes, Iterable[Union[bytes, Iterable[bytes]]]
                            ]
                        ],
                    ]
                ],
            ],
        ]:
            r"""
            This method parses the first line for HTTP response.

            >>> StandardRules.Http.response_start(b'HTTP/1.1 200 OK\r\n')
            (17, [[[b'H', b'T', b'T', b'P'], b'/', [[b'1'], b'.', [b'1']]], b' ', [b'2', b'0', b'0'], b' ', [b'O', b'K'], b'\r', b'\n'])
            >>> StandardRules.Http.response_start(b'HTTP/1.0 500 Internal Server Error\r\n')
            (36, [[[b'H', b'T', b'T', b'P'], b'/', [[b'1'], b'.', [b'0']]], b' ', [b'5', b'0', b'0'], b' ', [b'I', b'n', b't', b'e', b'r', b'n', b'a', b'l', b' ', b'S', b'e', b'r', b'v', b'e', b'r', b' ', b'E', b'r', b'r', b'o', b'r'], b'\r', b'\n'])
            >>>
            """

            return PegParser.sequence(
                [
                    StandardRules.Http.protocol_version,
                    StandardMatch.check_char(32),
                    StandardRules.Http.status_code,
                    StandardMatch.check_char(32),
                    StandardRules.Http.reason,
                    StandardMatch.check_char(13),
                    StandardMatch.check_char(10),
                ],
                data,
                position,
            )

        def token(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method parses the first line for HTTP response.

            >>> StandardRules.Http.token(b'Content-Type')
            (12, [b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'T', b'y', b'p', b'e'])
            >>> StandardRules.Http.token(b'Content-Length')
            (14, [b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'L', b'e', b'n', b'g', b't', b'h'])
            >>>
            """

            def character(data, position):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.is_letter,
                        StandardMatch.is_digit,
                        StandardMatch.or_check_chars(
                            33,
                            35,
                            36,
                            37,
                            38,
                            39,
                            42,
                            43,
                            45,
                            46,
                            94,
                            95,
                            96,
                            124,
                            126,
                        ),
                    ],
                    data,
                    position,
                )

            return PegParser.one_or_more(
                character,
                data,
                position,
            )

        def field_name(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            """
            This method returns `field_name` bytes for HTTP.

            >>> StandardRules.Http.field_name(b'Content-Type')
            (12, [b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'T', b'y', b'p', b'e'])
            >>> StandardRules.Http.field_name(b'Content-Length')
            (14, [b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'L', b'e', b'n', b'g', b't', b'h'])
            >>>
            """

            result = StandardRules.Http.token(data, position)

            if isinstance(result[1], MatchList):
                result[1]._match_name = "field_name"

            return result

        def header(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]]:
            r"""
            This method parses a HTTP header.

            >>> StandardRules.Http.header(b'Content-Type: application/json\r\n')
            (32, [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'T', b'y', b'p', b'e'], b':', b' ', [b'a', b'p', b'p', b'l', b'i', b'c', b'a', b't', b'i', b'o', b'n', b'/', b'j', b's', b'o', b'n'], b'\r', b'\n'])
            >>> StandardRules.Http.header(b'Content-Length: 12\r\n')
            (20, [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'L', b'e', b'n', b'g', b't', b'h'], b':', b' ', [b'1', b'2'], b'\r', b'\n'])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Http.field_name,
                    StandardMatch.check_char(58),
                    StandardMatch.check_char(32),
                    StandardRules.Http.field_value,
                    StandardMatch.check_char(13),
                    StandardMatch.check_char(10),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "header"

            return result

        def headers(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, Iterable[Union[bytes, Iterable[bytes]]]]]:
            r"""
            This method parses HTTP headers.

            >>> StandardRules.Http.headers(b'Content-Type: application/json\r\nContent-Length: 12\r\n\r\n')
            (54, [[[[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'T', b'y', b'p', b'e'], b':', b' ', [b'a', b'p', b'p', b'l', b'i', b'c', b'a', b't', b'i', b'o', b'n', b'/', b'j', b's', b'o', b'n'], b'\r', b'\n'], [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'L', b'e', b'n', b'g', b't', b'h'], b':', b' ', [b'1', b'2'], b'\r', b'\n']], b'\r', b'\n'])
            >>>
            """

            def _headers(data, position):
                return PegParser.one_or_more(
                    StandardRules.Http.header,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    _headers,
                    StandardMatch.check_char(13),
                    StandardMatch.check_char(10),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "headers"

            return result

        def response(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[
                    Iterable[
                        Union[
                            bytes,
                            Iterable[
                                Union[
                                    bytes,
                                    Iterable[Union[bytes, Iterable[bytes]]],
                                ]
                            ],
                        ]
                    ]
                ],
            ],
        ]:
            r"""
            This method parses HTTP response.

            >>> StandardRules.Http.response(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 12\r\n\r\n')
            (71, [[[[b'H', b'T', b'T', b'P'], b'/', [[b'1'], b'.', [b'1']]], b' ', [b'2', b'0', b'0'], b' ', [b'O', b'K'], b'\r', b'\n'], [[[[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'T', b'y', b'p', b'e'], b':', b' ', [b'a', b'p', b'p', b'l', b'i', b'c', b'a', b't', b'i', b'o', b'n', b'/', b'j', b's', b'o', b'n'], b'\r', b'\n'], [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'L', b'e', b'n', b'g', b't', b'h'], b':', b' ', [b'1', b'2'], b'\r', b'\n']], b'\r', b'\n']])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Http.response_start,
                    StandardRules.Http.headers,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "response"

            return result

        def request(data: bytes, position: int = 0):
            r"""
            This method parses HTTP request.

            >>> StandardRules.Http.request(b'POST http://test.test/test;test=test?test=test HTTP/1.0\r\nHost: myhost\r\nContent-Type: application/json; charset="utf-8"\r\nContent-Length: 12\r\n\r\nabcdefabcdef')
            (142, [[b'P', b'O', b'S', b'T'], b' ', [[b'h', [b't', b't', b'p']], b':', [b'/', b'/', [[b't', [b'e', b's', b't']], [[b'.', [b't', [b'e', b's', b't']]]]], [[b'/', [[b't', b'e', b's', b't']]]]], [b';', [[[b't', b'e', b's', b't'], b'=', [b't', b'e', b's', b't']], []]], [b'?', [[b't', b'e', b's', b't'], b'=', [b't', b'e', b's', b't']]], True], b' ', [[b'H', b'T', b'T', b'P'], b'/', [[b'1'], b'.', [b'0']]], b'\r', b'\n', [[[[b'H', b'o', b's', b't'], b':', b' ', [b'm', b'y', b'h', b'o', b's', b't'], b'\r', b'\n'], [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'T', b'y', b'p', b'e'], b':', b' ', [b'a', b'p', b'p', b'l', b'i', b'c', b'a', b't', b'i', b'o', b'n', b'/', b'j', b's', b'o', b'n', b';', b' ', b'c', b'h', b'a', b'r', b's', b'e', b't', b'=', b'"', b'u', b't', b'f', b'-', b'8', b'"'], b'\r', b'\n'], [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'L', b'e', b'n', b'g', b't', b'h'], b':', b' ', [b'1', b'2'], b'\r', b'\n']], b'\r', b'\n']])
            >>> StandardRules.Http.request(b'POST /test;test=test?test=test HTTP/1.0\r\nHost: myhost\r\nContent-Type: application/json; charset="utf-8"\r\nContent-Length: 12\r\n\r\nabcdefabcdef')
            (126, [[b'P', b'O', b'S', b'T'], b' ', [[[b'/', [[b't', b'e', b's', b't']]]], [b';', [[[b't', b'e', b's', b't'], b'=', [b't', b'e', b's', b't']], []]], [b'?', [[b't', b'e', b's', b't'], b'=', [b't', b'e', b's', b't']]]], b' ', [[b'H', b'T', b'T', b'P'], b'/', [[b'1'], b'.', [b'0']]], b'\r', b'\n', [[[[b'H', b'o', b's', b't'], b':', b' ', [b'm', b'y', b'h', b'o', b's', b't'], b'\r', b'\n'], [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'T', b'y', b'p', b'e'], b':', b' ', [b'a', b'p', b'p', b'l', b'i', b'c', b'a', b't', b'i', b'o', b'n', b'/', b'j', b's', b'o', b'n', b';', b' ', b'c', b'h', b'a', b'r', b's', b'e', b't', b'=', b'"', b'u', b't', b'f', b'-', b'8', b'"'], b'\r', b'\n'], [[b'C', b'o', b'n', b't', b'e', b'n', b't', b'-', b'L', b'e', b'n', b'g', b't', b'h'], b':', b' ', [b'1', b'2'], b'\r', b'\n']], b'\r', b'\n']])
            >>>
            """

            def uri(data, position):
                result = PegParser.ordered_choice(
                    [
                        lambda d, p: PegParser.sequence(
                            [
                                StandardRules.Url.path,
                                StandardRules.Url.parameters,
                                StandardRules.Url.query,
                            ],
                            d,
                            p,
                        ),
                        lambda d, p: PegParser.sequence(
                            [StandardRules.Url.path, StandardRules.Url.query],
                            d,
                            p,
                        ),
                        lambda d, p: PegParser.sequence(
                            [
                                StandardRules.Url.path,
                                StandardRules.Url.parameters,
                            ],
                            d,
                            p,
                        ),
                        StandardRules.Url.full,
                    ],
                    data,
                    position,
                )
                if isinstance(result[1], MatchList):
                    result[1]._match_name = "uri"
                return result

            result = PegParser.sequence(
                [
                    StandardRules.Http.verb,
                    StandardMatch.check_char(32),
                    uri,
                    StandardMatch.check_char(32),
                    StandardRules.Http.protocol_version,
                    StandardMatch.check_char(13),
                    StandardMatch.check_char(10),
                    StandardRules.Http.headers,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "request"

            return result

    class Csv:
        """
        This class implements a complete parser for CSV and multi-CSV.
        """

        def value(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[Union[bytes, List[bytes]]]]]:
            """
            This function parses a CSV value.

            >>> StandardRules.Csv.value(b'test""test')
            (10, [b't', b'e', b's', b't', [b'"', b'"'], b't', b'e', b's', b't'])
            >>> StandardRules.Csv.value(b'test"test')
            (4, [b't', b'e', b's', b't'])
            >>>
            """

            def escape_quotes(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(34),
                        StandardMatch.check_char(34),
                    ],
                    data,
                    position,
                )

            def character(data: bytes, position: int):
                if len(data) == position:
                    return position, None

                char = data[position]
                if char == 34:
                    return position, None
                return position + 1, bytes((char,))

            def character_or_escape(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        character,
                        escape_quotes,
                    ],
                    data,
                    position,
                )

            result = PegParser.zero_or_more(
                character_or_escape,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "csv_value"

            return result

        def quoted_value(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[None, List[Union[bytes, List[Union[bytes, List[bytes]]]]]],
        ]:
            """
            This function parses a CSV quoted value.

            >>> StandardRules.Csv.quoted_value(b'"test""test"')
            (12, [b'"', [b't', b'e', b's', b't', [b'"', b'"'], b't', b'e', b's', b't'], b'"'])
            >>> StandardRules.Csv.quoted_value(b'"test"test"')
            (6, [b'"', [b't', b'e', b's', b't'], b'"'])
            >>> StandardRules.Csv.quoted_value(b'"test')
            (0, None)
            >>> StandardRules.Csv.quoted_value(b'""')
            (2, [b'"', [], b'"'])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(34),
                    StandardRules.Csv.value,
                    StandardMatch.check_char(34),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "csv_quoted_value"

            return result

        def values(data: bytes, position: int = 0) -> Tuple[
            int,
            List[
                List[
                    Union[
                        bytes,
                        List[Union[bytes, List[Union[bytes, List[bytes]]]]],
                    ]
                ]
            ],
        ]:
            """
            This function parses second to last value in the line.

            >>> StandardRules.Csv.values(b',"test""test","other"')
            (21, [[b',', [b'"', [b't', b'e', b's', b't', [b'"', b'"'], b't', b'e', b's', b't'], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]])
            >>> StandardRules.Csv.values(b',"test"test","other"')
            (7, [[b',', [b'"', [b't', b'e', b's', b't'], b'"']]])
            >>> StandardRules.Csv.values(b',"test')
            (0, [])
            >>> StandardRules.Csv.values(b',"test,"other"')
            (8, [[b',', [b'"', [b't', b'e', b's', b't', b','], b'"']]])
            >>> StandardRules.Csv.values(b',"","other"')
            (11, [[b',', [b'"', [], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]])
            >>> StandardRules.Csv.values(b'')
            (0, [])
            >>>
            """

            def separator_value(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardMatch.check_char(44),
                        StandardRules.Csv.quoted_value,
                    ],
                    data,
                    position,
                )

            result = PegParser.zero_or_more(
                separator_value,
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "csv_values"

            return result

        def line(data: bytes, position: int = 0) -> Tuple[
            int,
            List[
                List[
                    Union[
                        bytes,
                        List[
                            Union[
                                bytes,
                                List[
                                    Union[
                                        bytes, List[Union[bytes, List[bytes]]]
                                    ]
                                ],
                            ]
                        ],
                    ]
                ]
            ],
        ]:
            """
            This function parses a CSV line.

            >>> StandardRules.Csv.line(b'"1","test""test","other"')
            (24, [[b'"', [b'1'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't', [b'"', b'"'], b't', b'e', b's', b't'], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]]])
            >>> StandardRules.Csv.line(b'"1","test"test","other"')
            (10, [[b'"', [b'1'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't'], b'"']]]])
            >>> StandardRules.Csv.line(b'"1","test')
            (3, [[b'"', [b'1'], b'"'], []])
            >>> StandardRules.Csv.line(b'"1","test,"other"')
            (11, [[b'"', [b'1'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't', b','], b'"']]]])
            >>> StandardRules.Csv.line(b'"1","","other"')
            (14, [[b'"', [b'1'], b'"'], [[b',', [b'"', [], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]]])
            >>> StandardRules.Csv.line(b'"1"')
            (3, [[b'"', [b'1'], b'"'], []])
            >>> StandardRules.Csv.line(b'')
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Csv.quoted_value,
                    StandardRules.Csv.values,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "csv_line"

            return result

        def line_delimiter(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[bytes]]]:
            r"""
            This function parses the line delimiter ('\n' or '\r\n').

            >>> StandardRules.Csv.line_delimiter(b'\n')
            (1, b'\n')
            >>> StandardRules.Csv.line_delimiter(b'\r\n')
            (2, [b'\r', b'\n'])
            >>> StandardRules.Csv.line_delimiter(b'"')
            (0, None)
            >>> StandardRules.Csv.line_delimiter(b'test')
            (0, None)
            >>>
            """

            return PegParser.ordered_choice(
                [
                    StandardMatch.check_char(10),
                    lambda d, p: PegParser.sequence(
                        [
                            StandardMatch.check_char(13),
                            StandardMatch.check_char(10),
                        ],
                        data,
                        position,
                    ),
                ],
                data,
                position,
            )

        def full(data: bytes, position: int = 0) -> Tuple[
            int,
            List[
                List[
                    Union[
                        bytes,
                        List[
                            Union[
                                bytes,
                                List[
                                    Union[
                                        bytes,
                                        List[
                                            Union[
                                                bytes,
                                                List[
                                                    Union[
                                                        bytes,
                                                        List[
                                                            Union[
                                                                bytes,
                                                                List[
                                                                    Union[
                                                                        bytes,
                                                                        List[
                                                                            bytes
                                                                        ],
                                                                    ]
                                                                ],
                                                            ]
                                                        ],
                                                    ]
                                                ],
                                            ]
                                        ],
                                    ]
                                ],
                            ]
                        ],
                    ]
                ]
            ],
        ]:
            r"""
            This function parses the full CSV file.

            >>> StandardRules.Csv.full(b'"1","test""test","other"\n')
            (24, [[[b'"', [b'1'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't', [b'"', b'"'], b't', b'e', b's', b't'], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]]], []])
            >>> StandardRules.Csv.full(b'"1","test"test","other"\r\n')
            (10, [[[b'"', [b'1'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't'], b'"']]]], []])
            >>> StandardRules.Csv.full(b'"1","test\n')
            (3, [[[b'"', [b'1'], b'"'], []], []])
            >>> StandardRules.Csv.full(b'"1","test,"other"\n"2"')
            (11, [[[b'"', [b'1'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't', b','], b'"']]]], []])
            >>> StandardRules.Csv.full(b'"1","","other"\n"2"\n"3","test"')
            (29, [[[b'"', [b'1'], b'"'], [[b',', [b'"', [], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]]], [[b'\n', [[b'"', [b'2'], b'"'], []]], [b'\n', [[b'"', [b'3'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't'], b'"']]]]]]])
            >>> StandardRules.Csv.full(b'"1"')
            (3, [[[b'"', [b'1'], b'"'], []], []])
            >>> StandardRules.Csv.full(b'')
            (0, None)
            >>>
            """

            def delimiter_line(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Csv.line_delimiter,
                        StandardRules.Csv.line,
                    ],
                    data,
                    position,
                )

            def delimiter_lines(data: bytes, position: int):
                return PegParser.zero_or_more(
                    delimiter_line,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    StandardRules.Csv.line,
                    delimiter_lines,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "csv"

            return result

        def multi(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                List[
                    List[
                        Union[
                            bytes,
                            List[
                                List[
                                    List[
                                        Union[
                                            bytes,
                                            List[
                                                Union[
                                                    bytes,
                                                    List[
                                                        Union[
                                                            bytes,
                                                            List[
                                                                Union[
                                                                    bytes,
                                                                    List[
                                                                        Union[
                                                                            bytes,
                                                                            List[
                                                                                Union[
                                                                                    bytes,
                                                                                    List[
                                                                                        Union[
                                                                                            bytes,
                                                                                            List[
                                                                                                bytes
                                                                                            ],
                                                                                        ]
                                                                                    ],
                                                                                ]
                                                                            ],
                                                                        ]
                                                                    ],
                                                                ]
                                                            ],
                                                        ]
                                                    ],
                                                ]
                                            ],
                                        ]
                                    ]
                                ],
                            ],
                        ]
                    ]
                ]
            ],
        ]:
            r"""
            This function parses a multi-csv.

            >>> StandardRules.Csv.multi(b'"1","","other"\n"2"\n"3","test"\n\r\n"1","","other"\r\n"2"\r\n"3","test"')
            (63, [[[[b'"', [b'1'], b'"'], [[b',', [b'"', [], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]]], [[b'\n', [[b'"', [b'2'], b'"'], []]], [b'\n', [[b'"', [b'3'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't'], b'"']]]]]]], [[b'\n', [b'\r', b'\n'], [[[b'"', [b'1'], b'"'], [[b',', [b'"', [], b'"']], [b',', [b'"', [b'o', b't', b'h', b'e', b'r'], b'"']]]], [[[b'\r', b'\n'], [[b'"', [b'2'], b'"'], []]], [[b'\r', b'\n'], [[b'"', [b'3'], b'"'], [[b',', [b'"', [b't', b'e', b's', b't'], b'"']]]]]]]]]])
            >>>
            """

            def delimiter_csv(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Csv.line_delimiter,
                        StandardRules.Csv.line_delimiter,
                        StandardRules.Csv.full,
                    ],
                    data,
                    position,
                )

            def delimiter_csvs(data: bytes, position: int):
                return PegParser.zero_or_more(
                    delimiter_csv,
                    data,
                    position,
                )

            result = PegParser.sequence(
                [
                    StandardRules.Csv.full,
                    delimiter_csvs,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "multi_csv"

            return result

    class Json:
        """
        This class implements strict and permissive JSON parser.
        """

        def null(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[bytes]]]:
            """
            This function checks for strict null value.

            >>> StandardRules.Json.null(b'null')
            (4, [b'n', b'u', b'l', b'l'])
            >>> StandardRules.Json.null(b'NulL')
            (0, None)
            >>> StandardRules.Json.null(b'None')
            (0, None)
            >>> StandardRules.Json.null(b'nonE')
            (0, None)
            >>> StandardRules.Json.null(b'nil')
            (0, None)
            >>> StandardRules.Json.null(b'nIl')
            (0, None)
            >>> StandardRules.Json.null(b'undefined')
            (0, None)
            >>> StandardRules.Json.null(b'undeFined')
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(110),
                    StandardMatch.check_char(117),
                    StandardMatch.check_char(108),
                    StandardMatch.check_char(108),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "null"

            return result

        def true(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[bytes]]]:
            """
            This function checks for strict true value.

            >>> StandardRules.Json.true(b'true')
            (4, [b't', b'r', b'u', b'e'])
            >>> StandardRules.Json.true(b'True')
            (0, None)
            >>> StandardRules.Json.true(b'TRUE')
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(116),
                    StandardMatch.check_char(114),
                    StandardMatch.check_char(117),
                    StandardMatch.check_char(101),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "true"

            return result

        def false(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[bytes]]]:
            """
            This function checks for strict false value.

            >>> StandardRules.Json.false(b'false')
            (5, [b'f', b'a', b'l', b's', b'e'])
            >>> StandardRules.Json.false(b'False')
            (0, None)
            >>> StandardRules.Json.false(b'FALSE')
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(102),
                    StandardMatch.check_char(97),
                    StandardMatch.check_char(108),
                    StandardMatch.check_char(115),
                    StandardMatch.check_char(101),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "false"

            return result

        def permissive_null(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[bytes]]]:
            """
            This function checks for permissive null value.

            >>> StandardRules.Json.permissive_null(b'null')
            (4, [b'n', b'u', b'l', b'l'])
            >>> StandardRules.Json.permissive_null(b'NulL')
            (4, [b'N', b'u', b'l', b'L'])
            >>> StandardRules.Json.permissive_null(b'None')
            (4, [b'N', b'o', b'n', b'e'])
            >>> StandardRules.Json.permissive_null(b'nonE')
            (4, [b'n', b'o', b'n', b'E'])
            >>> StandardRules.Json.permissive_null(b'nil')
            (3, [b'n', b'i', b'l'])
            >>> StandardRules.Json.permissive_null(b'nIl')
            (3, [b'n', b'I', b'l'])
            >>> StandardRules.Json.permissive_null(b'undefined')
            (9, [b'u', b'n', b'd', b'e', b'f', b'i', b'n', b'e', b'd'])
            >>> StandardRules.Json.permissive_null(b'undeFined')
            (9, [b'u', b'n', b'd', b'e', b'F', b'i', b'n', b'e', b'd'])
            >>>
            """

            result = PegParser.ordered_choice(
                [
                    lambda d, p: PegParser.sequence(
                        [
                            StandardMatch.or_check_chars(110, 78),
                            StandardMatch.or_check_chars(117, 85),
                            StandardMatch.or_check_chars(108, 76),
                            StandardMatch.or_check_chars(108, 76),
                        ],
                        d,
                        p,
                    ),
                    lambda d, p: PegParser.sequence(
                        [
                            StandardMatch.or_check_chars(110, 78),
                            StandardMatch.or_check_chars(111, 79),
                            StandardMatch.or_check_chars(110, 78),
                            StandardMatch.or_check_chars(101, 69),
                        ],
                        d,
                        p,
                    ),
                    lambda d, p: PegParser.sequence(
                        [
                            StandardMatch.or_check_chars(110, 78),
                            StandardMatch.or_check_chars(105, 73),
                            StandardMatch.or_check_chars(108, 76),
                        ],
                        d,
                        p,
                    ),
                    lambda d, p: PegParser.sequence(
                        [
                            StandardMatch.or_check_chars(117, 85),
                            StandardMatch.or_check_chars(110, 78),
                            StandardMatch.or_check_chars(100, 68),
                            StandardMatch.or_check_chars(101, 69),
                            StandardMatch.or_check_chars(102, 70),
                            StandardMatch.or_check_chars(105, 73),
                            StandardMatch.or_check_chars(110, 78),
                            StandardMatch.or_check_chars(101, 69),
                            StandardMatch.or_check_chars(100, 68),
                        ],
                        d,
                        p,
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "permissive_null"

            return result

        def permissive_true(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[bytes]]]:
            """
            This function checks for permissive true value.

            >>> StandardRules.Json.permissive_true(b'true')
            (4, [b't', b'r', b'u', b'e'])
            >>> StandardRules.Json.permissive_true(b'True')
            (4, [b'T', b'r', b'u', b'e'])
            >>> StandardRules.Json.permissive_true(b'TRUE')
            (4, [b'T', b'R', b'U', b'E'])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.or_check_chars(116, 84),
                    StandardMatch.or_check_chars(114, 82),
                    StandardMatch.or_check_chars(117, 85),
                    StandardMatch.or_check_chars(101, 69),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "permissive_true"

            return result

        def permissive_false(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List[bytes]]]:
            """
            This function checks for permissive false value.

            >>> StandardRules.Json.permissive_false(b'false')
            (5, [b'f', b'a', b'l', b's', b'e'])
            >>> StandardRules.Json.permissive_false(b'False')
            (5, [b'F', b'a', b'l', b's', b'e'])
            >>> StandardRules.Json.permissive_false(b'FALSE')
            (5, [b'F', b'A', b'L', b'S', b'E'])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.or_check_chars(102, 70),
                    StandardMatch.or_check_chars(97, 65),
                    StandardMatch.or_check_chars(108, 76),
                    StandardMatch.or_check_chars(115, 83),
                    StandardMatch.or_check_chars(101, 69),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "permissive_false"

            return result

        def simple_value(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[None, List[Union[bytes, List[Union[bytes, List[bytes]]]]]],
        ]:
            r"""
            This function checks for strict `simple` value (null,
            boolean, integer, float, string).

            >>> StandardRules.Json.simple_value(b'null')
            (4, [b'n', b'u', b'l', b'l'])
            >>> StandardRules.Json.simple_value(b'true')
            (4, [b't', b'r', b'u', b'e'])
            >>> StandardRules.Json.simple_value(b'false')
            (5, [b'f', b'a', b'l', b's', b'e'])
            >>> StandardRules.Json.simple_value(b'1234567890')
            (10, [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0'])
            >>> StandardRules.Json.simple_value(b'0x0123456789aBcDeF')
            (18, [b'0', b'x', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'a', b'B', b'c', b'D', b'e', b'F']])
            >>> StandardRules.Json.simple_value(b'0o01234567')
            (10, [b'0', b'o', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7']])
            >>> StandardRules.Json.simple_value(b'1.23')
            (4, [[b'1'], b'.', [b'2', b'3']])
            >>> StandardRules.Json.simple_value(b'"test\\"abc"')
            (11, [b'"', [b't', b'e', b's', b't', [b'\\', b'"'], b'a', b'b', b'c'], b'"'])
            >>>
            """

            return PegParser.ordered_choice(
                [
                    StandardRules.Json.null,
                    StandardRules.Json.true,
                    StandardRules.Json.false,
                    StandardRules.Types.float,
                    StandardRules.Types.hex_integer,
                    StandardRules.Types.octal_integer,
                    StandardRules.Types.digits,
                    StandardRules.Types.string,
                ],
                data,
                position,
            )

        def permissive_simple_value(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[None, List[Union[bytes, List[Union[bytes, List[bytes]]]]]],
        ]:
            r"""
            This function checks for permissive `simple` value
            (null, boolean, integer, float, string).

            >>> StandardRules.Json.permissive_simple_value(b'nUll')
            (4, [b'n', b'U', b'l', b'l'])
            >>> StandardRules.Json.permissive_simple_value(b'tRue')
            (4, [b't', b'R', b'u', b'e'])
            >>> StandardRules.Json.permissive_simple_value(b'faLSe')
            (5, [b'f', b'a', b'L', b'S', b'e'])
            >>> StandardRules.Json.permissive_simple_value(b'1234567890')
            (10, [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0'])
            >>> StandardRules.Json.permissive_simple_value(b'0x0123456789aBcDeF')
            (18, [b'0', b'x', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'a', b'B', b'c', b'D', b'e', b'F']])
            >>> StandardRules.Json.permissive_simple_value(b'0o01234567')
            (10, [b'0', b'o', [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7']])
            >>> StandardRules.Json.permissive_simple_value(b'1.23')
            (4, [[b'1'], b'.', [b'2', b'3']])
            >>> StandardRules.Json.permissive_simple_value(b'"test\\"abc"')
            (11, [b'"', [b't', b'e', b's', b't', [b'\\', b'"'], b'a', b'b', b'c'], b'"'])
            >>>
            """

            return PegParser.ordered_choice(
                [
                    StandardRules.Json.permissive_null,
                    StandardRules.Json.permissive_true,
                    StandardRules.Json.permissive_false,
                    StandardRules.Types.float,
                    StandardRules.Types.hex_integer,
                    StandardRules.Types.octal_integer,
                    StandardRules.Types.digits,
                    StandardRules.Types.string,
                ],
                data,
                position,
            )

        def _start_list(data: bytes, position: int):
            result = StandardMatch.check_char(91)(data, position)

            if result[1]:
                match = MatchList((result[1],))
                result = (result[0], match)
                match._match_name = "start_list"

            return result

        def _end_list(data: bytes, position: int):
            result = StandardMatch.check_char(93)(data, position)

            if result[1]:
                match = MatchList((result[1],))
                result = (result[0], match)
                match._match_name = "end_list"

            return result

        def list(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List]]:
            """
            This function checks for strict JSON list.

            >>> StandardRules.Json.list(b'[]')
            (2, [[b'['], [], [b']']])
            >>> StandardRules.Json.list(b'[ ]')
            (3, [[b'['], [b' '], [b']']])
            >>> StandardRules.Json.list(b'[null]')
            (6, [[b'['], [], [], [], [b'n', b'u', b'l', b'l'], [], [b']']])
            >>> StandardRules.Json.list(b'[1, 1.5, 2 , "test", true, [false, null], {"test": 1, "1": null}]')
            (65, [[b'['], [], [[[b'1'], [], b',', [b' ']], [[[b'1'], b'.', [b'5']], [], b',', [b' ']], [[b'2'], [b' '], b',', [b' ']], [[b'"', [b't', b'e', b's', b't'], b'"'], [], b',', [b' ']], [[b't', b'r', b'u', b'e'], [], b',', [b' ']], [[[b'['], [], [[[b'f', b'a', b'l', b's', b'e'], [], b',', [b' ']]], [], [b'n', b'u', b'l', b'l'], [], [b']']], [], b',', [b' ']]], [], [[b'{'], [], [[[[b'"', [b't', b'e', b's', b't'], b'"'], [], b':', [b' '], [b'1'], []], b',', [b' ']]], [], [[b'"', [b'1'], b'"'], [], b':', [b' '], [b'n', b'u', b'l', b'l'], []], [], [b'}']], [], [b']']])
            >>> StandardRules.Json.list(b'[')
            (0, None)
            >>> StandardRules.Json.list(b'[1,]')
            (0, None)
            >>> StandardRules.Json.list(b'[1 null]')
            (0, None)
            >>>
            """

            def list_value(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json.full,
                        StandardRules.Format.optional_blanks,
                        StandardMatch.check_char(44),
                        StandardRules.Format.optional_blanks,
                    ],
                    data,
                    position,
                )

            def list_values(data: bytes, position: int):
                return PegParser.zero_or_more(
                    list_value,
                    data,
                    position,
                )

            def list_non_empty(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_list,
                        StandardRules.Format.optional_blanks,
                        list_values,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json.full,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json._end_list,
                    ],
                    data,
                    position,
                )

            def list_empty(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_list,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json._end_list,
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    list_non_empty,
                    list_empty,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "list"

            return result

        def permissive_list(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List]]:
            """
            This function checks for a permissive JSON list
            (trailing comma, forgot comma, ...).

            >>> StandardRules.Json.permissive_list(b'[]')
            (2, [[b'['], [], [], [b']']])
            >>> StandardRules.Json.permissive_list(b'[ ]')
            (3, [[b'['], [b' '], [], [b']']])
            >>> StandardRules.Json.permissive_list(b'[uNdefIned]')
            (11, [[b'['], [], [], [], [b'u', b'N', b'd', b'e', b'f', b'I', b'n', b'e', b'd'], [], [b']']])
            >>> StandardRules.Json.permissive_list(b'[1 1.5,2 , "test" trUE,, , , FalSe,   nil,, {"test" fAlSe trUE nuLl} ,,,, ]')
            (75, [[b'['], [], [[[b'1'], [[b' ']]], [[[b'1'], b'.', [b'5']], [b',']], [[b'2'], [[b' '], b',', [b' ']]], [[b'"', [b't', b'e', b's', b't'], b'"'], [[b' ']]], [[b't', b'r', b'U', b'E'], [b',', b',', [b' '], b',', [b' '], b',', [b' ']]], [[b'F', b'a', b'l', b'S', b'e'], [b',', [b' ', b' ', b' ']]], [[b'n', b'i', b'l'], [b',', b',', [b' ']]], [[[b'{'], [], [[[[b'"', [b't', b'e', b's', b't'], b'"'], [[b' ']], [b'f', b'A', b'l', b'S', b'e']], [[b' ']]]], [], [[b't', b'r', b'U', b'E'], [[b' ']], [b'n', b'u', b'L', b'l']], [], [b'}']], [[b' '], b',', b',', b',', b',', [b' ']]]], [b']']])
            >>> StandardRules.Json.permissive_list(b'[')
            (0, None)
            >>> StandardRules.Json.permissive_list(b'[1,]')
            (4, [[b'['], [], [[[b'1'], [b',']]], [b']']])
            >>> StandardRules.Json.permissive_list(b'[1 noNe]')
            (8, [[b'['], [], [[[b'1'], [[b' ']]]], [], [b'n', b'o', b'N', b'e'], [], [b']']])
            >>>
            """

            def separator(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.check_char(44),
                        StandardRules.Format.blanks,
                    ],
                    data,
                    position,
                )

            def separators(data: bytes, position: int):
                return PegParser.one_or_more(
                    separator,
                    data,
                    position,
                )

            def list_value(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json.permissive_full,
                        separators,
                    ],
                    data,
                    position,
                )

            def list_values(data: bytes, position: int):
                return PegParser.zero_or_more(
                    list_value,
                    data,
                    position,
                )

            def strict_list(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_list,
                        StandardRules.Format.optional_blanks,
                        list_values,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json.permissive_full,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json._end_list,
                    ],
                    data,
                    position,
                )

            def flex_list(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_list,
                        StandardRules.Format.optional_blanks,
                        list_values,
                        StandardRules.Json._end_list,
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    strict_list,
                    flex_list,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "permissive_list"

            return result

        def _start_dict(data: bytes, position: int):
            result = StandardMatch.check_char(123)(data, position)

            if result[1]:
                match = MatchList((result[1],))
                result = (result[0], match)
                match._match_name = "start_dict"

            return result

        def _end_dict(data: bytes, position: int):
            result = StandardMatch.check_char(125)(data, position)

            if result[1]:
                match = MatchList((result[1],))
                result = (result[0], match)
                match._match_name = "end_dict"

            return result

        def dict(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List]]:
            """
            This function checks for strict JSON dict.

            >>> StandardRules.Json.dict(b'{"1": null}')
            (11, [[b'{'], [], [], [], [[b'"', [b'1'], b'"'], [], b':', [b' '], [b'n', b'u', b'l', b'l'], []], [], [b'}']])
            >>> StandardRules.Json.dict(b'{"1": null, "2": true}')
            (22, [[b'{'], [], [[[[b'"', [b'1'], b'"'], [], b':', [b' '], [b'n', b'u', b'l', b'l'], []], b',', [b' ']]], [], [[b'"', [b'2'], b'"'], [], b':', [b' '], [b't', b'r', b'u', b'e'], []], [], [b'}']])
            >>> StandardRules.Json.dict(b'{"1": null, "2" : 1.5 , "3": {"test": true, "1": 2}, "4": [1, 2, false]}')
            (72, [[b'{'], [], [[[[b'"', [b'1'], b'"'], [], b':', [b' '], [b'n', b'u', b'l', b'l'], []], b',', [b' ']], [[[b'"', [b'2'], b'"'], [b' '], b':', [b' '], [[b'1'], b'.', [b'5']], [b' ']], b',', [b' ']], [[[b'"', [b'3'], b'"'], [], b':', [b' '], [[b'{'], [], [[[[b'"', [b't', b'e', b's', b't'], b'"'], [], b':', [b' '], [b't', b'r', b'u', b'e'], []], b',', [b' ']]], [], [[b'"', [b'1'], b'"'], [], b':', [b' '], [b'2'], []], [], [b'}']], []], b',', [b' ']]], [], [[b'"', [b'4'], b'"'], [], b':', [b' '], [[b'['], [], [[[b'1'], [], b',', [b' ']], [[b'2'], [], b',', [b' ']]], [], [b'f', b'a', b'l', b's', b'e'], [], [b']']], []], [], [b'}']])
            >>> StandardRules.Json.dict(b'{"1": null')
            (0, None)
            >>> StandardRules.Json.dict(b'{"1" null}')
            (0, None)
            >>> StandardRules.Json.dict(b'{"1", null}')
            (0, None)
            >>> StandardRules.Json.dict(b'{"1": null,}')
            (0, None)
            >>>
            """

            def dict_key_value(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Types.string,
                        StandardRules.Format.optional_blanks,
                        StandardMatch.check_char(58),
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json.full,
                        StandardRules.Format.optional_blanks,
                    ],
                    data,
                    position,
                )

            def dict_key_value_separator(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        dict_key_value,
                        StandardMatch.check_char(44),
                        StandardRules.Format.optional_blanks,
                    ],
                    data,
                    position,
                )

            def dict_keys_values(data: bytes, position: int):
                return PegParser.zero_or_more(
                    dict_key_value_separator,
                    data,
                    position,
                )

            def dict_non_empty(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_dict,
                        StandardRules.Format.optional_blanks,
                        dict_keys_values,
                        StandardRules.Format.optional_blanks,
                        dict_key_value,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json._end_dict,
                    ],
                    data,
                    position,
                )

            def dict_empty(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_dict,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json._end_dict,
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    dict_non_empty,
                    dict_empty,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "dict"

            return result

        def permissive_dict(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List]]:
            """
            This function checks for a permissive JSON dict
            (trailing comma, forgot comma, ...).

            >>> StandardRules.Json.permissive_dict(b'{}')
            (2, [[b'{'], [], [], [b'}']])
            >>> StandardRules.Json.permissive_dict(b'{"1": nuLl}')
            (11, [[b'{'], [], [], [], [[b'"', [b'1'], b'"'], [b':', [b' ']], [b'n', b'u', b'L', b'l']], [], [b'}']])
            >>> StandardRules.Json.permissive_dict(b'{1: null "2": true}')
            (19, [[b'{'], [], [[[[b'1'], [b':', [b' ']], [b'n', b'u', b'l', b'l']], [[b' ']]]], [], [[b'"', [b'2'], b'"'], [b':', [b' ']], [b't', b'r', b'u', b'e']], [], [b'}']])
            >>> StandardRules.Json.permissive_dict(b'{"1" null, "2" : 1.5 , "3": {"test" true "1" 2},"4" :[1 2, false]}')
            (66, [[b'{'], [], [[[[b'"', [b'1'], b'"'], [[b' ']], [b'n', b'u', b'l', b'l']], [b',', [b' ']]], [[[b'"', [b'2'], b'"'], [[b' '], b':', [b' ']], [[b'1'], b'.', [b'5']]], [[b' '], b',', [b' ']]], [[[b'"', [b'3'], b'"'], [b':', [b' ']], [[b'{'], [], [[[[b'"', [b't', b'e', b's', b't'], b'"'], [[b' ']], [b't', b'r', b'u', b'e']], [[b' ']]]], [], [[b'"', [b'1'], b'"'], [[b' ']], [b'2']], [], [b'}']]], [b',']]], [], [[b'"', [b'4'], b'"'], [[b' '], b':'], [[b'['], [], [[[b'1'], [[b' ']]], [[b'2'], [b',', [b' ']]]], [], [b'f', b'a', b'l', b's', b'e'], [], [b']']]], [], [b'}']])
            >>> StandardRules.Json.permissive_dict(b'{"1": null')
            (0, None)
            >>> StandardRules.Json.permissive_dict(b'{true null}')
            (11, [[b'{'], [], [], [], [[b't', b'r', b'u', b'e'], [[b' ']], [b'n', b'u', b'l', b'l']], [], [b'}']])
            >>> StandardRules.Json.permissive_dict(b'{"1" null,unDefinEd "2"}')
            (24, [[b'{'], [], [[[[b'"', [b'1'], b'"'], [[b' ']], [b'n', b'u', b'l', b'l']], [b',']]], [], [[b'u', b'n', b'D', b'e', b'f', b'i', b'n', b'E', b'd'], [[b' ']], [b'"', [b'2'], b'"']], [], [b'}']])
            >>> StandardRules.Json.permissive_dict(b'{"1" niL unDefinEd "2"}')
            (23, [[b'{'], [], [[[[b'"', [b'1'], b'"'], [[b' ']], [b'n', b'i', b'L']], [[b' ']]]], [], [[b'u', b'n', b'D', b'e', b'f', b'i', b'n', b'E', b'd'], [[b' ']], [b'"', [b'2'], b'"']], [], [b'}']])
            >>> StandardRules.Json.permissive_dict(b'{"1", null}')
            (0, None)
            >>> StandardRules.Json.permissive_dict(b'{1.5:null,}')
            (11, [[b'{'], [], [[[[[b'1'], b'.', [b'5']], [b':'], [b'n', b'u', b'l', b'l']], [b',']]], [b'}']])
            >>>
            """

            def separator(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.check_char(44),
                        StandardRules.Format.blanks,
                    ],
                    data,
                    position,
                )

            def separators(data: bytes, position: int):
                return PegParser.one_or_more(
                    separator,
                    data,
                    position,
                )

            def dict_separator_key_value(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.check_char(58),
                        StandardRules.Format.optional_blanks,
                    ],
                    data,
                    position,
                )

            def dict_separators_key_value(data: bytes, position: int):
                return PegParser.one_or_more(
                    dict_separator_key_value,
                    data,
                    position,
                )

            def dict_key_value(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json.permissive_simple_value,
                        dict_separators_key_value,
                        StandardRules.Json.permissive_full,
                    ],
                    data,
                    position,
                )

            def dict_key_value_separator(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        dict_key_value,
                        separators,
                    ],
                    data,
                    position,
                )

            def dict_keys_values(data: bytes, position: int):
                return PegParser.zero_or_more(
                    dict_key_value_separator,
                    data,
                    position,
                )

            def strict_dict(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_dict,
                        StandardRules.Format.optional_blanks,
                        dict_keys_values,
                        StandardRules.Format.optional_blanks,
                        dict_key_value,
                        StandardRules.Format.optional_blanks,
                        StandardRules.Json._end_dict,
                    ],
                    data,
                    position,
                )

            def flex_dict(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        StandardRules.Json._start_dict,
                        StandardRules.Format.optional_blanks,
                        dict_keys_values,
                        StandardRules.Json._end_dict,
                    ],
                    data,
                    position,
                )

            result = PegParser.ordered_choice(
                [
                    strict_dict,
                    flex_dict,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "permissive_dict"

            return result

        def full(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List]]:
            """
            This function matchs all JSON type (dict, list, string, float,
            integer, boolean, null).

            >>> StandardRules.Json.full(b'{}')
            (2, [[b'{'], [], [b'}']])
            >>> StandardRules.Json.full(b'{"key": "value", "test": "test"}')
            (32, [[b'{'], [], [[[[b'"', [b'k', b'e', b'y'], b'"'], [], b':', [b' '], [b'"', [b'v', b'a', b'l', b'u', b'e'], b'"'], []], b',', [b' ']]], [], [[b'"', [b't', b'e', b's', b't'], b'"'], [], b':', [b' '], [b'"', [b't', b'e', b's', b't'], b'"'], []], [], [b'}']])
            >>> StandardRules.Json.full(b'[]')
            (2, [[b'['], [], [b']']])
            >>> StandardRules.Json.full(b'[1, 2.5, nul]')
            (0, None)
            >>> StandardRules.Json.full(b'"string"')
            (8, [b'"', [b's', b't', b'r', b'i', b'n', b'g'], b'"'])
            >>> StandardRules.Json.full(b'1.5')
            (3, [[b'1'], b'.', [b'5']])
            >>> StandardRules.Json.full(b'1')
            (1, [b'1'])
            >>> StandardRules.Json.full(b'true')
            (4, [b't', b'r', b'u', b'e'])
            >>> StandardRules.Json.full(b'null')
            (4, [b'n', b'u', b'l', b'l'])
            >>>
            """

            return PegParser.ordered_choice(
                [
                    StandardRules.Json.dict,
                    StandardRules.Json.list,
                    StandardRules.Json.simple_value,
                ],
                data,
                position,
            )

        def permissive_full(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[None, List]]:
            """
            This function matchs all JSON permissive type
            (dict, list, string, float, integer, boolean, null).

            >>> StandardRules.Json.permissive_full(b'{}')
            (2, [[b'{'], [], [], [b'}']])
            >>> StandardRules.Json.permissive_full(b'{NONE: FAlse 1.5 "test", ,}')
            (27, [[b'{'], [], [[[[b'N', b'O', b'N', b'E'], [b':', [b' ']], [b'F', b'A', b'l', b's', b'e']], [[b' ']]], [[[[b'1'], b'.', [b'5']], [[b' ']], [b'"', [b't', b'e', b's', b't'], b'"']], [b',', [b' '], b',']]], [b'}']])
            >>> StandardRules.Json.permissive_full(b'[]')
            (2, [[b'['], [], [], [b']']])
            >>> StandardRules.Json.permissive_full(b'[1, 2.5, unDefiNed nIl ,,,, ]')
            (29, [[b'['], [], [[[b'1'], [b',', [b' ']]], [[[b'2'], b'.', [b'5']], [b',', [b' ']]], [[b'u', b'n', b'D', b'e', b'f', b'i', b'N', b'e', b'd'], [[b' ']]], [[b'n', b'I', b'l'], [[b' '], b',', b',', b',', b',', [b' ']]]], [b']']])
            >>> StandardRules.Json.permissive_full(b'"string"')
            (8, [b'"', [b's', b't', b'r', b'i', b'n', b'g'], b'"'])
            >>> StandardRules.Json.permissive_full(b'1.5')
            (3, [[b'1'], b'.', [b'5']])
            >>> StandardRules.Json.permissive_full(b'1')
            (1, [b'1'])
            >>> StandardRules.Json.permissive_full(b'trUe')
            (4, [b't', b'r', b'U', b'e'])
            >>> StandardRules.Json.permissive_full(b'nUll')
            (4, [b'n', b'U', b'l', b'l'])
            >>>
            """

            return PegParser.ordered_choice(
                [
                    StandardRules.Json.permissive_dict,
                    StandardRules.Json.permissive_list,
                    StandardRules.Json.permissive_simple_value,
                ],
                data,
                position,
            )

    class Path:
        """
        This class implements Windows and NT path.
        """

        def base_filename(
            data: bytes, position: int = 0, in_extension: bool = False
        ) -> Tuple[int, Union[None, Iterable[bytes]]]:
            r"""
            This function matchs base filename.

            >>> StandardRules.Path.base_filename(b'test')
            (4, [b't', b'e', b's', b't'])
            >>> StandardRules.Path.base_filename(b't test*test')
            (6, [b't', b' ', b't', b'e', b's', b't'])
            >>> StandardRules.Path.base_filename(b'$MFT')
            (4, [b'$', b'M', b'F', b'T'])
            >>> StandardRules.Path.base_filename(b'\\test')
            (0, None)
            >>>
            """

            def characters(data: bytes, position: int):
                return PegParser.ordered_choice(
                    [
                        StandardMatch.is_letter,
                        StandardMatch.is_digit,
                        StandardMatch.or_check_chars(
                            32,
                            33,
                            36,
                            37,
                            38,
                            39,
                            40,
                            41,
                            43,
                            44,
                            45,
                            58,
                            61,
                            64,
                            91,
                            93,
                            94,
                            95,
                            96,
                            123,
                            125,
                            126,
                        ),
                    ],
                    data,
                    position,
                )

            result = PegParser.one_or_more(
                characters,
                data,
                position,
            )

            if not in_extension and isinstance(result[1], MatchList):
                result[1]._match_name = "base_filename"

            return result

        def extensions(
            data: bytes, position: int = 0
        ) -> Tuple[
            int, Union[None, Iterable[Iterable[Union[bytes, Iterable[bytes]]]]]
        ]:
            """
            This function matchs extensions.

            >>> StandardRules.Path.extensions(b'.exe')
            (4, [[b'.', [b'e', b'x', b'e']]])
            >>> StandardRules.Path.extensions(b'.dll')
            (4, [[b'.', [b'd', b'l', b'l']]])
            >>> StandardRules.Path.extensions(b'.py')
            (3, [[b'.', [b'p', b'y']]])
            >>> StandardRules.Path.extensions(b'.c.txt.zip.tar.gz')
            (17, [[b'.', [b'c']], [b'.', [b't', b'x', b't']], [b'.', [b'z', b'i', b'p']], [b'.', [b't', b'a', b'r']], [b'.', [b'g', b'z']]])
            >>>
            """

            def extension(data: bytes, position: int):
                result = PegParser.sequence(
                    [
                        StandardMatch.check_char(46),
                        StandardRules.Path.base_filename,
                    ],
                    data,
                    position,
                )

                if isinstance(result[1], MatchList):
                    result[1]._match_name = "extension"

                return result

            return PegParser.one_or_more(
                extension,
                data,
                position,
            )

        def filename_extension(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[Iterable[Iterable[Union[bytes, Iterable[bytes]]]]],
            ],
        ]:
            r"""
            This function matchs filename with extension.

            >>> StandardRules.Path.filename_extension(b'test.exe')
            (8, [[b't', b'e', b's', b't'], [[b'.', [b'e', b'x', b'e']]]])
            >>> StandardRules.Path.filename_extension(b'test*test.test')
            (0, None)
            >>> StandardRules.Path.filename_extension(b'$MFT.txt.tar.gz')
            (15, [[b'$', b'M', b'F', b'T'], [[b'.', [b't', b'x', b't']], [b'.', [b't', b'a', b'r']], [b'.', [b'g', b'z']]]])
            >>> StandardRules.Path.filename_extension(b'\\test.py')
            (0, None)
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardRules.Path.base_filename,
                    StandardRules.Path.extensions,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "filename_extension"

            return result

        def filename(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                None,
                Iterable[Iterable[Iterable[Union[bytes, Iterable[bytes]]]]],
            ],
        ]:
            r"""
            This function matchs filename.

            >>> StandardRules.Path.filename(b'test')
            (4, [b't', b'e', b's', b't'])
            >>> StandardRules.Path.filename(b'test*test.test')
            (4, [b't', b'e', b's', b't'])
            >>> StandardRules.Path.filename(b'$MFT.txt.tar.gz')
            (15, [[b'$', b'M', b'F', b'T'], [[b'.', [b't', b'x', b't']], [b'.', [b't', b'a', b'r']], [b'.', [b'g', b'z']]]])
            >>> StandardRules.Path.filename(b'\\test.py')
            (0, None)
            >>>
            """

            result = PegParser.ordered_choice(
                [
                    StandardRules.Path.filename_extension,
                    StandardRules.Path.base_filename,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "filename"

            return result

        def _directory_file(data: bytes, position: int, unix: bool = False):
            def base(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        lambda d, p: PegParser.one_or_more(
                            StandardMatch.check_char(47 if unix else 92), d, p
                        ),
                        StandardRules.Path.filename,
                    ],
                    data,
                    position,
                )

            def relative(data: bytes, position: int):
                return PegParser.sequence(
                    [
                        lambda d, p: PegParser.one_or_more(
                            StandardMatch.check_char(47 if unix else 92), d, p
                        ),
                        lambda d, p: PegParser.one_or_more(
                            StandardMatch.check_char(46), d, p
                        ),
                    ],
                    data,
                    position,
                )

            return PegParser.ordered_choice(
                [
                    base,
                    relative,
                ],
                data,
                position,
            )

        def _directories_file(data: bytes, position: int, unix: bool = False):
            return PegParser.one_or_more(
                lambda d, p: StandardRules.Path._directory_file(d, p, unix),
                data,
                position,
            )

        def _directories_or_file(
            data: bytes, position: int, unix: bool = False
        ):
            return PegParser.ordered_choice(
                [
                    lambda d, p: PegParser.sequence(
                        [
                            lambda x, y: StandardRules.Path._directories_file(
                                x, y, unix
                            ),
                            StandardMatch.check_char(47 if unix else 92),
                        ],
                        d,
                        p,
                    ),
                    lambda d, p: StandardRules.Path._directories_file(
                        d, p, unix
                    ),
                ],
                data,
                position,
            )

        def drive_path(data: bytes, position: int = 0) -> Tuple[
            int,
            Union[
                Iterable[
                    Union[
                        bytes,
                        Iterable[
                            Iterable[
                                Iterable[
                                    Union[
                                        bytes,
                                        Iterable[
                                            Union[Iterable[bytes], bytes]
                                        ],
                                    ]
                                ]
                            ]
                        ],
                    ]
                ],
                None,
            ],
        ]:
            r"""
            This function matchs Windows path starting by drive letter.

            >>> StandardRules.Path.drive_path(b'D:\\test')
            (7, [b'D', b':', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.drive_path(b'D:\\test\\')
            (8, [b'D', b':', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.drive_path(b'D:\\test\\1\\2\\test.txt')
            (20, [b'D', b':', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.is_letter,
                    StandardMatch.check_char(58),
                    StandardRules.Path._directories_or_file,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "drive_path"

            return result

        def nt_path(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[Iterable, None]]:
            r"""
            This function matchs NT path.

            >>> StandardRules.Path.nt_path(b'\\\\?\\test')
            (8, [b'\\', b'\\', b'?', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.nt_path(b'\\\\.\\test\\')
            (9, [b'\\', b'\\', b'.', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.nt_path(b'\\\\.\\test\\1\\2\\test.txt')
            (21, [b'\\', b'\\', b'.', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(92),
                    StandardMatch.check_char(92),
                    StandardMatch.or_check_chars(46, 63),
                    StandardRules.Path._directories_or_file,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "nt_path"

            return result

        def relative_path(
            data: bytes, position: int = 0, unix: bool = False
        ) -> Tuple[
            int,
            Union[
                Iterable[
                    Union[
                        bytes,
                        Iterable[
                            Iterable[
                                Iterable[
                                    Union[
                                        bytes,
                                        Iterable[
                                            Union[
                                                Iterable[
                                                    Union[
                                                        bytes, Iterable[bytes]
                                                    ]
                                                ],
                                                bytes,
                                            ]
                                        ],
                                    ]
                                ]
                            ]
                        ],
                    ]
                ],
                None,
            ],
        ]:
            r"""
            This function matchs relative path.

            >>> StandardRules.Path.relative_path(b'.\\test')
            (6, [b'.', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.relative_path(b'.\\test\\')
            (7, [b'.', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.relative_path(b'.\\test\\1\\2\\test.txt')
            (19, [b'.', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>>
            """

            result = PegParser.sequence(
                [
                    StandardMatch.check_char(46),
                    lambda x, y: StandardRules.Path._directories_or_file(
                        x, y, unix
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "relative_path"

            return result

        def windows_path(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[Iterable, None]]:
            r"""
            This function matchs Windows path.

            >>> StandardRules.Path.windows_path(b'.\\test')
            (6, [b'.', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.windows_path(b'.\\test\\')
            (7, [b'.', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.windows_path(b'.\\test\\1\\2\\test.txt')
            (19, [b'.', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>> StandardRules.Path.windows_path(b'\\\\?\\test')
            (8, [b'\\', b'\\', b'?', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.windows_path(b'\\\\.\\test\\')
            (9, [b'\\', b'\\', b'.', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.windows_path(b'\\\\.\\test\\1\\2\\test.txt')
            (21, [b'\\', b'\\', b'.', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>> StandardRules.Path.windows_path(b'D:\\test')
            (7, [b'D', b':', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.windows_path(b'D:\\test\\')
            (8, [b'D', b':', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.windows_path(b'D:\\test\\1\\2\\test.txt')
            (20, [b'D', b':', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>>
            """

            result = PegParser.ordered_choice(
                [
                    StandardRules.Path.drive_path,
                    StandardRules.Path.nt_path,
                    StandardRules.Path.relative_path,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "windows_path"

            return result

        def linux_path(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[Iterable, None]]:
            """
            This function matchs Linux path.

            >>> StandardRules.Path.linux_path(b'./test')
            (6, [b'.', [[[b'/'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.linux_path(b'/root/test')
            (10, [[[b'/'], [b'r', b'o', b'o', b't']], [[b'/'], [b't', b'e', b's', b't']]])
            >>> StandardRules.Path.linux_path(b'/root/test.txt')
            (14, [[[b'/'], [b'r', b'o', b'o', b't']], [[b'/'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]])
            >>> StandardRules.Path.linux_path(b'/1/2/3/.././../4/test.tar.gz')
            (28, [[[b'/'], [b'1']], [[b'/'], [b'2']], [[b'/'], [b'3']], [[b'/'], [b'.', b'.']], [[b'/'], [b'.']], [[b'/'], [b'.', b'.']], [[b'/'], [b'4']], [[b'/'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'a', b'r']], [b'.', [b'g', b'z']]]]]])
            >>>
            """

            result = PegParser.ordered_choice(
                [
                    lambda d, p: StandardRules.Path.relative_path(d, p, True),
                    lambda d, p: StandardRules.Path._directories_or_file(
                        d, p, True
                    ),
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "linux_path"

            return result

        def path(
            data: bytes, position: int = 0
        ) -> Tuple[int, Union[Iterable, None]]:
            r"""
            This function matchs system path.

            >>> StandardRules.Path.path(b'./test')
            (6, [b'.', [[[b'/'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.path(b'/root/test')
            (10, [[[b'/'], [b'r', b'o', b'o', b't']], [[b'/'], [b't', b'e', b's', b't']]])
            >>> StandardRules.Path.path(b'/root/test.txt')
            (14, [[[b'/'], [b'r', b'o', b'o', b't']], [[b'/'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]])
            >>> StandardRules.Path.path(b'/1/2/3/.././../4/test.tar.gz')
            (28, [[[b'/'], [b'1']], [[b'/'], [b'2']], [[b'/'], [b'3']], [[b'/'], [b'.', b'.']], [[b'/'], [b'.']], [[b'/'], [b'.', b'.']], [[b'/'], [b'4']], [[b'/'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'a', b'r']], [b'.', [b'g', b'z']]]]]])
            >>> StandardRules.Path.path(b'.\\test')
            (6, [b'.', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.path(b'.\\test\\')
            (7, [b'.', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.path(b'.\\test\\1\\2\\test.txt')
            (19, [b'.', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>> StandardRules.Path.path(b'\\\\?\\test')
            (8, [b'\\', b'\\', b'?', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.path(b'\\\\.\\test\\')
            (9, [b'\\', b'\\', b'.', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.path(b'\\\\.\\test\\1\\2\\test.txt')
            (21, [b'\\', b'\\', b'.', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>> StandardRules.Path.path(b'D:\\test')
            (7, [b'D', b':', [[[b'\\'], [b't', b'e', b's', b't']]]])
            >>> StandardRules.Path.path(b'D:\\test\\')
            (8, [b'D', b':', [[[[b'\\'], [b't', b'e', b's', b't']]], b'\\']])
            >>> StandardRules.Path.path(b'D:\\test\\1\\2\\test.txt')
            (20, [b'D', b':', [[[b'\\'], [b't', b'e', b's', b't']], [[b'\\'], [b'1']], [[b'\\'], [b'2']], [[b'\\'], [[b't', b'e', b's', b't'], [[b'.', [b't', b'x', b't']]]]]]])
            >>>
            """

            result = PegParser.ordered_choice(
                [
                    StandardRules.Path.linux_path,
                    StandardRules.Path.windows_path,
                ],
                data,
                position,
            )

            if isinstance(result[1], MatchList):
                result[1]._match_name = "system_path"

            return result


def match_getter(
    data: Iterable[Union[bytes, bool, Iterable]],
    process: Callable[str, bytearray],
) -> None:
    """
    This function gets all matchs and call `process`
    with `_match_name` and `data` as parameters.
    """

    def process_element(element):
        if isinstance(element, bool):
            return None

        if isinstance(element, MatchList):
            if getattr(element, "_match_name", None):
                process(element._match_name, flatten_bytes(element))

            for sub_element in element:
                process_element(sub_element)

    def flatten_bytes(element):
        byte_data = bytearray()
        for sublist in element:
            if isinstance(sublist, bytes):
                byte_data.extend(sublist)
            elif isinstance(sublist, MatchList):
                byte_data.extend(flatten_bytes(sublist))
        return byte_data

    process_element(data)


def get_ordered_matchs(
    data: Iterable[Union[bytes, bool, Iterable]]
) -> List[Tuple[str, bytearray]]:
    r"""
    This function returns the ordered match into a list of tuple.

    >>> get_ordered_matchs(StandardRules.Csv.full(b'"1","","other"\n"2"\n"3","test"')[1])
    [('csv', bytearray(b'"1","","other"\n"2"\n"3","test"')), ('csv_line', bytearray(b'"1","","other"')), ('csv_quoted_value', bytearray(b'"1"')), ('csv_value', bytearray(b'1')), ('csv_values', bytearray(b',"","other"')), ('csv_quoted_value', bytearray(b'""')), ('csv_value', bytearray(b'')), ('csv_quoted_value', bytearray(b'"other"')), ('csv_value', bytearray(b'other')), ('csv_line', bytearray(b'"2"')), ('csv_quoted_value', bytearray(b'"2"')), ('csv_value', bytearray(b'2')), ('csv_values', bytearray(b'')), ('csv_line', bytearray(b'"3","test"')), ('csv_quoted_value', bytearray(b'"3"')), ('csv_value', bytearray(b'3')), ('csv_values', bytearray(b',"test"')), ('csv_quoted_value', bytearray(b'"test"')), ('csv_value', bytearray(b'test'))]
    >>> get_ordered_matchs(StandardRules.Csv.multi(b'"1","","other"\n"2"\n"3","test"\n\r\n"1","","other"\r\n"2"\r\n"3","test"')[1])
    [('multi_csv', bytearray(b'"1","","other"\n"2"\n"3","test"\n\r\n"1","","other"\r\n"2"\r\n"3","test"')), ('csv', bytearray(b'"1","","other"\n"2"\n"3","test"')), ('csv_line', bytearray(b'"1","","other"')), ('csv_quoted_value', bytearray(b'"1"')), ('csv_value', bytearray(b'1')), ('csv_values', bytearray(b',"","other"')), ('csv_quoted_value', bytearray(b'""')), ('csv_value', bytearray(b'')), ('csv_quoted_value', bytearray(b'"other"')), ('csv_value', bytearray(b'other')), ('csv_line', bytearray(b'"2"')), ('csv_quoted_value', bytearray(b'"2"')), ('csv_value', bytearray(b'2')), ('csv_values', bytearray(b'')), ('csv_line', bytearray(b'"3","test"')), ('csv_quoted_value', bytearray(b'"3"')), ('csv_value', bytearray(b'3')), ('csv_values', bytearray(b',"test"')), ('csv_quoted_value', bytearray(b'"test"')), ('csv_value', bytearray(b'test')), ('csv', bytearray(b'"1","","other"\r\n"2"\r\n"3","test"')), ('csv_line', bytearray(b'"1","","other"')), ('csv_quoted_value', bytearray(b'"1"')), ('csv_value', bytearray(b'1')), ('csv_values', bytearray(b',"","other"')), ('csv_quoted_value', bytearray(b'""')), ('csv_value', bytearray(b'')), ('csv_quoted_value', bytearray(b'"other"')), ('csv_value', bytearray(b'other')), ('csv_line', bytearray(b'"2"')), ('csv_quoted_value', bytearray(b'"2"')), ('csv_value', bytearray(b'2')), ('csv_values', bytearray(b'')), ('csv_line', bytearray(b'"3","test"')), ('csv_quoted_value', bytearray(b'"3"')), ('csv_value', bytearray(b'3')), ('csv_values', bytearray(b',"test"')), ('csv_quoted_value', bytearray(b'"test"')), ('csv_value', bytearray(b'test'))]
    >>>
    """

    matches = []
    match_getter(data, lambda name, data: matches.append((name, data)))
    return matches


def get_matchs(
    data: Iterable[Union[bytes, bool, Iterable]]
) -> Dict[str, List[bytearray]]:
    r"""
    This function returns the structured matches into a dict.

    >>> get_matchs(StandardRules.Url.full(b"https://my.full.url/with/path;and=parameters?query=too#fragment")[1])
    defaultdict(<class 'list'>, {'url': [bytearray(b'https://my.full.url/with/path;and=parameters?query=too#fragment')], 'scheme': [bytearray(b'https')], 'host': [bytearray(b'my.full.url')], 'hostname': [bytearray(b'my'), bytearray(b'full'), bytearray(b'url')], 'path': [bytearray(b'/with/path')], 'parameters': [bytearray(b';and=parameters')], 'form_data': [bytearray(b'and=parameters')], 'query': [bytearray(b'?query=too')], 'fragment': [bytearray(b'#fragment')]})
    >>> get_matchs(StandardRules.Csv.full(b'"1","","other"\n"2"\n"3","test"')[1])
    defaultdict(<class 'list'>, {'csv': [bytearray(b'"1","","other"\n"2"\n"3","test"')], 'csv_line': [bytearray(b'"1","","other"'), bytearray(b'"2"'), bytearray(b'"3","test"')], 'csv_quoted_value': [bytearray(b'"1"'), bytearray(b'""'), bytearray(b'"other"'), bytearray(b'"2"'), bytearray(b'"3"'), bytearray(b'"test"')], 'csv_value': [bytearray(b'1'), bytearray(b''), bytearray(b'other'), bytearray(b'2'), bytearray(b'3'), bytearray(b'test')], 'csv_values': [bytearray(b',"","other"'), bytearray(b''), bytearray(b',"test"')]})
    >>>
    """

    match_dict = defaultdict(list)
    match_getter(data, lambda name, data: match_dict[name].append(data))
    return match_dict


def csv_parse(data: bytes) -> Iterable[Tuple[str]]:
    r"""
    This function parses CSV lines and yield values for each lines.

    >>> list(csv_parse(b'"1","","other"\n"2"\n"3","test"'))
    [('1', '', 'other'), ('2',), ('3', 'test')]
    >>>
    """

    position = 0
    data_length = len(data)

    while data_length != position:
        if position:
            position, result = StandardRules.Csv.line_delimiter(data, position)
            if result is None:
                error = ValueError("Invalid CSV data at " + str(position))
                error.position = position
                raise error
        position, result = StandardRules.Csv.line(data, position)
        if result is None:
            if data_length == position:
                break
            error = ValueError("Invalid CSV data at " + str(position))
            error.position = position
            raise error
        yield tuple(x.decode() for x in get_matchs(result)["csv_value"])


def get_json(
    data: bytes, permissive: bool = False
) -> Union[Union[List, Dict, bool, int, float, None]]:
    r"""
    This function returns the JSON content as python object.

    >>> get_json(b'{"1": null, "2" : 1.5 , "3": {"test": true, "1": 2}, "4": [1, 2, false]}')
    {'1': None, '2': 1.5, '3': {'test': True, '1': 2}, '4': [1, 2, False]}
    >>> get_json(b"[1, 2.5, unDefiNed nIl ,,{'test\\n' trUE fALSe nUll},, ]", True)
    [1, 2.5, None, None, {'test\n': True, False: None}]
    >>>
    """

    position, matchs = (
        StandardRules.Json.permissive_full
        if permissive
        else StandardRules.Json.full
    )(data)

    if matchs is not None and len(data) == position:
        return get_json_from_ordered_matchs(get_ordered_matchs(matchs))

    raise ValueError("Invalid JSON at:" + str(position))


def get_json_from_ordered_matchs(
    data: List[Tuple[str, bytearray]]
) -> Union[Union[List, Dict, bool, int, float, None]]:
    """
    This function returns a python object from the ordered matchs.

    >>> get_json_from_ordered_matchs(get_ordered_matchs(StandardRules.Json.full(b'{"1": null, "2" : 1.5 , "3": {"test": true, "1": 2}, "4": [1, 2, false]}')[1]))
    {'1': None, '2': 1.5, '3': {'test': True, '1': 2}, '4': [1, 2, False]}
    >>>
    """

    def call(data):
        if function := functions.get(
            data[0][0][11:]
            if data[0][0].startswith("permissive_")
            else data[0][0]
        ):
            return function(data[0][1], data[1:])
        return call(data[1:])

    def start_dict(data, matchs):
        data = {}
        while matchs[0][0] != "end_dict":
            key = call(matchs)[0]
            matchs = matchs[1:]
            value, matchs = call(matchs)
            data[key] = value
        return data, matchs[1:]

    def start_list(data, matchs):
        data = []
        while matchs[0][0] != "end_list":
            value, matchs = call(matchs)
            data.append(value)
        return data, matchs[1:]

    def digits(data, matchs):
        return int(data.decode()), matchs

    def hex_integer(data, matchs):
        return int(data.decode(), 16), matchs

    def octal_integer(data, matchs):
        return int(data.decode(), 8), matchs

    def strings(data, matchs):
        return decode(data[1:-1].decode(), "unicode_escape"), matchs

    def float2(data, matchs):
        return float(data.decode()), matchs[2:]

    def null(data, matchs):
        return None, matchs

    def true(data, matchs):
        return True, matchs

    def false(data, matchs):
        return False, matchs

    functions = locals()
    functions["float"] = functions["float2"]
    return call(data)[0]


def mjson_file_parse(
    file: _BufferedIOBase, permissive: bool = False
) -> Iterable[Union[List, Dict, bool, int, float, None]]:
    r"""
    This generator parses mJSON file and yield JSON for each line.

    >>> from io import BytesIO
    >>> list(mjson_file_parse(BytesIO(b'{}\n{"1": 1, "2": [true, false, null, 1.5, {"test": []}]}')))
    [{}, {'1': 1, '2': [True, False, None, 1.5, {'test': []}]}]
    >>> list(mjson_file_parse(BytesIO(b"{}\n{'1' 1,'2' [true false,null 1.5 {'test' []},,,],, }"), True))
    [{}, {'1': 1, '2': [True, False, None, 1.5, {'test': []}]}]
    >>>
    """

    file_position = file.tell()
    parser = (
        StandardRules.Json.permissive_full
        if permissive
        else StandardRules.Json.full
    )
    for line in file:
        if line[-1] == 10:
            line = line[:-1]
        position, data = parser(line)
        if data is None or len(line) != position:
            raise ValueError("Invalid JSON at:", position + file_position)
        yield get_json_from_ordered_matchs(get_ordered_matchs(data))


def csv_file_parse(file: _BufferedIOBase) -> Iterable[List[str]]:
    r"""
    This generator parses CSV file and yield values for each line.

    >>> from io import BytesIO
    >>> list(csv_file_parse(BytesIO(b'"1","","other"\n"2"\n"3","test"')))
    [('1', '', 'other'), ('2',), ('3', 'test')]
    >>> list(csv_file_parse(BytesIO(b'"1","","other"\n"2"\n"3","test"\n')))
    [('1', '', 'other'), ('2',), ('3', 'test')]
    >>>
    """

    data = True

    for line in file:
        if data is None:
            error = ValueError("Invalid CSV data at " + str(file_position))
            error.position = file_position
            raise error
        position, data = StandardRules.Csv.line(line, 0)
        if data is None:
            file_position = file.tell()
            continue
        yield tuple(x.decode() for x in get_matchs(data)["csv_value"])
        _, data = StandardRules.Csv.line_delimiter(line, position)
        file_position = file.tell()


def csv_files_parse(file: _BufferedIOBase) -> Iterable[List[str]]:
    r"""
    This function parses multi-CSV file, yield generator for each
    file and yield values for each lines.

    >>> from io import BytesIO
    >>> [list(x) for x in csv_files_parse(BytesIO(b'"1","","other"\n"2"\n"3","test"\n\r\n"1","","other"\r\n"2"\r\n"3","test"'))]
    [[('1', '', 'other'), ('2',), ('3', 'test')], [('1', '', 'other'), ('2',), ('3', 'test')]]
    >>>
    """

    error = True
    data = []
    while error:
        try:
            for line in csv_file_parse(file):
                data.append(line)
            yield data
            error = False
        except ValueError as e:
            if not hasattr(e, "position"):
                raise e
            file.seek(e.position)
            yield data
            data = []


def get_http_content(data: Iterable[Union[bytes, Iterable]]) -> Tuple[
    Dict[str, List[bytearray]],
    List[Tuple[str, str]],
    int,
    Union[None, str],
    Union[None, str],
]:
    """
    This function takes parsed HTTP response or request and use the parsing
    to transform into useful python object.
    """

    matches = get_matchs(data)
    headers = []
    values = matches["field_value"]
    host = None
    content_type = None
    content_length = 0

    for i, name in enumerate(matches["field_name"]):
        name = name.decode("ascii")
        value = values[i].decode("ascii")
        headers.append((name, value))
        if name.casefold() == "content-length":
            content_length = int(value)
        elif name.casefold() == "content-type":
            content_type = value
        elif name.casefold() == "host":
            host = value

    return matches, headers, content_length, content_type, host


def parse_http_request(data: bytes) -> HttpRequest:
    r"""
    This function takes HTTP request bytes as arguments,
    parses it and generates the HttpRequest object.

    >>> parse_http_request(b'POST /test;test=test?test=test HTTP/1.0\r\nHost: myhost\r\nContent-Type: application/json; charset="utf-8"\r\nContent-Length: 12\r\n\r\nabcdefabcdef')
    HttpRequest(verb='POST', uri='/test;test=test?test=test', magic=b'HTTP', version=1.0, headers=[('Host', 'myhost'), ('Content-Type', 'application/json; charset="utf-8"'), ('Content-Length', '12')], body=b'abcdefabcdef', content_length=12, content_type='application/json; charset="utf-8"', host='myhost')
    >>>
    """

    content_start, request = StandardRules.Http.request(data)

    if not request:
        raise ValueError("Invalid HTTP request")

    request_matches, headers, content_length, content_type, host = (
        get_http_content(request)
    )

    return HttpRequest(
        request_matches["verb"][0].decode("ascii"),
        request_matches["uri"][0].decode("ascii"),
        bytes(request_matches["magic"][0]),
        float(request_matches["version"][0].decode("ascii")),
        headers,
        data[content_start:],
        content_length,
        content_type,
        host,
    )


def parse_http_response(data: bytes) -> HttpResponse:
    r"""
    This function takes HTTP response bytes as arguments,
    parses it and generates the HttpResponse object.

    >>> parse_http_response(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 12\r\n\r\nabcdefabcdef')
    HttpResponse(magic=b'HTTP', version=1.1, code=200, reason='OK', headers=[('Content-Type', 'application/json'), ('Content-Length', '12')], body=b'abcdefabcdef', content_length=12, content_type='application/json')
    >>>
    """

    body_start, response = StandardRules.Http.response(data)

    if not response:
        raise ValueError("Invalid HTTP response")

    response_matches, headers, content_length, content_type, _ = (
        get_http_content(response)
    )

    return HttpResponse(
        bytes(response_matches["magic"][0]),
        float(response_matches["version"][0].decode("ascii")),
        int(response_matches["status_code"][0].decode("ascii")),
        response_matches["reason"][0].decode("ascii"),
        headers,
        data[body_start:],
        content_length,
        content_type,
    )


def match(
    rule: Callable, data: bytes, minimum_length: int = 0
) -> Union[None, bytes]:
    r"""
    This function returns the full match for a rule on data.

    >>> match(StandardRules.Path.path, b'D:\\test\\1\\2\\test.txt\0', 7)
    b'D:\\test\\1\\2\\test.txt'
    >>> match(StandardRules.Path.path, b'\\\\?\\test\\1\\2\\test.txt**', 7)
    b'\\\\?\\test\\1\\2\\test.txt'
    >>> match(StandardRules.Path.path, b'/1/2/3/.././../4/test.tar.gz\7', 7)
    b'/1/2/3/.././../4/test.tar.gz'
    >>> match(StandardRules.Path.path, b'./test.txt\0\1', 7)
    b'./test.txt'
    >>>
    """

    position, match = rule(data)

    if match is not None and minimum_length <= position:
        return data[:position]


StandardRules_Url = StandardRules.Url
StandardRules_Csv = StandardRules.Csv
StandardRules_Path = StandardRules.Path
StandardRules_Json = StandardRules.Json
StandardRules_Http = StandardRules.Http
StandardRules_Types = StandardRules.Types
StandardRules_Format = StandardRules.Format
StandardRules_Network = StandardRules.Network


def host_port_true_positive(host_port: bytes) -> bool:
    """
    >>> host_port_true_positive(b'1456:45')
    False
    >>> host_port_true_positive(b'update.windows.xyz:443')
    True
    >>>
    """

    host, port = host_port.rsplit(b":", 1)
    return (
        len(host_port) > 15
        and len(port) > 2
        and (b"." in host or b"[" in host)
    )


def host_port_false_positive(host_port: bytes) -> bool:
    """
    >>> host_port_false_positive(b'1456:45')
    True
    >>> host_port_false_positive(b'update.windows.xyz:443')
    False
    >>>
    """

    host, port = host_port.rsplit(b":", 1)
    return (
        len(host_port) < 10
        or len(port) < 2
        or not (b"." in host or b"[" in host)
    )


def linux_path_true_positive(linux_path: bytes) -> bool:
    """
    >>> linux_path_true_positive(b'windows/update.php')
    True
    >>> linux_path_true_positive(b'/test/o+e...t')
    False
    >>>
    """

    if len(linux_path) < 15:
        return False
    splitted = linux_path.split(b"/")
    splitted_length = len(splitted)
    if splitted_length < 3:
        return all((97 <= x <= 122 or x == 46 or x == 47) for x in linux_path)
    root, *directories, file = splitted
    if not root and splitted_length < 4:
        return False
    return all(46 <= character <= 122 for character in linux_path)


def linux_path_false_positive(linux_path: bytes) -> bool:
    """
    >>> linux_path_false_positive(b'windows/update.php')
    False
    >>> linux_path_false_positive(b'/test/o+e...t')
    True
    >>>
    """

    if len(linux_path) < 9:
        return True
    splitted = linux_path.split(b"/")
    splitted_length = len(splitted)
    if splitted_length < 3:
        return not all(
            (97 <= x <= 122 or x == 46 or x == 47) for x in linux_path
        )
    root, *directories, file = splitted
    if not root and splitted_length < 4:
        return True
    return not all(directories)


def filename_false_positive(filename: bytes) -> bool:
    """
    >>> filename_false_positive(b'update.php')
    False
    >>> filename_false_positive(b'e...t')
    True
    >>>
    """

    if len(filename) < 8:
        return True

    extension = False
    length = 0

    for character in filename:
        is_legit_character = (
            48 <= character <= 57
            or 65 <= character <= 90
            or 97 <= character <= 122
        )
        if extension and not is_legit_character:
            return True
        elif is_legit_character:
            length += 1
        elif character == 46:
            extension = True

    return (
        length < 7
        or len(
            filename.rsplit(
                b".",
            )[-1]
        )
        > 5
    )


def word_false_positive(word: bytes) -> bool:
    """
    >>> word_false_positive(b'GetSystemTime')
    False
    >>> word_false_positive(b'abcdefgh')
    True
    >>>
    """

    length = len(word)
    if length < 7:
        return True

    characters = set()
    first = True
    lower_count = 0

    for character in word:
        if 97 <= character <= 122:
            characters.add(character)
            if first:
                first = False
                continue
            lower_count += 1
        else:
            characters.add((character + 32))

    if lower_count < 6:
        return True

    characters_length = len(characters)
    if characters_length == length:
        return True

    if length < 10 and characters_length > 8:
        return True

    if length < 15 and characters_length > 12:
        return True

    if length < 20 and characters_length > 16:
        return True

    return characters_length >= 20


def word_true_positive(word: bytes) -> bool:
    """
    >>> word_true_positive(b'GetSystemTime')
    True
    >>> word_true_positive(b'abcdefgh')
    False
    >>>
    """

    length = len(word)
    if length < 9:
        return False

    characters = set()
    first = True
    lower_count = 0

    for character in word:
        if 97 <= character <= 122:
            characters.add(character)
            if first:
                first = False
                continue
            lower_count += 1
        else:
            characters.add(character - 32)

    if lower_count < 8:
        return True

    characters_length = len(characters)
    if characters_length == length:
        return False

    if length < 10 and characters_length > 7:
        return False

    if length < 15 and characters_length > 10:
        return False

    if length < 20 and characters_length > 13:
        return False

    return characters_length < 17


def uri_false_positive(uri: bytes) -> bytes:
    """
    >>> uri_false_positive(b'ftp://test.com/')
    False
    >>> uri_false_positive(b'test+test:test@com')
    True
    >>>
    """

    for character in uri:
        if character == 58:
            break
        elif not (97 <= character <= 122 or 65 <= character <= 90):
            return True
    return b"://" not in uri or b":" in uri[-6:]


def uri_true_positive(uri: bytes) -> bytes:
    """
    >>> uri_true_positive(b'http://test.com/')
    True
    >>> uri_true_positive(b'test+test:test@com')
    False
    >>>
    """

    for character in uri:
        if character == 58:
            break
        elif not (97 <= character <= 122 or 65 <= character <= 90):
            return False
    return b"://" in uri and b":" not in uri[-10:] and b":" not in uri[:4]


formats = {
    "json": Format(
        "json",
        partial(match, StandardRules.Json.full),
        lambda x: x,
        lambda x: StandardRules.Json.dict(x)[1] is not None
        or StandardRules.Json.list(x)[1] is not None,
        lambda x: len(x) < 20,
    ),
    "http_response": Format(
        "http_response",
        partial(match, StandardRules.Http.response),
        lambda x: x,
        lambda x: True,
        lambda x: False,
    ),
    "http_request": Format(
        "http_request",
        partial(match, StandardRules.Http.request),
        lambda x: x,
        lambda x: True,
        lambda x: False,
    ),
    "uri": Format(
        "uri",
        partial(match, StandardRules.Url.full),
        lambda x: x,
        uri_true_positive,
        uri_false_positive,
    ),
    "windows_path": Format(
        "windows_path",
        partial(match, StandardRules.Path.windows_path),
        lambda x: x,
        lambda x: len(x) > 20,
        lambda x: len(x) < 10,
    ),
    "linux_path": Format(
        "linux_path",
        partial(match, StandardRules.Path.linux_path),
        lambda x: x,
        linux_path_true_positive,
        linux_path_false_positive,
    ),
    "filename": Format(
        "filename",
        partial(match, StandardRules.Path.filename_extension),
        lambda x: x,
        lambda x: len(x) > 10
        and len(x.split(b".")[-1]) < 5
        and not [
            y
            for y in x
            if not (
                y == 46 or 48 <= y <= 57 or 65 <= y <= 90 or 97 <= y <= 122
            )
        ],
        filename_false_positive,
    ),
    "host_port": Format(
        "host_port",
        partial(match, StandardRules.Network.host_port),
        lambda x: x,
        host_port_true_positive,
        host_port_false_positive,
    ),
    "ipvfuture": Format(
        "ipvfuture",
        partial(match, StandardRules.Network.ipvfuture),
        lambda x: x,
        lambda x: False,
        lambda x: True,
    ),
    "ipv6_zoneid": Format(
        "ipv6_zoneid",
        partial(match, StandardRules.Network.ipv6_zoneid),
        lambda x: x,
        lambda x: len(x) > 8,
        lambda x: False,
    ),
    "ipv6": Format(
        "ipv6",
        partial(match, StandardRules.Network.ipv6),
        lambda x: x,
        lambda x: len(x) > 15,
        lambda x: len(x) <= 8,
    ),
    "ipv4": Format(
        "ipv4",
        partial(match, StandardRules.Network.ipv4),
        lambda x: x,
        lambda x: len(x) > 12,
        lambda x: len(x) <= 8,
    ),
    "fqdn": Format(
        "fqdn",
        partial(match, StandardRules.Network.fqdn),
        lambda x: x,
        lambda x: len(x) > 15 and 1 < len(x.split(b".")[-1]) < 5,
        lambda x: len(x) < 8 or not (2 < len(x.split(b".")[-1]) < 5),
    ),
    "csv": Format(
        "csv",
        partial(match, StandardRules.Csv.full),
        lambda x: x,
        lambda x: len(x) > 50 and len(x.split()) > 10,
        lambda x: len(x) < 30 or len(x.split()) < 4,
    ),
    "base85": Format(
        "base85",
        partial(match, StandardRules.Format.base85),
        b85decode,
        lambda x: len(x) > 70 and len(set(x)) > 25,
        lambda x: len(x) < 30 or len(set(x)) < 15,
    ),
    "base64": Format(
        "base64",
        partial(match, StandardRules.Format.base64),
        b64decode,
        lambda x: len(x) > 20 and len(set(x)) > 10 and x.endswith(b"="),
        lambda x: len(x) < 10 or len(set(x)) < 5,
    ),
    "base64_urlsafe": Format(
        "base64_urlsafe",
        partial(match, StandardRules.Format.base64_urlsafe),
        b64decode,
        lambda x: len(x) > 20 and len(set(x)) > 10 and x.endswith(b"="),
        lambda x: len(x) < 10 or len(set(x)) < 5,
    ),
    "base32": Format(
        "base32",
        partial(match, StandardRules.Format.base32),
        b32decode,
        lambda x: len(x) > 22 and len(set(x)) > 8 and x.endswith(b"="),
        lambda x: len(x) < 12 or len(set(x)) < 5,
    ),
    "base32_lower": Format(
        "base32_lower",
        partial(match, StandardRules.Format.base32),
        lambda x: b32decode(x.upper()),
        lambda x: len(x) > 22 and len(set(x)) > 8 and x.endswith(b"="),
        lambda x: len(x) < 12 or len(set(x)) < 5,
    ),
    "base32_insensitive": Format(
        "base32_insensitive",
        partial(match, StandardRules.Format.base32),
        lambda x: b32decode(x.upper()),
        lambda x: len(x) > 22 and len(set(x)) > 8 and x.endswith(b"="),
        lambda x: len(x) < 12 or len(set(x)) < 5,
    ),
    "hex": Format(
        "hex",
        partial(match, StandardRules.Format.hexadecimal),
        unhexlify,
        lambda x: len(x) > 20 and len(set(x)) > 7,
        lambda x: len(x) < 10 or len(set(x)) < 4,
    ),
    "string_null_terminated": Format(
        "string_null_terminated",
        partial(match, StandardRules.Format.string_null_terminated_length(5)),
        lambda x: x[:-1],
        lambda x: len(x) > 15 and len(set(x)) > 8,
        lambda x: len(x) < 8 or len(set(x)) < 5,
    ),
    "unicode_null_terminated": Format(
        "unicode_null_terminated",
        partial(match, StandardRules.Format.unicode_null_terminated_length(5)),
        lambda x: x.replace(b"\0", b""),
        lambda x: len(x) > 30 and len(set(x)) > 8,
        lambda x: len(x) < 16 or len(set(x)) < 5,
    ),
    "word": Format(
        "word",
        partial(match, StandardRules.Format.word),
        lambda x: x,
        word_true_positive,
        word_false_positive,
    ),
}

if __name__ == "__main__":
    from doctest import testmod

    testmod()
