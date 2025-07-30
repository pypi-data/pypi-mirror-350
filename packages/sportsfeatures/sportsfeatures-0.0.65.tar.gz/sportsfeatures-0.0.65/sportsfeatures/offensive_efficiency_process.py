"""A process function for determing offensive efficiency of entities."""

import functools

import pandas as pd
from tqdm import tqdm

from .cache import MEMORY
from .columns import DELIMITER
from .identifier import Identifier

OFFENSIVE_EFFICIENCY_COLUMN = "offensiveefficiency"


@MEMORY.cache
def _record_offensive_efficiency(
    row: pd.Series, identifiers: list[Identifier]
) -> pd.Series:
    for identifier in identifiers:
        if identifier.field_goals_column is None:
            continue
        field_goals_value = row[identifier.field_goals_column]
        if pd.isnull(field_goals_value):
            continue
        field_goals = float(field_goals_value)
        if identifier.assists_column is None:
            continue
        assists_value = row[identifier.assists_column]
        if pd.isnull(assists_value):
            continue
        assists = float(assists_value)
        if identifier.field_goals_attempted_column is None:
            continue
        field_goals_attempted_value = row[identifier.field_goals_attempted_column]
        if pd.isnull(field_goals_attempted_value):
            continue
        field_goals_attempted = float(row[identifier.field_goals_attempted_column])
        if identifier.offensive_rebounds_column is None:
            continue
        offensive_rebounds_value = row[identifier.offensive_rebounds_column]
        if pd.isnull(offensive_rebounds_value):
            continue
        offensive_rebounds = float(offensive_rebounds_value)
        if identifier.turnovers_column is None:
            continue
        turnovers_value = row[identifier.turnovers_column]
        if pd.isnull(turnovers_value):
            continue
        turnovers = float(turnovers_value)
        offensive_efficiency_column = DELIMITER.join(
            [identifier.column_prefix, OFFENSIVE_EFFICIENCY_COLUMN]
        )
        row[offensive_efficiency_column] = (field_goals + assists) / (
            field_goals_attempted - offensive_rebounds + assists + turnovers
        )
        if offensive_efficiency_column not in identifier.feature_columns:
            identifier.feature_columns.append(offensive_efficiency_column)
    return row


def offensive_efficiency_process(
    df: pd.DataFrame, identifiers: list[Identifier]
) -> pd.DataFrame:
    """Process a dataframe for offensive efficiency."""
    tqdm.pandas(desc="Offensive Efficiency Features")

    return df.progress_apply(
        functools.partial(
            _record_offensive_efficiency,
            identifiers=identifiers,
        ),
        axis=1,
    ).copy()  # type: ignore
