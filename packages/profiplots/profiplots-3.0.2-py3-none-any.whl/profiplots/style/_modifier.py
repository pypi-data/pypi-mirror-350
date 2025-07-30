import contextlib

from profiplots import settings, theme
from profiplots.style import _utils

with contextlib.suppress(ImportError):
    import plotnine as pn


def colored() -> dict:
    """Changes color cycle to a colored type.

    ::: {.callout-important}

    This style is more-or-less for explorations. Finaliz visualizations should have all colors specified manually.

    :::

    ::: {.callout-warning}
    This option is not supported by plotnine.
    :::

    Returns
    -------
    dict
        Dictionary containing the changed color cycle.

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
    (
        so.Plot(data=data, x="sex", y="survived", color="embark_town")
        .theme(pf.style.colored())
        .add(so.Bar(alpha=1), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```

    ### Plotnine

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    import plotnine as pn
    import numpy as np

    data = sns.load_dataset("titanic").dropna(subset=['sex', 'survived', 'embark_town'])
    pf.set_theme(experimental=True)
    ```

    ```{python}
    pf.set_style(pf.style.colored(), plotnine=True)
    plot = (
        pn.ggplot(data, pn.aes(x='sex', y='survived', fill='embark_town'))
        + pn.stat_summary(
            fun_y=np.mean,
            geom='bar',
            position=pn.position_dodge(),
        )
        + pn.labs(
            title='Survival Rate of Various Groups of Passengers',
            x='Sex',
            y='Survival Rate'
        )
        + pn.scale_y_continuous(labels=lambda l: [f'{v:.0%}' for v in l])
    )
    plot
    ```

    :::

    """
    _utils.validate_active_style()

    return {"axes.prop_cycle": theme.COLOR_CYCLER[settings.active_theme], "image.cmap": "pf_blue_white_red"}


def grey() -> dict:
    """Changes color cycle to a grey type (no colors).

    Returns
    -------
    dict
        RC Dictionary containing the changed color cycle.

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
    (
        so.Plot(data=data, x="sex", y="survived")
        .theme(pf.style.grey())
        .add(so.Bar(), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```
    ### Plotnine

    ```{python}
    #| echo: false
    import numpy as np
    import seaborn as sns
    import plotnine as pn
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(experimental=True)
    ```

    ```{python}
    pf.set_style(pf.style.grey())

    plot = (
        pn.ggplot(data, pn.aes(x='sex', y='survived'))
        + pn.stat_summary(
            fun_y=np.mean,
            geom='bar',
            position=pn.position_dodge(),
        )
        + pn.labs(
            title='Survival Rate of Various Groups of Passengers',
            x='Sex',
            y='Survival Rate'
        )
        + pn.scale_y_continuous(labels=lambda l: [f'{v:.0%}' for v in l])
    )
    plot
    ```

    :::
    """
    _utils.validate_active_style()

    return {"axes.prop_cycle": theme.GREY_CYCLER[settings.active_theme], "image.cmap": "pf_grey"}

def greyscale() -> dict:
    """Changes color cycle to a greyscale. Unlike `grey` style, it uses multiple shades of grey.

    ::: {.callout-warning}
    This style is not supported by plotnine.
    :::

    Returns
    -------
    dict
        RC Dictionary containing the changed color cycle.

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
    (
        so.Plot(data=data, x="sex", y="survived", color="embark_town")
        .theme(pf.style.greyscale())
        .add(so.Bar(alpha=1), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```

    ### Plotnine

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    import plotnine as pn
    import numpy as np

    data = sns.load_dataset("titanic").dropna(subset=['sex', 'survived', 'embark_town'])
    pf.set_theme(experimental=True)
    ```

    ```{python}
    pf.set_style(pf.style.greyscale(), plotnine=True)
    plot = (
        pn.ggplot(data, pn.aes(x='sex', y='survived', fill='embark_town'))
        + pn.stat_summary(
            fun_y=np.mean,
            geom='bar',
            position=pn.position_dodge(),
        )
        + pn.labs(
            title='Survival Rate of Various Groups of Passengers',
            x='Sex',
            y='Survival Rate'
        )
        + pn.scale_y_continuous(labels=lambda l: [f'{v:.0%}' for v in l])
    )
    plot
    ```

    :::
    """
    _utils.validate_active_style()

    return {"axes.prop_cycle": theme.GREYSCALE_CYCLER[settings.active_theme], "image.cmap": "pf_grey"}

def bluescale() -> dict:
    """Changes color cycle to a bluescale.

    ::: {.callout-warning}
    This style is not supported by plotnine.
    :::

    Returns
    -------
    dict
        RC Dictionary containing the changed color cycle.

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
    (
        so.Plot(data=data, x="sex", y="survived", color="embark_town")
        .theme(pf.style.bluescale())
        .add(so.Bar(alpha=1), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```

    ### Plotnine

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    import plotnine as pn
    import numpy as np

    data = sns.load_dataset("titanic").dropna(subset=['sex', 'survived', 'embark_town'])
    pf.set_theme(experimental=True)
    ```

    ```{python}
    pf.set_style(pf.style.bluescale(), plotnine=True)
    plot = (
        pn.ggplot(data, pn.aes(x='sex', y='survived', fill='embark_town'))
        + pn.stat_summary(
            fun_y=np.mean,
            geom='bar',
            position=pn.position_dodge(),
        )
        + pn.labs(
            title='Survival Rate of Various Groups of Passengers',
            x='Sex',
            y='Survival Rate'
        )
        + pn.scale_y_continuous(labels=lambda l: [f'{v:.0%}' for v in l])
    )
    plot
    ```

    :::
    """
    _utils.validate_active_style()

    return {"axes.prop_cycle": theme.BLUESCALE_CYCLER[settings.active_theme], "image.cmap": "pf_blue"}


def grid(x: bool | None = None, y: bool | None = None, plotnine: bool = False) -> dict:
    """Shows or hides grid in the image.

    Parameters
    ----------
    x : bool | None
        If True, then shows X grid. If False, hides it. If None, does nothing. Defaults to None.
    y : bool | None
        If True, then shows Y grid. If False, hides it. If None, does nothing. Defaults to None.
    plotnine : bool
        Get the styles for plotnine.

    Returns
    -------
    dict
        Dictionary containing the new grid configuration.

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
    (
        so.Plot(data=data, x="age", y="fare")
        .theme(pf.style.grid(x=True, y=True))
        .add(so.Dots())
        .label(title="Dependency between Age and Fare of Titanic passengers")
    )
    ```

    ### Plotnine

    ```{python}
    #| echo: false
    import plotnine as pn
    import seaborn as sns
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(experimental=True)
    ```

    ```{python}
    pf.set_style(pf.style.grid(x=True, y=True, plotnine=True), plotnine=True)

    (
        pn.ggplot(data=data, mapping=pn.aes(x="age", y="fare"))
        + pn.geom_point()
        + pn.labs(title="Dependency between Age and Fare of Titanic passengers")
    )
    ```

    :::
    """
    _utils.validate_active_style()

    styles = {}

    if plotnine:
        if x is not None:
            styles["panel_grid"] = pn.element_line()
            styles["panel_grid_major_x"] = pn.element_line() if x is True else pn.element_blank()
            styles["panel_grid_minor_x"] = pn.element_line() if x is True else pn.element_blank()
        if y is not None:
            styles["panel_grid"] = pn.element_line()
            styles["panel_grid_major_y"] = pn.element_line() if y is True else pn.element_blank()
            styles["panel_grid_minor_y"] = pn.element_line() if x is True else pn.element_blank()
    elif x is True and y is True:
        styles["axes.grid"] = True
        styles["axes.grid.axis"] = "both"
    elif x is True:  # and y is False or None
        styles["axes.grid"] = True
        styles["axes.grid.axis"] = "x"
    elif y is True:  # and x is False or None
        styles["axes.grid"] = True
        styles["axes.grid.axis"] = "y"
    elif x is False and y is False:
        styles["axes.grid"] = False
    else:
        # both are None => nothing changes
        pass

    return styles


def ticks(x: bool | None = None, y: bool | None = None, plotnine: bool = False) -> dict:
    """Returns configuration of the plots that shows or hides ticks on x or y axis.

    Parameters
    ----------
    x : bool | None
        If True, then x axis ticks are shown. If False, they are hidden. If None, does nothing. Defaults to None.
    y : bool | None
        If True, then y axis ticks are shown. If False, they are hidden. If None, does nothing. Defaults to None.
    plotnine : bool
        Get the styles for plotnine.

    Returns
    -------
    dict
        Configuration of the plots that shows or hides ticks when applied.

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
    (
        so.Plot(data=data, x="age", y="fare")
        .theme(pf.style.ticks(x=False, y=False))
        .add(so.Dots())
        .label(title="Dependency between Age and Fare.")
    )
    ```


    ### Plotnine

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import plotnine as pn
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(experimental=True)
    ```

    ```{python}
    pf.set_style(pf.style.ticks(x=False, y=False, plotnine=True), plotnine=True)
    (
        pn.ggplot(data=data, mapping=pn.aes(x="age", y="fare"))
        + pn.geom_point()
        + pn.labs(title="Dependency between Age and Fare.")
    )
    ```

    :::
    """
    _utils.validate_active_style()

    styles = {}

    if plotnine:
        if x is not None:
            styles["axis_ticks"] = pn.element_line()
            styles["axis_ticks_x"] = pn.element_line() if x is True else pn.element_blank()
        if y is not None:
            styles["axis_ticks"] = pn.element_line()
            styles["axis_ticks_y"] = pn.element_line() if y is True else pn.element_blank()
    else:
        if x is not None:
            styles.update({"xtick.top": False, "xtick.bottom": x, "xtick.labeltop": False, "xtick.labelbottom": x})
        if y is not None:
            styles.update({"ytick.right": False, "ytick.left": y, "ytick.labelright": False, "ytick.labelleft": y})

    return styles


def spines(
    left: bool | None = None, right: bool | None = None, top: bool | None = None, bottom: bool | None = None, plotnine: bool = False
) -> dict:
    """Adds or removes borders of the plots.

    Parameters
    ----------
    left : bool | None
        If True, then the left spine is added. If False, it is remoted. If None, nothing is altered. Defaults to None.
    right : bool | None
        If True, then the right spine is added. If False, it is remoted. If None, nothing is altered.. Defaults to None.
    top : bool | None
        If True, then the top spine is added. If False, it is remoted. If None, nothing is altered.. Defaults to None.
    bottom : bool | None
        If True, then the bottom spine is added. If False, it is remoted. If None, nothing is altered.. Defaults to None.
    plotnine : bool
        If True, then returns styling for plotnine.

    Returns
    -------
    dict
        Configuration of the spines.

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
    (
        so.Plot(data=data, x="survived", y="sex")
        .theme(pf.style.spines(left=True, right=True, top=True, bottom=True))
        .add(so.Bar(), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```

    ### Plotnine

    ```{python}
    #| echo: false
    import plotnine as pn
    import numpy as np
    import seaborn as sns
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(experimental=True)
    ```

    ```{python}
    pf.set_style(pf.style.spines(left=True, right=True, top=True, bottom=True))
    (
        pn.ggplot(data=data, mapping=pn.aes(x="sex", y="survived"))
        + pn.stat_summary(
            fun_y=np.mean,
            geom='bar',
            position=pn.position_dodge()
        )
        + pn.labs(title="Survival of various groups of passengers")
        + pn.coord_flip()
    )
    ```
    :::
    """
    _utils.validate_active_style()

    styles = {}

    if plotnine:
        if top is True or right is True:
            raise NotImplementedError("'top' and 'right' are unsupported for plotnine.")
        if bottom is not None:
            styles["axis_line_x"] = pn.element_line() if bottom is True else pn.element_blank()
        if left is not None:
            styles["axis_line_y"] = pn.element_line() if left is True else pn.element_blank()
    else:
        if left is not None:
            styles["axes.spines.left"] = left
        if right is not None:
            styles["axes.spines.right"] = right
        if top is not None:
            styles["axes.spines.top"] = top
        if bottom is not None:
            styles["axes.spines.bottom"] = bottom

    return styles
