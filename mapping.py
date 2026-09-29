import pandas as pd

def map_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """
    Maps the columns of a DataFrame based on a provided mapping dictionary.

    Parameters:
    df (pd.DataFrame): The input DataFrame whose columns need to be mapped.
    mapping (dict): A dictionary where keys are the original column names and values are the new column names.

    Returns:
    pd.DataFrame: A new DataFrame with the columns renamed according to the mapping.
    """
    return df.rename(columns=mapping)

