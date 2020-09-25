from pandas import Series


class Evaluator(object):
    @staticmethod
    def series_match(series: Series, pattern: str):
        series = series.dropna()
        return series.astype(str).str.match(pattern).eq(True).all()

    @staticmethod
    def series_contains(series: Series, pattern: str):
        series = series.dropna()
        return series.astype(str).str.contains(pattern).eq(True).any()
