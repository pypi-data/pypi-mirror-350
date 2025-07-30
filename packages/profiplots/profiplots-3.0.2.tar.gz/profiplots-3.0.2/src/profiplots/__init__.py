"""
`profiplots` package enables us to use profinit plot styling in:

- `seaborn`,
- `matplotlib`.

The main function of this package is `set_theme`. It replaces default seaborn and matplotlib styling with our custom, Profinit styling. To try it out, just call:

```python
import profiplots as pf
pf.set_theme()
```

Now all `matplotlib` and `seaborn` plots will have our Profinit theme. These plots can be further customized. This is handled by submodules. Check out packages (and modules) `profiplots.style` and `profiplots.profile`. For even better control, we can use `profiplots.colors` to create perfectly colored plots.

"""

import contextlib
import warnings

import matplotlib as _mpl
import matplotlib.pyplot as _plt
import seaborn.objects as _so

from profiplots import color, profile, settings, style, theme
from profiplots._patch import apply_patch, reset_patch

__all__ = ["reset_theme", "set_theme", "set_style", "style_context", "style", "profile", "color", "settings", "theme"]
_pn_patch_enabled = False

with contextlib.suppress(ImportError):
    import plotnine as _pn
    globals()["_original_ggplot"] = _pn.ggplot


with contextlib.suppress(ImportError):
    import plotnine as _pn

# register colormaps
_mpl.colormaps.register(color.WHITE_GREY_CMAP, force=True)
_mpl.colormaps.register(color.WHITE_GREY_CMAP.reversed(), force=True)
_mpl.colormaps.register(color.GREY_CMAP, force=True)
_mpl.colormaps.register(color.GREY_CMAP.reversed(), force=True)
_mpl.colormaps.register(color.WHITE_BLUE_CMAP, force=True)
_mpl.colormaps.register(color.WHITE_BLUE_CMAP.reversed(), force=True)
_mpl.colormaps.register(color.BLUE_CMAP, force=True)
_mpl.colormaps.register(color.BLUE_CMAP.reversed(), force=True)
_mpl.colormaps.register(color.WHITE_RED_CMAP, force=True)
_mpl.colormaps.register(color.WHITE_RED_CMAP.reversed(), force=True)
_mpl.colormaps.register(color.RED_CMAP, force=True)
_mpl.colormaps.register(color.RED_CMAP.reversed(), force=True)
_mpl.colormaps.register(color.BLUE_WHITE_RED_CMAP, force=True)
_mpl.colormaps.register(color.BLUE_WHITE_RED_CMAP.reversed(), force=True)
_mpl.colormaps.register(color.BLUE_RED_CMAP, force=True)
_mpl.colormaps.register(color.BLUE_RED_CMAP.reversed(), force=True)

_orig_rc_config = _mpl.rcParams.copy()
"""Original rc settings before calling the first `set_theme`."""

if "_pn" in globals():
    _orig_plotnine_theme = _pn.theme_get()
    """Original plotnine theme."""

class _RCAesthetics:
    """ """
    def __init__(self, **kwargs):
        self.config = kwargs

    def __enter__(self):
        self._orig = _mpl.rcParams.copy()
        _mpl.rcParams.update(self.config)
        _so.Plot.config.theme.update(self.config)

    def __exit__(self, exc_type, exc_value, exc_tb):
        _so.Plot.config.theme.update(self._orig)
        _mpl.rcParams.update(self._orig)


def set_theme(name: str = "default", experimental = False):
    """Calling this function will set `profiplots` styling as the default styling for `matplotlib` and `seaborn` plots.

    Their corresponding values can be found in `profiplots.color`.
    This function must be called before calling additional styling functions, like `colored`, `grid` etc.

    Parameters
    ----------
    name: str
        Name of the theme.

    Examples
    -------
    ::: {.panel-tabset}
    ### Seaborn Objects

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    data = sns.load_dataset("titanic")
    ```

    **No theme set**
    ```{python}
    (
        so.Plot(data=data, x="sex", y="survived")
        .add(so.Bar(), so.Agg())
        .label(title="Survival rate of titanic female passengers was significantly higher than male passengers")
    )
    ```
    ### Plotnine

    ```{python}
    #| echo: false
    import numpy as np
    import plotnine as pn
    ```

    ```{python}
    plot = (
        pn.ggplot(data, pn.aes(x='sex', y='survived'))
        + pn.stat_summary(geom='bar', fun_y=np.mean)
        + pn.labs(
            title="Survival rate of Titanic female passengers was significantly higher than male passengers",
            x="Sex",
            y="Survival Rate"
        )
    )
    plot
    ```
    :::

    **Profiplots theme**

    ::: {.panel-tabset}
    ### Seaborn Objects

    ```{python}
    import profiplots as pf

    # set theme
    pf.set_theme(name="default")

    (
        so.Plot(data=data, x="sex", y="survived")
        .add(so.Bar(), so.Agg())
        .label(title="Survival rate of titanic female passengers was significantly higher than male passengers")
    )
    ```

    ### Plotnine

    ```{python}
    import profiplots as pf

    # set theme
    pf.set_theme(experimental=True)

    plot = (
        pn.ggplot(data, pn.aes(x='sex', y='survived'))
        + pn.stat_summary(geom='bar', fun_y=np.mean)
        + pn.labs(
            title="Survival rate of Titanic female passengers was significantly higher than male passengers",
            x="Sex",
            y="Survival Rate"
        )
    )
    plot
    ```
    :::
    """
    if name not in settings.SUPPORTED_THEMES:
        raise ValueError(f"Theme with name '{name}' is not supported.")

    # reset theme before setting up the new one
    reset_theme()

    # set up global themes
    _plt.style.use(f"profiplots.theme.{name}")
    _so.Plot.config.theme.update(_mpl.rcParams)
    if "_pn" in globals():
        _pn.theme_set(theme._theme_profiplots())

        if(experimental):
            globals()["_pn_patch_enabled"] = True
            warnings.warn(
                "Temporary solution."
                "Monkey patching is enabled: overriding default color behavior in plotnine to include profinit palette htough overriding build function of the ggplot object.",
                UserWarning, stacklevel=2
            )

            cmap = _plt.get_cmap(_plt.rcParams["image.cmap"]) if _plt.rcParams["image.cmap"] else None

            apply_patch(_plt.rcParams["axes.prop_cycle"], cmap)

    settings.active_theme = name


def reset_theme():
    """Reset theme to previous defaults."""
    _mpl.rcParams.update(_orig_rc_config)
    _so.Plot.config.theme.update(_orig_rc_config)
    if "_pn" in globals():
        _pn.theme_set(_orig_plotnine_theme)

        globals()["_pn_patch_enabled"] = False
        reset_patch()

    settings.active_theme = None


def style_context(rc_config: dict):
    """Alters default Profinit theme with new settings in a context window. Works both for `matplotlib` and `seaborn` (and `seaborn.objects.Plot`).

    Use this method instead of [mpl.rc_context](https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rc_context).

    Parameters
    ----------
    rc_config : dict
        rc config values (for seaborn / matplotlib) to be set for the duration of the context window.

    Examples
    -------

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    import plotnine as pn
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(experimental=True)
    ```

    First let's look at what happens **inside** of the style context.

    ::: {.panel-tabset}

    ### Seaborn Objects
    ```{python}
    # Inside style context
    with pf.style_context(pf.style.grid(x=True, y=True)):
        p = (
            so.Plot(data=data, x="age", y="fare")
            .add(so.Dots())
            .label(title="Title example")
            .plot()
        )
    p
    ```
    ### Plotnine
    ```{python}
    with pf.style_context(pf.style.grid(x=True, y=True)):
        p = (
            pn.ggplot(data=data, mapping=pn.aes(x="age", y="fare"))
            + pn.geom_point()
            + pn.labs(title="Title example")
        )
    p
    ```

    :::
    And now **outside** the default styles are being used..

    ::: {.panel-tabset}
    ### Seaborn Objects

    ```{python}
    # Inside style context
    p = (
        so.Plot(data=data, x="age", y="fare")
        .add(so.Dots())
        .label(title="Title example")
        .plot()
    )
    p
    ```
    ### Plotnine
    ```{python}
    p = (
        pn.ggplot(data=data, mapping=pn.aes(x="age", y="fare"))
        + pn.geom_point()
        + pn.labs(title="Title example")
    )
    p
    ```
    :::
    """
    return _RCAesthetics(**rc_config)


def set_style(styles: dict, plotnine: bool = False):
    """Sets up the specific style permanently.

    Parameters
    ----------
    styles : dict
        style config values to be set. Either rc config or plotnine.
    plotnine : bool
        If True, then sets styles for plotnine.

    Examples
    -------
    ::: {.panel-tabset}

    ### Seaborn Objects
    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(name="default")
    ```

    ```{python}
    # set styles
    pf.set_style(pf.style.colored())

    (
        so.Plot(data=data, x="age", y="fare", color="sex")
        .add(so.Dots())
    )
    ```
    ### Plotnine

    ```{python}
    #| echo: false
    import plotnine as pn

    data = sns.load_dataset("titanic")
    pf.set_theme(experimental=True)
    ```

    ```{python}
    # set styles
    pf.set_style(pf.style.colored(), plotnine=True)

    p = (
        pn.ggplot(data=data, mapping=pn.aes(x="age", y="fare", color="sex"))
        + pn.geom_point()
    )
    p
    ```
    :::
    """
    if not plotnine:
        _plt.rcParams.update(**styles)
        _so.Plot.config.theme.update(_mpl.rcParams)
        return

    if _pn_patch_enabled:
        _pn.ggplot = globals()["_original_ggplot"]
        prop_cycle = styles.get("axes.prop_cycle")

        cmap = _plt.get_cmap(styles["image.cmap"]) if styles.get("image.cmap") else None

        if prop_cycle:
            apply_patch(prop_cycle, cmap)

    # remove unsupported keys for plotnine connected to palette
    for key in ("axes.prop_cycle", "image.cmap"):
        styles.pop(key, None)

    _pn.theme_update(**styles)
