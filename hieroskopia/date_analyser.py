from pandas import Series

from hieroskopia.utils.evaluator import Evaluator


class InferDatetime:
    """
    Receive a column and try to get the date or datetime
    format pattern using regexp.
    Return a dict with key named 'format'
    with the pandas patterns
    """

    @staticmethod
    def infer(series: Series, return_format='C89'):
        generic_date_pattern = "\\d{1,4}(-|\\/)\\d{1,2}(-|\\/)\\d{1,4}(?:(T| )\\d{2}:\\d{2}(?::\\d{2})?(?:\\.\\d{3,6})?(?:Z|(?: )?AM|(?: )?PM|(?: )?am|(?: )?pm)?)?"
        hour_pattern = "\\d{2}:\\d{2}:\\d{2}"
        dates_dict = {
            # Todo: Add string dates like ( 03 May 2020)
            # 1930-08-05
            "^\\d{4}-\\d{1,2}-\\d{1,2}$": {"C89": "%Y-%m-%d", 'snowflake': 'yyyy-mm-dd', 'java': 'yyyy-MM-dd'},
            # 08-05-30
            "^\\d{1,2}-\\d{1,2}-\\d{2}$": {"C89": "%m-%d-%y", 'snowflake': 'mm-dd-yy', 'java': 'MM-dd-yy'},
            # 08-05-1930
            "^\\d{1,2}-\\d{1,2}-\\d{4}$": {"C89": "%m-%d-%Y", 'snowflake': 'mm-dd-yyyy', 'java': 'MM-dd-yyyy'},
            # 8-5-30
            "^\\d{1}-\\d{1}-\\d{2}$": {"C89": "%-m/%-d/%y", 'snowflake': 'mm-dd-yy', 'java': 'M-d-yy'},
            # 1930/08/05
            "^\\d{4}/\\d{1,2}/\\d{1,2}$": {"C89": "%Y/%m/%d", 'snowflake': 'yyyy/mm/dd', 'java': 'yyyy/MM/dd'},
            # 08/05/30
            "^\\d{1,2}/\\d{1,2}/\\d{2}$": {"C89": "%m/%d/%y", 'snowflake': 'mm/dd/yy', 'java': 'MM/dd/yy'},
            # 08/05/1930
            "^\\d{1,2}/\\d{1,2}/\\d{4}$": {"C89": "%m-%d-%Y", 'snowflake': 'mm/dd/yyyy', 'java': 'MM/dd/yyyy'},
            # 8/5/30
            "^\\d{1}/\\d{1}/\\d{2}$": {"C89": "%-m/%-d/%y", 'snowflake': 'mm/dd/yy', 'java': 'M/d/yy'},
        }
        datetime_dict = {
            # 1930-08-05 12:00:05
            "^\\d{4}-\\d{1,2}-\\d{1,2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%Y-%m-%d %H:%M:%S",
                                                                'snowflake': 'yyyy-MM-dd hh:mi:ss',
                                                                'java': 'yyyy-MM-dd HH:mm:ss'},
            # 08-05-30 12:00:05
            "^\\d{1,2}-\\d{1,2}-\\d{2}$ \\d{2}:\\d{2}:\\d{2}$": {"C89": "%m-%d-%y %H:%M:%S",
                                                                 'snowflake': 'mm-dd-yy hh:mi:ss',
                                                                 'java': 'MM-dd-yy HH:mm:ss'},
            # 08-05-1930 12:00:05
            "^\\d{1,2}-\\d{1,2}-\\d{4}$ \\d{2}:\\d{2}:\\d{2}$": {"C89": "%m-%d-%Y %H:%M:%S",
                                                                 'snowflake': 'mm-dd-yyyy hh:mi:ss',
                                                                 'java': 'MM-dd-yyyy HH:mm:ss'},
            # 8-5-30 12:00:05
            "^\\d{1}-\\d{1}-\\d{2}$ \\d{2}:\\d{2}:\\d{2}$": {"C89": "%-m/%-d/%y %H:%M:%S",
                                                             'snowflake': 'mm-dd-yy hh:mi:ss',
                                                             'java': 'M-d-yy HH:mm:ss'},
            # 1930/08/05 12:00:05
            "^\\d{4}/\\d{1,2}/\\d{1,2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%Y/%m/%d %H:%M:%S",
                                                                'snowflake': 'yyyy/MM/dd hh:mi:ss',
                                                                'java': 'yyyy/MM/dd HH:mm:ss'},
            # 08/05/30 12:00:05
            "^\\d{1,2}/\\d{1,2}/\\d{2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%m/%d/%y %H:%M:%S",
                                                                'snowflake': 'MM /dd/yy hh:mi:ss',
                                                                'java': 'MM/dd/yy HH:mm:ss'},
            # 08/05/1930 12:00:05
            "^\\d{1,2}/\\d{1,2}/\\d{4} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%m-%d-%Y %H:%M:%S",
                                                                'snowflake': 'MM/dd/yyyy hh:mi:ss',
                                                                'java': 'MM/dd/yyyy HH:mm:ss'},
            # 8/5/30 12:00:05
            "^\\d{1}/\\d{1}/\\d{2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%-m/%-d/%y %H:%M:%S",
                                                            'snowflake': 'MM/dd/yy hh:mi:ss',
                                                            'java': 'M/d/yy HH:mm:ss'},
            # 2019-11-27T12:00:05.000Z
            "^\\d{4}-\\d{1,2}-\\d{1,2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$": {"C89": "%Y-%m-%dT%H:%M:%S.%fZ",
                                                                        'snowflake': 'yyyy-MM-ddTHH:mm:ss.SSZ',
                                                                        'java': "yyyy-MM-dd'T'HH:mm:ss.SS'Z'"}
        }
        # Have this column a generic date format ?
        if Evaluator(series).series_match(generic_date_pattern):
            # Have this column time ?
            formats_dict = datetime_dict if Evaluator(series).series_contains(hour_pattern) else dates_dict
            format_result = {
                'formats': [date_format.get(return_format) for (re_exp, date_format) in formats_dict.items() if
                            Evaluator(series).series_contains(re_exp)], 'type': 'datetime'}
            return format_result
        return {}
