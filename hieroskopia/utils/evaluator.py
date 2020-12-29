import warnings

from pandas import Series

# This warning is alerting that the regex uses a capturing group but the match is not used.
warnings.filterwarnings("ignore", 'This pattern has match groups')


class Evaluator:
    series: Series

    def __init__(self, series: Series):
        self.series = series
        self.unique_series = list(self.series.dropna().unique())

    def series_match(self, pattern: str):
        """
        Evaluate if all series match the pattern
        """
        if len(self.unique_series) == 0:
            return False
        return Series(
            self.unique_series).astype(str).str.match(pattern).eq(True).all()

    def series_contains(self, pattern: str):
        """
        Evaluate if the series contains the pattern
        """
        return (Series(self.unique_series).astype(str).str.contains(
            pattern).eq(True).any())
