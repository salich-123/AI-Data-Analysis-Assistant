
import pandas as pd

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)

        print("Dataset loaded successfully!")
        print("\nFirst 5 rows:")
        print(df.head())

        print("\nDataset Shape:")
        print(df.shape)

        print("\nColumn Names:")
        print(df.columns.tolist())

        return df

    except Exception as e:
        print("Error loading dataset:", e)
