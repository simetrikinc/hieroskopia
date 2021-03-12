import numpy as np
import pandas as pd
import pytest

from hieroskopia import InferDatetime


class TestDateAnalyser:
    @staticmethod
    def date_analyser_unittest(expected_list: list, data: dict, return_format='C89'):
        # Create test data frame
        df = pd.DataFrame(data)
        # Result list with format dicts
        result_list = []
        # Loop every df columns
        for col in df.columns:
            # Infer data format
            result_list.append(InferDatetime.infer(df[col], return_format))
        # Print lists
        print('\n', '  Result list:', result_list, '\n', 'Expected list:',
              expected_list)
        # Test lists
        assert expected_list == result_list

    @pytest.mark.parametrize('return_formats, expected',
                             [('snowflake', ['yyyy-mm-dd', 'yyyy/mm/dd']), ('java', ['yyyy-MM-dd', 'yyyy/MM/dd']),
                              ('C89', ['%Y-%m-%d', '%Y/%m/%d'])])
    def test_date_analyser(self, return_formats, expected):
        """
        Bad argument:
        Special logic:
        Boundary Values:
        """
        self.date_analyser_unittest(
            expected_list=[{'formats': expected, 'type': 'date'}, {}, {}, {}, {}], data={
                "date": ["2019-11-27",
                         "2019/11/28",
                         "2018-11-08"],
                "gateway": ["PROSA", "PROSA", "PROSA"],
                "amount": ["$4591", "$4592", "$4593"],
                "order_id": [767313628196, 767313628196, 767313628196],
                "nan": [np.nan, np.nan, np.nan]
            }, return_format=return_formats)

    @pytest.mark.parametrize('return_formats, expected',
                             [('snowflake', ['yyyy-MM-dd hh:mi:ss', 'dd/MM/yyyy hh:mi', "yyyy-MM-dd HH:mm:ss.S0000"]),
                              ('java', ['yyyy-MM-dd HH:mm:ss', 'dd/MM/yyyy HH:mm', "yyyy-MM-dd HH:mm:ss.S0000"]),
                              ('C89', ['%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M', "%Y-%m-%d %H:%M:%S.%f0000"])])
    def test_datetime_analyser(self, return_formats, expected):
        """
        Bad argument:
        Special logic:
        Boundary Values:
        """
        self.date_analyser_unittest(
            expected_list=[{'formats': expected, 'type': 'datetime'}, {}, {},
                           {}, {}], data={
                "date": ["2019-11-27 12:00:00",
                         "28/11/2018 12:00",
                         '2021-01-12 13:23:45.0000000000', np.nan],
                "gateway": ["PROSA", "PROSA", "PROSA", "PROSA"],
                "amount": ["$4591", "$4592", "$4593", "$4594"],
                "order_id": [767313628196, 767313628196, 767313628196, 767313628196],
                "nan": [np.nan, np.nan, np.nan, np.nan]
            }, return_format=return_formats)
