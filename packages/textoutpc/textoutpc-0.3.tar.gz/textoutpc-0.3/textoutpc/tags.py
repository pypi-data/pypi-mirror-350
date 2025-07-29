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
"""Tag definitions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Sequence
from typing import TYPE_CHECKING, ClassVar

from .nodes import Node, TextNode

if TYPE_CHECKING:
    from .parser import Parser

__all__ = ["RawTag", "Tag"]


class Tag(ABC):
    """A tag for textoutpc's BBCode.

    Note that the provided name may be surrounded by brackets if the tag is
    a normal tag, or not if it is a special tag such as "`".

    :param name: The name of the tag.
    :param value: The value of the content.
    :param parser: Parser with which to parse subcontent, if relevant.
    """

    __slots__ = ("name", "parser", "value")

    CLOSE_IF_OPENED_WITHIN_ITSELF: ClassVar[bool] = False
    """Whether to close and re-open the tag, if opened within itself.

    This is for tags such as ``[li]`` not to have to be closed if placed
    within themselves, e.g.::

        [list]
        [li]Bullet 1
        [li]Bullet 2
        [/list]
    """

    name: str
    """Name of the tag.

    This is surrounded by brackets in case of a normal tag, or the character
    directly if a special character has been used, e.g. backquotes.
    """

    value: str | None
    """Value passed to the tag, e.g. ``[tag=my_value]``.

    Set to :py:data:`None` if no value has been passed, e.g. ``[tag]``.
    """

    parser: Parser
    """Parser for which the tag has been instanciated.

    This can be used to parse the value or any subcontent as BBCode as well.
    """

    @classmethod
    def get_text_from_children(self, children: Iterable[Node], /) -> str:
        """Get text from children.

        This is mostly used in case the tag is raw, to obtain the contents.

        :param children: Children to extract text from.
        :return: Extracted text.
        """
        text = ""
        for node in children:
            if not isinstance(node, TextNode):
                raise TypeError(f"Expected text node, got {type(node)!r}")

            text += node.content

        return text

    def __init__(
        self,
        /,
        *,
        name: str,
        value: str | None,
        parser: Parser,
    ):
        self.name = name
        self.value = value
        self.parser = parser

        self.validate()

    def validate(self) -> None:  # noqa: B027
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """

    def is_raw(self) -> bool:
        """Return whether the content of this tag should be read as raw or not.

        This will be called after the tag is initialized, but before the tag
        is used to populate a node, in order to read if what follows the tag
        is interpreted or not and whether we should look for an end tag or not.

        This may take into account both the name and the value of the tag.
        """
        return False

    def parse(self, content: str, /) -> Iterator[Node]:
        """Parse content.

        :param content: Content to parse.
        :return: Obtained nodes.
        """
        yield from self.parser.parse(content)

    @abstractmethod
    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """


class RawTag(Tag):
    """A tag for textoutpc's BBCode, except always raw.

    This means that the content for such tags must systematically be
    not interpreted, whatever the name and values are.
    """

    __slots__ = ()

    def is_raw(self) -> bool:
        """Return whether the content of this tag should be read as raw or not.

        Since the tag is a raw tag, this will always be true.
        """
        return True
