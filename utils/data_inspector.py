
def inspect_data(df):

    print("\n========== DATASET INSPECTION ==========")

    # 1. Dataset size
    print("\n1. Dataset Shape:")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    # 2. Column data types
    print("\n2. Column Data Types:")
    print(df.dtypes)

    # 3. Missing values
    print("\n3. Missing Values:")
    print(df.isnull().sum())

    # 4. Duplicate records
    print("\n4. Duplicate Rows:")
    print(df.duplicated().sum())

    # 5. Statistical summary
    print("\n5. Statistical Summary:")
    print(df.describe())

    print("\n========== INSPECTION COMPLETED ==========")
