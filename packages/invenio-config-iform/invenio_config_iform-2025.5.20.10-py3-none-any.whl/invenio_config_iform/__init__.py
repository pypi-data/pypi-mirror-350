# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 Graz University of Technology.
#
# invenio-config-iform is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds I-Form configs."""

from .__about__ import __version__
from .ext import InvenioConfigIform
from .utils import get_identity_from_user_by_email

__all__ = (
    "InvenioConfigIform",
    "__version__",
    "get_identity_from_user_by_email",
)
