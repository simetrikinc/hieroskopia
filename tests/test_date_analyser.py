import pandas as pd

from hieroskopia import InferDatetime


class TestDateAnalyser(object):
    @staticmethod
    def date_analyser_unittest(expected_list: list, data: dict):
        # Create test data frame
        df = pd.DataFrame(data)
        # Result list with format dicts
        result_list = []
        # Loop every df columns
        for col in df.columns:
            # Infer data format
            result_list.append(InferDatetime.infer(df[col]))
        # Print lists
        print('\n', '  Result list:', result_list, '\n', 'Expected list:',
              expected_list)
        # Test lists
        assert expected_list == result_list

    def test_date_analyser(self):
        """
        Bad argument:
        Special logic:
        Boundary Values:
        """
        self.date_analyser_unittest(expected_list=[{'formats': ['%Y-%m-%d', '%Y/%m/%d']}, {}, {}, {}], data={
            "date": ["2019-11-27",
                     "2019/11/28",
                     "2018-11-08"],
            "gateway": ["PROSA", "PROSA", "PROSA"],
            "amount": ["$4591", "$4592", "$4593"],
            "order_id": [767313628196, 767313628196, 767313628196]
        })
