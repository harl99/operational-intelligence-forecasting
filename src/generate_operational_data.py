import numpy as np
import pandas as pd
from pathlib import Path


def generate_operational_data(
    start_date: str = "2023-01-01",
    end_date: str = "2025-12-31 23:00:00",
    output_path: str = "data/raw/industrial_operations_timeseries.csv",
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a realistic hourly industrial operations time series dataset.

    The dataset simulates an industrial facility with:
    - hourly energy consumption
    - production throughput
    - ambient temperature
    - shift patterns
    - weekends
    - maintenance events
    - operational anomalies
    - estimated energy cost
    """

    np.random.seed(random_seed)

    timestamp = pd.date_range(
        start=start_date,
        end=end_date,
        freq="h"
    )

    df = pd.DataFrame({"timestamp": timestamp})

    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["month"] = df["timestamp"].dt.month
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Operational shifts
    df["shift"] = np.select(
        [
            df["hour"].between(6, 13),
            df["hour"].between(14, 21),
        ],
        [
            "morning",
            "evening",
        ],
        default="night",
    )

    shift_multiplier = df["shift"].map(
        {
            "morning": 1.15,
            "evening": 1.05,
            "night": 0.75,
        }
    )

    weekend_multiplier = np.where(df["is_weekend"] == 1, 0.65, 1.0)

    # Seasonal ambient temperature pattern
    annual_temperature = 26 + 7 * np.sin(
        2 * np.pi * (df["timestamp"].dt.dayofyear / 365.25)
    )

    daily_temperature = 3 * np.sin(
        2 * np.pi * ((df["hour"] - 6) / 24)
    )

    df["ambient_temperature_c"] = (
        annual_temperature
        + daily_temperature
        + np.random.normal(0, 1.5, len(df))
    ).round(2)

    # Production throughput
    base_throughput = 110

    weekly_pattern = np.where(df["day_of_week"].isin([0, 1, 2, 3]), 1.05, 0.95)

    df["production_throughput_units"] = (
        base_throughput
        * shift_multiplier
        * weekend_multiplier
        * weekly_pattern
        + np.random.normal(0, 8, len(df))
    )

    df["production_throughput_units"] = df["production_throughput_units"].clip(lower=20).round(2)

    # Maintenance events
    df["maintenance_event"] = 0
    maintenance_dates = pd.date_range(start=start_date, end=end_date, freq="30D")

    for maintenance_date in maintenance_dates:
        mask = (
            df["timestamp"] >= maintenance_date
        ) & (
            df["timestamp"] < maintenance_date + pd.Timedelta(hours=8)
        )
        df.loc[mask, "maintenance_event"] = 1

    # Energy consumption
    base_energy = 450

    temperature_load = np.where(
        df["ambient_temperature_c"] > 28,
        (df["ambient_temperature_c"] - 28) * 9,
        0,
    )

    throughput_load = df["production_throughput_units"] * 2.7

    maintenance_reduction = np.where(df["maintenance_event"] == 1, -180, 0)

    df["energy_consumption_kwh"] = (
        base_energy
        + throughput_load
        + temperature_load
        + maintenance_reduction
        + np.random.normal(0, 35, len(df))
    )

    df["energy_consumption_kwh"] = df["energy_consumption_kwh"].clip(lower=100).round(2)

    # Operational anomalies
    df["anomaly_event"] = 0
    anomaly_indices = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)

    df.loc[anomaly_indices, "anomaly_event"] = 1
    df.loc[anomaly_indices, "energy_consumption_kwh"] *= np.random.uniform(
        1.15, 1.45, size=len(anomaly_indices)
    )

    df["energy_consumption_kwh"] = df["energy_consumption_kwh"].round(2)

    # Energy price by hour
    df["energy_price_usd_per_kwh"] = np.select(
        [
            df["hour"].between(18, 22),
            df["hour"].between(8, 17),
        ],
        [
            0.18,
            0.13,
        ],
        default=0.09,
    )

    df["estimated_energy_cost_usd"] = (
        df["energy_consumption_kwh"] * df["energy_price_usd_per_kwh"]
    ).round(2)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    data = generate_operational_data()
    print("Dataset generated successfully.")
    print(f"Rows: {len(data)}")
    print(f"Columns: {len(data.columns)}")
    print("Saved to: data/raw/industrial_operations_timeseries.csv")
    print(data.head())
