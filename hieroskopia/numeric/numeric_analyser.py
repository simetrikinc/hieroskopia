from pandas import Series

from ..utils.evaluator import Evaluator


class NumericAnalyser(object):
    """
    Receive a column and try to analyze  the three digit separator,
    the decimal separator and get the numeric format pattern
    using regexp
    Return a dict with key named 'format'
    with the pandas patterns
    """

    @staticmethod
    def numeric_format_matcher(series: Series):
        # Identify stage
        numeric_dict = {
            # -1234 or -1234.12
            "^(?=.)([+-]?([0-9]*)(\\.([0-9]+))?)$": {
                'three_digit_separator': '',
                'decimal_separator': '.'
            },
            # -12,345.1234
            "^[-]?\\d{1,3}(,\\d{3})*(\\.\\d+)?$": {
                'three_digit_separator': ',',
                'decimal_separator': '.'
            }
        }

        simple_int_pattern = "\\d+"
        chars_not_allowed = r'[^\d,.\s\-\+]'

        # Trim whitespaces and currencies
        series = series.astype(str).str.replace(r'[\$€£¥ ]', '', regex=True)
        if Evaluator.series_match(series, simple_int_pattern) and not Evaluator.series_match(series, chars_not_allowed):
            format_result = [numeric_format for (re_exp, numeric_format) in
                             numeric_dict.items() if
                             Evaluator.series_match(series, re_exp)]
            return format_result
        else:
            return []
