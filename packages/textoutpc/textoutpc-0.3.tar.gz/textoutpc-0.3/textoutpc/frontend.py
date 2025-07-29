#!/usr/bin/env python
# *****************************************************************************
# Copyright (C) 2025 Thomas Touhey <thomas@touhey.fr>
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
"""Front-end functions."""

from __future__ import annotations

from typing import Literal, TextIO

from .builtin.parsers import (
    default_inline_parser,
    default_parser,
    strict_inline_parser,
    strict_parser,
)
from .nodes import LinkTarget, NodeHTMLRenderEnvironment
from .parser import Parser


def render_as_html(
    inp: str | TextIO,
    /,
    *,
    parser: Parser
    | Literal["strict_inline", "strict", "inline", "default"] = "default",
    link_target: LinkTarget = LinkTarget.BLANK,
) -> str:
    """Convert textout-style BBCode to HTML.

    :param inp: Input, either as a string or text stream.
    :param parser: Parser to use.
    :param link_target: Target to add to references / hyperlinks.
    :return: Obtained HTML.
    """
    if parser == "strict_inline":
        parser_to_use = strict_inline_parser
    elif parser == "strict":
        parser_to_use = strict_parser
    elif parser == "inline":
        parser_to_use = default_inline_parser
    elif parser == "default":
        parser_to_use = default_parser
    else:
        parser_to_use = parser

    env = NodeHTMLRenderEnvironment(link_target=link_target)
    return "".join(node.render_html(env) for node in parser_to_use.parse(inp))
