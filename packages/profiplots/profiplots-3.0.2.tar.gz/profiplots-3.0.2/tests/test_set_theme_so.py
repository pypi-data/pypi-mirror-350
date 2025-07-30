import matplotlib
import profiplots as pf
import seaborn as sns
import seaborn.objects as so


def _get_plot_colors(fig):
    colors_in_plot = set()
    for ax in fig.axes:
        for coll in ax.collections:
            colors = coll.get_facecolors()
            for color in colors:
                rgba = tuple(color)
                hex_color = matplotlib.colors.to_hex(rgba)
                colors_in_plot.add(hex_color)

    return colors_in_plot


def test_theme_set_doesnt_throw():
    pf.set_theme()
    pf.set_style(pf.style.colored())


def test_greyscale_theme_works():
    data = sns.load_dataset("titanic")

    pf.set_theme()
    pf.set_style(pf.style.greyscale())

    plot = so.Plot(data=data, x="age", y="fare", color="sex").add(so.Dot()).plot()

    fig = plot._figure
    colors_in_plot = _get_plot_colors(fig)
    profi_greys_hex = pf.color.GREYS

    assert colors_in_plot.issubset(
        profi_greys_hex
    ), f"Non-gray colors found in plot: {colors_in_plot - profi_greys_hex}"

    assert len(colors_in_plot) == 2, "There are two sexes, should be two colors"


def test_greyscale_theme_overwritable():
    data = sns.load_dataset("titanic")

    pf.set_theme()
    pf.set_style(pf.style.greyscale())

    plot = (
        so.Plot(data=data, x="age", y="fare", color="sex")
        .scale(color={"female": pf.color.RED, "male": pf.color.BLUE})
        .add(so.Dot())
        .plot()
    )

    fig = plot._figure
    colors_in_plot = _get_plot_colors(fig)
    profi_red_blue_hex = [pf.color.BLUE.lower(), pf.color.RED.lower()]

    assert colors_in_plot.issubset(
        profi_red_blue_hex
    ), f"Non-red-blue colors found in plot: {colors_in_plot - profi_red_blue_hex}"

    assert set(profi_red_blue_hex).issubset(
        colors_in_plot
    ), f"Both red and blue should be in the plot: {colors_in_plot - profi_red_blue_hex}"


def test_reset_theme():
    data = sns.load_dataset("titanic")

    pf.set_theme()
    pf.set_style(pf.style.greyscale())
    pf.reset_theme()

    plot = so.Plot(data=data, x="age", y="fare", color="sex").add(so.Dot()).plot()

    fig = plot._figure
    colors_in_plot = _get_plot_colors(fig)

    assert not any(
        color in colors_in_plot for color in pf.color.GREYS
    ), "Plot contains colors from the GREYS theme after reset. Should be back to matplotlib defaul colors."
