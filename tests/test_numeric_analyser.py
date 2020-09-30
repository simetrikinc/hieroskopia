import pandas as pd
from hieroskopia import InferNumeric


class TestNumericAnalyser(object):
    @staticmethod
    def numeric_analyser_unittest(expected_list: list, data: dict):
        # Create test data frame
        df = pd.DataFrame(data)
        # Result list with format dicts
        result_list = []
        # Loop every df columns
        for col in df.columns:
            # Infer data format
            result_list.append(InferNumeric.infer(df[col]))
        # Print lists
        print('\n', '  Result list:', result_list, '\n', 'Expected list:',
              expected_list)
        # Test lists
        assert expected_list == result_list

    def test_numeric_analyser(self):
        """
        Bad argument:
        Special logic:
        Boundary Values:
        """
        self.numeric_analyser_unittest(expected_list=[[],
                                                      [],
                                                      [{'three_digit_separator': '', 'decimal_separator': '.'}],
                                                      [{'three_digit_separator': '', 'decimal_separator': '.'}]],
                                       data={
                                           "date": ["2019-11-27",
                                                    "2019-11-28",
                                                    "2019-11-29"],
                                           "gateway": ["PROSA", "PROSA", "PROSA"],
                                           "amount": ["$4591", "$4592", "-$.5"],
                                           "order_id": ['767313628196.2', '76731362819.6', '767313628196']
                                       })
