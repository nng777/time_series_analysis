import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

"""try:
    import yfinance as yf
except ImportError:
    raise SystemExit(
        "The 'yfinance' package is required to run this script. Install it via pip"
    )
"""

def fetch_stock_data(symbol: str, period: str = "1mo") -> pd.DataFrame:
    """Download recent stock prices for the given symbol.

    If the request fails or returns no data, a SystemExit exception is raised
    with an informative error message.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
    except Exception as exc:  # covers network issues and invalid symbols
        raise SystemExit(
            f"Failed to get ticker '{symbol}' reason: {exc}"
        ) from exc

    if df.empty:
        raise SystemExit(
            f"{symbol}: No price data found, symbol may be delisted (period={period})"
        )

    return df


def plot_series(series: pd.Series, ma_series: pd.Series, symbol: str, window: int) -> None:
    """Plot the original series and moving average."""
    plt.figure(figsize=(12, 6))
    plt.plot(series, label="Close Price")
    plt.plot(ma_series, label=f"{window}-Day MA", linestyle="--")
    plt.title(f"{symbol} Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("stock_moving_average.png")


def main(symbol: str = "AAPL", window: int = 7, period: str = "1mo") -> None:
    df = fetch_stock_data(symbol, period=period)

    close_series = df["Close"]
    ma_series = close_series.rolling(window=window).mean()

    plot_series(close_series, ma_series, symbol, window)

    forecast = close_series.tail(window).mean()
    print("--- Forecasting ---")
    print(close_series.tail(window))
    print(f"\nPredicted next closing price for {symbol}: {forecast:.2f} USD")


if __name__ == "__main__":
    main()