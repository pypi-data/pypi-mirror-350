# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 TUGRAZ.
#
# invenio-theme-iform is free software.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-theme-iform-theme": "./less/invenio_theme_iform/theme.less",
                "invenio-theme-iform-js": "./js/invenio_theme_iform/theme.js",
                "invenio-theme-iform-unlock": "./js/invenio_theme_iform/unlock.js",
            },
            dependencies={
                "jquery": "^3.2.1",  # zammad-form, semantic-ui's modals
            },
        )
    },
)
