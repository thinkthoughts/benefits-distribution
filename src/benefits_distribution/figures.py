from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .context import RepositoryContext


def _save_figure(
    figure: plt.Figure,
    output_path: Path,
) -> Path:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.savefig(
        output_path,
        dpi=240,
        bbox_inches="tight",
    )

    plt.show()
    return output_path


def plot_engineering_grammar(
    context: RepositoryContext,
    output_path: Path,
) -> Path:
    labels = context.grammar

    figure, axis = plt.subplots(
        figsize=(8, 9.5)
    )
    axis.axis("off")

    ys = np.linspace(
        0.84,
        0.18,
        len(labels),
    )
    x = 0.5

    for index, (label, y) in enumerate(
        zip(labels, ys)
    ):
        axis.add_patch(
            plt.Rectangle(
                (x - 0.28, y - 0.04),
                0.56,
                0.08,
                fill=False,
                linewidth=1.8,
            )
        )

        axis.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=13,
            fontweight=(
                "bold"
                if index < 4
                else "normal"
            ),
        )

        if index < len(labels) - 1:
            axis.annotate(
                "",
                xy=(
                    x,
                    ys[index + 1] + 0.05,
                ),
                xytext=(
                    x,
                    y - 0.05,
                ),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.8,
                },
            )

    axis.set_title(
        "Engineering Specification Grammar",
        fontsize=18,
        fontweight="bold",
        pad=24,
    )

    axis.text(
        0.5,
        0.07,
        (
            "Engineering specifies objects before measuring "
            "variables, and measures variables before "
            "evaluating indicators."
        ),
        ha="center",
        fontsize=10.5,
    )

    return _save_figure(
        figure,
        output_path,
    )


def plot_repository_lane(
    context: RepositoryContext,
    output_path: Path,
) -> Path:
    symbols = context.lane_symbols
    labels = context.lane_labels

    figure, axis = plt.subplots(
        figsize=(12, 4.8)
    )
    axis.axis("off")

    xs = np.linspace(
        0.12,
        0.88,
        len(symbols),
    )
    y = 0.54

    for index, (x, symbol, label) in enumerate(
        zip(xs, symbols, labels)
    ):
        axis.add_patch(
            plt.Rectangle(
                (x - 0.075, y - 0.09),
                0.15,
                0.18,
                fill=False,
                linewidth=1.8,
            )
        )

        axis.text(
            x,
            y + 0.025,
            symbol,
            ha="center",
            va="center",
            fontsize=20,
        )

        axis.text(
            x,
            y - 0.055,
            label,
            ha="center",
            va="center",
            fontsize=9,
        )

        if index < len(symbols) - 1:
            axis.annotate(
                "",
                xy=(
                    xs[index + 1] - 0.09,
                    y,
                ),
                xytext=(
                    x + 0.09,
                    y,
                ),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.8,
                },
            )

    axis.set_title(
        context.repository_variable_title,
        fontsize=18,
        fontweight="bold",
        pad=24,
    )

    axis.text(
        0.5,
        0.16,
        context.lane_caption,
        ha="center",
        fontsize=10.5,
    )

    return _save_figure(
        figure,
        output_path,
    )


def plot_construction_sequence(
    context: RepositoryContext,
    output_path: Path,
) -> Path:
    sequence = context.construction_sequence

    figure, axis = plt.subplots(
        figsize=(
            max(15, len(sequence) * 1.35),
            5,
        )
    )
    axis.axis("off")

    xs = np.linspace(
        0.04,
        0.96,
        len(sequence),
    )
    y = 0.53

    for index, (x, item) in enumerate(
        zip(xs, sequence)
    ):
        number, title = item.split(
            " ",
            1,
        )

        axis.add_patch(
            plt.Rectangle(
                (x - 0.041, y - 0.10),
                0.082,
                0.20,
                fill=False,
                linewidth=1.6,
            )
        )

        axis.text(
            x,
            y + 0.045,
            number,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )

        axis.text(
            x,
            y - 0.035,
            title.replace(" ", "\n", 1),
            ha="center",
            va="center",
            fontsize=7.5,
        )

        if index < len(sequence) - 1:
            axis.annotate(
                "",
                xy=(
                    xs[index + 1] - 0.048,
                    y,
                ),
                xytext=(
                    x + 0.048,
                    y,
                ),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.5,
                },
            )

    axis.set_title(
        "Repository Construction Sequence",
        fontsize=18,
        fontweight="bold",
        pad=24,
    )

    axis.text(
        0.5,
        0.17,
        (
            "Each notebook specifies one connected stage "
            "of repository development."
        ),
        ha="center",
        fontsize=10.5,
    )

    return _save_figure(
        figure,
        output_path,
    )


def generate_context_figures(
    context: RepositoryContext,
    figures_dir: Path,
) -> dict[str, Path]:
    figures_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return {
        "grammar": plot_engineering_grammar(
            context,
            figures_dir
            / "00_engineering_specification_grammar.png",
        ),
        "lane": plot_repository_lane(
            context,
            figures_dir
            / "00_repository_lane_specification.png",
        ),
        "sequence": plot_construction_sequence(
            context,
            figures_dir
            / "00_repository_construction_sequence.png",
        ),
    }
