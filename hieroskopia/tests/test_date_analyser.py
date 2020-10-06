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
        if expected_list != result_list:
            raise AssertionError

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
            expected_list=[{'formats': expected, 'type': 'datetime'}, {}, {}, {}], data={
                "date": ["2019-11-27",
                         "2019/11/28",
                         "2018-11-08"],
                "gateway": ["PROSA", "PROSA", "PROSA"],
                "amount": ["$4591", "$4592", "$4593"],
                "order_id": [767313628196, 767313628196, 767313628196]
            }, return_format=return_formats)
