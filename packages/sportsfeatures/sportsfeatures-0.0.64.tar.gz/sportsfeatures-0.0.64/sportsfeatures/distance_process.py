"""Process the distance between two locations."""

# pylint: disable=duplicate-code,too-many-branches,too-many-locals,too-many-statements

import geopy.distance  # type: ignore
import pandas as pd
from tqdm import tqdm

from .columns import DELIMITER
from .entity_type import EntityType
from .identifier import Identifier


def distance_process(df: pd.DataFrame, identifiers: list[Identifier]) -> pd.DataFrame:
    """Process a dataframe for offensive efficiency."""
    last_identifier_locations: dict[str, tuple[float, float]] = {}
    team_identifiers = [x for x in identifiers if x.entity_type == EntityType.TEAM]
    player_identifiers = [x for x in identifiers if x.entity_type == EntityType.PLAYER]
    venue_identifiers = [x for x in identifiers if x.entity_type == EntityType.VENUE]
    df_dict: dict[str, list[float | None]] = {}
    df_cols = df.columns.values.tolist()

    written_columns = set()
    for row in tqdm(
        df.itertuples(name=None), desc="Distance Processing", total=len(df)
    ):
        row_dict = {x: row[count + 1] for count, x in enumerate(df_cols)}

        current_location = None
        for venue_identifier in venue_identifiers:
            if venue_identifier.latitude_column is None:
                continue
            if venue_identifier.latitude_column not in row_dict:
                continue
            latitude = row_dict[venue_identifier.latitude_column]
            if latitude is None:
                continue
            if venue_identifier.longitude_column is None:
                continue
            if venue_identifier.longitude_column not in row_dict:
                continue
            longitude = row_dict[venue_identifier.longitude_column]
            if longitude is None:
                continue
            current_location = (latitude, longitude)
        if current_location is None:
            continue

        for identifier in team_identifiers + player_identifiers:
            if identifier.column not in row_dict:
                continue
            identifier_id = row_dict[identifier.column]
            if identifier_id is None:
                continue
            if not isinstance(identifier_id, str):
                continue
            key = "_".join([str(identifier.entity_type), identifier_id])
            last_location = last_identifier_locations.get(key)
            if last_location is not None:
                latitude_diff_column = DELIMITER.join(
                    [identifier.column_prefix, "latitudediff"]
                )
                if latitude_diff_column not in df_dict:
                    df_dict[latitude_diff_column] = [None for _ in range(len(df))]
                written_columns.add(latitude_diff_column)
                df_dict[latitude_diff_column][row[0]] = abs(
                    last_location[0] - current_location[0]
                )
                longitude_diff_column = DELIMITER.join(
                    [identifier.column_prefix, "longitudediff"]
                )
                if longitude_diff_column not in df_dict:
                    df_dict[longitude_diff_column] = [None for _ in range(len(df))]
                written_columns.add(longitude_diff_column)
                df_dict[longitude_diff_column][row[0]] = abs(
                    last_location[1] - current_location[1]
                )
                distance_column = DELIMITER.join([identifier.column_prefix, "distance"])
                if distance_column not in df_dict:
                    df_dict[distance_column] = [None for _ in range(len(df))]
                df_dict[distance_column][row[0]] = geopy.distance.geodesic(
                    last_location, current_location
                ).km
                written_columns.add(distance_column)
            last_identifier_locations[key] = current_location

    for column in written_columns:
        df[column] = df_dict[column]

    return df[sorted(df.columns.values.tolist())].copy()
