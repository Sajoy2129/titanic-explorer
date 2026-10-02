"""Create charts and save them as PNG files. Each function makes one chart."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save to files only; never open a window

import matplotlib.pyplot as plt  # noqa: E402 (must come after matplotlib.use)
import seaborn as sns  # noqa: E402


def _save(fig, out_dir, filename):
    """Save a figure to out_dir/filename and free its memory."""
    path = Path(out_dir) / filename
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_survival_by_sex(df, out_dir):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x="sex", y="survived", ax=ax)
    ax.set(title="Survival rate by sex", ylabel="Survival rate")
    return _save(fig, out_dir, "survival_by_sex.png")


def plot_survival_by_class(df, out_dir):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x="pclass", y="survived", ax=ax)
    ax.set(title="Survival rate by ticket class",
           xlabel="Class (1 = first)", ylabel="Survival rate")
    return _save(fig, out_dir, "survival_by_class.png")


def plot_age_distribution(df, out_dir):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(data=df, x="age", hue="survived", bins=30,
                 multiple="stack", ax=ax)
    ax.set(title="Age distribution by survival (1 = survived)")
    return _save(fig, out_dir, "age_distribution.png")


def plot_correlation_heatmap(df, out_dir):
    fig, ax = plt.subplots(figsize=(7, 6))
    correlations = df.select_dtypes("number").corr()
    sns.heatmap(correlations, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, ax=ax)
    ax.set(title="Correlation between numeric columns")
    return _save(fig, out_dir, "correlation_heatmap.png")


def save_all_charts(df, out_dir="outputs"):
    """Create every chart and return the list of saved file paths."""
    Path(out_dir).mkdir(exist_ok=True)
    chart_functions = [
        plot_survival_by_sex,
        plot_survival_by_class,
        plot_age_distribution,
        plot_correlation_heatmap,
    ]
    return [make_chart(df, out_dir) for make_chart in chart_functions]
