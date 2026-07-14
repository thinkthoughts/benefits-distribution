from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np

from .context import RepositoryContext


def _save_figure(
    figure: plt.Figure,
    output_path: Path,
) -> Path:
    """Save, display, and close a generated figure."""

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
    plt.close(figure)

    print("Saved:", output_path)
    return output_path


def _wrap_label(
    label: str,
    width: int = 18,
) -> str:
    """Wrap a label without breaking words."""

    lines = wrap(
        label,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return "\n".join(lines)


def plot_engineering_grammar(
    context: RepositoryContext,
    output_path: Path,
) -> Path:
    """Generate the shared specification grammar."""

    labels = context.grammar

    figure, axis = plt.subplots(
        figsize=(8, 9.5),
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
        context.grammar_title,
        fontsize=18,
        fontweight="bold",
        pad=24,
    )

    axis.text(
        0.5,
        0.07,
        context.design_principle,
        ha="center",
        va="center",
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
    """Generate the repository-specific engineering-variable lane."""

    symbols = context.lane_symbols
    labels = context.lane_labels

    if len(symbols) != len(labels):
        raise ValueError(
            "lane_symbols and lane_labels must have equal length"
        )

    count = len(symbols)

    figure, axis = plt.subplots(
        figsize=(
            max(12, count * 3.1),
            4.8,
        )
    )
    axis.axis("off")

    xs = np.linspace(
        0.11,
        0.89,
        count,
    )
    y = 0.54

    box_width = min(
        0.17,
        0.58 / count,
    )
    box_height = 0.19

    for index, (x, symbol, label) in enumerate(
        zip(xs, symbols, labels)
    ):
        axis.add_patch(
            plt.Rectangle(
                (
                    x - box_width / 2,
                    y - box_height / 2,
                ),
                box_width,
                box_height,
                fill=False,
                linewidth=1.8,
            )
        )

        axis.text(
            x,
            y + 0.035,
            symbol,
            ha="center",
            va="center",
            fontsize=20,
        )

        axis.text(
            x,
            y - 0.055,
            _wrap_label(
                label,
                width=16,
            ),
            ha="center",
            va="center",
            multialignment="center",
            fontsize=8.6,
            linespacing=1.05,
        )

        if index < count - 1:
            axis.annotate(
                "",
                xy=(
                    xs[index + 1]
                    - box_width / 2
                    - 0.012,
                    y,
                ),
                xytext=(
                    x
                    + box_width / 2
                    + 0.012,
                    y,
                ),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.8,
                    "shrinkA": 0,
                    "shrinkB": 0,
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
        0.15,
        context.lane_caption,
        ha="center",
        va="center",
        fontsize=10.2,
        wrap=True,
    )

    return _save_figure(
        figure,
        output_path,
    )


def plot_construction_sequence(
    context: RepositoryContext,
    output_path: Path,
) -> Path:
    """Generate the repository notebook sequence."""

    sequence = context.construction_sequence
    count = len(sequence)

    if count < 2:
        raise ValueError(
            "construction_sequence must contain at least two items"
        )

    figure, axis = plt.subplots(
        figsize=(
            max(16, count * 1.55),
            5.2,
        )
    )
    axis.axis("off")

    xs = np.linspace(
        0.055,
        0.945,
        count,
    )
    y = 0.53

    spacing = xs[1] - xs[0]

    box_width = min(
        0.075,
        spacing * 0.78,
    )
    box_height = 0.20

    for index, (x, item) in enumerate(
        zip(xs, sequence)
    ):
        try:
            number, title = item.split(
                " ",
                1,
            )
        except ValueError as error:
            raise ValueError(
                "Each construction-sequence item must begin "
                "with a notebook number followed by a title: "
                f"{item!r}"
            ) from error

        axis.add_patch(
            plt.Rectangle(
                (
                    x - box_width / 2,
                    y - box_height / 2,
                ),
                box_width,
                box_height,
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
            fontsize=11.5,
            fontweight="bold",
        )

        axis.text(
            x,
            y - 0.035,
            _wrap_label(
                title,
                width=13,
            ),
            ha="center",
            va="center",
            multialignment="center",
            fontsize=7.6,
            linespacing=1.0,
        )

        if index < count - 1:
            axis.annotate(
                "",
                xy=(
                    xs[index + 1]
                    - box_width / 2
                    - 0.006,
                    y,
                ),
                xytext=(
                    x
                    + box_width / 2
                    + 0.006,
                    y,
                ),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.5,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
            )

    axis.set_title(
        context.repository_sequence_title,
        fontsize=18,
        fontweight="bold",
        pad=24,
    )

    axis.text(
        0.5,
        0.16,
        context.repository_sequence_caption,
        ha="center",
        va="center",
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
    """Generate all Notebook 00 figures from one context object."""

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
