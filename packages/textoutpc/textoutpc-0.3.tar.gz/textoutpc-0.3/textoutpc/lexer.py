#!/usr/bin/env python
# *****************************************************************************
# Copyright (C) 2018-2025 Thomas Touhey <thomas@touhey.fr>
#
# This software is governed by the CeCILL-C license under French law and
# abiding by the rules of distribution of free software. You can use, modify
# and/or redistribute the software under the terms of the CeCILL-C license
# as circulated by CEA, CNRS and INRIA at the following
# URL: https://cecill.info
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean
# that it is complicated to manipulate, and that also therefore means that it
# is reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C license and that you accept its terms.
# *****************************************************************************
"""Lexer definition."""

from __future__ import annotations

import re
from collections.abc import Iterator
from io import StringIO
from typing import Any, TextIO, Union

import regex
from pydantic import BaseModel, ConfigDict
from typing_extensions import TypeAlias

__all__ = [
    "CloseTagToken",
    "OpenTagToken",
    "SpecialToken",
    "TextToken",
    "parse_textout_tokens",
]

# A tag can basically be one of the following things:
# - a starting tag, looking like [<name>] or [<name>=<attribute>]
# - an ending tag, looking like [/<name>]
# - a special tag (starting or ending), usually one-char (the only
#   one currently available is the ` tag).
#
# A tag name is 32 chars at most (at least 1 char).
# A closing tag can have no name, which means that it will close the
# last opened tag automatically.
# A tag attribute is 256 chars at most.
#
# FIXME: Check the sizes.
MAX_TAG_NAME_SIZE: int = 32
MAX_TAG_VALUE_SIZE: int = 256
MAX_TOKEN_SIZE: int = MAX_TAG_NAME_SIZE + MAX_TAG_VALUE_SIZE + 3
BUFFER_SIZE: int = 1024  # Must be more than MAX_TOKEN_SIZE!
TOKEN_PATTERN = regex.compile(
    r"""
        \[\s*[\\\/] (?P<ename>
            (?P<ename_e>
                [^\[\]\=\r\n]+ (\[(?&ename_e)*\]?)*
                | [^\[\]\=\r\n]* (\[(?&ename_e)*\]?)+
            )*
        )
        \s?\]
    |
        \[\s* (?P<bname>
            (?P<bname_e>
                [^\[\]\=\r\n]* (\[(?P&bname_e)*\]?)+
                | [^\[\]\=\r\n]+ (\[(?P&bname_e)*\]?)*
            )+
        )
        (\s* = \s* (?P<value>
            (?P<value_e>
                [^\[\]\r\n]* (\[(?&value_e)*\]?)+
                | [^\[\]\r\n]+ (\[(?&value_e)*\]?)*
            )*
        ))?
        \s?\]
    |
        (?P<sname>`)
    """,
    regex.VERBOSE | regex.DOTALL,
)

NEWLINE_PATTERN = re.compile(r"\r?\n|\r")


class BaseToken(BaseModel):
    """Base token."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")
    """Model configuration."""


class OpenTagToken(BaseToken):
    """Explicit opening of a tag."""

    name: str
    """Name of the tag that is being opened."""

    value: str | None = None
    """Optional value transmitted with the tag."""

    raw: str = ""
    """Raw token, if need be to yield it."""

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, OpenTagToken)
            and other.name == self.name
            and other.value == self.value
        )


class CloseTagToken(BaseToken):
    """Closing of a tag closing object for textout BBCode."""

    name: str
    """Name of the tag that is being closed."""

    raw: str = ""
    """Raw token, if need be to yield it."""

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, CloseTagToken) and other.name == self.name


class SpecialToken(BaseToken):
    """Special characters that could mean the opening or closing of a tag."""

    value: str
    """Special character(s) for the token."""

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SpecialToken) and other.value == self.value


class TextToken(BaseToken):
    """Token representing raw text."""

    content: str
    """Content in the text."""

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TextToken) and other.content == self.content


class EndToken(BaseToken):
    """Token representing an end of input."""

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, EndToken)


def get_token_from_match(
    match: regex.Match,
) -> OpenTagToken | CloseTagToken | SpecialToken | None:
    """Get a textout token from the given match.

    :param match: The full (non-partial) match to yield a token from.
    :return: The obtained token, or None if an error has occurred during
        matching.
    """
    parts = match.groupdict()
    if parts["bname"] is not None:
        name = parts["bname"]
        value = parts["value"]

        if len(name) > MAX_TAG_NAME_SIZE or (
            value is not None and len(value) > MAX_TAG_VALUE_SIZE
        ):
            return None

        return OpenTagToken(
            name=name.casefold(),
            value=value,
            raw=match.group(0),
        )

    if parts["ename"] is not None:
        name = parts["ename"]

        if len(name) > MAX_TAG_NAME_SIZE:
            return None

        return CloseTagToken(
            name=name.casefold(),
            raw=match.group(0),
        )

    if parts["sname"] is None:  # pragma: no cover
        raise AssertionError("sname should be filled here!")

    return SpecialToken(value=parts["sname"])


Token: TypeAlias = Union[
    OpenTagToken,
    CloseTagToken,
    SpecialToken,
    TextToken,
]


def clean_text(text: str, /) -> str:
    """Clean the provided text, e.g. normalize newlines.

    :param text: Text to clean.
    :return: Cleaned text.
    """
    return NEWLINE_PATTERN.sub("\n", text)


def parse_textout_tokens(
    stream_or_string: TextIO | str,
    /,
) -> Iterator[Token]:
    """Parse tokens from text input.

    :param stream_or_string: The text stream or string to read from.
    :return: The iterator for lexer tokens.
    """
    stream: TextIO | None
    text = StringIO()
    if isinstance(stream_or_string, str):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string

    buf = ""  # Current buffer of unprocessed input.

    while True:
        if not buf and stream is not None:
            buf = stream.read(BUFFER_SIZE - len(buf))

        if not buf:
            break

        # Try and match a tag.
        result = TOKEN_PATTERN.search(buf, partial=True)
        if not result or not result.group(0):
            text.write(buf)
            buf = ""
            continue

        # If there is some text, return it.
        start, end = result.span()
        if start > 0:
            text.write(buf[:start])
            buf = buf[start:]

        if not result.partial:
            # Result is actually exploitable, we can go on!
            pass
        elif len(buf) >= MAX_TOKEN_SIZE:
            # A partial result cannot be more than the maximum token size!
            # In such case, maybe if we start later, we can get a full match?
            text.write(buf[:1])
            buf = buf[1:]
            continue
        else:
            # We need to complete the buffer from here to get a full tag.
            if stream is not None:
                new_data = stream.read(BUFFER_SIZE - len(buf))
                if new_data:
                    # We have full data to complete the match, we need to try!
                    buf += new_data
                    continue

            # We've reached the end of our stream, we need to continue with
            # what we've got. Maybe if we start later, we can get a full
            # match?
            text.write(buf[:1])
            buf = buf[1:]
            stream = None
            continue

        token = get_token_from_match(result)
        if token is None:
            text.write(buf[:1])
            buf = buf[1:]
            continue

        if text.tell() > 0:
            yield TextToken(content=clean_text(text.getvalue()))
            text = StringIO()

        buf = buf[end - start :]
        yield token

    if text.tell() > 0:
        yield TextToken(content=clean_text(text.getvalue()))

    yield EndToken()
