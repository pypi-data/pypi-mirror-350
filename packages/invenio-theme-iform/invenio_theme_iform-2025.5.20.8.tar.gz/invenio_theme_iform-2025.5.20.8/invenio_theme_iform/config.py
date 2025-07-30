# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 Graz University of Technology.
#
# invenio-theme-iform is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for I-Form theme."""

INVENIO_THEME_IFORM_DEFAULT_VALUE = "I-Form Repository"
"""Default value for the application."""

INVENIO_THEME_IFORM_BASE_TEMPLATE = "invenio_theme_iform/base.html"
"""I-Form Default base template"""

INVENIO_THEME_IFORM_ACCOUNT_BASE = "invenio_theme_iform/accounts/accounts_base.html"
"""I-Form Default account base template"""

INVENIO_THEME_IFORM_ICON = "images/icon_use.png"
"""icon used in login page"""

INVENIO_THEME_IFORM_LOGIN_IMG = "images/login_logo.png"
"""I-Form Logo for forms"""

THEME_IFORM_CONTACT_FORM = False
"""Enable/Disable Contact form."""

THEME_IFORM_PRODUCTION = False
"""Production environment.

    Can also be set as an environment variable in a .env file. Then the name
    has to be 'INVENIO_THEME_IFORM_PRODUCTION'.
"""

THEME_IFORM_SUPPORT_EMAIL = ""
"""Shown as contact-info on default error-page."""

# Invenio-theme
# ============
# See https://invenio-theme.readthedocs.io/en/latest/configuration.html
#
THEME_500_TEMPLATE = "invenio_theme_iform/default_error.html"
"""Used for any internal server errors and uncaught exceptions."""

THEME_LOGO = "images/iform_logo.png"
"""I-Form logo"""

THEME_SEARCHBAR = False
"""Enable or disable the header search bar."""

THEME_HEADER_TEMPLATE = "invenio_theme_iform/header.html"
"""I-Form header template"""

THEME_FRONTPAGE = False
"""Use default frontpage."""

THEME_HEADER_LOGIN_TEMPLATE = "invenio_theme_iform/accounts/header_login.html"
"""login page header"""

THEME_FOOTER_TEMPLATE = "invenio_theme_iform/footer.html"
"""footer template"""

THEME_FRONTPAGE_TITLE = "I-Form Repository"
"""Frontpage title."""

THEME_SITENAME = "Repository"
"""Site name."""

# Invenio-accounts
# ============
# See https://invenio-accounts.readthedocs.io/en/latest/configuration.html

# COVER_TEMPLATE = 'invenio_theme_iform/accounts/accounts_base.html'
"""Cover page template for login and sign up pages."""

SECURITY_LOGIN_USER_TEMPLATE = "invenio_theme_iform/accounts/login_user.html"
"""Login template"""

SECURITY_REGISTER_USER_TEMPLATE = "invenio_theme_iform/accounts/register_user.html"
"""Sigup template"""

# Invenio-app-rdm
# =============
# See https://invenio-app-rdm.readthedocs.io/en/latest/configuration.html
SEARCH_UI_HEADER_TEMPLATE = "invenio_theme_iform/header.html"
"""Search page's header template."""

DEPOSITS_HEADER_TEMPLATE = "invenio_theme_iform/header.html"
"""Deposits header page's template."""


# Invenio-rdm-records
# =============
# See https://invenio-rdm-records.readthedocs.io/en/latest/configuration.html
# Uncomment below to override records landingpage.
# from invenio_rdm_records.config import RECORDS_UI_ENDPOINTS
# RECORDS_UI_ENDPOINTS["recid"].update(
#     template="invenio_theme_iform/record_landing_page.html"
# )
"""override the default record landing page"""

# Invenio-search-ui
# =============
# See https://invenio-search-ui.readthedocs.io/en/latest/configuration.html
# SEARCH_UI_SEARCH_TEMPLATE = "invenio_theme_iform/search.html"
# """override the default search page"""

IFORM_ROUTES = {
    "index": "/",
    "comingsoon": "/comingsoon",
}
