import pandas as pd


DATA_PATH = "data/raw/industrial_operations_timeseries.csv"


def inspect_dataset(path: str = DATA_PATH) -> None:
    df = pd.read_csv(path)

    print("\n=== DATASET SHAPE ===")
    print(df.shape)

    print("\n=== COLUMNS ===")
    print(df.columns.tolist())

    print("\n=== DATA TYPES ===")
    print(df.dtypes)

    print("\n=== FIRST ROWS ===")
    print(df.head())

    print("\n=== LAST ROWS ===")
    print(df.tail())

    print("\n=== MISSING VALUES ===")
    print(df.isna().sum())

    print("\n=== DUPLICATED ROWS ===")
    print(df.duplicated().sum())

    print("\n=== BASIC NUMERIC SUMMARY ===")
    print(df.describe())

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    print("\n=== TIME RANGE ===")
    print("Start:", df["timestamp"].min())
    print("End:", df["timestamp"].max())

    print("\n=== EXPECTED HOURLY FREQUENCY CHECK ===")
    expected_rows = pd.date_range(
        start=df["timestamp"].min(),
        end=df["timestamp"].max(),
        freq="h"
    )

    print("Expected hourly rows:", len(expected_rows))
    print("Actual rows:", len(df))
    print("Missing timestamps:", len(expected_rows) - len(df))

    print("\n=== TARGET VARIABLE CHECK ===")
    print(df["energy_consumption_kwh"].describe())

    print("\n=== SAMPLE BY TIMESTAMP ===")
    print(df[["timestamp", "energy_consumption_kwh", "production_throughput_units", "ambient_temperature_c"]].head(10))


if __name__ == "__main__":
    inspect_dataset()
