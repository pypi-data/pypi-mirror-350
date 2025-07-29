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
"""Built-in tag and parser definitions.

This module defines four parsers:

``strict_inline_parser``
    Parser only defining tags and smileys used in inline contexts on PCv43,
    without extensions.

``strict_parser``
    Parser only defining tags and smileys used in other contexts on PCv43,
    without extensions.

``default_inline_parser``
    Parser defining tags and smileys used in inline contexts on PCv43,
    with extensions.

``default_parser``
    Parser defining tags and smileys used in other contexts on PCv43,
    with extensions.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator, Sequence
from decimal import Decimal
from string import ascii_lowercase, ascii_uppercase
from typing import ClassVar, Literal
from urllib.parse import urlparse

from thcolor.colors import Color
from thcolor.errors import ColorExpressionSyntaxError

from textoutpc.errors import InvalidValue, MissingValue, UnexpectedValue
from textoutpc.nodes import (
    Node,
    ParagraphNode,
    ReferenceNode,
    TextNode,
)
from textoutpc.parser import Parser
from textoutpc.tags import RawTag, Tag

from .nodes import (
    AdminImageNode,
    BackColorNode,
    CalcIconNode,
    CodeNode,
    EmphasisNode,
    FontColorNode,
    FontFamilyNode,
    FontName,
    FontSizeNode,
    ImageNode,
    IndentNode,
    InlineCodeNode,
    ListItemNode,
    ListNode,
    ListType,
    OverlineNode,
    ProfileReferenceNode,
    ProgramReferenceNode,
    ProgressBarNode,
    QuoteAuthorNode,
    QuoteContentNode,
    QuoteNode,
    SpoilerCloseLabelNode,
    SpoilerContentNode,
    SpoilerNode,
    SpoilerOpenLabelNode,
    StrikeThroughNode,
    StrongNode,
    SubtitleNode,
    TableCellNode,
    TableHeaderNode,
    TableNode,
    TableRowNode,
    TargetNode,
    TitleNode,
    TopicReferenceNode,
    TutorialReferenceNode,
    UnderlineNode,
    VideoNode,
)

# ---
# Strict inline parser definition.
# ---


strict_inline_parser = Parser("strict_inline_parser")
strict_inline_parser.add_smiley(">:)", name="twisted")
strict_inline_parser.add_smiley(">:(", name="evil")
strict_inline_parser.add_smiley(":)", name="smile")
strict_inline_parser.add_smiley(";)", name="wink")
strict_inline_parser.add_smiley(":(", name="sad")
strict_inline_parser.add_smiley(":D", name="grin")
strict_inline_parser.add_smiley(":p", name="hehe")
strict_inline_parser.add_smiley("8-)", name="cool2")
strict_inline_parser.add_smiley(":@", name="mad")
strict_inline_parser.add_smiley("0_0", name="eek")
strict_inline_parser.add_smiley(":E", name="mrgreen")
strict_inline_parser.add_smiley(":O", name="shocked")
strict_inline_parser.add_smiley(":s", name="confused2")
strict_inline_parser.add_smiley("^^", name="eyebrows")
strict_inline_parser.add_smiley(":'(", name="cry")
strict_inline_parser.add_smiley(":-°", name="whistle", style="height: 15px;")

# Name based smileys.
strict_inline_parser.add_smiley(":lol:", name="lol")
strict_inline_parser.add_smiley(":oops:", name="confused2")
strict_inline_parser.add_smiley(":grr:", name="evil")
strict_inline_parser.add_smiley(":sry:", name="redface")
strict_inline_parser.add_smiley(":mmm:", name="rolleyes")
strict_inline_parser.add_smiley(":waza:", name="waza")
strict_inline_parser.add_smiley(
    ":whistle:",
    name="whistle",
    style="height: 15px",
)
strict_inline_parser.add_smiley(":here:", name="pointer")
strict_inline_parser.add_smiley(":bow:", name="bow")
strict_inline_parser.add_smiley(":cool:", name="cool")
strict_inline_parser.add_smiley(":good:", name="welldone")
strict_inline_parser.add_smiley(":love:", name="love")
strict_inline_parser.add_smiley(":cry:", name="cry")
strict_inline_parser.add_smiley(":facepalm:", name="facepalm")
strict_inline_parser.add_smiley(":argh:", name="insults")
strict_inline_parser.add_smiley(":?:", name="what")
strict_inline_parser.add_smiley(":!:", name="excl")
strict_inline_parser.add_smiley(":+:", name="comiteplus")
strict_inline_parser.add_smiley(":-:", name="comitemoins")
strict_inline_parser.add_smiley(":~:", name="comitetilde")
strict_inline_parser.add_smiley(":arrow:", name="here")
strict_inline_parser.add_smiley(":grin:", name="grin")


_STRICT_INLINE_TAG_NAMES: Sequence[str] = (
    "[b]",
    "[color]",
    "[i]",
    "[u]",
    "[strike]",
    # Colors.
    "[blue]",
    "[brown]",
    "[gray]",
    "[green]",
    "[maroon]",
    "[purple]",
    "[red]",
    "[yellow]",
    # Fonts.
    "[arial]",
    "[comic]",
    "[courier]",
    "[haettenschweiler]",
    "[mono]",
    "[monospace]",
    "[tahoma]",
)


@strict_inline_parser.tag(*_STRICT_INLINE_TAG_NAMES)
class TextTag(Tag):
    """Main tag for setting text formatting.

    Example uses::

        [b]Bold text.[/b]
        [i]Italic text.[/i]
        [u]Underlined text.[/u]
        [strike]Striked text.[/strike]
        [striked]Text strikes again.[/striked]
        [font=arial]Arial text.[/font]
        [arial]Arial text again.[/arial]
        [blue]This will be in blue[/blue]
        [color=blue]This as well[/color]
        [color=rgb(255, 255, 255, 0.4)]BLACKNESS[/color]
        [color=hsl(0, 100%, 0.5)]This will be red.[/color]

    Also supports a hack used on Planète Casio for a while, which
    is a CSS injection, e.g.::

        [color=brown; size: 16pt]Hello world![/color]

    See the following sections for more information:

    * :ref:`markup-strong`
    * :ref:`markup-italic`
    * :ref:`markup-decoration`
    * :ref:`markup-font`
    * :ref:`markup-color`
    """

    __slots__ = (
        "back_color",
        "font_name",
        "font_size",
        "font_size_unit",
        "italic",
        "overline",
        "strike",
        "strong",
        "text_color",
        "underline",
    )

    SIZE_ALLOWED: ClassVar[bool] = False
    """Whether size changes are allowed."""

    BIG_FONT_SIZE: ClassVar[float] = 2.00
    """Big font size, in points."""

    SMALL_FONT_SIZE: ClassVar[float] = 0.75
    """Small font size, in points."""

    FONT_NAMES: ClassVar[dict[str, str]] = {
        "arial": "Arial",
        "comic": "Comic MS",
        "tahoma": "Tahoma",
        "courier": "Courier",
        "haettenschweiler": "Haettenschweiler",
        "mono": "monospace",
        "monospace": "monospace",
    }
    """Tag names to decode as fonts, and corresponding font family names."""

    COLOR_TAG_NAMES: ClassVar[set[str]] = {
        "blue",
        "brown",
        "gray",
        "green",
        "grey",
        "maroon",
        "purple",
        "red",
        "yellow",
    }
    """Tag names to decode as colors."""

    strong: bool
    """Whether the text should be set as strong or not."""

    italic: bool
    """Whether the text should be set as italic or not."""

    underline: bool
    """Whether the text should be underlined or not."""

    overline: bool
    """Whether the text should be overlined or not."""

    strike: bool
    """Whether the text should be striked or not."""

    font_name: FontName | None
    """Name of the font to set to the text."""

    font_size: float | None
    """Size of the font to set to the text."""

    font_size_unit: Literal["pt", "em"]
    """Unit of the font size."""

    text_color: Color | None
    """Color to set to the text."""

    back_color: Color | None
    """Color to set to the text background."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        self.strong = self.name == "[b]"
        self.italic = self.name == "[i]"
        self.underline = self.name == "[u]"
        self.overline = self.name == "[o]"
        self.strike = self.name in ("[s]", "[strike]", "[striked]")
        self.font_name = None
        self.font_size = None
        self.font_size_unit = "pt"
        self.text_color = None
        self.back_color = None

        # Historically, such tags used to be used for CSS injections.
        # We want to support limited CSS injections here, by parsing a lighter
        # syntax of CSS.
        value = self.value
        css_properties: list[str] = []
        if value is not None:
            css_properties = value.split(";")
            value = css_properties.pop(0)

        if self.name == "[font]":
            if value is None:
                raise MissingValue()

            if value not in self.FONT_NAMES:
                raise InvalidValue(
                    'Invalid font name "{font_name}".',
                    font_name=value,
                )

            self.font_name = self.FONT_NAMES[value]
        elif self.name[1:-1] in self.FONT_NAMES:
            if value is not None:
                raise UnexpectedValue()

            self.font_name = self.FONT_NAMES[self.name[1:-1]]
        elif self.name == "[big]":
            if value is not None:
                raise UnexpectedValue()

            self.font_size = self.BIG_FONT_SIZE
        elif self.name == "[small]":
            if value is not None:
                raise UnexpectedValue()

            self.font_size = self.SMALL_FONT_SIZE
        elif self.name == "[size]":
            if value is None:
                raise MissingValue()

            if value == "big":
                self.font_size = self.BIG_FONT_SIZE
            elif value == "small":
                self.font_size = self.SMALL_FONT_SIZE
            else:
                try:
                    self.font_size = round(int(value) / 100.0, 2)
                except ValueError as exc:
                    raise InvalidValue(
                        "Invalid font size: {value}",
                        value=value,
                    ) from exc

                if self.font_size <= 0 or self.font_size > 3.0:
                    raise InvalidValue(
                        "Invalid font size: {value}",
                        value=value,
                    )
        elif self.name in ("[c]", "[color]"):
            if value is None:
                raise MissingValue()

            try:
                self.text_color = Color.fromtext(value)
            except (ColorExpressionSyntaxError, ValueError) as exc:
                raise InvalidValue(f"Invalid color: {exc}") from exc
        elif self.name == "[f]":
            if value is None:
                raise MissingValue()

            try:
                self.back_color = Color.fromtext(value)
            except (ColorExpressionSyntaxError, ValueError) as exc:
                raise InvalidValue(f"Invalid color: {exc}") from exc
        elif self.name[1:-1] in self.COLOR_TAG_NAMES:
            if value is not None:
                raise UnexpectedValue()

            self.text_color = Color.fromtext(self.name[1:-1])
        elif self.name == "[css]":
            if value is None:
                raise MissingValue()

            css_properties.insert(0, value)
        elif self.value is not None:
            # Other tags do not expect any value.
            raise UnexpectedValue()

        # CSS properties.
        # NOTE: Unknown CSS properties are removed.
        for css_property in css_properties:
            name, *value_list = css_property.split(":")
            if not value_list:
                continue

            name = name.strip()
            value = ":".join(value_list).strip()

            if name in ("size", "font-size"):
                unit: Literal["pt", "em"]
                if value.endswith("pt"):
                    value = value[:-2].rstrip()
                    unit = "pt"
                elif value.endswith("em"):
                    value = value[:-2].rstrip()
                    unit = "em"

                try:
                    size = float(int(value))
                except ValueError:
                    continue

                if size <= 0:
                    continue

                self.font_size = size
                self.font_size_unit = unit
            elif name == "color":
                try:
                    self.text_color = Color.fromtext(value)
                except ValueError:
                    continue
            elif name == "background-color":
                try:
                    self.back_color = Color.fromtext(value)
                except ValueError:
                    continue

        if not self.SIZE_ALLOWED:
            self.font_size = None

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        if self.text_color is not None:
            children = (FontColorNode(children, color=self.text_color),)

        if self.back_color is not None:
            children = (BackColorNode(children, color=self.back_color),)

        if self.font_name is not None:
            children = (FontFamilyNode(children, name=self.font_name),)

        if self.font_size is not None:
            children = (
                FontSizeNode(
                    children,
                    size=self.font_size,
                    unit=self.font_size_unit,
                ),
            )

        if self.underline:
            children = (UnderlineNode(children),)

        if self.overline:
            children = (OverlineNode(children),)

        if self.strike:
            children = (StrikeThroughNode(children),)

        if self.strong:
            children = (StrongNode(children),)

        if self.italic:
            children = (EmphasisNode(children),)

        yield from children


@strict_inline_parser.tag("`", "[inlinecode]")
class InlineCodeTag(RawTag):
    """Inline code tag.

    This tag does not display a box, simply doesn't evaluate the content and
    uses a monospace font.

    Example uses::

        `some inline code`
        [inlinecode][b]The tags will be shown verbatim.[/b][/inlinecode]
        [inlinecode][inlinecode][i]This also[/inlinecode] works![/inlinecode]

    See :ref:`markup-code` for more information.
    """

    __slots__ = ()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield InlineCodeNode(
            content=self.get_text_from_children(children),
            language=self.value,
        )


@strict_inline_parser.tag("[url]")
class LinkTag(Tag):
    """Tag for linking to an external resource.

    Example uses::

        [url=https://example.org/hi]Go to example.org[/url]!
        [url=/Fr/index.php][/url]
        [url]https://random.org/randomize.php[/url]

    See :ref:`markup-url` for more information.
    """

    __slots__ = ("url",)

    url: str | None
    """The stored URL for the link tag."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        self.url = None
        if self.value is None:
            return None

        self.url = self.process_url(self.value)
        if self.url is None:
            raise InvalidValue("Not a valid URL: {url}", url=self.value)

    def is_raw(self) -> bool:
        """Return whether the content of this tag should be read as raw.

        :return: Whether the tag should be read as raw or not.
        """
        return self.value is None

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        url = self.value
        if url is None:
            orig_url = self.get_text_from_children(children)
            url = self.process_url(orig_url)
            if url is None:
                raise ValueError(f"Not a valid URL: {orig_url}")

        # If there is no contents and the URL was passed in the value, we
        # want to set the URL as the contents.
        if (
            self.value is not None
            and all(isinstance(node, TextNode) for node in children)
            and not "".join(node.content for node in children).strip()
        ):
            children = (TextNode(url),)

        yield ReferenceNode(children, url=url)

    def process_url(self, url: str) -> str | None:
        """Process the URL.

        :param url: The URL to process.
        :return: The adapted URL, or :py:data:`None` if the URL is invalid.
        """
        for prefix in ("http://", "https://", "ftp://", "ftps://", "/"):
            if url.startswith(prefix):
                return url

        return None


@strict_inline_parser.tag("[profil]")
class ProfileTag(RawTag):
    """Tag for linking to a profile for the current site.

    This tag was originally made for Planète Casio's profiles.
    It adds a prefix to the content, and sets the value.

    Example uses::

        [profil]Cakeisalie5[/]

    See :ref:`markup-url` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is not None:
            raise UnexpectedValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        username = self.get_text_from_children(children)
        yield ProfileReferenceNode(username=username)


@strict_inline_parser.tag("[noeval]")
class NoEvalTag(RawTag):
    """Tag for not evaluating content.

    Same as above, except doesn't apply any parent container or additional
    style.

    Example uses::

        [noeval][b]wow, and no need for monospace![/b][/noeval]
    """

    __slots__ = ()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield from children


@strict_inline_parser.tag("[calc]")
class CalcTag(RawTag):
    """Tag for displaying a calculator icon.

    Example use::

        [calc]g90+e[/calc]
    """

    __slots__ = ()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield CalcIconNode(name=self.get_text_from_children(children))


# ---
# Strict parser definition.
# ---


strict_parser = strict_inline_parser.copy("strict_parser")
strict_parser.add_smiley(":champ:", name="champion")
strict_parser.add_smiley(":bounce:", name="bounce")
strict_parser.add_smiley(":fusil:", name="fusil")
strict_parser.add_smiley(":boulet2:", name="boulet2")
strict_parser.add_smiley(":omg:", name="shocked2")
strict_parser.add_smiley(":mdr:", name="mdr")
strict_parser.add_smiley(":thx:", name="merci")
strict_parser.add_smiley(":aie:", name="banghead2")


@strict_parser.tag(*_STRICT_INLINE_TAG_NAMES, replace=True)
@strict_parser.tag("[big]", "[small]")
class TextTagWithSizeAllowed(TextTag):
    """Extended text tag."""

    SIZE_ALLOWED = True


@strict_parser.tag("[label]")
class LabelTag(Tag):
    """Tag for defining an anchor at a point of the document.

    Example uses::

        [label=installation]Installation de tel logiciel... (no ending req.)
        [label=compilation][/label] Compilation de tel logiciel...

    See :ref:`markup-label` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is None:
            raise MissingValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield TargetNode(anchor=self.value)
        yield from children


@strict_parser.tag("[target]")
class TargetTag(Tag):
    """Tag for linking to an anchor defined in the document.

    Example uses::

        [target=installation]Check out the installation manual[/target]!

    See :ref:`markup-label` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is None:
            raise MissingValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        if self.value is None:  # pragma: no cover
            raise MissingValue()

        yield ReferenceNode(children, anchor=self.value)


@strict_parser.tag("[img]")
class ImageTag(RawTag):
    """Tag for displaying an image.

    Example uses::

        [img]picture_url[/img]
        [img=center]picture_url[/img]
        [img=12x24]picture_url[/img]
        [img=center|12x24]picture_url[/img]
        [img=x24|right]picture_url[/img]

    See :ref:`markup-image` for more information.
    """

    __slots__ = ("alignment", "floating", "height", "width")

    MODES: ClassVar[
        dict[
            str,
            tuple[Literal["center", "left", "right"] | None, bool],
        ]
    ] = {
        "center": ("center", False),
        "centre": ("center", False),
        "left": ("left", False),
        "right": ("right", False),
        "float": (None, True),
        "floating": (None, True),
        "float-left": ("left", True),
        "float-center": ("center", True),
        "float-centre": ("center", True),
        "float-right": ("right", True),
    }
    """The mapping between mode strings and alignment and floating."""

    width: int | None
    """The width in pixels to display the image as, if provided."""

    height: int | None
    """The height in pixels to display the image as, if provided."""

    alignment: Literal["center", "left", "right"] | None
    """The alignment to display the image as, if provided."""

    floating: bool
    """Whether the image should be floating or not."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        self.width = None
        self.height = None
        self.alignment = None
        self.floating = False

        if self.value is None:
            return

        for arg in self.value.split("|"):
            arg = arg.strip().casefold()
            if not arg:
                continue

            if arg[0] in "0123456789x":
                try:
                    raw_w, *raw_hs = arg.split("x")
                    (raw_h,) = raw_hs if raw_hs else (raw_w,)

                    w = None
                    if raw_w:
                        w = int(raw_w)

                    h = None
                    if raw_h:
                        h = int(raw_h)
                except ValueError:
                    continue

                if w == 0 or h == 0:
                    continue

                self.width = w
                self.height = h
            elif arg in self.MODES:
                self.alignment, self.floating = self.MODES[arg]

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        url = self.get_text_from_children(children)

        # Compatibility: if the URL starts and ends with double quotes,
        # we want to remove them.
        if url.startswith('"') and url.endswith('"'):
            url = url[1:-1]

        yield self.build_node(url=url)

    def build_node(self, *, url: str) -> ImageNode:
        """Build the image node.

        :param url: The URL of the image node.
        :return: Built node.
        """
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            raise ValueError(
                f"Forbidden image source scheme: {parsed_url.scheme!r}",
            )

        # Quickfix present in the original fix, in order to redirect
        # both /images/ad/ and /images/staff/ when explicitely present.
        if (
            parsed_url.netloc
            in (
                None,
                "",
                "planet-casio.com",
                "www.planet-casio.com",
                "dev.planet-casio.com",
            )
            and parsed_url.path.startswith("/images/ad")
        ) or parsed_url.path.startswith("/images/staff"):
            path = parsed_url.path
            if path.startswith("/images/ad"):
                path = path.removeprefix("/images/ad")
            else:
                path = path.removeprefix("/images/staff")

            return AdminImageNode(
                align=self.alignment,
                width=self.width,
                height=self.height,
                float=self.floating,
                path=path,
            )

        return ImageNode(
            align=self.alignment,
            width=self.width,
            height=self.height,
            float=self.floating,
            url=url,
        )


@strict_parser.tag("[adimg]")
class AdminImageTag(ImageTag):
    """Tag for displaying an image from the administration.

    This tag is special for Planète Casio, as it takes images from the
    administration's (hence ``ad``) image folder. It adds the folder's prefix.

    Example uses::

        [adimg]some_picture.png[/img]
        [adimg=center]some_picture.png[/img]
        [adimg=12x24]some_picture.png[/img]
        [adimg=center|12x24]some_picture.png[/img]
        [adimg=x24|right]some_picture.png[/img]

    See :ref:`markup-image` for more information.
    """

    __slots__ = ()

    def build_node(self, *, url: str) -> ImageNode:
        """Build the image node.

        :param url: The URL of the image node.
        :return: Built node.
        """
        return AdminImageNode(
            align=self.alignment,
            width=self.width,
            height=self.height,
            float=self.floating,
            path=url,
        )


@strict_parser.tag("[center]", "[justify]")
class AlignTag(Tag):
    """Main tag for aligning paragraphs.

    Example uses::

        [align=center]This text is centered horizontally.[/align]
        [justify]This text is justified.[/justify]

    See :ref:`markup-align` for more information.
    """

    __slots__ = ("kind",)

    ALIGN_KEYS: ClassVar[
        dict[str, Literal["center", "left", "right", "justify"]]
    ] = {
        "center": "center",
        "centre": "center",
        "left": "left",
        "right": "right",
        "justify": "justify",
    }
    """Alignment keys recognized as tags or tag values."""

    kind: Literal["center", "left", "right", "justify"]
    """Kind of alignment."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.name == "[align]":
            if self.value is None:
                raise MissingValue()

            if self.value not in self.ALIGN_KEYS:
                raise InvalidValue(
                    "Expected one of these values:"
                    + ", ".join(self.ALIGN_KEYS.keys()),
                )

            kind = self.value
        elif (
            not self.name.startswith("[")
            or not self.name.endswith("]")
            or self.name[1:-1] not in self.ALIGN_KEYS
        ):
            raise ValueError(
                "Only supported the following names: "
                + ", ".join(
                    f"[{name}]" for name in ("align", *self.ALIGN_KEYS)
                ),
            )
        elif self.value is not None:
            raise UnexpectedValue()
        else:
            kind = self.name[1:-1]

        self.kind = self.ALIGN_KEYS[kind]

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield ParagraphNode(children, align=self.kind)


@strict_parser.tag("[quote]")
class QuoteTag(Tag):
    """Tag for presenting a quote.

    Example uses::

        [quote]Someone said that.[/]
        [quote=Cakeisalie5]Ever realized that my name contained “Cake”?[/]

    See :ref:`markup-quote` for more information.
    """

    __slots__ = ()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        quote_children = [
            QuoteContentNode(children),
        ]
        if self.value is not None:
            quote_children.insert(0, QuoteAuthorNode(self.parse(self.value)))

        yield QuoteNode(quote_children)


@strict_parser.tag("[spoiler]")
class SpoilerTag(Tag):
    """Tag for hiding content at first glance.

    This tag produces a node that requires the reader to click on a
    button to read its content. It can help to contain "secret" nodes,
    such as solutions, source code, or various other things.

    Example uses::

        [spoiler]This is hidden![/spoiler]

        [spoiler=Y a quelque chose de caché !|Ah, bah en fait non :)]:E
        And it's multiline, [big]and formatted[/big], as usual :D[/spoiler]

    See :ref:`markup-spoiler` for more information.
    """

    __slots__ = ("_close_title", "_open_title")

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        closed, opened = "", ""
        if self.value is not None:
            closed, _, opened = self.value.partition("|")

        self._open_title = closed or "Cliquez pour découvrir"
        self._close_title = opened or "Cliquez pour recouvrir"

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield SpoilerNode(
            (
                SpoilerOpenLabelNode(self.parse(self._open_title)),
                SpoilerCloseLabelNode(self.parse(self._close_title)),
                SpoilerContentNode(children),
            ),
        )


@strict_parser.tag("[code]")
class CodeTag(RawTag):
    """Basic code tag, for displaying code.

    Example uses::

        [code]int main()
        {
            printf("hello, world");
        }[/code]

    See :ref:`markup-code` for more information.
    """

    __slots__ = ()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield CodeNode(
            self.get_text_from_children(children),
            language=self.value,
        )


@strict_parser.tag("[indent]")
class IndentTag(RawTag):
    """Indentation tag.

    Example uses::

        [indent]Indented text![/indent]
    """

    __slots__ = ()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield IndentNode(children)


@strict_parser.tag("[progress]")
class ProgressTag(Tag):
    """Tag for displaying a progress bar.

    Example uses::

        [progress=50]My great progress bar[/progress]
        [progress=100][/progress]

    See :ref:`markup-progress-bar` for more information.
    """

    __slots__ = ("progress_value",)

    progress_value: int
    """The progress value, between 0 and 100 included."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is None:
            raise MissingValue("Expected an integer between 0 and 100.")

        try:
            self.progress_value = int(self.value)
        except ValueError as exc:
            raise InvalidValue(
                "Value should have been an integer between 0 and 100.",
            ) from exc

        if self.progress_value < 0 or self.progress_value > 100:
            raise InvalidValue(
                "Value should have been an integer between 0 and 100.",
            )

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield ProgressBarNode(
            children,
            value=Decimal(self.progress_value) / 100,
        )


@strict_parser.tag("[list]")
class ListTag(Tag):
    """Tag for creating a list.

    Example uses::

        [list]
            [li]hello[/li]
            [li]world[/li]
        [/list]
    """

    type: ListType
    """List type."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        try:
            if self.name == "[list]":
                self.type = ListType(self.value or "ul")
            else:
                self.type = ListType(self.name[1:-1])
        except ValueError as exc:
            raise InvalidValue("Value should be ul, ol or arrow.") from exc

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield ListNode(children, type=self.type)


@strict_parser.tag("[li]")
class ListItemTag(Tag):
    """Tag for creating a list element.

    See :py:class:`ListTag` for more information.
    """

    CLOSE_IF_OPENED_WITHIN_ITSELF = True

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield ListItemNode(children)


@strict_parser.tag("[table]")
class TableTag(Tag):
    """Tag for creating a table.

    An example use of the base elements is the following::

        [table]
            [tr][th]Col 1[/th][th]Col 2[/th][/tr]
            [tr][td]Data 1_1[/td][td]Data 1_2[/td][/tr]
            [tr][td]Data 2_1[/td][td]Data 2_2[/td][/tr]
        [/table]

    An example use with separators is the following::

        [table]
            [tr=|]Col 1 | Col 2[/tr]
            [tr=|]Data 1_1 | Data 1_2[/tr]
            [tr=|]Data 2_1 | Data 2_2[/tr]
        [/table]
    """

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield TableNode(children)


@strict_parser.tag("[tr]")
class TableRowTag(Tag):
    """Tag for creating a table row.

    See :py:class:`TableTag` for more information.
    """

    separator: str | None = None

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        self.separator = self.value or None

    def is_raw(self) -> bool:
        """Return whether the content of this tag should be read as raw.

        :return: Whether the tag should be read as raw or not.
        """
        return self.separator is not None

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        if self.separator:
            cells: Iterable[Node] = (
                TableCellNode((TextNode(cell),))
                for cell in self.get_text_from_children(children).split(
                    self.separator,
                )
            )
        else:
            cells = children

        yield TableRowNode(cells)


@strict_parser.tag("[th]")
class TableHeaderTag(Tag):
    """Tag for creating a table header (cell).

    See :py:class:`TableTag` for more information.
    """

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield TableHeaderNode(children)


@strict_parser.tag("[td]")
class TableCellTag(Tag):
    """Tag for creating a table cell.

    See :py:class:`TableTag` for more information.
    """

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield TableCellNode(children)


@strict_parser.tag("[video]", "[video tiny]")
class VideoTag(RawTag):
    """Tag for displaying a video player.

    Example uses::

        [video]https://www.youtube.com/watch?v=yDp3cB5fHXQ[/video]
        [video tiny]https://youtu.be/0twDETh6QaI[/video tiny]
    """

    __slots__ = ("format", "width")

    format: Literal["normal", "tiny"]
    """Format."""

    width: int | None
    """Explicit width, if specified."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        self.format = "tiny" if self.name == "[video tiny]" else "normal"
        self.width = None

        try:
            if self.value is not None:
                self.width = min(int(self.value), 560)
        except ValueError as exc:
            raise InvalidValue(
                "Value should have been a valid width.",
            ) from exc

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield VideoNode(
            url=self.get_text_from_children(children),
            format=self.format,
            width=self.width,
        )


# ---
# Default inline parser, with extensions.
# ---


default_inline_parser = strict_inline_parser.copy("default_inline_parser")
default_inline_parser.add_tag(ProfileTag, "[profile]")

# We want to allow setting the font size in inline contexts as well.
default_inline_parser.add_tag(
    TextTagWithSizeAllowed,
    *_STRICT_INLINE_TAG_NAMES,
    "[css]",  # Direct (filtered) CSS, without need for injection.
    "[c]",  # Shorthand for [color]
    "[font]",  # General font tag.
    "[o]",  # Overline.
    "[s]",  # Shorthand for [strike]
    "[grey]",  # British people also exist!
    "[size]",  # General tag, instead of [big] and [small]
    "[big]",  # Not normally present for inline, but allowed here.
    "[small]",  # Same as above.
    replace=True,
)


@default_inline_parser.tag("[topic]")
class TopicTag(LinkTag):
    """Tag for linking topics for the current site.

    Originally made for Planète Casio's forum topics.

    Example uses::

        [topic]234[/]

    See :ref:`markup-url` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is not None:
            raise UnexpectedValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        topic_id = self.get_text_from_children(children)
        yield TopicReferenceNode(id=topic_id)


@default_inline_parser.tag("[tutorial]")
class TutorialTag(LinkTag):
    """Tag for linking tutorials for the current site.

    Originally made for Planète Casio's tutorials.

    Example uses::

        [tutorial]71[/]

    See :ref:`markup-url` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is not None:
            raise UnexpectedValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        tutorial_id = self.get_text_from_children(children)
        yield TutorialReferenceNode(id=tutorial_id)


@default_inline_parser.tag("[program]")
class ProgramTag(LinkTag):
    """Tag for linking programs for the current site.

    Originally made for Planète Casio's programs.

    Example uses::

        [program]3598[/]

    See :ref:`markup-url` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is not None:
            raise UnexpectedValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        program_id = self.get_text_from_children(children)
        yield ProgramReferenceNode(id=program_id)


@default_inline_parser.tag("[rot]", "[rot13]")
class RotTag(RawTag):
    """Tag for un-rot13-ing raw text and returning such text.

    Example uses::

        [rot=13]obawbhe[/rot]
        [rot13]Obawbhe[/rot13]
    """

    __slots__ = "_rot"

    general_tag_names = ("[rot]",)
    """The accepted tag names for this tag, with an expected value."""

    embedded_tag_pattern = re.compile(r"\[rot0*?([0-9]|1[0-9]|2[0-5])\]", re.I)
    """The compiled pattern for tag names with embedded rot values."""

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.name in self.general_tag_names:
            if self.value is None:
                raise MissingValue()

            try:
                self._rot = int(self.value)
            except ValueError as exc:
                raise InvalidValue(
                    "Expected a rot value between 0 and 25",
                ) from exc

            if self._rot < 0 or self._rot >= 26:
                raise InvalidValue("Expected a rot value between 0 and 25")

            return

        m = self.embedded_tag_pattern.match(self.name)
        if m is None:
            raise ValueError(f"Unsupported tag name {self.name!r} for rot")

        if self.value is not None:
            raise UnexpectedValue()

        self._rot = int(m.group(1))

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        text = self.get_text_from_children(children)
        result = str.translate(
            text,
            str.maketrans(
                ascii_uppercase + ascii_lowercase,
                ascii_uppercase[self._rot :]
                + ascii_uppercase[: self._rot]
                + ascii_lowercase[self._rot :]
                + ascii_lowercase[: self._rot],
            ),
        )

        yield TextNode(result)


# ---
# Default parser, with extensions.
# ---

default_parser = default_inline_parser.copy("default_parser")
default_parser.add_from(strict_parser)
default_parser.add_tag(AlignTag, "[align]")
default_parser.add_tag(ListTag, "[ul]", "[ol]")
default_parser.add_tag(ListItemTag, "[*]")


@default_parser.tag("[title]")
class TitleTag(RawTag):
    """Title tag.

    Example uses::

        [title]Example title[/]

    See :ref:`markup-title` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is not None:
            raise UnexpectedValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield TitleNode(children)


@default_parser.tag("[subtitle]")
class SubtitleTag(RawTag):
    """Subtitle tag.

    Example uses::

        [subtitle]Example subtitle[/]

    See :ref:`markup-title` for more information.
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is not None:
            raise UnexpectedValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield SubtitleNode(children)


@default_parser.tag("[youtube]")
class YoutubeTag(RawTag):
    """Tag for displaying a YouTube video player.

    Example uses::

        [youtube]yDp3cB5fHXQ[/youtube]
    """

    __slots__ = ()

    def validate(self) -> None:
        """Validate the name and value for this tag.

        :raises TagValidationError: The name and value combination is invalid.
        """
        if self.value is not None:
            raise UnexpectedValue()

    def process(self, *, children: Sequence[Node]) -> Iterator[Node]:
        """Process the tag with children to build document nodes.

        :param children: The children to process.
        :return: The produced nodes.
        """
        yield VideoNode(
            url=f"https://youtu.be/{self.get_text_from_children(children)}",
        )
