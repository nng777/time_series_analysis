import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate a time series with a clear pattern (sine wave)
def generate_sine_wave(timesteps=100):
    t = np.linspace(0, 10, timesteps)
    # Introduce some noise to make it more realistic
    noise = np.random.normal(0, 0.2, timesteps)
    return pd.Series(np.sin(t) + noise, index=pd.to_datetime(pd.date_range('2023-01-01', periods=timesteps)))

# Calculate the moving average of a time series
def moving_average(series, window):
    return series.rolling(window=window).mean()

# --- Main Application ---
if __name__ == "__main__":
    # 1. Generate and Visualize Data
    time_series = generate_sine_wave()
    plt.figure(figsize=(12, 6))
    plt.plot(time_series, label='Original Data')
    plt.title('Time Series Data (Sine Wave with Noise)')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('time_series_plot.png')
    plt.show()

    # 2. Calculate and Plot Moving Average
    window_size = 5
    ma_series = moving_average(time_series, window_size)
    plt.figure(figsize=(12, 6))
    plt.plot(time_series, label='Original Data')
    plt.plot(ma_series, label=f'{window_size}-Day Moving Average', linestyle='--')
    plt.title('Time Series with Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('moving_average_plot.png')
    plt.show()

    # 3. Forecast the Next Value
    last_values = time_series.tail(window_size)
    forecast = last_values.mean()
    print(f"\n--- Forecasting ---")
    print(f"Last {window_size} values: \n{last_values.to_string()}")
    print(f"\nPredicted next value: {forecast:.2f}")
