from datetime import timedelta

import numpy as np
import pandas as pd


def calc_delivery_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates 'delivery_date' and 'period' columns for a time-indexed DataFrame,
    handling timezone conversions and Daylight Saving Time (DST) changes.

    The 'delivery_date' is the date part of the index converted to CET.
    The 'period' represents the elapsed time from the start of the delivery date (in CET)
    to the current timestamp, adjusted for the specified time resolution, which is
    now read from the 'time_resolution' column in the DataFrame.

    Args:
        df (pd.DataFrame): A Pandas DataFrame with:
                           - A timezone-aware DatetimeIndex. The index must already
                             have a timezone assigned (e.g., 'UTC', 'Europe/Berlin', etc.).
                           - A 'time_resolution' column containing string values
                             "PT60M" (hourly) or "PT15M" (15-minute).

    Returns:
        pd.DataFrame: The original DataFrame with two new columns:
                      - 'delivery_date': The date in CET (datetime.date objects).
                      - 'period': The calculated period (integer).

    Raises:
        ValueError: If the DataFrame index is not a timezone-aware DatetimeIndex,
                    if the 'time_resolution' column is missing, or if it contains
                    unsupported time resolution values.
    """
    # Validate the DataFrame index
    if not isinstance(df.index, pd.DatetimeIndex) or df.index.tz is None:
        raise ValueError("DataFrame index must be a timezone-aware DatetimeIndex.")

    # Validate the presence of the 'time_resolution' column
    if 'time_resolution' not in df.columns:
        raise ValueError("DataFrame must contain a 'time_resolution' column.")

    # Validate the values in the 'time_resolution' column
    supported_resolutions = {"PT60M", "PT15M"}
    # Convert the unique values from the column to a set before performing set difference
    unsupported_values = set(df['time_resolution'].unique()) - supported_resolutions
    if unsupported_values:
        raise ValueError(f"Unsupported time resolution values found in 'time_resolution' column: {unsupported_values}. "
                         "Please use 'PT60M' or 'PT15M'.")

    # 1. Convert the DataFrame index to CET (Central European Time)
    # This step ensures all calculations for delivery_date are based on CET local time.
    df_cet_index = df.index.tz_convert('CET')

    # 2. Extract the delivery date from the CET-converted index
    # .date property returns a NumPy array of datetime.date objects, which is efficient.
    delivery_date = df_cet_index.date

    # 3. Convert the original DataFrame index to UTC
    # This 'utc' timestamp is used as the reference point for calculating elapsed hours.
    df_utc_index = df.index.tz_convert('UTC')

    # 4. Determine 'utc_from': The UTC equivalent of midnight (00:00:00) on the
    #    'delivery_date' in CET.
    #    - .normalize() sets the time component of each timestamp in df_cet_index to midnight
    #      while preserving the CET timezone.
    #    - .tz_convert('UTC') then converts these CET midnight timestamps to their
    #      corresponding UTC timestamps. This is crucial for correctly handling DST shifts.
    utc_from = df_cet_index.normalize().tz_convert('UTC')

    # 5. Calculate the difference in hours between 'utc_from' and 'df_utc_index'
    # This difference represents the elapsed time in hours since the start of the
    # delivery day (in CET) in a UTC-consistent manner, effectively accounting for DST.
    hours = (df_utc_index - utc_from).total_seconds() / 3600

    # 6. Calculate the 'period' based on the 'time_resolution' column vectorially
    # Initialize a Series for periods
    period = pd.Series(np.zeros(len(df), dtype=int), index=df.index)

    # Apply calculation for "PT60M" resolution
    is_60m = df['time_resolution'] == "PT60M"
    period.loc[is_60m] = (hours[is_60m]).astype(int) + 1

    # Apply calculation for "PT15M" resolution
    is_15m = df['time_resolution'] == "PT15M"
    period.loc[is_15m] = (hours[is_15m] * 4).astype(int) + 1

    # Assign the newly calculated columns back to the DataFrame
    df['delivery_date'] = delivery_date
    df['period'] = period
    return df


def download_long_period(client, curve, start_date, end_date, step_days=100, **params):
    """
    Download data over a long period by splitting into smaller chunks
    """
    all_data = []
    current_date = start_date
    chunk_number = 1

    print(f"📅 Downloading data from {start_date} to {end_date} in {step_days}-day chunks")
    print("=" * 60)

    while current_date <= end_date:
        # Calculate chunk end date
        chunk_end = min(current_date + timedelta(days=step_days - 1), end_date)

        print(f"📦 Chunk {chunk_number}: {current_date} to {chunk_end}", end=" ")

        try:
            # Download chunk
            response = client.get(
                curve=curve,
                date_from=current_date,
                date_to=chunk_end,
                **params
            )

            # Convert to DataFrame and add to collection
            chunk_df = response.to_pandas_cet()
            all_data.append(chunk_df)

            print(f"✅ {len(response)} points")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

        # Move to next chunk
        current_date = chunk_end + timedelta(days=1)
        chunk_number += 1

    # Combine all chunks
    if all_data:
        final_df = pd.concat(all_data, ignore_index=False)
        final_df = final_df.sort_index()  # Ensure chronological order

        print(f"\n🎉 Download complete!")
        print(f"📊 Total data points: {len(final_df)}")
        print(f"📅 Period: {final_df.index.min()} to {final_df.index.max()}")

        return final_df
    else:
        print("❌ No data downloaded")
        return pd.DataFrame()
