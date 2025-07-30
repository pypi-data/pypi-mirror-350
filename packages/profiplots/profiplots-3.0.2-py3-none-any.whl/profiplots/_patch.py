import contextlib
from itertools import combinations
from typing import List, Union

import pandas as pd
from matplotlib.colors import Colormap as CMap

with contextlib.suppress(ImportError):
    import plotnine as _pn
    from plotnine.geoms import geom as _geom_base
    from plotnine.scales import scale_color_gradient, scale_color_manual, scale_fill_gradient, scale_fill_manual
    _original_build = _pn.ggplot._build
    _original_aes = {}

from colour import XYZ_to_Lab, delta_E, sRGB_to_XYZ
from cycler import Cycler


def _format_palette(prop_cycle: Union[List[str], str, Cycler]) -> List[str]:
    """Formats a color palette from various accepted types into a list of hex colors

    Parameters
    ----------
    prop_cycle : Union[List[str], str, Cycler]
        Object containing the hexadecimal colors to the applied palette.

    Returns
    -------
    List[str]
        Formatted palette of hexadecimal colors.

    Raises
    ------
    TypeError
        The applied palette must be of the types List[str], str, or Cycler.
    """
    if isinstance(prop_cycle, str):
        palette = [prop_cycle]

    elif isinstance(prop_cycle, Cycler):
        palette = [item["color"] for item in prop_cycle]

    elif isinstance(prop_cycle, list):
        palette = prop_cycle

    else:
        raise TypeError(f"Unsupported palette type: {type(prop_cycle)}")

    if len(palette) == 1:
        palette = [palette[0], palette[0]]

    return palette


def find_most_contrasting_pair(palette: List[str]) -> tuple[str, str]:
    """Find the most visually contrasting pair of hex colors from a palette.

    Parameters
    ----------
    palette : List[str]
        A list of hex color strings.

    Returns
    -------
    tuple[str, str]
        The pair of hex colors with the highest contrast.
    """
    def _hex_to_lab(hex_color: str):
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))
        return XYZ_to_Lab(sRGB_to_XYZ([r, g, b]))

    def _delta_e_cie76(c1, c2):
        return delta_E(c1, c2, method="CIE 1976")

    return max(
        combinations(palette, 2),
        key=lambda pair: _delta_e_cie76(_hex_to_lab(pair[0]), _hex_to_lab(pair[1]))
    )


def _reset_defaul_color():
    """Resets all geom default colors to their original values."""
    for name, original_aes in _original_aes.items():
        geom = getattr(_pn.geoms, name, None)
        if geom and hasattr(geom, "DEFAULT_AES"):
            geom.DEFAULT_AES = original_aes.copy()
    _original_aes.clear()



def reset_patch():
    """Resets patch of the build function to its original implementation."""
    _pn.ggplot._build = _original_build
    _reset_defaul_color()


def _patch_geom_default_color(palette: List[str]):
    """Patches default color of geom to the first color in the provided palette.

    Parameters
    ----------
    palette : List[str]
        Palette with hexadecimal colors.
    """
    primary_color = palette[0]

    for name in dir(_pn.geoms):
        geom = getattr(_pn.geoms, name)

        if isinstance(geom, type) and issubclass(type(geom), type(_geom_base.geom)):
            aes = getattr(geom, "DEFAULT_AES", None)
            if aes:
                if name not in _original_aes:
                    _original_aes[name] = aes.copy()

                if "fill" in aes and aes["fill"] is not None:
                    aes["fill"] = primary_color
                elif "color" in aes and aes["color"] is not None:
                    aes["color"] = primary_color


def _patch_build_method(palette: List[str], cmap: CMap = None):
    """
    Patches the ggplot build method to apply color/fill scales automatically.

    This function modifies `ggplot._build` to inject scale definitions based on aesthetic mappings:
    - If a color/fill is mapped to a categorical variable and no manual scale exists,
      a `scale_*_manual` is added using the provided palette.
    - If mapped to a continuous variable and no manual scale exists, a
      `scale_*_gradient` is added using:
        - the low/high ends of the provided `cmap`
        - or most contrasting pair from the palette (if `cmap` is None) as a fallback.

    Parameters
    ----------
    palette : List[str]
        List of hex color codes to be used for manual scales or fallback contrast.

    cmap : matplotlib.colors.Colormap, optional
        A colormap to derive low/high values for continuous scales.
    """
    def patched_build(self):
        def _is_categorical(column):
            col = self.data[column]
            return pd.api.types.is_object_dtype(col) or pd.api.types.is_categorical_dtype(col)

        def _has_manual_scale(aes_type):
            scale_cat, scale_con = {
                "color": (scale_color_manual, scale_color_gradient),
                "fill": (scale_fill_manual, scale_fill_gradient)
            }[aes_type]
            return any(isinstance(s, (scale_cat, scale_con)) for s in self.scales)

        def _get_mapping(aes):
            if aes in (self.mapping or {}):
                return self.mapping[aes]
            for layer in self.layers:
                mapping = layer.geom.mapping or {}
                if aes in mapping:
                    return mapping[aes]
            return None

        for aes, (scale_cat, scale_con) in {
            "color": (scale_color_manual, scale_color_gradient),
            "fill": (scale_fill_manual, scale_fill_gradient)
        }.items():
            if _has_manual_scale(aes):
                continue

            column = _get_mapping(aes)
            if column is None:
                continue

            if _is_categorical(column):
                self += scale_cat(values=palette)
            else:
                pair = find_most_contrasting_pair(palette) if cmap is None else [cmap(0.0), cmap(1.0)]

                self += scale_con(low=pair[0], high=pair[1])

        return _original_build(self)

    _pn.ggplot._build = patched_build


def apply_patch(palette: Union[List[str], str, Cycler], cmap: CMap = None):
    """
    Applies patching to plotnine to enforce a custom color palette and optional colormap.

    This function modifies internal behaviors of plotnine to support custom color palettes
    and colormaps in the profiplots environment, where theme-level palette definitions
    are not natively supported.

    It patches:
    1. The default colors of geoms (e.g., bars, points) to use the first color from the palette.
    2. The ggplot build process:
        - For categorical variables, injects manual color/fill scales using the palette.
        - For continuous variables, injects gradient scales using either:
            - the min/max colors from the provided `cmap`.
            - contrasting pair from the palette (if no cmap is provided) as a fallback

    Parameters
    ----------
    palette : Union[List[str], str, Cycler]
        A list of hexadecimal color codes, a single hex string, or a Matplotlib Cycler.

    cmap : matplotlib.colors.Colormap, optional
        A Matplotlib colormap. If provided, it is used to define the gradient range
        for continuous color/fill mappings, based on `cmap(0.0)` and `cmap(1.0)`.
    """
    palette = _format_palette(palette)

    _patch_geom_default_color(palette)

    _patch_build_method(palette, cmap)
