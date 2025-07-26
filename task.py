import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import argparse

"""try:
    import yfinance as yf
except ImportError:
    raise SystemExit(
        "The 'yfinance' package is required to run this script. Install it via pip"
    )
"""

def fetch_stock_data(symbol: str, period: str = "1mo") -> pd.DataFrame:
    """Download recent stock prices for the given symbol."""
    try:
        tickers = yf.Tickers(symbol)
        ticker = tickers.tickers.get(symbol)
        if ticker is None:
            raise ValueError(f"Symbol '{symbol}' not recognized")
        df = ticker.history(period=period)
    except Exception as exc:  # covers network issues and invalid symbols
        raise SystemExit(
            f"Failed to get ticker '{symbol}' reason: {exc}"
        )

    if df.empty:
        raise SystemExit(
            f"{symbol}: No price data found, symbol may be delisted (period={period})"
            " or network unavailable"
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


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Plot stock closing prices and forecast next value")
    parser.add_argument("symbol", nargs="?", default="MSFT", help="Stock ticker symbol")
    parser.add_argument("--period", default="1mo", help="Period to download, e.g. 1mo or 3mo")
    parser.add_argument("--window", type=int, default=7, help="Moving average window")
    return parser.parse_args()


def main(symbol: str = "MSFT", window: int = 7, period: str = "1mo") -> None:
    df = fetch_stock_data(symbol, period=period)

    close_series = df["Close"]
    ma_series = close_series.rolling(window=window).mean()

    plot_series(close_series, ma_series, symbol, window)

    forecast = close_series.tail(window).mean()
    print("--- Forecasting ---")
    print(close_series.tail(window))
    print(f"\nPredicted next closing price for {symbol}: {forecast:.2f} USD")


if __name__ == "__main__":
    args = parse_args()
    main(args.symbol, window=args.window, period=args.period)