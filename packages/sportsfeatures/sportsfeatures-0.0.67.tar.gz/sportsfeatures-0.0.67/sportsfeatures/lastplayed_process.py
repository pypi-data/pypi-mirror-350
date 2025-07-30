"""Process the time delta between the last time played."""

# pylint: disable=duplicate-code,too-many-branches

import datetime
import functools

import pandas as pd
from tqdm import tqdm

from .columns import DELIMITER
from .identifier import Identifier


def lastplayed_process(
    df: pd.DataFrame, identifiers: list[Identifier], dt_column: str
) -> pd.DataFrame:
    """Process a dataframe for last played."""
    tqdm.pandas(desc="Last Played Features")
    last_identifier_dts: dict[str, datetime.datetime | None] = {}
    first_identifier_dts: dict[str, datetime.datetime] = {}

    def record_time(
        row: pd.Series,
        identifiers: list[Identifier],
        dt_column: str,
    ) -> pd.Series:
        nonlocal last_identifier_dts
        nonlocal first_identifier_dts

        dt = row[dt_column]
        for identifier in identifiers:
            if identifier.column not in row:
                continue
            identifier_id = row[identifier.column]
            if pd.isnull(identifier_id):
                continue
            if not isinstance(identifier_id, str):
                continue
            key = "_".join([str(identifier.entity_type), identifier_id])
            last_dt = last_identifier_dts.get(key)
            if last_dt is not None and dt is not None:
                row[DELIMITER.join([identifier.column_prefix, "lastplayeddays"])] = (
                    dt - last_dt
                ).days
            last_identifier_dts[key] = dt
            first_dt = first_identifier_dts.get(key)
            if first_dt is not None and dt is not None:
                row[DELIMITER.join([identifier.column_prefix, "firstplayeddays"])] = (
                    dt - first_dt
                ).days
            elif first_dt is None and dt is not None:
                first_identifier_dts[key] = dt
        return row

    return df.progress_apply(
        functools.partial(
            record_time,
            identifiers=identifiers,
            dt_column=dt_column,
        ),
        axis=1,
    ).copy()  # type: ignore
