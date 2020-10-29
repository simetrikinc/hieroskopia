from pandas import Series

import warnings
# This warning is alerting that the regex uses a capturing group but the match is not used.
warnings.filterwarnings("ignore", 'This pattern has match groups')


class Evaluator:
    series: Series

    def __init__(self, series: Series):
        self.series = series
        self.unique_series = list(self.series.dropna().unique())

    # Evaluate if all series match the pattern
    def series_match(self, pattern: str):
        return Series(
            self.unique_series).astype(str).str.match(pattern).eq(True).all()

    # Evaluate if the series contains the pattern
    def series_contains(self, pattern: str):
        return (Series(self.unique_series).astype(str).str.contains(
            pattern).eq(True).any())
