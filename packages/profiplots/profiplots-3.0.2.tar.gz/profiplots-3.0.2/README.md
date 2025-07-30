# profiplots

Make Matplotlib and Seaborn plots with Profinit theme!

- Documentation: https://datascience.profinitservices.cz/sablony/profiplots/.

## Installation

```sh
python -m pip install profiplots
```

## Usage

```python
import profiplots as pf
import seaborn as sns
import seaborn.objects as so

# set theme
pf.set_theme()

# create a basic plot
dataset = sns.load_dataset("titanic")
(
    so.Plot(data=dataset, x="survived", y="sex")
    .add(so.Bar(alpha=1), so.Agg(), legend=False)
    .label(title="Female passengers survived much more frequently", x="Survival Rate", y="Sex")
    .save("my_first_plot.png")
)
```
