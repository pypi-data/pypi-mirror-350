"""Process the current dataframe by adding skill features."""

# pylint: disable=duplicate-code,too-many-locals,too-many-statements

import datetime
import functools
import os

import numpy as np
import pandas as pd
from tqdm import tqdm

from .cache import MEMORY, create_cache, find_best_cache
from .columns import DELIMITER
from .entity_type import EntityType
from .identifier import Identifier
from .windowed_rating import WindowedRating

SKILL_COLUMN_PREFIX = "skill"
SKILL_MU_COLUMN = "mu"
SKILL_SIGMA_COLUMN = "sigma"
SKILL_RANKING_COLUMN = "ranking"
SKILL_PROBABILITY_COLUMN = "probability"
TIME_SLICE_ALL = "all"
_SKILL_CACHE_NAME = "skill"
_RESULTS_PARQUET_FILENAME = "results.parquet"


@MEMORY.cache
def _calculate_skills(
    row: pd.Series,
    rating_windows: list[WindowedRating],
    team_identifiers: list[Identifier],
    player_identifiers: list[Identifier],
) -> pd.Series:
    for rating_window in rating_windows:
        window_id = (
            TIME_SLICE_ALL
            if rating_window.window is None
            else f"window{rating_window.window.days}"
        )
        team_result, player_result = rating_window.add(
            row, team_identifiers, player_identifiers
        )
        for team_identifier in team_identifiers:
            if team_identifier.column not in row:
                continue
            team_id = row[team_identifier.column]
            if pd.isnull(team_id):
                continue
            if team_id in team_result:
                rating, ranking, prob = team_result[team_id]
                window_prefix = DELIMITER.join(
                    [team_identifier.column_prefix, SKILL_COLUMN_PREFIX, window_id]
                )
                row[DELIMITER.join([window_prefix, SKILL_MU_COLUMN])] = rating.mu
                row[DELIMITER.join([window_prefix, SKILL_SIGMA_COLUMN])] = rating.sigma
                row[DELIMITER.join([window_prefix, SKILL_RANKING_COLUMN])] = ranking
                row[DELIMITER.join([window_prefix, SKILL_PROBABILITY_COLUMN])] = prob
            for player_identifier in player_identifiers:
                if player_identifier.column not in row:
                    continue
                player_id = row[player_identifier.column]
                if pd.isnull(player_id):
                    continue
                if player_id in player_result:
                    rating, ranking, prob = team_result[team_id]
                    window_prefix = DELIMITER.join(
                        [
                            player_identifier.column_prefix,
                            SKILL_COLUMN_PREFIX,
                            window_id,
                        ]
                    )
                    row[DELIMITER.join([window_prefix, SKILL_MU_COLUMN])] = rating.mu
                    row[DELIMITER.join([window_prefix, SKILL_SIGMA_COLUMN])] = (
                        rating.sigma
                    )
                    row[DELIMITER.join([window_prefix, SKILL_RANKING_COLUMN])] = ranking
                    row[DELIMITER.join([window_prefix, SKILL_PROBABILITY_COLUMN])] = (
                        prob
                    )

    return row


def skill_process(
    df: pd.DataFrame,
    dt_column: str,
    identifiers: list[Identifier],
    windows: list[datetime.timedelta | None],
) -> pd.DataFrame:
    """Add skill features to the dataframe."""
    tqdm.pandas(desc="Skill Features")
    original_df = df.copy()

    team_identifiers = [x for x in identifiers if x.entity_type == EntityType.TEAM]
    player_identifiers = [x for x in identifiers if x.entity_type == EntityType.PLAYER]
    rating_windows = [WindowedRating(x, dt_column) for x in windows]

    cache_folder, idx = find_best_cache(_SKILL_CACHE_NAME, df)
    if cache_folder is not None:
        load_success = False
        for rating_window in rating_windows:
            load_success = rating_window.load(cache_folder)
            if not load_success:
                break
        if not load_success:
            for rating_window in rating_windows:
                rating_window.reset()
            cache_folder = None
        else:
            df_cache = pd.read_parquet(
                os.path.join(cache_folder, _RESULTS_PARQUET_FILENAME)
            )
            if len(df_cache) == len(df):
                return df
            df = df.join(
                df_cache.drop(
                    columns=[col for col in df_cache.columns if col in df.columns]
                ),
                how="left",
            )

    if cache_folder is not None:
        processed_ilocs = np.arange(idx)
        all_ilocs = np.arange(len(df))
        unprocessed_ilocs = np.setdiff1d(all_ilocs, processed_ilocs)
        df.iloc[unprocessed_ilocs] = df.iloc[unprocessed_ilocs].progress_apply(
            functools.partial(
                _calculate_skills,
                rating_windows=rating_windows,
                team_identifiers=team_identifiers,
                player_identifiers=player_identifiers,
            ),
            axis=1,
        )  # type: ignore
    else:
        df = df.progress_apply(
            functools.partial(
                _calculate_skills,
                rating_windows=rating_windows,
                team_identifiers=team_identifiers,
                player_identifiers=player_identifiers,
            ),
            axis=1,
        )  # type: ignore

    cache_folder = create_cache(_SKILL_CACHE_NAME, original_df)
    for rating_window in rating_windows:
        rating_window.save(cache_folder)
    df.to_parquet(os.path.join(cache_folder, _RESULTS_PARQUET_FILENAME))

    return df.copy()
