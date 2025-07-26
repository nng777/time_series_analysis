import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def fetch_time_series(
    symbol: str, start: str | None = None, end: str | None = None
) -> pd.Series:
    """Download a daily stock price time series for ``symbol`` from Yahoo Finance.

    ``yfinance`` changed the default of ``auto_adjust`` to ``True`` which adjusts
    prices for dividends and splits. Explicitly setting ``auto_adjust`` avoids a
    future warning and makes the behaviour clear.
    """
    data = yf.download(
        symbol,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
    )
    return data["Close"]


def moving_average(series: pd.Series, window: int) -> pd.Series:
    """Return the moving average for ``series`` with the given ``window`` size."""
    return series.rolling(window=window).mean()


def forecast_next(series: pd.Series, window: int) -> float:
    """Predict the next value as the mean of the last ``window`` observations."""
    return float(series.tail(window).mean())


def main() -> None:
    symbol = "AAPL"  # Apple Inc.
    start_date = "2023-01-01"

    time_series = fetch_time_series(symbol, start=start_date)

    # Plot the stock prices
    plt.figure(figsize=(12, 6))
    time_series.plot(label="Stock Price")
    plt.title(f"{symbol} Daily Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.savefig("aapl_stock_prices.png")
    #plt.show()

    # Calculate and plot a 7-day moving average
    window_size = 7
    ma_series = moving_average(time_series, window_size)
    plt.figure(figsize=(12, 6))
    plt.plot(time_series, label='Original Data')
    plt.plot(ma_series, label=f'{window_size}-Day Moving Average', linestyle='--')
    plt.title(f"{symbol} Stock Price with {window_size}-Day Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.savefig("aapl_moving_average.png")
    #plt.show()

    # Forecast the next value
    predicted = forecast_next(time_series, window_size)
    print(f"Predicted next stock price for {symbol} (mean of last {window_size} days): {predicted:.2f}")

    # Conclusion message
    print(
        "Using a simple moving average, we predicted the next stock price based on recent prices. "
        "This approach is a basic forecasting technique and works best when trends are relatively stable."
    )


if __name__ == "__main__":
    main()