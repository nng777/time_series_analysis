# Time Series Forecasting App

This simple Python application demonstrates the basics of time series analysis and forecasting. It generates a synthetic time series, visualizes it, calculates a moving average, and makes a simple forecast.

## How to Run the App

1.  **Install Dependencies:**

    Make sure you have Python installed. Then, install the required libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Script:**

    Execute the `app.py` script from your terminal:

    ```bash
    python app.py
    ```

## What the App Does

1.  **Generates Data:**

    *   The app creates a time series based on a sine wave with some random noise to simulate real-world data.
    *   It saves a plot of this data as `time_series_plot.png`.

2.  **Calculates Moving Average:**

    *   It computes a 5-day moving average to smooth out the data and identify the underlying trend.
    *   It saves a plot comparing the original data and the moving average as `moving_average_plot.png`.

3.  **Makes a Forecast:**

    *   The app uses the last 5 data points to predict the next value in the series by calculating their average.
    *   It prints the last few values and the final prediction to the console.

This application provides a hands-on example of the concepts covered in our lesson on time series analysis.
