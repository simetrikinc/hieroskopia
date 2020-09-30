# Hieroskopia

[![codecov](https://codecov.io/gh/simetrikinc/hieroskopia/branch/master/graph/badge.svg)](https://codecov.io/gh/simetrikinc/hieroskopia)

The hiereskopia package is a library to infer properties like date formats or
numeric separators in pandas series of type object or string.

## Support

### Date-times:

- Support to dates and datetime format
- This library receive a series as input and try to return a dictionary with the
  format found in the series Based on the 1989 C Standard date time format code

### Numeric:

- This library receive a series as input and try to return a dictionary with the
  three digit and decimal character separator

## Usage

#### Infer datetime

```Python
>>> from hieroskopia import InferDatetime
>>> InferDatetime.infer(pd.Series(["2019-11-27",
                     "2019/11/28",
                     "2018-11-08"]))
>>> {'formats': ['%Y-%m-%d', '%Y/%m/%d']}
```

The above method works with a best guess approach to detect a format in a object
type series and try to return a `datetime.strftime`/`strptime` format that will
cover or parse the majority of the samples.

#### Infer numeric

```Python
>>> from hieroskopia import InferNumeric
>>> InferNumeric.infer(pd.Series(['767313628196.2', '76731362819.546', '767313628196']))
>>> {'three_digit_separator': '', 'decimal_separator': '.' }
```

The above method will try to detect and return certain properties in a object
type series like `three_digit_separator` or `decimal_separator` character that
will cover the majority of the samples.

## To do:

- Specify another output standard format to support java date format, snowflake
  date characters definition etc.
- Feed more regular expressions
- Add Time format
- Develop multiple algorithms to get a better precision.
