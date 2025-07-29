"""Process a dataframe for its datetime information."""

from warnings import simplefilter

import pandas as pd
from feature_engine.datetime import DatetimeFeatures


def datetime_process(df: pd.DataFrame, dt_column: str) -> pd.DataFrame:
    """Process datetime features."""
    simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
    dtf = DatetimeFeatures(
        variables=[dt_column],
        features_to_extract="all",
        missing_values="ignore",
        drop_original=False,
        utc=True,
    )
    return dtf.fit_transform(df).copy()
