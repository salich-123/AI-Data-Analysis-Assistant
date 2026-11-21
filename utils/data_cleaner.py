
def clean_data(df):

    print("\n========== DATA CLEANING ==========")

    # Make a copy of the original dataset
    df = df.copy()

    # 1. Check missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # 2. Fill missing values
    for column in df.columns:

        if df[column].isnull().any():

            if df[column].dtype in ["int64", "float64"]:
                df[column] = df[column].fillna(
                    df[column].median()
                )

            else:
                mode_values = df[column].mode()

                if not mode_values.empty:
                    df[column] = df[column].fillna(
                        mode_values[0]
                    )

    # 3. Remove duplicate rows
    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    # 4. Display cleaning results
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    print("\nDuplicate rows removed:", removed)

    print("\nCleaned dataset:")
    print(df)

    print("\nFinal dataset shape:", df.shape)

    print("\n========== CLEANING COMPLETED ==========")

    return df
