import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

def autocorrelation():
    
    # Generate a sample time series with a seasonal pattern
    np.random.seed(0)
    time = np.arange(100)
    seasonal_pattern = 10 * np.sin(2 * np.pi * time / 12)
    noise = 2 * np.random.randn(100)
    series = pd.Series(seasonal_pattern + noise)

    # Plot the series
    plt.figure(figsize=(10,4))
    plt.plot(series)
    plt.title("Sample Time Series")
    plt.show()

    # Plot the autocorrelation
    plot_acf(series, lags=40)
    plt.title("Autocorrelation Plot")
    plt.show()
