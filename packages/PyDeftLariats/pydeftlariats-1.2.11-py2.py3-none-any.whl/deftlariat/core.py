"""Main module."""
__version__ = '0.0.1'

from abc import ABC, abstractmethod
import logging

from hamcrest import anything, match_equality, equal_to, has_item, starts_with, \
    greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, \
    close_to, contains_string, string_contains_in_order, equal_to_ignoring_case, \
    equal_to_ignoring_whitespace, not_none, none, any_of, all_of, is_not, \
    has_entry, has_entries

# TODO: did not utilize the "is_" function from hamcrest


from enum import Enum


class MatcherType(Enum):
    NOTHING = 'Nothing'
    ANYTHING = 'Anything'
    EQUAL_TO = 'EqualTo'
    STARTS_WITH = 'StartsWith'
    CONTAINS_STRING = 'ContainsString'
    CONTAINS_STRING_IN_ORDER = 'ContainsStringInOrder'
    EQUAL_TO_IGNORE_CASE = 'EqualToIgnoreCase'
    EQUAL_TO_IGNORE_WHITESPACE = 'EqualToIgnoreWhitespace'
    GREATER_THAN = 'GreaterThan'
    GREATER_THAN_EQUAL_TO = 'GreaterThanEqualTo'
    LESS_THAN = 'LessThan'
    LESS_THAN_EQUAL_TO = 'LessThanEqualTo'
    CLOSE_TO = 'CloseTo'
    NONE = 'None'
    NONE_OR_EMPTY = 'NoneOrEmpty'
    NOT_NONE = 'NotNone'
    NOT_NONE_OR_EMPTY = 'NotNoneOrEmpty'
    HAS_ENTRY = 'HasEntry'
    HAS_ENTRIES = 'HasEntries'


# pull values from list...support for list of input parameters and *list syntax
def pull_val(x):
    return x


class Matcher(ABC):

    def __init__(self, match_col_key):
        self.matcher_type = MatcherType.NOTHING
        self.match_col_key = match_col_key
        self.my_logger = logging.getLogger('matching')

    @abstractmethod
    def is_match(self, match_values, data_record) -> bool:
        pass

    def validate_key_exists(self, data_record) -> bool:
        """ Validate match-key-column exists in data record"""

        if self.match_col_key not in data_record:
            self.my_logger.warning((f"'{self.match_col_key}' not present"
                                    f" in data record \n\n{data_record}. Matcher will return False\n\n"))
            return False
        else:
            return True

    def get_key_val(self):
        """ Generate a value suitable for hashing, dictionary key"""
        return frozenset((self.matcher_type.value, self.match_col_key))

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.matcher_type!r}, {self.match_col_key!r})')

    def __str__(self):
        return (f'Matcher for {self.matcher_type.value!r} '
                f'matching on field {self.match_col_key!r}')

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.matcher_type, self.match_col_key) == \
                (other.matcher_type, other.match_col_key)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.__class__, self.matcher_type, self.match_col_key))


class NothingMatcher(Matcher):
    """
    Matcher never successfully matches any input. Always returns False.
    """

    def __init__(self, match_col_key):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.NOTHING

    def is_match(self, match_values, data_record) -> bool:
        self.my_logger.info("No Matcher set, defaults to Nothing Matcher. Always False.")
        return False


class AnythingMatcher(Matcher):
    """
    Matcher always successfully matches any input. Always returns True.
    """

    def __init__(self, match_col_key):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.ANYTHING
        self.my_matcher = anything(f"Anything for {match_col_key}")

    def is_match(self, match_values, data_record) -> bool:
        return match_equality(self.my_matcher) == data_record


class EqualTo(Matcher):
    """ Equal To matching style. Cast everything to str. """

    def __init__(self, match_col_key, ):
        super().__init__(match_col_key, )
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.EQUAL_TO

    def is_match(self, match_values, data_record) -> bool:
        if not self.validate_key_exists(data_record):
            return False

        if len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, raising Error")
            raise NotImplementedError("Cannot use Equal To to check for empty "
                                      "string. Use None or Not_None.")

        elif isinstance(match_values, list):
            if len(match_values) == 0:
                # covered by len ==0 above
                pass

            elif len(match_values) == 1 and not isinstance(data_record[self.match_col_key], list):
                q_match_values = pull_val(*match_values)
                return (match_equality(equal_to(q_match_values))
                        == data_record[self.match_col_key])

            else:
                # has_item will iterate a sequence ...
                if isinstance(data_record[self.match_col_key], list):
                    check_list = []
                    for dr in data_record[self.match_col_key]:
                        check_list.append(match_equality(
                            has_item(equal_to(dr))) == [x for x in match_values])
                    return any(check_list)
                else:
                    return (match_equality(
                        has_item(equal_to(data_record[self.match_col_key]))) == [x for x in match_values])
        else:
            return (match_equality(equal_to(match_values))
                    == data_record[self.match_col_key])


class TextComparer(Matcher):

    def __init__(self, match_col_key, matcher_type):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key

        if matcher_type == MatcherType.STARTS_WITH:
            self.matcher_type = MatcherType.STARTS_WITH
            self.my_matcher = starts_with

        elif matcher_type == MatcherType.CONTAINS_STRING:
            self.matcher_type = MatcherType.CONTAINS_STRING
            self.my_matcher = contains_string

        elif matcher_type == MatcherType.CONTAINS_STRING_IN_ORDER:
            self.matcher_type = MatcherType.CONTAINS_STRING_IN_ORDER
            self.my_matcher = string_contains_in_order

        elif matcher_type == MatcherType.EQUAL_TO_IGNORE_CASE:
            self.matcher_type = MatcherType.EQUAL_TO_IGNORE_CASE
            self.my_matcher = equal_to_ignoring_case

        elif matcher_type == MatcherType.EQUAL_TO_IGNORE_WHITESPACE:
            self.matcher_type = MatcherType.EQUAL_TO_IGNORE_WHITESPACE
            self.my_matcher = equal_to_ignoring_whitespace

        else:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")

    def is_match(self, match_values, data_record) -> bool:

        if not self.validate_key_exists(data_record):
            return False

        if len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, raising Error")
            raise NotImplementedError(f"Cannot use {self.matcher_type.value} to check for "
                                      "empty string. Use None or Not_None.")

        elif isinstance(match_values, list):

            if len(match_values) == 1:
                q_match_values = pull_val(*match_values)
                return (match_equality(self.my_matcher(q_match_values))
                        == str(data_record[self.match_col_key]))
            else:
                matches_list = [q for q in match_values
                                if match_equality(self.my_matcher(q))
                                == str(data_record[self.match_col_key])]
                if len(matches_list) > 0:
                    return True
                else:
                    return False
        else:
            return (match_equality(self.my_matcher(match_values))
                    == str(data_record[self.match_col_key]))


class NumberComparer(Matcher):

    def __init__(self, match_col_key, matcher_type, convert_none_to=None):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key
        self.replacement_val = None
        if convert_none_to is None:
            self.convert_none = False
        else:
            self.convert_none = True
            self.replacement_val = convert_none_to

        if matcher_type == MatcherType.GREATER_THAN:
            self.matcher_type = MatcherType.GREATER_THAN
            self.my_matcher = greater_than

        elif matcher_type == MatcherType.GREATER_THAN_EQUAL_TO:
            self.matcher_type = MatcherType.GREATER_THAN_EQUAL_TO
            self.my_matcher = greater_than_or_equal_to

        elif matcher_type == MatcherType.LESS_THAN:
            self.matcher_type = MatcherType.LESS_THAN
            self.my_matcher = less_than

        elif matcher_type == MatcherType.LESS_THAN_EQUAL_TO:
            self.matcher_type = MatcherType.LESS_THAN_EQUAL_TO
            self.my_matcher = less_than_or_equal_to

        elif matcher_type == MatcherType.CLOSE_TO:
            self.matcher_type = MatcherType.CLOSE_TO
            self.my_matcher = close_to
        else:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")

    def get_record_value(self, data_record) -> int:
        """  If you want to convert a None to an Int, set a replacement value. """
        if self.convert_none and data_record[self.match_col_key] is None:
            return_val = self.replacement_val
        else:
            return_val = data_record[self.match_col_key]
        return return_val

    def is_match(self, match_values, data_record) -> bool:
        if not self.validate_key_exists(data_record):
            return False

        if isinstance(match_values, list):
            if len(match_values) == 0:
                self.my_logger.warning("No Match Values provided, raising Error")
                cls_name = self.__class__.__name__
                raise NotImplementedError(fr"Cannot use {cls_name} to check for "
                                          "empty string. Use None or Not_None.")
            elif len(match_values) == 1:
                q_match_values = pull_val(*match_values)
                test_val = self.get_record_value(data_record)
                return (match_equality(self.my_matcher(q_match_values))
                        == test_val)
            else:
                cls_name = self.__class__.__name__
                raise NotImplementedError(fr"Cannot use {cls_name} to check "
                                          " a list of values")
        else:

            if self.matcher_type == MatcherType.CLOSE_TO:
                # Expect a tuple for Close To for Num, Delta...so unpack values
                test_val = self.get_record_value(data_record)
                return (match_equality(self.my_matcher(*match_values))
                        == test_val)
            else:
                test_val = self.get_record_value(data_record)
                return (match_equality(self.my_matcher(match_values))
                        == test_val)


class ExistsMatchers(Matcher):

    def __init__(self, match_col_key, matcher_type):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key

        if matcher_type in (MatcherType.NONE, MatcherType.NONE_OR_EMPTY):
            self.matcher_type = MatcherType(matcher_type)
            self.my_matcher = none

        elif matcher_type in (MatcherType.NOT_NONE, MatcherType.NOT_NONE_OR_EMPTY):
            self.matcher_type = MatcherType(matcher_type)
            self.my_matcher = not_none

        else:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")

    def is_match(self, data_record) -> bool:

        if not self.validate_key_exists(data_record):
            return False

        if self.matcher_type in (MatcherType.NONE, MatcherType.NOT_NONE):
            return (match_equality(self.my_matcher())
                    == data_record[self.match_col_key])
        else:
            r""" Special case of chaining equal to with none """
            if self.matcher_type == MatcherType.NONE_OR_EMPTY:
                result = match_equality(any_of(
                    self.my_matcher(),
                    equal_to(''), equal_to([]), equal_to({}), equal_to(())
                )) == data_record[self.match_col_key]
                return result

            elif self.matcher_type == MatcherType.NOT_NONE_OR_EMPTY:
                result = match_equality(all_of(
                    self.my_matcher(),
                    is_not(equal_to('')), is_not(equal_to([])),
                    is_not(equal_to({})), is_not(equal_to(()))
                )) == data_record[self.match_col_key]
                return result
            else:
                raise NotImplementedError(f"Matcher for {self.matcher_type} not implemented")


class DictMatchers(Matcher):

    def __init__(self, match_col_key, matcher_type):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key

        if matcher_type == MatcherType.HAS_ENTRY:
            self.matcher_type = MatcherType(matcher_type)
            self.my_matcher = has_entry

        elif matcher_type == MatcherType.HAS_ENTRIES:
            self.matcher_type = MatcherType(matcher_type)
            self.my_matcher = has_entries

        else:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")

    def is_match(self, *match_values, data_record) -> bool:
        if not self.validate_key_exists(data_record):
            return False

        if not data_record[self.match_col_key]:
            """ If record is None or empty, no match"""
            return False

        if self.matcher_type == MatcherType.HAS_ENTRY and len(match_values) > 2:
            raise ValueError("HAS_ENTRY matcher only accepts two values")

        if isinstance(match_values[0], list) and isinstance(data_record[self.match_col_key], list):
            """ Two lists... """
            check_list = []
            for m_dict in match_values[0]:
                # Unpack list of dictionaries to list of tuples to list of match_values
                mv = [item for tup in m_dict.items() for item in tup]
                check_list.append(match_equality(has_item(has_entries(*mv))) == list(data_record[self.match_col_key]))
            return any(check_list)

        if isinstance(match_values[0], list) and isinstance(data_record[self.match_col_key], dict):
            """ Two lists... """
            check_list = []
            for m_dict in match_values[0]:
                # Unpack list of dictionaries to list of tuples to list of match_values
                mv = [item for tup in m_dict.items() for item in tup]
                check_list.append(match_equality(self.my_matcher(*mv)) == data_record[self.match_col_key])
            return any(check_list)

        if isinstance(data_record[self.match_col_key], list):
            # has_item will iterate a sequence ...
            return match_equality(has_item(has_entry(*match_values))) == list(data_record[self.match_col_key])

        if isinstance(match_values[0], dict):
            check_list = []
            for m_dict in match_values:
                # Unpack list of dictionaries to list of tuples to list of match_values
                mv = [item for tup in m_dict.items() for item in tup]
                check_list.append(match_equality(self.my_matcher(*mv)) == data_record[self.match_col_key])
            return any(check_list)

        return (match_equality(self.my_matcher(*match_values))
                == data_record[self.match_col_key])
