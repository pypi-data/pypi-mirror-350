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
"""Miscellaneous utilities."""

from __future__ import annotations

from collections.abc import Sequence
from urllib.parse import parse_qsl, urlencode, urlparse


def html_escape(text: str, /) -> str:
    """Escape HTML entities in the given text.

    :param text: Text to escape.
    :return: Text with escaped HTML entities.
    """
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def html_start_tag(
    name: str,
    /,
    *,
    cls: str | Sequence[str] | None = None,
    **kwargs: str | None,
) -> str:
    """Get an HTML start tag.

    :param name: Name of the start tag.
    :param cls: CSS classes for the tag.
    :return: Rendered start tag.
    """
    attrs = {}
    if isinstance(cls, str):
        cls = (cls,)
    if cls:
        attrs["class"] = " ".join(cls)

    for key, value in kwargs.items():
        if value is not None:
            attrs[key] = value

    return (
        f"<{name}"
        + "".join(
            f' {aname}="{html_escape(avalue)}"'
            if avalue != ""
            else f" {aname}"
            for aname, avalue in attrs.items()
        )
        + ">"
    )


def get_url_with_params(url: str, **kwargs: str | None) -> str:
    """Get an URL with additional or without some query parameters.

    :param url: The URL to modify.
    """
    parsed_url = urlparse(url)
    params = dict(parse_qsl(parsed_url.query, keep_blank_values=True))

    for key, value in kwargs.items():
        if value is None:
            if key in params:
                del params[key]
        else:
            params[key] = str(value)

    return parsed_url._replace(
        query=urlencode(params, doseq=True),
    ).geturl()


def get_url_param(
    url: str,
    name: str,
    /,
) -> str:
    """Get a specific query parameter from an URL.

    :param url: The URL to get the parameter from.
    :param name: The name of the query parameter to get.
    :return: Value, or empty string if the parameter was not present.
    """
    parsed_url = urlparse(url)
    params = dict(parse_qsl(parsed_url.query, keep_blank_values=True))
    if name not in params:
        return ""

    return params[name]
