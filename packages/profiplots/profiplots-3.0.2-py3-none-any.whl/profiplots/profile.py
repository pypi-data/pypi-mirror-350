"""
This module contains implementation of profiles. Profiles is a combination of multiple settings made for a specific purpose. For example profile `exploration` was made to allow quick data exploration.
"""


from profiplots import settings as _settings
from profiplots import theme as _theme

__all__ = [
    "exploration",
    "publish",
    "presentation"
]


def exploration() -> dict:
    """Profile whose purpose is to be used for exploratory analysis.

    Returns
    -------
    dict
        Matplotlib rc settings.

    Examples
    -------

    ```{python}
    import seaborn.objects as so
    import seaborn as sns
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(name="default")

    (
        so.Plot(data=data, x="age", y="fare")
        .theme(pf.profile.exploration())
        .add(so.Dots())
        .label(title="Passenger's Age vs Fare")
    )
    ```

    """
    return _theme.EXPLORATION_PROFILE[_settings.active_theme]


def publish() -> dict:
    """Use this profile for final visualizations that we want to publish. It has a very clean look.

    Returns
    -------
    dict
        Matplotlib rc settings.

    Examples
    -------

    ```{python}
    import seaborn.objects as so
    import seaborn as sns
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(name="default")

    (
        so.Plot(data=data, x="age", y="fare")
        .theme(pf.profile.publish())
        .add(so.Dots())
        .label(title="Passenger's Age vs Fare")
    )
    ```

    """
    return _theme.PUBLISH_PROFILE[_settings.active_theme]

def presentation() -> dict:
    """Use this profile for presentation. The plot components are adjusted to be visible with a slide projector.

    Returns
    -------
    dict
        Matplotlib rc settings.

    Examples
    -------

    ```{python}
    import seaborn.objects as so
    import seaborn as sns
    import profiplots as pf

    data = sns.load_dataset("titanic")
    pf.set_theme(name="default")

    (
        so.Plot(data=data, x="age", y="fare")
        .theme(pf.profile.presentation())
        .add(so.Dots())
        .label(title="Passenger's Age vs Fare")
    )
    ```

    """
    return _theme.PRESENTATION_PROFILE[_settings.active_theme]
