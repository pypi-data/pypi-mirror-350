#!/usr/bin/env python
# *****************************************************************************
# Copyright (C) 2024-2025 Thomas Touhey <thomas@touhey.fr>
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
"""Node definitions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Sequence
from enum import Enum
from typing import Annotated, ClassVar, Literal, TypeVar, overload

from pydantic import (
    AnyUrl,
    BaseModel,
    ConfigDict,
    StringConstraints,
    field_validator,
)

from .errors import ChildNotFound, TooManyChildren
from .misc import get_url_with_params, html_escape, html_start_tag

NodeT = TypeVar("NodeT", bound="Node")


class LinkTarget(str, Enum):
    """Target to add to links."""

    SELF = "self"
    """Whether the target is the current window and tab."""

    BLANK = "blank"
    """Whether the target is a different window / tab.

    In this case, ``rel="noopener"`` is also added, in order for the new
    window / tab to have no access to the current window / tab.
    """


class NodeHTMLRenderEnvironment(BaseModel):
    """Node rendering environment."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=True,
    )
    """Model configuration."""

    link_target: LinkTarget = LinkTarget.BLANK
    """Link target."""

    smiley_url_format: str = (
        "https://www.planet-casio.com/images/smileys/{name}.gif"
    )
    """URL format for smileys."""

    calc_url_format: str = (
        "https://www.planet-casio.com/images/icones/calc/{name}.png"
    )
    """URL format for calculator icons."""

    staff_image_url_format: str = (
        "https://www.planet-casio.com/storage/staff/{path}"
    )
    """URL format for staff images."""

    user_profile_url_format: str = (
        "https://www.planet-casio.com/Fr/compte/voir_profil.php"
        "?membre={username}"
    )
    """URL format for members."""

    topic_url_format: str = (
        "https://www.planet-casio.com/Fr/forums/lecture_sujet.php?id={id}"
    )
    """URL format for topics."""

    tutorial_url_format: str = (
        "https://www.planet-casio.com/Fr/programmation/tutoriels.php?id={id}"
    )
    """URL format for tutorials."""

    program_url_format: str = (
        "https://www.planet-casio.com/Fr/programmes/"
        "voir_un_programme_casio.php?showid={id}"
    )
    """URL format for programs."""

    email_script_url: str = (
        "https://www.planet-casio.com/scripts/public/email.php"
    )
    """URL to the e-mail display format."""


class Node(ABC, BaseModel):
    """Base node in a textoutpc tree."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
        extra="forbid",
    )
    """Model configuration."""

    @abstractmethod
    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """


class TextNode(Node):
    """Textual node in a textoutpc tree."""

    content: str
    """Content."""

    def __init__(self, /, content: str | None = None, **kwargs) -> None:
        kwargs["content"] = content
        super().__init__(**kwargs)

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return html_escape(self.content)


class ContainerNode(Node):
    """Container node in a textoutpc tree."""

    AUTHORIZED_CHILDREN_TYPES: ClassVar[
        Sequence[type[Node] | tuple[type[Node], int | range]] | None
    ] = None
    """Authorized children types.

    This is a sequence of either the type to check, or the authorized count
    of this type of node. Here's an example use of this property::

        class MyContainerNode(ContainerNode):
            AUTHORIZED_CHILDREN_TYPES = (
                MyFirstNode,
                (MySecondNode, 4),
                (MyThirdNode, range(1, 3)),
            )

    This example presents the following constraints:

    * Children are either instances of ``MyFirstNode``, ``MySecondNode`` or
      ``MyThirdNode``;
    * There must be exactly 4 ``MySecondNode`` instances;
    * There must be 1 or 2 ``MyThirdNode`` instances.
    """

    children: tuple[Node, ...]
    """Children."""

    def __init__(
        self,
        /,
        children: Iterable[Node] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(children=children or [], **kwargs)

    @field_validator("children", mode="after")
    @classmethod
    def _check_children_types(cls, value: Sequence[Node], /) -> Sequence[Node]:
        """Check that the children types are authorized.

        If :py:attr:`AUTHORIZED_CHILDREN_TYPES` is set, this validator
        removes :py:class:`TextNode` instances from the children, then
        validates that all nodes are instances of the provided types.

        :return: Reference to current, validated object.
        """
        if cls.AUTHORIZED_CHILDREN_TYPES is None:
            return value

        types_allowed = tuple(
            entry if isinstance(entry, type) else entry[0]
            for entry in cls.AUTHORIZED_CHILDREN_TYPES
        )
        counters = [0 for _ in types_allowed]
        text_allowed = TextNode in types_allowed

        # Check if there is any forbidden types in the children.
        # Optionally remove the text nodes if they are not explicitely allowed.
        children = list(value)
        for child_no, child in list(enumerate(children))[::-1]:
            if isinstance(child, TextNode) and not text_allowed:
                # Ignore the child.
                children.pop(child_no)
                continue

            at_least_one_constraint = False
            for i, typ in enumerate(types_allowed):
                if isinstance(child, typ):
                    counters[i] += 1
                    at_least_one_constraint = True

            if not at_least_one_constraint:
                raise TypeError(
                    f"Child #{child_no} ({child.__class__.__name__}) is not "
                    "an instance of one of the allowed types: "
                    f"{', '.join(typ.__name__ for typ in types_allowed)}",
                )

        # Check the counters.
        for entry, count in zip(cls.AUTHORIZED_CHILDREN_TYPES, counters):
            if isinstance(entry, type):
                # No specific count for that type, we can ignore.
                continue

            cls, numeric_constraint = entry
            if isinstance(numeric_constraint, range):
                respected = count in numeric_constraint
            else:
                respected = count == numeric_constraint

            if not respected:
                raise TypeError(
                    f"Invalid count for {cls.__name__} instances (expected: "
                    f"{numeric_constraint}, got: {count})",
                )

        return children

    def find_children(
        self,
        type_or_types: tuple[type, ...] | type | None = None,
        /,
        *,
        exclude_type: type | None = None,
        exclude_types: tuple[type, ...] | None = None,
    ) -> Iterator[Node]:
        """Find children with the provided filters.

        :param type_or_types: Only count children of the provided type
            or types.
        :param exclude_type: Exclude the provided type in the count.
        :param exclude_types: Exclude the provided types in the count.
        :return: Children for the provided filters.
        """
        if exclude_types:
            if exclude_type is not None:
                exclude_types = (*exclude_types, exclude_type)
        elif exclude_type is not None:
            exclude_types = (exclude_type,)
        else:
            # If exclude_types is an empty list, we also want to set it
            # to None.
            exclude_types = None

        types: tuple[type, ...] | None = None
        if isinstance(type_or_types, type):
            types = (type_or_types,)
        elif type_or_types is not None:
            types = tuple(type_or_types)

        if types is not None and exclude_types is not None:
            types = tuple(typ for typ in types if typ not in exclude_types)

        if types is not None and not types:
            return

        if types is None:
            if exclude_types is None:
                yield from self.children
            else:
                for child in self.children:
                    if not isinstance(child, exclude_types):
                        yield child
        elif exclude_types is None:
            for child in self.children:
                if isinstance(child, types):
                    yield child
        else:
            for child in self.children:
                if isinstance(child, types) and not isinstance(
                    child,
                    exclude_types,
                ):
                    yield child

    @overload
    def find_child(
        self,
        type_or_types: tuple[type, ...] | type | None = None,
        /,
        *,
        exclude_type: type | None = None,
        exclude_types: tuple[type, ...] | None = None,
        optional: Literal[True],
    ) -> Node | None: ...

    @overload
    def find_child(
        self,
        type_or_types: tuple[type, ...] | type | None = None,
        /,
        *,
        exclude_type: type | None = None,
        exclude_types: tuple[type, ...] | None = None,
        optional: Literal[False] = False,
    ) -> Node: ...

    def find_child(
        self,
        type_or_types: tuple[type, ...] | type | None = None,
        /,
        *,
        exclude_type: type | None = None,
        exclude_types: tuple[type, ...] | None = None,
        optional: bool = False,
    ) -> Node | None:
        """Find a single child with the provided filters.

        :param type_or_types: Only count children of the provided type
            or types.
        :param exclude_type: Exclude the provided type in the count.
        :param exclude_types: Exclude the provided types in the count.
        :return: Child for the provided filters.
        :raises ChildNotFound:
        :raises TooManyChildren:
        """
        found: Node | None = None
        for node in self.find_children(
            type_or_types,
            exclude_type=exclude_type,
            exclude_types=exclude_types,
        ):
            if found is not None:
                raise TooManyChildren()

            found = node

        if found is None and not optional:
            raise ChildNotFound()

        return found

    def count_children(
        self,
        type_or_types: tuple[type, ...] | type | None = None,
        /,
        *,
        exclude_type: type | None = None,
        exclude_types: tuple[type, ...] | None = None,
    ) -> int:
        """Count children of a provided type.

        :param type_or_types: Only count children of the provided type
            or types.
        :param exclude_type: Exclude the provided type in the count.
        :param exclude_types: Exclude the provided types in the count.
        :return: Count of children for the provided filters.
        """
        return sum(
            1
            for _ in self.find_children(
                type_or_types,
                exclude_type=exclude_type,
                exclude_types=exclude_types,
            )
        )

    def render_children_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node's children as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node's children.
        """
        return "".join(node.render_html(env) for node in self.children)


class BlockNode(Node):
    """Block-level node."""


class BlockContainerNode(ContainerNode, BlockNode):
    """Block-level node that can contain both block and inline nodes."""


class BlockInlineContainerNode(ContainerNode, BlockNode):
    """Block-level node that can contain inline nodes."""


class InlineNode(Node):
    """Inline-level node."""


class InlineContainerNode(ContainerNode, InlineNode):
    """Inline-level node that can contain other inline nodes."""


class ParagraphNode(BlockInlineContainerNode):
    """Paragraph node."""

    align: Literal["center", "left", "right", "justify"] | None = None
    """Optional method to use to align the text within the paragraph."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return (
            html_start_tag(
                "p",
                cls=(f"align-{self.align}",) if self.align is not None else (),
            )
            + self.render_children_html(env)
            + "</p>"
        )


class SmileyNode(InlineNode):
    """Smiley node."""

    name: str
    """Smiley name."""

    style: str | None = None
    """Optional inline style."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        return html_start_tag(
            "img",
            src=env.smiley_url_format.format(name=self.name),
            style=self.style,
        )


class EmailAddressNode(InlineNode):
    """E-mail address node."""

    email_address: Annotated[str, StringConstraints(pattern=r"^[^@]+@[^@]+$")]
    """E-mail address."""

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        user, domain = self.email_address.replace(".", "▶").split("@")
        return html_start_tag(
            "img",
            src=get_url_with_params(
                env.email_script_url,
                domain=domain,
                user=user,
            ),
            alt="Email address, replace the 【arobase】 with a @ and ▶ with a "
            f". : {user}【arobase】{domain}",  # noqa: RUF001
        )


class BaseReferenceNode(InlineContainerNode):
    """Reference to an HTTP URL."""

    @abstractmethod
    def build_html_url(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Build the URL for HTML output.

        :param env: Environment with all of the options.
        :return: Obtained URL.
        """

    def render_html(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Render the node as HTML.

        :param env: Environment with all of the options.
        :return: Rendered HTML version of the node.
        """
        kwargs = {}
        if env.link_target == LinkTarget.BLANK:
            kwargs["target"] = "_blank"
            kwargs["rel"] = "noopener"

        return "".join(
            (
                html_start_tag(
                    "a",
                    href=self.build_html_url(env),
                    **kwargs,
                ),
                self.render_children_html(env),
                "</a>",
            ),
        )


class ReferenceNode(BaseReferenceNode):
    """Reference to an HTTP URL."""

    url: AnyUrl
    """URL to reference."""

    def build_html_url(self, env: NodeHTMLRenderEnvironment, /) -> str:
        """Build the URL for HTML output.

        :param env: Environment with all of the options.
        :return: Obtained URL.
        """
        return str(self.url)
