from dataclasses import dataclass
from typing import Tuple


@dataclass
class RepositoryContext:

    repository: str
    repository_description: str

    engineering_statement_title: str
    engineering_statement: str

    grammar_title: str
    grammar: Tuple[str, ...]

    constraint: str
    connected_lane: str

    engineering_objects: Tuple[str, ...]
    engineering_variables: Tuple[str, ...]
    observable_states: Tuple[str, ...]
    indicators: Tuple[str, ...]

    lane_symbols: Tuple[str, ...]
    lane_labels: Tuple[str, ...]

    repository_variable_title: str
    lane_caption: str

    repository_sequence_title: str
    repository_sequence_caption: str

    construction_sequence: Tuple[str, ...]

    design_principle: str

    next_notebook: str

    source: str
    notes: str
