#!/usr/bin/env python
# *****************************************************************************
# Copyright (C) 2023-2025 Thomas Touhey <thomas@touhey.fr>
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
"""Error definitions."""

from __future__ import annotations


class Error(Exception):
    """An error has occurred."""

    __slots__ = ()

    def __init__(self, message: str | None, /) -> None:
        Exception.__init__(self, message or "")


class TagValidationError(Error, ValueError):
    """A tag validation has failed for an unknown error."""

    __slots__ = ("args", "kwargs", "message")

    def __init__(self, message: str = "", *args, **kwargs):
        self.message = message
        self.args = args
        self.kwargs = kwargs


class MissingValue(TagValidationError):
    """A value should have been provided, and wasn't."""


class UnexpectedValue(TagValidationError):
    """No value should have been provided, but one was."""


class InvalidValue(TagValidationError):
    """An invalid value was provided."""


class AlreadyRegistered(Error, ValueError):
    """The tag name was already registered."""

    names: set[str]
    """Names that were already registered."""

    def __init__(self, /, *, names: set[str]) -> None:
        super().__init__(
            f"The following names were already registered: {', '.join(names)}",
        )
        self.names = names


class ChildNotFound(Error, ValueError):
    """The child was already found."""

    def __init__(self, message: str | None = None, /) -> None:
        super().__init__(message or "")


class TooManyChildren(Error, ValueError):
    """Too many children were found for the given filters."""

    def __init__(self, message: str | None = None, /) -> None:
        super().__init__(message or "")
