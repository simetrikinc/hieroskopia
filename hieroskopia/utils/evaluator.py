from pandas import Series


class Evaluator:
    series: Series

    def __init__(self, series: Series):
        self.series = series
        self.unique_series = list(self.series.dropna().unique())

    def series_match(self, pattern: str):
        return Series(
            self.unique_series).astype(str).str.match(pattern).eq(True).all()

    def series_contains(self, pattern: str):
        return (Series(self.unique_series).astype(str).str.contains(
            pattern).eq(True).any())
