import pandas as pd

def tget(df, *args):
    # If no arguments are provided, return the original dataframe
    if not args:
        return df

    # Initialize the mask to select all rows
    mask = pd.Series([True] * len(df), index=df.index)

    # Initialize the columns to select all columns
    columns = df.columns.tolist()

    # Default columns to always include
    default_columns = ['Station', 'JobClass']

    # Iterate through the arguments
    for arg in args:
        # Check if the argument is an object with getName method
        if hasattr(arg, 'getName'):
            arg_value = str(arg.getName())
        else:
            arg_value = str(arg)

        if arg_value in df.columns:
            # If the argument is a column name, set columns to default columns plus this column
            columns = default_columns + [arg_value]
        else:
            # Update the mask to filter rows where any column matches the argument value
            mask = mask & df.apply(lambda row: row.astype(str).str.contains(arg_value).any(), axis=1)

    # Apply the mask to filter rows and select the columns
    return df.loc[mask, columns].drop_duplicates()
