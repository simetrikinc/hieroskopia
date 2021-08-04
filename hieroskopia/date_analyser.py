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
        alternative_hour_pattern = "\\d{2}:\\d{2}"
        dates_dict = {
            # Todo: Add string dates like ( 03 May 2020)
            # 1930-08-05
            "^\\d{4}-\\d{1,2}-\\d{1,2}$": {"C89": "%Y-%m-%d", 'snowflake': 'yyyy-mm-dd', 'java': 'yyyy-MM-dd'},
            # 08-05-30
            "^\\d{1,2}-\\d{1,2}-\\d{2}$": {"C89": "%d-%m-%y", 'snowflake': 'dd-mm-yy', 'java': 'dd-MM-yy'},
            # 08-05-1930
            "^\\d{1,2}-\\d{1,2}-\\d{4}$": {"C89": "%d-%m-%Y", 'snowflake': 'dd-mm-yyyy', 'java': 'dd-MM-yyyy'},
            # 8-5-30
            "^\\d{1}-\\d{1}-\\d{2}$": {"C89": "%-d/%-m/%y", 'snowflake': 'dd-mm-yy', 'java': 'd-M-yy'},
            # 1930/08/05
            "^\\d{4}/\\d{1,2}/\\d{1,2}$": {"C89": "%Y/%m/%d", 'snowflake': 'yyyy/mm/dd', 'java': 'yyyy/MM/dd'},
            # 08/05/30
            "^\\d{1,2}/\\d{1,2}/\\d{2}$": {"C89": "%d/%m/%y", 'snowflake': 'dd/mm/yy', 'java': 'dd/MM/yy'},
            # 08/05/1930
            "^\\d{1,2}/\\d{1,2}/\\d{4}$": {"C89": "%d-%m-%Y", 'snowflake': 'dd/mm/yyyy', 'java': 'dd/MM/yyyy'},
            # 8/5/30
            "^\\d{1}/\\d{1}/\\d{2}$": {"C89": "%-d/%-m/%y", 'snowflake': 'dd/mm/yy', 'java': 'd/M/yy'},
        }
        datetime_dict = {
            # 1930-08-05 12:00:05
            "^\\d{4}-\\d{1,2}-\\d{1,2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%Y-%m-%d %H:%M:%S",
                                                                'snowflake': 'yyyy-MM-dd hh:mi:ss',
                                                                'java': 'yyyy-MM-dd HH:mm:ss'},
            # 08-05-30 12:00:05
            "^\\d{1,2}-\\d{1,2}-\\d{2}$ \\d{2}:\\d{2}:\\d{2}$": {"C89": "%d-%m-%y %H:%M:%S",
                                                                 'snowflake': 'dd-mm-yy hh:mi:ss',
                                                                 'java': 'dd-MM-yy HH:mm:ss'},
            # 08-05-1930 12:00:05
            "^\\d{1,2}-\\d{1,2}-\\d{4}$ \\d{2}:\\d{2}:\\d{2}$": {"C89": "%d-%m-%Y %H:%M:%S",
                                                                 'snowflake': 'dd-mm-yyyy hh:mi:ss',
                                                                 'java': 'dd-MM-yyyy HH:mm:ss'},
            # 8-5-30 12:00:05
            "^\\d{1}-\\d{1}-\\d{2}$ \\d{2}:\\d{2}:\\d{2}$": {"C89": "%-d/%-m/%y %H:%M:%S",
                                                             'snowflake': 'dd-mm-yy hh:mi:ss',
                                                             'java': 'd-M-yy HH:mm:ss'},
            # 1930/08/05 12:00:05
            "^\\d{4}/\\d{1,2}/\\d{1,2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%Y/%m/%d %H:%M:%S",
                                                                'snowflake': 'yyyy/MM/dd hh:mi:ss',
                                                                'java': 'yyyy/MM/dd HH:mm:ss'},
            # 08/05/30 12:00:05
            "^\\d{1,2}/\\d{1,2}/\\d{2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%d/%m/%y %H:%M:%S",
                                                                'snowflake': 'dd/MM/yy hh:mi:ss',
                                                                'java': 'dd/MM/yy HH:mm:ss'},
            # 08/05/1930 12:00:05
            "^\\d{1,2}/\\d{1,2}/\\d{4} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%d-%m-%Y %H:%M:%S",
                                                                'snowflake': 'dd/MM/yyyy hh:mi:ss',
                                                                'java': 'dd/MM/yyyy HH:mm:ss'},

            # 08/05/1930 12:00
            "^\\d{1,2}/\\d{1,2}/\\d{4} \\d{2}:\\d{2}$": {"C89": "%d/%m/%Y %H:%M",
                                                                'snowflake': 'dd/MM/yyyy hh:mi',
                                                                'java': 'dd/MM/yyyy HH:mm'},

            # 8/5/30 12:00:05
            "^\\d{1}/\\d{1}/\\d{2} \\d{2}:\\d{2}:\\d{2}$": {"C89": "%-d/%-m/%y %H:%M:%S",
                                                            'snowflake': 'dd/MM/yy hh:mi:ss',
                                                            'java': 'd/M/yy HH:mm:ss'},

            # 2019-11-27 12:00:05.000000
            r"^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}.\d{1,6}$": {"C89": "%Y-%m-%d %H:%M:%S.%f",
                                                                   'snowflake': 'yyyy-MM-dd HH:mm:ss.S',
                                                                   'java': "yyyy-MM-dd HH:mm:ss.S"},

            # 2019-11-27T12:00:05.000Z
            r"^\d{4}-\d{1,2}-\d{1,2}T\d{2}:\d{2}:\d{2}.\d{3,6}Z": {"C89": "%Y-%m-%dT%H:%M:%S.%fZ",
                                                                   'snowflake': 'yyyy-MM-ddTHH:mm:ss.SZ',
                                                                   'java': "yyyy-MM-dd'T'HH:mm:ss.S'Z'"},
            # 2019-11-27 12:00:05.0000000000 special case
            # Others workarounds: [:26], Capture 6 digits after dot in a group, etc...
            # Todo: Delete on snowflake casts
            r"^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}.\d{10}$": {"C89": "%Y-%m-%d %H:%M:%S.%f0000",
                                                                  'snowflake': "yyyy-MM-dd HH:mm:ss.S0000",
                                                                  'java': "yyyy-MM-dd HH:mm:ss.S0000"},

            r"^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}.\d{9}$": {"C89": "%Y-%m-%d %H:%M:%S.%f000",
                                                                  'snowflake': "yyyy-MM-dd HH:mm:ss.S000",
                                                                  'java': "yyyy-MM-dd HH:mm:ss.S000"},


        }
        # Have this column a generic date format ?
        if Evaluator(series).series_match(generic_date_pattern):
            # Have this column time ?
            format_type = 'datetime'
            if Evaluator(series).series_contains(hour_pattern) or Evaluator(series).series_contains(alternative_hour_pattern):
                formats_dict = datetime_dict
            else:
                formats_dict = dates_dict
                format_type = 'date'
            format_result = {
                'formats': [date_format.get(return_format) for (re_exp, date_format) in formats_dict.items() if
                            Evaluator(series).series_contains(re_exp)], 'type': format_type}
            return format_result
        return {}
