"""Process a dataframe for its news information."""

# pylint: disable=too-many-locals,too-many-branches
import statistics
from warnings import simplefilter

import pandas as pd
import tqdm
from textfeats.process import process  # type: ignore

from .columns import DELIMITER
from .identifier import Identifier

COUNT_COLUMN = "count"
MENTIONS_COLUMN = "mentions"
EMBEDDING_COLUMN = "embedding"
NEWS_COLUMN = "news"


def news_process(df: pd.DataFrame, identifiers: list[Identifier]) -> pd.DataFrame:
    """Process news features."""
    simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
    df_dict: dict[str, list[float | None]] = {}
    df_cols = df.columns.values.tolist()

    written_columns = set()
    for row in tqdm.tqdm(
        df.itertuples(name=None), desc="News Processing", total=len(df)
    ):
        row_dict = {x: row[count + 1] for count, x in enumerate(df_cols)}

        for identifier in identifiers:
            summary_columns = []
            for news in identifier.news:
                if news.summary_column not in row_dict:
                    continue
                if row_dict[news.summary_column] is None:
                    continue
                summary_columns.append(news.summary_column)

            # Calculate counts
            count_col = DELIMITER.join(
                [identifier.column_prefix, NEWS_COLUMN, COUNT_COLUMN]
            )
            if count_col not in df_dict:
                df_dict[count_col] = [None for _ in range(len(df))]
            df_dict[count_col][row[0]] = float(len(summary_columns))
            written_columns.add(count_col)

            # Calculate injury mentions
            summaries = [row_dict[x] for x in summary_columns]
            injury_mentions = 0
            for summary in summaries:
                if "injur" in summary:
                    injury_mentions += 1
            injury_mentions_column = DELIMITER.join(
                [identifier.column_prefix, NEWS_COLUMN, MENTIONS_COLUMN, "injury"]
            )
            if injury_mentions_column not in df_dict:
                df_dict[injury_mentions_column] = [None for _ in range(len(df))]
            df_dict[injury_mentions_column][row[0]] = float(injury_mentions)
            written_columns.add(injury_mentions_column)

            # Calculate embeddings
            news_df = process(
                pd.DataFrame(
                    data={k: v for k, v in row_dict.items() if k in summary_columns}
                )
            )
            news_df = news_df.drop(columns=summary_columns, errors="ignore")
            embedding_indexes = set()
            for column in news_df.columns.values.tolist():
                column_split = column.split("_")
                embedding_indexes.add(column_split[-1])
            for embedding_index in embedding_indexes:
                values = []
                for column in news_df.columns.values.tolist():
                    column_split = column.split("_")
                    if column_split[-1] == embedding_index:
                        values.append(news_df[column].tolist()[0])
                embedding_column = DELIMITER.join(
                    [
                        identifier.column_prefix,
                        NEWS_COLUMN,
                        EMBEDDING_COLUMN,
                        embedding_index,
                    ]
                )
                if embedding_column not in df_dict:
                    df_dict[embedding_column] = [None for _ in range(len(df))]
                df_dict[embedding_column][row[0]] = statistics.mean(values)
                written_columns.add(embedding_column)

    for column in written_columns:
        df[column] = df_dict[column]

    return df.copy()
