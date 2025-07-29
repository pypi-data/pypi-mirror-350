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
"""Built-in node definitions."""

from __future__ import annotations

import re
from abc import abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Annotated, ClassVar, Literal

from annotated_types import Ge, Gt, Le
from pydantic import HttpUrl, StringConstraints, field_validator
from thcolor.colors import Color

from textoutpc.misc import get_url_param, html_escape, html_start_tag
from textoutpc.nodes import (
    BlockContainerNode,
    BlockInlineContainerNode,
    BlockNode,
    InlineContainerNode,
    InlineNode,
    LinkTarget,
    Node,
    NodeHTMLRenderEnvironment,
)

Anchor = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9_]+$")]
"""Anchor."""

FontName = Annotated[str, StringConstraints(pattern=r"^[a-z0-9 ]+$")]
"""Name of a font."""

Username = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9_ .-]+$")]
"""Username of a Planète Casio user."""

CodeLanguage = Annotated[
    str,
    StringConstraints(pattern=r"^[^\s](?:.*[^\s])?$"),
]
"""Name of a code language."""

# ---
# Structural nodes.
# ---


class TitleNode(BlockInlineContainerNode):
    """Document title node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return f"<h1>{self.render_children_html(env)}</h1>"


class SubtitleNode(BlockInlineContainerNode):
    """Document subtitle node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return f'<p class="subtitle">{self.render_children_html(env)}</p>'


class QuoteAuthorNode(BlockInlineContainerNode):
    """Quote author node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return (
            f"<b><i>{self.render_children_html(env)} a écrit&nbsp;:"
            + "</i></b><br />"
        )


class QuoteContentNode(BlockContainerNode):
    """Quote content node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return self.render_children_html(env)


class QuoteNode(BlockContainerNode):
    """Quote node."""

    AUTHORIZED_CHILDREN_TYPES = (
        (QuoteAuthorNode, range(0, 2)),
        (QuoteContentNode, 1),
    )

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        author_node = self.find_child(QuoteAuthorNode, optional=True)
        content_node = self.find_child(QuoteContentNode)

        result = html_start_tag("div", cls="citation")
        if author_node is not None:
            result += author_node.render_html(env)

        return result + content_node.render_html(env) + "</div>"


class IndentNode(BlockInlineContainerNode):
    """Indentation node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return (
            html_start_tag("div", style="text-indent: 30px")
            + self.render_children_html(env)
            + "</div>"
        )


class SpoilerOpenLabelNode(BlockInlineContainerNode):
    """Node to display to prompt the user to open the spoiler."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag(
                    "div",
                    cls="title on",
                    onclick="toggleSpoiler(this.parentNode, 'open')",
                ),
                self.render_children_html(env),
                "</div>",
            ),
        )


class SpoilerCloseLabelNode(BlockInlineContainerNode):
    """Node to display to prompt the user to close the spoiler."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag(
                    "div",
                    cls="title off",
                    onclick="toggleSpoiler(this.parentNode, 'close')",
                ),
                self.render_children_html(env),
                "</div>",
            ),
        )


class SpoilerContentNode(BlockContainerNode):
    """Spoiler content node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return (
            html_start_tag("div", cls="off")
            + self.render_children_html(env)
            + "</div>"
        )


class SpoilerNode(BlockContainerNode):
    """Spoiler node."""

    AUTHORIZED_CHILDREN_TYPES = (
        (SpoilerOpenLabelNode, 1),
        (SpoilerCloseLabelNode, 1),
        (SpoilerContentNode, 1),
    )

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        open_label_node = self.find_child(SpoilerOpenLabelNode)
        close_label_node = self.find_child(SpoilerCloseLabelNode)
        content_node = self.find_child(SpoilerContentNode)

        return "".join(
            (
                html_start_tag("div", cls="spoiler"),
                open_label_node.render_html(env),
                close_label_node.render_html(env),
                content_node.render_html(env),
                "</div>",
            ),
        )


class CodeNode(BlockNode):
    """Code node."""

    content: str
    """Content."""

    language: CodeLanguage | None = None
    """Language of the code."""

    def __init__(self, /, content: str, **kwargs) -> None:
        super().__init__(content=content, **kwargs)

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag("div", cls="code"),
                html_escape(self.content),
                "</div>",
            ),
        )


class BaseImageNode(Node):
    """Image node."""

    align: Literal["center", "left", "right"] | None = None
    """Optional alignment to apply to the image."""

    width: int | None = None
    """Optional width to display the image as, in pixels."""

    height: int | None = None
    """Optional height to display the image as, in pixels."""

    float: bool = False
    """Whether the image should be displayed as floating or not."""

    @abstractmethod
    def get_url_for_html_output(
        self,
        env: NodeHTMLRenderEnvironment,
        /,
    ) -> str:
        """Get the URL to the image for HTML output.

        :return: Obtained URL.
        """

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        kwargs = {"src": self.get_url_for_html_output(env)}
        if self.width is not None:
            kwargs["width"] = f"{self.width}px"
        if self.height is not None:
            kwargs["height"] = f"{self.height}px"
        if self.float:
            kwargs["cls"] = f"img-float-{self.align or 'right'}"
        elif self.align is not None:
            kwargs["cls"] = f"img-{self.align}"

        return html_start_tag("img", **kwargs)


class ImageNode(BaseImageNode):
    """Image node."""

    url: HttpUrl
    """URL of the image to display."""

    def get_url_for_html_output(
        self,
        env: NodeHTMLRenderEnvironment,
        /,
    ) -> str:
        """Get the URL to the image for HTML output.

        :return: Obtained URL.
        """
        return str(self.url)


class AdminImageNode(BaseImageNode):
    """Admin image node."""

    path: str
    """Path to the image to display."""

    @field_validator("path", mode="after")
    @classmethod
    def _remove_prefix_from_path(cls, value: str, /) -> str:
        """Remove the initial slash from the path, if present."""
        return value.removeprefix("/")

    def get_url_for_html_output(
        self,
        env: NodeHTMLRenderEnvironment,
        /,
    ) -> str:
        """Get the URL to the image for HTML output.

        :return: Obtained URL.
        """
        return env.staff_image_url_format.format(path=self.path)


class ProgressBarNode(BlockContainerNode):
    """Progress bar node."""

    value: Annotated[Decimal, Ge(0), Le(1)]
    """Value of the progress bar, between 0 and 1 included."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                "<div>",
                self.render_children_html(env),
                html_start_tag(
                    "div",
                    style="".join(
                        (
                            "background-color: white; ",
                            "border: 1px solid black; ",
                            "width: 50%; ",
                            "margin-top: 2px; ",
                            "text-align: left",
                        ),
                    ),
                ),
                html_start_tag(
                    "div",
                    style="".join(
                        (
                            "background-color: #FF3E28; ",
                            "color: black; ",
                            "font-weight: bold; ",
                            "max-width: 100%; ",
                            f"width: {int(self.value * 100)}%; ",
                            "height: 18px",
                        ),
                    ),
                ),
                f"&nbsp;&nbsp;&nbsp;{int(self.value * 100)}%",
                "</div></div></div>",
            ),
        )


class CalcIconNode(InlineNode):
    """Calculator icon node."""

    name: str
    """Smiley name."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return html_start_tag(
            "img",
            src=env.calc_url_format.format(name=self.name),
        )


class ListItemNode(BlockContainerNode):
    """List item node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "<li>" + self.render_children_html(env) + "</li>"


class ListType(str, Enum):
    """List type."""

    UL = "ul"
    """Unordered list."""

    OL = "ol"
    """Ordered list."""

    ARROW = "arrow"
    """Arrow-based list."""


class ListNode(BlockContainerNode):
    """List node."""

    AUTHORIZED_CHILDREN_TYPES = (ListItemNode,)

    type: ListType = ListType.UL
    """List type."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        if self.type == ListType.ARROW:
            typ = "ul"
            kwargs = {"cls": "arrow"}
        else:
            typ = self.type.value
            kwargs = {}

        return (
            html_start_tag(typ, **kwargs)
            + self.render_children_html(env)
            + f"</{typ}>"
        )


class TableHeaderNode(BlockInlineContainerNode):
    """Table header node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "<th>" + self.render_children_html(env) + "</th>"


class TableCellNode(BlockInlineContainerNode):
    """Table cell node."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "<td>" + self.render_children_html(env) + "</td>"


class TableRowNode(BlockContainerNode):
    """Table row node."""

    AUTHORIZED_CHILDREN_TYPES = (TableHeaderNode, TableCellNode)

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "<tr>" + self.render_children_html(env) + "</tr>"


class TableNode(BlockContainerNode):
    """Table node."""

    AUTHORIZED_CHILDREN_TYPES = (TableRowNode,)

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "<table>" + self.render_children_html(env) + "</table>"


# ---
# Inline nodes.
# ---


class StrongNode(InlineContainerNode):
    """Node to place text in strong."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return f"<b>{self.render_children_html(env)}</b>"


class EmphasisNode(InlineContainerNode):
    """Node to place text in emphasis (italic)."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return f"<i>{self.render_children_html(env)}</i>"


class UnderlineNode(InlineContainerNode):
    """Node to place text with an underline."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return f"<u>{self.render_children_html(env)}</u>"


class OverlineNode(InlineContainerNode):
    """Node to place text with an overline."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return (
            f'<span class="overline">{self.render_children_html(env)}</span>'
        )


class StrikeThroughNode(InlineContainerNode):
    """Node to place text with a strike-through."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return (
            f'<span class="strike-through">{self.render_children_html(env)}'
            "</span>"
        )


class FontFamilyNode(InlineContainerNode):
    """Node to set the font manually on a given text."""

    name: FontName
    """Name of the font to set."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag("span", style=f"font-family: {self.name}"),
                self.render_children_html(env),
                "</span>",
            ),
        )


class FontSizeNode(InlineContainerNode):
    """Node to set the font size manually on a given text."""

    size: Annotated[Decimal, Gt(0)]
    """Font size, in the provided unit."""

    unit: Literal["pt", "em"]
    """Unit of the font size to set."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag(
                    "span",
                    style=f"font-size: {self.size}{self.unit}",
                ),
                self.render_children_html(env),
                "</span>",
            ),
        )


class FontColorNode(InlineContainerNode):
    """Node to set the font color manually."""

    color: Color
    """Color to set to the font."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag(
                    "span",
                    style="; ".join(
                        f"color: {css}" for css in self.color.css()
                    ),
                ),
                self.render_children_html(env),
                "</span>",
            ),
        )


class BackColorNode(InlineContainerNode):
    """Node to set the background color manually on text."""

    color: Color
    """Color to set to the background color manually."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag(
                    "span",
                    style="; ".join(
                        f"background-color: {css}" for css in self.color.css()
                    ),
                ),
                self.render_children_html(env),
                "</span>",
            ),
        )


class InlineCodeNode(InlineNode):
    """Inline code node."""

    content: str
    """Content."""

    language: CodeLanguage | None = None
    """Language of the code."""

    def __init__(self, content: str, **kwargs) -> None:
        super().__init__(content=content, **kwargs)

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag("span", style="font-family: monospace"),
                html_escape(self.content),
                "</span>",
            ),
        )


class AnchorNode(InlineContainerNode):
    """Anchor node."""

    anchor: Anchor
    """Anchor to place."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag("span", href=self.anchor),
                self.render_children_html(env),
                "</span>",
            ),
        )


class TargetNode(InlineContainerNode):
    """Target node."""

    anchor: Anchor
    """Anchor to reference."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return "".join(
            (
                html_start_tag("a", href=f"#{self.anchor}"),
                self.render_children_html(env),
                "</a>",
            ),
        )


class ExternalReferenceNode(InlineNode):
    """Reference to an external resource."""

    @abstractmethod
    def build_data(self, env: NodeHTMLRenderEnvironment, /) -> tuple[str, str]:
        """Build external reference data.

        :param env: Environment with all of the options.
        :return: Obtained title and URL.
        """

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        title, url = self.build_data(env)

        kwargs = {}
        if env.link_target == LinkTarget.BLANK:
            kwargs["target"] = "_blank"
            kwargs["rel"] = "noopener"

        return "".join(
            (
                html_start_tag(
                    "a",
                    href=url,
                    **kwargs,
                ),
                html_escape(title),
                "</a>",
            ),
        )


class ProfileReferenceNode(ExternalReferenceNode):
    """Reference to a Planète Casio user profile."""

    username: Username
    """Username to reference."""

    def build_data(self, env: NodeHTMLRenderEnvironment, /) -> tuple[str, str]:
        """Build external reference data.

        :param env: Environment with all of the options.
        :return: Obtained title and URL.
        """
        return (
            self.username,
            env.user_profile_url_format.format(username=self.username),
        )


class TopicReferenceNode(ExternalReferenceNode):
    """Reference to a Planète Casio forum topic."""

    id: Annotated[int, Ge(1)]
    """Topic to reference."""

    def build_data(self, env: NodeHTMLRenderEnvironment, /) -> tuple[str, str]:
        """Build external reference data.

        :param env: Environment with all of the options.
        :return: Obtained title and URL.
        """
        return (
            f"Topic #{self.id}",
            env.topic_url_format.format(id=str(self.id)),
        )


class TutorialReferenceNode(ExternalReferenceNode):
    """Reference to a Planète Casio tutorial."""

    id: Annotated[int, Ge(1)]
    """Tutorial to reference."""

    def build_data(self, env: NodeHTMLRenderEnvironment, /) -> tuple[str, str]:
        """Build external reference data.

        :param env: Environment with all of the options.
        :return: Obtained title and URL.
        """
        return (
            f"Tutorial #{self.id}",
            env.tutorial_url_format.format(id=str(self.id)),
        )


class ProgramReferenceNode(ExternalReferenceNode):
    """Reference to a Planète Casio program."""

    id: Annotated[int, Ge(1)]
    """Program to reference."""

    def build_data(self, env: NodeHTMLRenderEnvironment, /) -> tuple[str, str]:
        """Build external reference data.

        :param env: Environment with all of the options.
        :return: Obtained title and URL.
        """
        return (
            f"Program #{self.id}",
            env.program_url_format.format(id=str(self.id)),
        )


class VideoNode(BlockNode):
    """Video node."""

    YOUTUBE_VIDEO_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"^/?([a-zA-Z0-9_-]+)$",
    )
    """Pattern for matching ``youtu.be`` paths and extracting the video."""

    GFYCAT_PATH_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"^(.*)-mobile(\.(?:mp4|webm))$",
    )
    """Pattern for matching ``thumbs.gfycat.com`` paths."""

    url: HttpUrl
    """URL to the video."""

    format: Literal["normal", "tiny"] = "normal"
    """Format, that determines the dimensions of the final player."""

    width: int | None = None
    """Explicit width, if defined."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        width, height = (560, 340) if self.format == "normal" else (470, 300)
        if self.width is not None:
            width = self.width

        if (
            self.url.host == "youtu.be"
            and (match := self.YOUTUBE_VIDEO_PATTERN.match(self.url.path))
        ) or (
            self.url.host in ("youtube.com", "www.youtube.com")
            and (
                match := self.YOUTUBE_VIDEO_PATTERN.match(
                    get_url_param(str(self.url), "v"),
                )
            )
        ):
            return (
                html_start_tag(
                    "iframe",
                    width=str(width),
                    height=str(height),
                    src=f"https://www.youtube.com/embed/{match[1]}",
                    frameborder="0",
                    allowfullscreen="",
                )
                + "</iframe>"
            )

        # Gfycat was closed, but planet-casio hosts a proxy for some of the
        # videos on there, so we use that.
        if self.url.host == "giant.gfycat.com":
            return (
                html_start_tag("video", controls="", width=str(width))
                + html_start_tag(
                    "source",
                    src=f"https://www.planet-casio.com/images/gfycat{self.url.path}",
                )
                + "</video>"
            )

        if self.url.host == "thumbs.gfycat.com":
            match = self.GFYCAT_PATH_PATTERN.match(self.url.path)
            if match is not None:
                return (
                    html_start_tag("video", controls="", width=str(width))
                    + html_start_tag(
                        "source",
                        src=f"https://www.planet-casio.com/images/gfycat{match[1]}{match[2]}",
                    )
                    + "</video>"
                )

        if "gfycat" in self.url.host:
            return (
                "<b>"
                + html_start_tag("span", style="color: red")
                + html_escape(str(self.url))
                + "</span></b>"
            )

        return (
            html_start_tag("video", controls="", width=str(width))
            + html_start_tag("source", src=str(self.url))
            + "</video>"
        )
