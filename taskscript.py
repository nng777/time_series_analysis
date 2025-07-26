import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf


def fetch_time_series(
    symbol: str, start: str | None = None, end: str | None = None
) -> pd.Series:
    """Download a daily stock price time series for ``symbol`` from Yahoo Finance.
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
    symbol = "XRP-USD"  # Tickers
    start_date = "2025-20-07" # yyyy-dd-mm

    time_series = fetch_time_series(symbol, start=start_date)

    # Plot the stock prices
    plt.figure(figsize=(12, 6))
    time_series.plot(label="Stock Price")
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
    plt.title(f"{symbol} Daily Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.savefig("stock_prices.png")
   #plt.show()

    # Calculate and plot a 7-day moving average
    window_size = 7
    ma_series = moving_average(time_series, window_size)
    plt.figure(figsize=(12, 6))
    plt.plot(time_series, label='Stock Price')
    plt.plot(ma_series, label=f'{window_size}-Day Moving Average', linestyle='--')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
    plt.title(f"{symbol} Stock Price with {window_size}-Day Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.savefig("moving_average.png")
    #plt.show()

    # Create a single figure containing both the stock price and moving average plots
    plt.figure(figsize=(12, 10))

    ax1 = plt.subplot(2, 1, 1)
    time_series.plot(ax=ax1, label="Stock Price")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
    ax1.set_title(f"{symbol} Daily Stock Prices")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price (USD)")
    ax1.legend()
    ax1.grid(True)

    ax2 = plt.subplot(2, 1, 2)
    time_series.plot(ax=ax2, label="Stock Price")
    ma_series.plot(
        ax=ax2,
        label=f"{window_size}-Day Moving Average",
        linestyle="--",
    )
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
    ax2.set_title(f"{symbol} Stock Price with {window_size}-Day Moving Average")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Price (USD)")
    ax2.legend()
    ax2.grid(True)

    plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.savefig("combined.png")
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