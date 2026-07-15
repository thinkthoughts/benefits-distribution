from __future__ import annotations

from .context import RepositoryContext


class ContextValidationError(ValueError):
    """Raised when repository context is incomplete or inconsistent."""


def validate_context(context: RepositoryContext) -> None:
    """Validate a RepositoryContext before generating artifacts."""

    scalar_fields = {
        "repository": context.repository,
        "repository_description": context.repository_description,
        "engineering_statement_title": (
            context.engineering_statement_title
        ),
        "engineering_statement": context.engineering_statement,
        "grammar_title": context.grammar_title,
        "constraint": context.constraint,
        "connected_lane": context.connected_lane,
        "repository_variable_title": (
            context.repository_variable_title
        ),
        "repository_sequence_title": (
            context.repository_sequence_title
        ),
        "repository_sequence_caption": (
            context.repository_sequence_caption
        ),
        "design_principle": context.design_principle,
        "next_notebook": context.next_notebook,
    }

    for name, value in scalar_fields.items():
        if not isinstance(value, str):
            raise ContextValidationError(
                f"{name} must be a string"
            )

        if not value.strip():
            raise ContextValidationError(
                f"{name} must be non-empty"
            )

    sequence_fields = {
        "grammar": context.grammar,
        "engineering_objects": context.engineering_objects,
        "engineering_variables": context.engineering_variables,
        "observable_states": context.observable_states,
        "indicators": context.indicators,
        "lane_symbols": context.lane_symbols,
        "lane_labels": context.lane_labels,
        "lane_relationships": context.lane_relationships,
        "construction_sequence": context.construction_sequence,
    }

    for name, values in sequence_fields.items():
        if not isinstance(values, tuple):
            raise ContextValidationError(
                f"{name} must be a tuple"
            )

        if not values:
            raise ContextValidationError(
                f"{name} must contain at least one item"
            )

        if any(
            not isinstance(item, str)
            for item in values
        ):
            raise ContextValidationError(
                f"{name} must contain only strings"
            )

        if any(
            not item.strip()
            for item in values
        ):
            raise ContextValidationError(
                f"{name} contains an empty item"
            )

    expected_grammar = (
        "Constraint",
        "Connected lane",
        "Engineering object",
        "Engineering variable",
        "Observable state",
        "Indicator",
    )

    if context.grammar != expected_grammar:
        raise ContextValidationError(
            "grammar must match the canonical specification grammar: "
            "Constraint, Connected lane, Engineering object, "
            "Engineering variable, Observable state, Indicator"
        )

    if (
        len(context.lane_symbols)
        != len(context.lane_labels)
    ):
        raise ContextValidationError(
            "lane_symbols and lane_labels must have equal length"
        )

    if len(context.lane_symbols) < 2:
        raise ContextValidationError(
            "repository lane must contain at least two stages"
        )

    expected_relationship_count = (
        len(context.lane_symbols) - 1
    )

    if (
        len(context.lane_relationships)
        != expected_relationship_count
    ):
        raise ContextValidationError(
            "lane_relationships must contain exactly one relationship "
            "for each transition between lane stages: "
            f"expected {expected_relationship_count}, "
            f"received {len(context.lane_relationships)}"
        )

    if len(context.construction_sequence) < 2:
        raise ContextValidationError(
            "construction_sequence must include Notebook 00 "
            "and at least one subsequent notebook"
        )

    first_item = context.construction_sequence[0]

    if not first_item.startswith("00 "):
        raise ContextValidationError(
            "construction_sequence must begin with Notebook 00"
        )

    notebook_numbers: list[str] = []

    for item in context.construction_sequence:
        parts = item.split(" ", 1)

        if len(parts) != 2:
            raise ContextValidationError(
                "each construction_sequence item must contain "
                "a notebook number followed by a title"
            )

        number, title = parts

        if not number.isdigit():
            raise ContextValidationError(
                "invalid notebook number in construction_sequence: "
                f"{number!r}"
            )

        if not title.strip():
            raise ContextValidationError(
                f"construction_sequence item {item!r} "
                "must include a title"
            )

        notebook_numbers.append(number)

    if len(set(notebook_numbers)) != len(notebook_numbers):
        raise ContextValidationError(
            "construction_sequence contains duplicate notebook numbers"
        )

    next_number = (
        context.construction_sequence[1]
        .split(" ", 1)[0]
    )

    if not context.next_notebook.startswith(
        f"{next_number}_"
    ):
        raise ContextValidationError(
            "next_notebook must match the second item "
            "in construction_sequence"
        )

    if not context.next_notebook.endswith(
        ".ipynb"
    ):
        raise ContextValidationError(
            "next_notebook must end with .ipynb"
        )
