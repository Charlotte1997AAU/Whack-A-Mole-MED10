import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def normalizeDataframe(df, exclude_columns=None):
    """Normalize all numeric columns in the DataFrame using Min-Max Scaling (0 to 1), excluding specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        exclude_columns (list): List of column names to exclude from normalization.

    Returns:
        pd.DataFrame: Normalized DataFrame.
    """
    if exclude_columns is None:
        exclude_columns = []

    # Select columns to normalize
    columns_to_normalize = [col for col in df.columns if col not in exclude_columns]

    scaler = MinMaxScaler()
    df_normalized = df.copy()

    # Apply normalization only to selected columns
    df_normalized[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])

    return df_normalized


def standardizeDataframe(df, exclude_columns=None):
    """
    Standardize all numeric columns in the DataFrame using Z-score Normalization,
    excluding specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        exclude_columns (list): List of column names to exclude from standardization.

    Returns:
        pd.DataFrame: Standardized DataFrame.
    """
    if exclude_columns is None:
        exclude_columns = []

    # Select columns to standardize
    columns_to_standardize = [col for col in df.columns if col not in exclude_columns]

    scaler = StandardScaler()
    df_standardized = df.copy()

    # Apply standardization only to selected columns
    df_standardized[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

    return df_standardized
