from pandas import Series

from hieroskopia.utils.evaluator import Evaluator


class InferDatetime(object):
    """
    Receive a column and try to get the date or datetime
    format pattern using regexp.
    Return a dict with key named 'format'
    with the pandas patterns
    """

    @staticmethod
    def infer(series: Series):
        generic_date_pattern = "\\d{1,4}(-|\\/)\\d{1,2}(-|\\/)\\d{1,4}(?:(T| )\\d{2}:\\d{2}(?::\\d{2})?(?:\\.\\d{3,6})?(?:Z|(?: )?AM|(?: )?PM|(?: )?am|(?: )?pm)?)?"
        hour_pattern = "\\d{2}:\\d{2}:\\d{2}"
        dates_dict = {
            # Todo: Add string dates like ( 03 May 2020)
            # 1930-08-05
            "^\\d{4}-\\d{1,2}-\\d{1,2}$": "%Y-%m-%d",
            # 08-05-30
            "^\\d{1,2}-\\d{1,2}-\\d{2}$": "%m-%d-%y",
            # 08-05-1930
            "^\\d{1,2}-\\d{1,2}-\\d{4}$": "%m-%d-%Y",
            # 8-5-30
            "^\\d{1}-\\d{1}-\\d{2}$": "%-m/%-d/%y",
            # 1930/08/05
            "^\\d{4}/\\d{1,2}/\\d{1,2}$": "%Y/%m/%d",
            # 08/05/30
            "^\\d{1,2}/\\d{1,2}/\\d{2}$": "%m/%d/%y",
            # 08/05/1930
            "^\\d{1,2}/\\d{1,2}/\\d{4}$": "%m-%d-%Y",
            # 8/5/30
            "^\\d{1}/\\d{1}/\\d{2}$": "%-m/%-d/%y",
        }
        datetime_dict = {
            # 1930-08-05 12:00:05
            "^\\d{4}-\\d{1,2}-\\d{1,2}$": "%Y-%m-%d %H:%M:%S ",
            # 08-05-30 12:00:05
            "^\\d{1,2}-\\d{1,2}-\\d{2}$": "%m-%d-%y %H:%M:%S",
            # 08-05-1930 12:00:05
            "^\\d{1,2}-\\d{1,2}-\\d{4}$": "%m-%d-%Y %H:%M:%S",
            # 8-5-30 12:00:05
            "^\\d{1}-\\d{1}-\\d{2}$": "%-m/%-d/%y %H:%M:%S",
            # 1930/08/05 12:00:05
            "^\\d{4}/\\d{1,2}/\\d{1,2}$": "%Y/%m/%d %H:%M:%S",
            # 08/05/30 12:00:05
            "^\\d{1,2}/\\d{1,2}/\\d{2}$": "%m/%d/%y %H:%M:%S",
            # 08/05/1930 12:00:05
            "^\\d{1,2}/\\d{1,2}/\\d{4}$": "%m-%d-%Y %H:%M:%S",
            # 8/5/30 12:00:05
            "^\\d{1}/\\d{1}/\\d{2}$": "%-m/%-d/%y %H:%M:%S",
            # 2019-11-27T12:00:05.000Z
            "^\\d{4}-\\d{1,2}-\\d{1,2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$": "%Y-%m-%dT%H:%M:%S.%fZ"
        }
        # Have this column a generic date format ?
        if Evaluator(series).series_match(generic_date_pattern):
            # Have this column time ?
            formats_dict = datetime_dict if Evaluator(series).series_contains(hour_pattern) else dates_dict
            format_result = {'formats': [date_format for (re_exp, date_format) in formats_dict.items() if
                             Evaluator(series).series_contains(re_exp)]}
            return format_result

        return {}
