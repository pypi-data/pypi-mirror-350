"""Processing for time series features."""

# pylint: disable=duplicate-code,too-many-branches,too-many-nested-blocks

import datetime
import multiprocessing
from warnings import simplefilter

import pandas as pd
from timeseriesfeatures.feature import FEATURE_TYPE_LAG  # type: ignore
from timeseriesfeatures.feature import (FEATURE_TYPE_ROLLING, VALUE_TYPE_DAYS,
                                        VALUE_TYPE_NONE, Feature)
from timeseriesfeatures.process import process  # type: ignore
from timeseriesfeatures.transform import Transform  # type: ignore
from tqdm import tqdm

from .columns import DELIMITER
from .entity_type import EntityType
from .identifier import Identifier

_COLUMN_PREFIX_COLUMN = "_column_prefix"


def _pool_process(
    identifier_id: str,
    df: pd.DataFrame,
    features: list[Feature],
    dt_column: str,
) -> tuple[str, pd.DataFrame, pd.Series]:
    original_identifier_df = df.copy()
    drop_columns = df.columns.values.tolist()
    if "" in drop_columns:
        drop_columns.remove("")
    drop_columns.remove(_COLUMN_PREFIX_COLUMN)
    return (
        identifier_id,
        process(df, features=features, on=dt_column).drop(columns=drop_columns).copy(),
        original_identifier_df[_COLUMN_PREFIX_COLUMN],
    )


def _extract_identifier_timeseries(
    df: pd.DataFrame, identifiers: list[Identifier], dt_column: str
) -> dict[str, pd.DataFrame]:
    tqdm.pandas(desc="Timeseries Progress")
    identifier_ts: dict[str, pd.DataFrame] = {}
    team_identifiers = [x for x in identifiers if x.entity_type == EntityType.TEAM]
    player_identifiers = [x for x in identifiers if x.entity_type == EntityType.PLAYER]
    relevant_identifiers = team_identifiers + player_identifiers

    def record_timeseries_features(row: pd.Series) -> pd.Series:
        nonlocal identifier_ts
        nonlocal relevant_identifiers

        for identifier in relevant_identifiers:
            if identifier.column not in row:
                continue
            identifier_id = row[identifier.column]
            if pd.isnull(identifier_id):
                continue
            key = DELIMITER.join([identifier.entity_type, identifier_id])
            identifier_df = identifier_ts.get(key, pd.DataFrame())
            identifier_df.loc[row.name, _COLUMN_PREFIX_COLUMN] = (  # type: ignore
                identifier.column_prefix
            )
            identifier_df.loc[row.name, dt_column] = row[dt_column]  # type: ignore
            for feature_column in identifier.numeric_action_columns:
                if feature_column not in row:
                    continue
                value = row[feature_column]
                if pd.isnull(value):
                    continue
                column = feature_column[len(identifier.column_prefix) :]
                if not column:
                    continue
                if column not in identifier_df:
                    identifier_df[column] = None
                identifier_df.loc[row.name, column] = value  # type: ignore
            identifier_ts[key] = identifier_df.infer_objects()

        return row

    df.progress_apply(record_timeseries_features, axis=1)  # type: ignore
    return identifier_ts


def _process_identifier_ts(
    identifier_ts: dict[str, pd.DataFrame],
    windows: list[datetime.timedelta | None],
    dt_column: str,
) -> dict[str, pd.DataFrame]:
    # pylint: disable=too-many-locals
    features = [
        Feature(
            feature_type=FEATURE_TYPE_LAG,
            columns=[],
            value1=1,
            transform=str(Transform.NONE),
        ),
        Feature(
            feature_type=FEATURE_TYPE_LAG,
            columns=[],
            value1=2,
            transform=str(Transform.NONE),
        ),
        Feature(
            feature_type=FEATURE_TYPE_LAG,
            columns=[],
            value1=4,
            transform=str(Transform.NONE),
        ),
        Feature(
            feature_type=FEATURE_TYPE_LAG,
            columns=[],
            value1=8,
            transform=str(Transform.NONE),
        ),
    ] + [
        Feature(
            feature_type=FEATURE_TYPE_ROLLING,
            columns=[],
            value1=VALUE_TYPE_NONE if x is None else VALUE_TYPE_DAYS,
            value2=None if x is None else x.days,
            transform=str(Transform.NONE),
        )
        for x in windows
    ]
    with multiprocessing.Pool() as pool:
        for identifier_id, identifier_df, column_prefix_series in pool.starmap(
            _pool_process,
            tqdm(
                [(k, v, features, dt_column) for k, v in identifier_ts.items()],
                desc="Timeseries Processing",
            ),
        ):
            identifier_ts[identifier_id] = identifier_df
            identifier_ts[identifier_id][_COLUMN_PREFIX_COLUMN] = column_prefix_series

    return identifier_ts


def _write_ts_features(
    df: pd.DataFrame,
    identifier_ts: dict[str, pd.DataFrame],
    dt_column: str,
) -> pd.DataFrame:
    df_dict = df.to_dict(orient="list")

    written_columns = set()
    for identifier_df in tqdm(
        identifier_ts.values(), desc="Writing Timeseries Features"
    ):
        for row in identifier_df.itertuples(name=None):
            row_dict = {
                x: row[count + 1]
                for count, x in enumerate(identifier_df.columns.values.tolist())
            }
            column_prefix = row_dict[_COLUMN_PREFIX_COLUMN]
            for column, value in row_dict.items():
                if column in {_COLUMN_PREFIX_COLUMN, dt_column, ""}:
                    continue
                key = column_prefix + column
                if key not in df_dict:
                    df_dict[key] = [None for _ in range(len(df))]
                df_dict[key][row[0]] = value
                written_columns.add(key)
    for column in written_columns:
        df[column] = df_dict[column]

    return df


def timeseries_process(
    df: pd.DataFrame,
    identifiers: list[Identifier],
    windows: list[datetime.timedelta | None],
    dt_column: str,
) -> pd.DataFrame:
    """Process a dataframe for its timeseries features."""
    # pylint: disable=too-many-locals,consider-using-dict-items,too-many-statements,duplicate-code
    tqdm.pandas(desc="Progress")
    simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

    # Write the columns to the dataframe ahead of time.
    df[_COLUMN_PREFIX_COLUMN] = None

    identifier_ts: dict[str, pd.DataFrame] = _extract_identifier_timeseries(
        df, identifiers, dt_column
    )
    identifier_ts = _process_identifier_ts(identifier_ts, windows, dt_column)
    df = _write_ts_features(df, identifier_ts, dt_column)
    return df.drop(columns=[_COLUMN_PREFIX_COLUMN]).copy()
