import pandas as pd


def sanitize_dataframe(
    df: pd.DataFrame, sanitizing_strategy: int
) -> pd.DataFrame:
    """
    Dataframe sanitizer to remove or set a default value for the index, col,
    based on the sanitizing strategy.

    :param df:
    :param sanitizing_strategy:
    :return: A sanitized pandas DataFrame
    """
    default_values = {
        "object": "",
        "int64": 0,
        "float64": 0,
        "bool": False,
    }

    # Determining the sanitizing strategy
    use_default_types = sanitizing_strategy or 0

    # Create a copy to avoid modifying the original DataFrame
    validated_df = df.copy()

    for idx, row in df.iterrows():

        for col in df.columns:
            col_type = str(df[col].dtype)

            # Check if the value is NaN or None
            is_nan = pd.isna(row[col]) or pd.isnull(row[col])
            if is_nan and use_default_types:
                validated_df.at[idx, col] = default_values.get(col_type)
            elif is_nan and not use_default_types:
                validated_df.drop(index=idx)

            # Check for other invalid values based on column data type
            else:
                value = row[col]

                # Type-specific validation
                if col_type == "int64" or col_type == "float64":
                    if not isinstance(value, (int, float)) and use_default_types:
                        validated_df.at[idx, col] = default_values.get(col_type)
                    else:
                        validated_df.drop(index=idx)

                elif col_type == "object":
                    # For string columns, check if the value is wrong type
                    if not isinstance(value, str) and use_default_types:
                        validated_df.at[idx, col] = default_values.get(col_type)
                    else:
                        validated_df.drop(index=idx)

    return validated_df
