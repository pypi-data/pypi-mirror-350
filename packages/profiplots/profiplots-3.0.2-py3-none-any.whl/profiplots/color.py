"""
This module contains all colors and cmaps. They can be used directly when plotting, or in case of a cmap, we can use its string alias. The available cmap aliases are:

- `pf_grey`, `pf_white_grey`,
- `pf_blue`, `pf_white_blue`,
- `pf_red`, `pf_white_red`,
- `pf_blue_white_red`.

We can also use their reversed variant with sufix `_r`, such as `pf_grey_r`.

Examples
--------

```{python}
#| echo: false
import numpy as np
import seaborn.objects as so
import seaborn as sns
import plotnine as pn
import profiplots as pf

data = sns.load_dataset("titanic")
pf.set_theme(name="default")
```

::: {.panel-tabset}

### Seaborn objects

::: {.panel-tabset}

#### Discrete

```{python}
(
    so.Plot(data=data, x="sex", y="survived")
    .add(so.Bar(), so.Agg(), color="sex", legend=False)
    .scale(color={"female": pf.color.RED, "male": pf.color.LIGHT_GREY})  # color mapping
    .label(title="Survival rate of titanic female passengers was significantly higher than male passengers")
)
```

#### Continuous

```{python}
(
    so.Plot(data=data, x="age", y="fare", color="age")
    .add(so.Dots(alpha=1))
    .scale(color="pf_blue")  # specification of cmap
)
```

:::

### Plotnine

::: {.panel-tabset}

#### Discrete

```{python}
plot = (
    pn.ggplot(data=data, mapping=pn.aes(x="sex", y="survived", fill="sex"))
    + pn.stat_summary(geom='bar', fun_y=np.mean)
    + pn.scale_fill_manual(values={"male": pf.color.LIGHT_GREY, "female": pf.color.RED})
    + pn.labs(
        title="Survival rate of Titanic female passengers was significantly higher than male passengers",
        x="Sex",
        y="Survival Rate"
    )
)
plot
```

#### Continuous

```{python}
blues = pf._patch.find_most_contrasting_pair(pf.color.BLUES)
(
    pn.ggplot(data=data, mapping=pn.aes(x="age", y="fare", color="age"))
    + pn.geom_point()
    + pn.scale_color_gradient(high=blues[0], low=blues[1])
)
```
:::

:::
"""

import matplotlib.colors as _colors

BLUE = "#465A9B"
"""
Profinit blue color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.BLUE])
```

"""

RED = "#E63C41"
"""
Profinit red color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.RED])
```

"""

GREY = "#282828"
"""
Profinit grey color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.GREY])
```

"""

PURPLE = "#7D4191"
"""
Profinit purple color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.PURPLE])
```

"""

PINK = "#B5578D"
"""
Profinit pink color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.PINK])
```

"""

YELLOW = "#FFD21E"
"""
Profinit yellow color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.YELLOW])
```

"""

ORANGE = "#F3943B"
"""
Profinit orange color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.ORANGE])
```

"""

GREEN = "#41C34B"
"""
Profinit green color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.GREEN])
```

"""

AZURE = "#3DADE5"
"""
Profinit azure color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.AZURE])
```

"""

WHITE = "#FFFFFF"
"""
Profinit white color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.WHITE])
```

"""

BLACK = "#000000"
"""
Profinit black color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.BLACK])
```

"""


# LIGHT colors
LIGHT_GREY = "#AAAAAA"
"""
Profinit light grey color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.LIGHT_GREY])
```

"""


# DARK colors
DARK_BLUE = "#2B436C"
"""
Profinit dark blue color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.DARK_BLUE])
```

"""

DARK_GREEN = "#007938"
"""
Profinit dark green color from its theme.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette([pf.color.DARK_GREEN])
```

"""

# Multiple shades
BLUES = ["#ECEEF5", "#C7CDE1", "#A2ACCD", "#7D8BB8", BLUE]
"""
List of blue colors. From lightest to darkest.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette(pf.color.BLUES)
```

"""

GREYS = [
    "#D7D7D7",
    LIGHT_GREY,
    "#7D7D7D",
    "#555555",
    GREY
]
"""
List of grey colors. From lightest to darkest.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette(pf.color.GREYS)
```
"""
REDS = ["#F8EBEB", "#EBC3C2", "#DE9B99", "#D17270", RED]
"""
List of red colors. From lightest to darkest.

```{python}
#| echo: false
import seaborn as sns
import profiplots as pf

sns.color_palette(pf.color.REDS)
```
"""

# CMAPs
GREY_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_grey", colors=GREYS)
"""
Colors: Light grey - grey. Also available under "pf_grey".

```{python}
#| echo: false
import profiplots as pf

pf.color.GREY_CMAP
```
"""

WHITE_GREY_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_white_grey", colors=[WHITE, *GREYS])
"""
Colors: White - grey. Also available under "pf_white_grey".

```{python}
#| echo: false
import profiplots as pf

pf.color.WHITE_GREY_CMAP
```
"""

BLUE_RED_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_blue_red", colors=BLUES[::-1] + REDS)
"""
Colors: Blue - Red. Blue is for minimum values and Red is for maximum values. Also available under "pf_blue_red".

```{python}
#| echo: false
import profiplots as pf

pf.color.BLUE_RED_CMAP
```
"""


BLUE_WHITE_RED_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_blue_white_red", colors=BLUES[::-1] + [WHITE] + REDS)
"""
Colors: Blue - White - Red. Blue is for minimum values and Red is for maximum values. Use when both ends of the spectrum have strong semantic meaning. For example where minimum is negative correlation and maximum is positive correlation. Also available under "pf_blue_white_red".

```{python}
#| echo: false
import profiplots as pf

pf.color.BLUE_WHITE_RED_CMAP
```
"""

BLUE_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_blue", colors=BLUES)
"""
Colors: Blue. Light Blue is used for minimum values and darker Blue is for maximum values. Also available under "pf_blue".

```{python}
#| echo: false
import profiplots as pf

pf.color.BLUE_CMAP
```
"""

WHITE_BLUE_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_white_blue", colors=[WHITE, *BLUES])
"""
Colors: White - Blue. White is for minimum values and Blue is for maximum values. Also available under "pf_white_blue".

```{python}
#| echo: false
import profiplots as pf

pf.color.WHITE_BLUE_CMAP
```
"""

RED_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_red", colors=REDS)
"""
Colors: White - Red. Light Red is for minimum values and Red is for maximum values. Also available under "pf_red".

```{python}
#| echo: false
import profiplots as pf

pf.color.RED_CMAP
```
"""

WHITE_RED_CMAP = _colors.LinearSegmentedColormap.from_list(name="pf_white_red", colors=[WHITE, *REDS])
"""
Colors: White - Red. White is for minimum values and Red is for maximum values. Also available under "pf_white_red".

```{python}
#| echo: false
import profiplots as pf

pf.color.WHITE_RED_CMAP
```
"""
