"""
Package contains implementation of various themes (for example `default`). It also contains their specific implementations mapped to theme names, such as `GREY_CYCLER`.
"""

import contextlib

from cycler import cycler as _cycler

from profiplots import settings as _settings

__all__ = ["GREY_CYCLER", "GREYSCALE_CYCLER", "COLOR_CYCLER", "PUBLISH_PROFILE", "EXPLORATION_PROFILE", "PRESENTATION_PROFILE"]

with contextlib.suppress(ImportError):
    from profiplots.theme._plotnine import theme_profiplots as _theme_profiplots
    __all__ += ["_theme_profiplots"]

GREY_CYCLER = {"default": _cycler(color=["#7D7D7D", "#7D7D7D", "#7D7D7D", "#7D7D7D", "#7D7D7D", "#7D7D7D", "#7D7D7D"])}
"""Mapping of name of the theme to the color cycler of the theme with a grey color."""

GREYSCALE_CYCLER = {"default": _cycler(color=["#282828", "#555555", "#7D7D7D", "#AAAAAA", "#BEBEBE"])}
"""Mapping of name of the theme to the color cycler of the theme with greyscale colors (multiple shades of grey)."""

BLUESCALE_CYCLER = {"default": _cycler(color=["#465A9B", "#6B7BAF", "#909CC3", "#B5BDD7", "#C7CDE1"])}
"""Mapping of name of the theme to the color cycler of the theme with bluescale colors (multiple shades of blue)."""

COLOR_CYCLER = {"default": _cycler(color=["#465A9B", "#E63C41", "#B5578D", "#FFD21E", "#F3943B", "#41C34B", "#3DADE5"])}
"""Mapping of name of the theme to the color cycler of the theme with colors."""

PUBLISH_PROFILE = {
    "default": {
        # GENERAL
        "font.size": 10.0,
        # GRID
        "axes.grid": False,
        "axes.grid.axis": "both",
        "grid.linewidth": 0.5,
        "grid.color": "#D7D7D7",
        # TICKS
        "xtick.top": False,
        "xtick.bottom": True,
        "xtick.labeltop": False,
        "xtick.labelbottom": True,
        "xtick.color": "#D7D7D7",
        "xtick.major.width": 0.5,
        "ytick.right": False,
        "ytick.left": True,
        "ytick.labelright": False,
        "ytick.labelleft": True,
        "ytick.color": "#D7D7D7",
        "ytick.major.width": 0.5,
        # SPINES
        "axes.edgecolor": "#D7D7D7",
        "axes.linewidth": 0.8,
        "axes.spines.left": True,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.spines.bottom": True,
    }
}
"""Matplotlib RC settings for the publish profile."""

EXPLORATION_PROFILE = {
    "default": {
        # GENERAL
        "font.size": 10.0,
        # GRID
        "axes.grid": True,
        "axes.grid.axis": "both",
        "grid.linewidth": 0.5,
        "grid.color": "#D7D7D7",
        # TICKS
        "xtick.top": False,
        "xtick.bottom": True,
        "xtick.labeltop": False,
        "xtick.labelbottom": True,
        "xtick.color": "#D7D7D7",
        "xtick.major.width": 0.5,
        "ytick.right": False,
        "ytick.left": True,
        "ytick.labelright": False,
        "ytick.labelleft": True,
        "ytick.color": "#D7D7D7",
        "ytick.major.width": 0.5,
        # SPINES
        "axes.linewidth": 0.8,
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.spines.bottom": False,
    }
}
"""Matplotlib RC settings for the exploration profile."""

PRESENTATION_PROFILE = {
    "default": {
        # GENERAL
        "font.size": 12.0,
        # GRID
        "axes.grid": False,
        "axes.grid.axis": "both",
        "grid.linewidth": 1,
        "grid.color": "#BEBEBE",
        # TICKS
        "xtick.top": False,
        "xtick.bottom": True,
        "xtick.labeltop": False,
        "xtick.labelbottom": True,
        "xtick.color": "#BEBEBE",
        "xtick.major.width": 1,
        "ytick.right": False,
        "ytick.left": True,
        "ytick.labelright": False,
        "ytick.labelleft": True,
        "ytick.color": "#BEBEBE",
        "ytick.major.width": 1,
        # SPINES
        "axes.edgecolor": "#BEBEBE",
        "axes.linewidth": 1.25,
        "axes.spines.left": True,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.spines.bottom": True,
    }
}
"""Matplotlib RC settings for the presentation profile."""

assert all(k in _settings.SUPPORTED_THEMES for k in GREY_CYCLER), "Invalid theme name in `GREY_CYCLER`."
assert all(k in _settings.SUPPORTED_THEMES for k in COLOR_CYCLER), "Invalid theme name in `COLOR_CYCLER`."
assert all(k in _settings.SUPPORTED_THEMES for k in PUBLISH_PROFILE), "Invalid theme name in `PUBLISH_PROFILE`."
assert all(k in _settings.SUPPORTED_THEMES for k in EXPLORATION_PROFILE), "Invalid theme name in `EXPLORATION_PROFILE`."
assert all(k in _settings.SUPPORTED_THEMES for k in PRESENTATION_PROFILE), "Invalid theme name in `PRESENTATION_PROFILE`."
