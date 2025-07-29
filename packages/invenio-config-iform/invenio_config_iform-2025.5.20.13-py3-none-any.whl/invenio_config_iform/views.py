# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 Graz University of Technology.
#
# invenio-config-iform is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for I-Form config."""

from flask import Blueprint, Flask, redirect, url_for
from invenio_i18n import get_locale
from werkzeug.wrappers import Response as BaseResponse


def ui_blueprint(app: Flask) -> Blueprint:
    """Blueprint for the routes and resources provided by invenio-config-iform."""
    routes = app.config.get("CONFIG_IFORM_ROUTES")

    blueprint = Blueprint(
        "invenio_config_iform",
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    blueprint.add_url_rule(routes["guide"], view_func=guide)
    blueprint.add_url_rule(routes["terms"], view_func=terms)
    blueprint.add_url_rule(routes["gdpr"], view_func=gdpr)

    return blueprint


def guide() -> BaseResponse:
    """I-Form_Repository_Guide."""
    locale = get_locale()
    return redirect(
        url_for(
            "static",
            filename=f"documents/I-Form_Repository_Guide_02.1_{locale}.pdf",
            _external=True,
        ),
    )


def terms() -> BaseResponse:
    """Terms_And_Conditions."""
    locale = get_locale()
    return redirect(
        url_for(
            "static",
            filename=f"documents/I-Form_Repository_Terms_And_Conditions_{locale}.pdf",
            _external=True,
        ),
    )


def gdpr() -> BaseResponse:
    """General_Data_Protection_Rights."""
    locale = get_locale()
    return redirect(
        url_for(
            "static",
            filename=f"documents/I-Form_Repository_General_Data_Protection_Rights_{locale}.pdf",
            _external=True,
        ),
    )
