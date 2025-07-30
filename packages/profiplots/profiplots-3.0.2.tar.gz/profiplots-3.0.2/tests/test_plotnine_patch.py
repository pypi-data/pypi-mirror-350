import matplotlib
import plotnine as pn
import profiplots as pf
import seaborn as sns
from profiplots._patch import apply_patch


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


def test_default_geom_colors_overriden():
    data = sns.load_dataset("titanic")

    palette = [pf.color.BLUE, pf.color.YELLOW]

    apply_patch(palette)

    plot = pn.ggplot(data, pn.aes(x="age", y="fare")) + pn.geom_point()

    colors_in_plot = _get_plot_colors(plot.draw())

    assert len(colors_in_plot) == 1, "Only the first color inside of our palette should be present."
    assert palette[0].lower() in colors_in_plot, "Only the first color inside of our palette should be present."


def test_profiplots_geom_color_overwritable():
    data = sns.load_dataset("titanic")

    palette = [pf.color.BLUE, pf.color.YELLOW]
    apply_patch(palette)

    plot = pn.ggplot(data, pn.aes(x="age", y="fare")) + pn.geom_point(color=pf.color.RED, fill=pf.color.RED)

    colors_in_plot = _get_plot_colors(plot.draw())

    assert len(colors_in_plot) == 1, "Only the first color inside of our palette should be present."
    assert pf.color.RED.lower() in colors_in_plot, "Only the first color inside of our palette should be present."


def test_aestethic_mapped_correctly_to_profiplots_theme():
    data = sns.load_dataset("titanic")

    palette = [pf.color.BLUE, pf.color.YELLOW]

    apply_patch(palette)

    plot = pn.ggplot(data, pn.aes(x="age", y="fare", fill="sex", color="sex")) + pn.geom_point()

    colors_in_plot = _get_plot_colors(plot.draw())

    assert len(colors_in_plot) == 2, "Only colors from of our palette should be present."
    assert palette[0].lower() in colors_in_plot, "Both colors from our our palette should be present."
    assert palette[1].lower() in colors_in_plot, "Both colors from our our palette should be present."


def test_aestethic_mapped_profiplots_colors_overwritable():
    data = sns.load_dataset("titanic")

    palette = [pf.color.BLUE, pf.color.YELLOW]

    apply_patch(palette)

    plot = (
        pn.ggplot(data, pn.aes(x="age", y="fare", fill="sex", color="sex"))
        + pn.scale_color_manual(values=[pf.color.AZURE, pf.color.PURPLE])
        + pn.scale_fill_manual(values=[pf.color.AZURE, pf.color.PURPLE])
        + pn.geom_point()
    )

    colors_in_plot = _get_plot_colors(plot.draw())

    assert len(colors_in_plot) == 2, "Only colors from of our palette should be present."
    assert pf.color.AZURE.lower() in colors_in_plot, "Both colors from our our palette should be present."
    assert pf.color.PURPLE.lower() in colors_in_plot, "Both colors from our our palette should be present."


def test_ignores_continuous_arestethic():
    data = sns.load_dataset("titanic")

    data["age_sq"] = data["age"] * data["age"]

    palette = [pf.color.BLUE, pf.color.YELLOW]

    apply_patch(palette)

    plot = pn.ggplot(data, pn.aes(x="age", y="fare", fill="age_sq", color="age_sq")) + pn.geom_point()

    colors_in_plot = _get_plot_colors(plot.draw())

    assert len(colors_in_plot) > 2, "For continuous variable a spectrum should be mapped onto the aestethic."
    assert pf.color.AZURE.lower() not in colors_in_plot, "Both colors from our our palette should be present."
    assert pf.color.PURPLE.lower() not in colors_in_plot, "Both colors from our our palette should be present."


def test_handles_local_aestethic():
    data = sns.load_dataset("titanic")

    palette = [pf.color.BLUE, pf.color.YELLOW]

    apply_patch(palette)

    plot = pn.ggplot(data, pn.aes(x="age", y="fare")) + pn.geom_point(pn.aes(color="sex", fill="sex"))

    colors_in_plot = _get_plot_colors(plot.draw())

    assert len(colors_in_plot) == 2, "For continuous variable a spectrum should be mapped onto the aestethic."
    assert pf.color.BLUE.lower() in colors_in_plot, "Both colors from our our palette should be present."
    assert pf.color.YELLOW.lower() in colors_in_plot, "Both colors from our our palette should be present."


def test_plotnine_patching_e2e():
    data = sns.load_dataset("titanic")

    pf.set_theme(experimental=True)
    pf.set_style(pf.style.greyscale(), plotnine=True)

    plot = pn.ggplot(data, pn.aes(x="age", y="fare", fill="sex", color="sex")) + pn.geom_point()

    colors_in_plot = _get_plot_colors(plot.draw())

    profi_greys_hex = pf.color.GREYS

    assert colors_in_plot.issubset(
        [color.lower() for color in profi_greys_hex]
    ), f"Non-gray colors found in plot: {colors_in_plot - profi_greys_hex}"

    assert len(colors_in_plot) == 2, "There are two sexes, should be two colors"


def test_plotnine_patching_colored_style_e2e():
    data = sns.load_dataset("titanic")

    pf.set_theme(experimental=True)
    pf.set_style(pf.style.colored(), plotnine=True)

    plot = pn.ggplot(data, pn.aes(x="age", y="fare", fill="sex", color="sex")) + pn.geom_point()

    colors_in_plot = _get_plot_colors(plot.draw())

    profi_colors = [pf.color.BLUE, pf.color.RED]

    assert colors_in_plot.issubset(
        [color.lower() for color in profi_colors]
    ), f"Non-gray colors found in plot: {colors_in_plot - profi_colors}"

    assert len(colors_in_plot) == 2, "There are two sexes, should be two colors"


def test_reset_style():
    data = sns.load_dataset("titanic")

    pf.set_theme(experimental=True)
    pf.set_style(pf.style.greyscale(), plotnine=True)
    pf.reset_theme()

    plot = pn.ggplot(data, pn.aes(x="age", y="fare", fill="sex", color="sex")) + pn.geom_point()

    colors_in_plot = _get_plot_colors(plot.draw())
    assert not any(
        color in colors_in_plot for color in pf.color.GREYS
    ), "Plot contains colors from the GREYS theme after reset. Should be back to matplotlib defaul colors."


def test_does_not_fall_on_colorless_theme():
    pf.set_theme(experimental=True)
    pf.set_style(pf.style.grid(), plotnine=True)
