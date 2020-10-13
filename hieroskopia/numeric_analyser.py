import re

import numpy as np
from pandas import Series

from hieroskopia.utils.evaluator import Evaluator


class InferNumeric:
    """
    Receive a column and try to analyze  the three digit separator,
    the decimal separator and get the numeric format pattern
    using regexp
    Return a dict with key named 'format'
    with the pandas patterns
    """

    @staticmethod
    def infer(series: Series):
        # Identify stage
        numeric_dict = {
            # ($)(+-) 1234 or 1234.12
            r'^([+-]?([0-9]*)(\.([0-9]+))?)$': {
                'three_digit_separator': '',
                'decimal_separator': '.'
            },
            # ($)(+-) 12,345 or 12,345.1234
            "^[+-]?\\d{1,3}(,\\d{3})*(\\.\\d+)?$": {
                'three_digit_separator': ',',
                'decimal_separator': '.'
            }
        }

        simple_int_pattern = r'[-+]?\d+'
        chars_not_allowed = r'[^\d,.\-\+]'

        # Todo: Add more currencies symbols and code & Support intermediate space by parameter
        # Trim Currencies
        series = series.astype(str).str.replace(r'[\$€£¥R]', '', regex=True)
        # Trim lateral spaces
        series = series.str.strip()
        # Add 0 if start with .
        series = Series(np.array(
            [re.sub(r'^(?=.)([+-]?)(\.)([0-9]*)$', '\\g<1>0\\g<2>\\g<3>', str(s)) for s in
             series.values])) if Evaluator(
            series).series_contains(r'^(?=.)([+-]?)(\.)([0-9]*)$') else series

        # If the series contains any number and not have any invalid character
        if Evaluator(series).series_match(simple_int_pattern) and not Evaluator(series).series_match(chars_not_allowed):
            # Validate each regular expression into the series
            for (re_exp, numeric_format) in numeric_dict.items():
                # If any regexp match, save this as its format
                if Evaluator(series).series_match(re_exp):
                    format_result = numeric_format
                    # Classify as float if the series have the decimal separator found in the regexp
                    format_result.update(type='float') if Evaluator(series).series_contains('\\' + format_result.get(
                        'decimal_separator')) else format_result.update(type='integer')
                    return format_result
        return {}
