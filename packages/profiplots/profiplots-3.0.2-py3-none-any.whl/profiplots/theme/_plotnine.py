import matplotlib as mpl
from plotnine import element_blank, element_line, element_rect, element_text
from plotnine.options import get_option
from plotnine.themes import theme


class theme_profiplots(theme):
    """
    Profiplots theme that is set based on parameters configured in `mpl.rcParams`
    and other defaults.
    """
    def __init__(
        self,
    ):
        rcparams = mpl.rcParams
        base_size = rcparams["font.size"]
        half_line = base_size / 2
        line_margin = half_line * 0.8 / 2
        m = get_option("base_margin")

        super().__init__(
            aspect_ratio=get_option("aspect_ratio"),
            dpi=get_option("dpi"),
            figure_size=get_option("figure_size"),
            text=element_text(size=base_size, rotation=0, margin={}),
            axis_text=element_text(
                size=base_size * 0.8,
                margin={
                    "t": line_margin,
                    "b": line_margin,
                    "l": line_margin,
                    "r": line_margin,
                    "units": "pt",
                },
            ),
            axis_title_x=element_text(
                va="bottom", margin={"t": m, "units": "fig"}
            ),
            axis_title_y=element_text(
                angle=90,
                va="center",
                margin={"r": m, "units": "fig"},
            ),
            legend_box_margin=3,
            legend_box_spacing=m * 3,  # figure units
            legend_key_spacing_x=6,
            legend_key_spacing_y=2,
            legend_key_size=base_size * 0.8 * 1.8,
            legend_frame=element_blank(),
            legend_background=element_rect(color="#BEBEBE", fill="#FFFFFF"),
            legend_ticks_length=0.2,
            legend_margin=0,
            legend_position="right",
            legend_spacing=10,  # points
            legend_text=element_text(
                margin={
                    "t": m / 1.5,
                    "b": m / 1.5,
                    "l": m / 1.5,
                    "r": m / 1.5,
                    "units": "fig",
                },
                color="#696969",
                va="center",
                size=base_size * 0.8
            ),
            legend_ticks=element_line(color="#CCCCCC", size=1),
            legend_title=element_text(
                margin={
                    "t": m / 2,
                    "b": m * 1.5,
                    "l": m * 2,
                    "r": m * 2,
                    "units": "fig",
                },
                ha="center",
                size=base_size * 0.8
            ),
            panel_spacing=m,
            plot_caption=element_text(
                size=base_size * 0.8,
                ha="right",
                va="bottom",
                ma="left",
                margin={"t": m, "units": "fig"},
            ),
            plot_margin=m,
            plot_subtitle=element_text(
                size=base_size * 1,
                va="top",
                ma="left",
                ha="left",
                margin={"b": m, "units": "fig"},
                color="#282828"
            ),
            plot_title=element_text(
                size=base_size * 1.2,
                va="top",
                ma="left",
                ha="left",
                margin={"b": m, "units": "fig"},
                color="#282828"
            ),
            strip_align=0,
            strip_background=element_blank(),
            strip_text=element_text(
                size=base_size * 0.9,
                linespacing=1.0,
                margin={
                    "t": 1 / 3,
                    "b": 1 / 3,
                    "l": 1 / 3,
                    "r": 1 / 3,
                    "units": "lines",
                },
            ),
            strip_text_y=element_text(rotation=-90),
            complete=True
        )

        self._rcParams.update(rcparams)
