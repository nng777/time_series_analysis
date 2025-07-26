import argparse
from json import JSONDecodeError

try:  # noqa: WPS433 - optional import guard
    import requests
except ImportError as exc:  # pragma: no cover - clearer error for missing deps
    raise SystemExit(
        "The 'requests' package is required to run this script. Install it via pip"
    ) from exc
try:  # noqa: WPS433 - allow optional import guard
    import pandas as pd
except ImportError as exc:  # pragma: no cover - clearer error for missing deps
    raise SystemExit(
        "The 'pandas' package is required to run this script. Install it via pip"
    ) from exc

try:
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover - clearer error for missing deps
    raise SystemExit(
        "The 'matplotlib' package is required to run this script. Install it via pip"
    ) from exc

try:
    import yfinance as yf
except ImportError as exc:  # pragma: no cover - clearer error for missing deps
    raise SystemExit(
        "The 'yfinance' package is required to run this script. Install it via pip"
    ) from exc



def fetch_stock_data(
    symbol: str,
    period: str = "1mo",
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    """Return recent stock prices for ``symbol`` using ``yfinance``.

    Either ``period`` or explicit ``start`` and ``end`` dates may be provided.
    Dates should be in the ``YYYY-MM-DD`` format.
    """

    try:
        if start or end:
            df = yf.download(
                symbol,
                start=start,
                end=end,
                progress=False,
                threads=False,
            )
        else:
            df = yf.download(symbol, period=period, progress=False, threads=False)
    except (requests.exceptions.RequestException, JSONDecodeError, ValueError) as exc:
        raise SystemExit(
            f"Could not retrieve data for {symbol}: {exc}. "
            "Check your internet connection or ticker symbol."
        ) from exc

    if df.empty:
        raise SystemExit(
            f"No data fetched for {symbol}. "
            "Check your internet connection or verify the ticker symbol."
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
    parser.add_argument(
        "--start",
        default="2025-01-01",
        help="Explicit start date YYYY-MM-DD",
    )
    parser.add_argument(
        "--end",
        default="2025-06-01",
        help="Explicit end date YYYY-MM-DD",
    )
    parser.add_argument("--window", type=int, default=7, help="Moving average window")
    return parser.parse_args()


def main(
    symbol: str = "MSFT",
    window: int = 7,
    period: str = "1mo",
    start: str | None = "2025-01-01",
    end: str | None = "2025-06-01",
) -> None:
    df = fetch_stock_data(symbol, period=period, start=start, end=end)

    close_series = df["Close"]
    ma_series = close_series.rolling(window=window).mean()

    plot_series(close_series, ma_series, symbol, window)

    forecast = close_series.tail(window).mean()
    print("--- Forecasting ---")
    print(close_series.tail(window))
    print(f"\nPredicted next closing price for {symbol}: {forecast:.2f} USD")


if __name__ == "__main__":
    args = parse_args()
    main(
        args.symbol,
        window=args.window,
        period=args.period,
        start=args.start,
        end=args.end,
    )