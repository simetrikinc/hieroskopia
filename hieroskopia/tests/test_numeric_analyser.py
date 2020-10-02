import pandas as pd

from hieroskopia import InferNumeric


class TestNumericAnalyser:
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
        if expected_list != result_list:
            raise AssertionError

    def test_numeric_analyser(self):
        """
        Bad argument:
        Special logic:
        Boundary Values:
        """
        self.numeric_analyser_unittest(expected_list=[{},
                                                      {},
                                                      {'three_digit_separator': '', 'decimal_separator': '.',
                                                       'type': 'integer'},
                                                      {'three_digit_separator': ',', 'decimal_separator': '.',
                                                       'type': 'float'}],
                                       data={
                                           "date": ["2019-11-27",
                                                    "2019-11-28",
                                                    "2019-11-29"],
                                           "gateway": ["PROSA", "PROSA", "PROSA"],
                                           "amount": ["$4591", "$4592", "-$5"],
                                           "order_id": ['767,313,628,196.2', '76,731,362,819', '767,313,628,196']
                                       })
