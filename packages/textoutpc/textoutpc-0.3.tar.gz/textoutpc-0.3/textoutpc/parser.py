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
"""Parser definition."""

from __future__ import annotations

import re
from collections.abc import Iterator
from functools import cached_property
from logging import getLogger
from typing import Annotated, Callable, TextIO, TypeVar

import regex
from pydantic import BaseModel, ConfigDict, Field

from .errors import AlreadyRegistered, TagValidationError
from .lexer import (
    CloseTagToken,
    EndToken,
    OpenTagToken,
    SpecialToken,
    TextToken,
    parse_textout_tokens,
)
from .nodes import EmailAddressNode, Node, ReferenceNode, SmileyNode, TextNode
from .tags import Tag

__all__ = ["Parser"]

ParserT = TypeVar("ParserT", bound="Parser")
TagT = TypeVar("TagT", bound=Tag)

logger = getLogger(__name__)


class SmileyData(BaseModel):
    """Smiley data."""

    name: str
    """Name of the emoji, to include in the final image URL."""

    style: str | None = None
    """Optional inline CSS to include in the HTML output."""


class StackElement(BaseModel):
    """Element of the parsing stack."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")
    """Model configuration."""

    name: str
    """Name of the tag."""

    tag: Tag
    """Instantiated tag."""

    is_raw: bool
    """Whether the tag is raw or not."""

    raw_depth: int = 0
    """Raw depth."""

    children: Annotated[list[Node], Field(default_factory=list)]
    """Children nodes which to add to the parent element."""

    text: str = ""
    """Text currently present at this level."""


class StateMachine(BaseModel):
    """State machine.

    :param parser: Parser for which the state machine is initialized.
    :param inp: Input to process.
    """

    nodes: Annotated[list[Node], Field(default_factory=list)]
    """Obtained list of top-level nodes."""

    parser: Parser
    """Parser for which the state machine has been created."""

    stack: Annotated[list[StackElement], Field(default_factory=list)]
    """Element stack."""

    text: str = ""
    """Text at the top-most level."""

    @cached_property
    def text_entity_pattern(self, /) -> re.Pattern:
        """Get the text entity pattern.

        This is used to match URLs, e-mail addresses, and smileys.
        """
        return regex.compile(
            r"(^|\s|[[:punct:]])((?:https?|ftps?|magnet):"
            r"([^\[\]\(\)\s\,]+|(?:\[(?3)*\])|(?:\((?3)*\)))+)"
            r"|([A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+)"
            r"|(" + "|".join(map(re.escape, self.parser.smileys)) + ")",
        )

    def parse_inline_text(self, text: str, /) -> Iterator[Node]:
        """Parse inline text as nodes.

        This extracts URLs, e-mail addresses and smileys from such text.

        :param text: Text to parse.
        :return: Node iterator.
        """
        start = 0
        while start < len(text):
            match = self.text_entity_pattern.search(text[start:])
            if match is None:
                break

            prefix = text[start : start + match.start() + len(match[1] or "")]
            if prefix:
                yield TextNode(prefix)

            start += match.end()
            if match[2] is not None:
                # URL.
                yield ReferenceNode(
                    (TextNode(match[2]),),
                    url=match[2],
                )
            elif match[4] is not None:
                # E-mail address.
                yield EmailAddressNode(email_address=match[4])
            elif match[5] is not None:
                # Smiley.
                smiley = self.parser.smileys[match[5]]
                yield SmileyNode(name=smiley.name, style=smiley.style)

        if start < len(text):
            yield TextNode(text[start:])

    def add_text(self, text: str, /) -> None:
        """Add text to the current level.

        :param text: Text at the current level.
        """
        if self.stack:
            self.stack[0].text += text
        else:
            self.text += text

    def open_tag(self, tag: Tag, /) -> None:
        """Open a new stack level.

        :param tag: The tag with which to open the tag.
        """
        self.stack.insert(
            0,
            StackElement(
                name=tag.name,
                tag=tag,
                is_raw=tag.is_raw(),
            ),
        )

    def close_multiple(self, count: int, /, *, last_end_tag: str = "") -> None:
        """Close multiple tags.

        :param count: Number of elements in the stack to close.
        :param last_end_tag: End tag for the last iteration of the tag to
            close.
        """
        if len(self.stack) < count:  # pragma: no cover
            raise AssertionError(
                f"Could not close {count} contexts with a {len(self.stack)}-"
                + "deep stack.",
            )

        for i in range(count):
            level = self.stack.pop(0)

            # If there is text, we want to add it to the current list of
            # children.
            if leftover_text := level.text:
                if level.is_raw:
                    level.children.append(TextNode(leftover_text))
                else:
                    level.children.extend(
                        self.parse_inline_text(leftover_text),
                    )

            # Now we actually want to cause the tag to process the obtained
            # nodes.
            try:
                nodes = tuple(level.tag.process(children=level.children))
            except Exception:
                logger.warning(
                    "Tag instance %s could not process children.",
                    level.tag.__class__.__name__,
                    exc_info=True,
                )

                # There was an error in processing the tags.
                start_tag = level.tag.name
                if start_tag[0] == "[" and level.tag.value is not None:
                    start_tag = start_tag[:-1] + "=" + level.tag.value + "]"

                # If the tag has been closed implicitely, we want to remove it.
                if i == count - 1:
                    end_tag = last_end_tag
                    if end_tag[:1] == "[":
                        end_tag = "[/" + end_tag[1:]
                else:
                    end_tag = ""

                nodes = (
                    TextNode(start_tag),
                    *level.children,
                )
                if end_tag:
                    nodes += (TextNode(end_tag),)

            # We need to process the text at the upper level.
            if len(self.stack) > 0:
                upper_level = self.stack[0]
                if upper_level.text:
                    upper_level.children.extend(
                        self.parse_inline_text(upper_level.text),
                    )
                    upper_level.text = ""

                children: list[Node] = upper_level.children
            else:
                if self.text:
                    self.nodes.extend(self.parse_inline_text(self.text))
                    self.text = ""

                children = self.nodes

            children.extend(nodes)

    def process(self, inp: str | TextIO, /) -> None:
        """Process all tokens gathered from the lexer.

        :param inp: Input to process.
        """
        for token in parse_textout_tokens(inp):
            if isinstance(token, EndToken):
                break

            if isinstance(token, TextToken):
                self.add_text(token.content)
                continue

            if isinstance(token, OpenTagToken):
                if self.stack and self.stack[0].is_raw:
                    # We are not allowed to open tags in a raw context.
                    # However, if the name corresponds to the current tag,
                    # we want to consider this as adding raw depth.
                    if self.stack[0].name == f"[{token.name}]":
                        self.stack[0].raw_depth += 1

                    self.add_text(token.raw)
                    continue

                tag_name = f"[{token.name}]"
                tag_cls = self.parser.tags.get(tag_name)
                if tag_cls is None:
                    self.add_text(token.raw)
                    continue

                try:
                    tag = tag_cls(
                        name=tag_name,
                        value=token.value,
                        parser=self.parser,
                    )
                except TagValidationError:
                    logger.warning(
                        "Could not instantiate %s with value %r.",
                        tag_cls.__name__,
                        token.value,
                        exc_info=True,
                    )

                    self.add_text(token.raw)
                    continue

                if (
                    tag.CLOSE_IF_OPENED_WITHIN_ITSELF
                    and self.stack
                    and self.stack[0].name == tag_name
                ):
                    self.close_multiple(1)

                self.open_tag(tag)
                continue

            if isinstance(token, CloseTagToken):
                tag_name = f"[{token.name}]"
                if self.stack and self.stack[0].is_raw:
                    if tag_name in ("[]", self.stack[0].name):
                        # We are indeed closing the current raw tag.
                        #
                        # There is a depth system here, inherited from what
                        # existed in PHP, in order for embedded raw tags
                        # to be still considered as such.
                        #
                        # A visual example is this:
                        #
                        #    a[noeval]b[noeval]c[/noeval]d[/noeval]e
                        #
                        # This must render as the following:
                        #
                        #    ab[noeval]c[/noeval]de
                        #
                        # This is because the [noeval] within the raw tag is
                        # matched to the inner [/noeval].
                        #
                        # Why is this system here? No idea, but we want to be
                        # compatible with the legacy one!
                        if self.stack[0].raw_depth > 0:
                            self.stack[0].raw_depth -= 1
                            self.add_text(token.raw)
                        else:
                            self.close_multiple(1, last_end_tag=tag_name)
                    else:
                        # We are not closing the raw tag, and cannot close any
                        # parent tag, so we actually just consider this as
                        # text.
                        self.add_text(token.raw)

                    continue

                for i, el in enumerate(self.stack):
                    # In non-raw cases, the [/] tag means that we want to close
                    # the first found tag.
                    if tag_name in ("[]", el.name):
                        self.close_multiple(1 + i, last_end_tag=tag_name)
                        break
                else:
                    # The closing tag doesn't correspond to an existing tag,
                    # so we consider it as simple text.
                    self.add_text(token.raw)

                continue

            if isinstance(token, SpecialToken):
                # This either opens or closes a tag.
                if self.stack and self.stack[0].is_raw:
                    if self.stack[0].name == token.value:
                        self.close_multiple(1, last_end_tag=token.value)
                    else:
                        self.add_text(token.value)

                    continue

                # If the tag is opened, we want to close it.
                for i, el in enumerate(self.stack):
                    if token.value == el.name:
                        self.close_multiple(1 + i, last_end_tag=token.value)
                        break
                else:
                    # The tag does not correspond to an already opened tag,
                    # we want to open it.
                    tag_cls = self.parser.tags.get(token.value)
                    if tag_cls is None:
                        self.add_text(token.value)
                        continue

                    # Otherwise, we want to open the tag.
                    try:
                        tag = tag_cls(
                            name=token.value,
                            value=None,
                            parser=self.parser,
                        )
                    except TagValidationError:
                        logger.warning(
                            "Could not instantiate %s with value %r.",
                            tag_cls.__name__,
                            token.value,
                            exc_info=True,
                        )

                        self.add_text(token.value)
                        continue

                    self.open_tag(tag)

                continue

            raise NotImplementedError(  # pragma: no cover
                f"Unsupported token {token!r}",
            )

    def finish(self, /) -> None:
        """Finish by closing all levels, and processing the leftover text."""
        self.close_multiple(len(self.stack))
        if self.text:
            self.nodes.extend(self.parse_inline_text(self.text))


class Parser(BaseModel):
    """Parser definition."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Model configuration."""

    name: str | None = None
    """Name of the parser."""

    tags: Annotated[dict[str, type[Tag]], Field(default_factory=dict)]
    """Currently registered tags."""

    smileys: Annotated[dict[str, SmileyData], Field(default_factory=dict)]
    """Currently registered emojis."""

    def __init__(self, /, name: str | None = None, **kwargs) -> None:
        kwargs["name"] = name
        super().__init__(**kwargs)

    def copy(self: ParserT, name: str | None = None, /) -> ParserT:
        """Copy as another parser.

        :param name: Name as which to copy the parser.
        :return: Copied parser.
        """
        return self.__class__(
            name or self.name,
            tags=self.tags,
            smileys=self.smileys,
        )

    def add_smiley(
        self,
        smiley: str,
        /,
        *,
        name: str,
        style: str | None = None,
    ) -> None:
        """Register an emoji.

        :param smiley: Smiley to match.
        :param name: Name to match the smiley as, or include in the URL.
        :param style: Optional HTML inline style to add.
        """
        if smiley in self.smileys:
            raise AlreadyRegistered(names={smiley})

        self.smileys[smiley] = SmileyData(name=name, style=style)

    def add_tag(
        self,
        tag: type[Tag],
        name: str,
        /,
        *other_names: str,
        replace: bool = False,
    ) -> None:
        """Register a tag as one or more names.

        :param tag: Tag class to register the tag as.
        :param name: First name to register the tag as.
        :param other_names: Other names to register the tag as.
        :param replace: If any of the provided names is already registered,
            whether to replace the tag silently, or raise an exception.
        :raises AlreadyRegistered: At least one of the provided names was
            already registered to another tag.
        """
        if not replace:
            names_already_taken = set((name, *other_names)).intersection(
                self.tags,
            )
            if names_already_taken:
                raise AlreadyRegistered(names=names_already_taken)

        for name_to_register in (name, *other_names):
            self.tags[name_to_register] = tag

    def tag(
        self,
        name: str,
        /,
        *other_names: str,
        replace: bool = False,
    ) -> Callable[[type[TagT]], type[TagT]]:
        """Register a tag as one or more names (decorator syntax).

        :param name: First name to register the tag as.
        :param other_names: Other names to register the tag as.
        :param replace: If any of the provided names is already registered,
            whether to replace the tag silently, or raise an exception.
        :return: Callable to pass the tag type to.
        :raises AlreadyRegistered: At least one of the provided names was
            already registered to another tag.
        """

        def decorator(tag: type[TagT]) -> type[TagT]:
            self.add_tag(tag, name, *other_names, replace=replace)
            return tag

        return decorator

    def add_from(self, parser: Parser, /) -> None:
        """Add missing tags and smileys from the provided parser.

        :param parser: Parser to copy missing tags and smileys from.
        """
        for name, tag in parser.tags.items():
            if name not in self.tags:
                self.tags[name] = tag

        for smiley, sdata in parser.smileys.items():
            if smiley not in self.smileys:
                self.smileys[smiley] = sdata

    def parse(self, inp: str | TextIO, /) -> Iterator[Node]:
        """Parse a given input into nodes.

        :param inp: Input, as a string or text stream.
        :return: Nodes.
        """
        sm = StateMachine(parser=self)
        sm.process(inp)
        sm.finish()

        # TODO: Add paragraphs.
        # TODO: Reorganize block, block inline and inline nodes.
        # TODO: Group TextNode instances, as well as StrongNode, etc.

        yield from sm.nodes
