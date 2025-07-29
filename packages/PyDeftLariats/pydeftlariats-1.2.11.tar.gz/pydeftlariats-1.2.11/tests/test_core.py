from unittest import TestCase
from hamcrest import *
from deftlariat import AnythingMatcher, EqualTo, \
    Matcher, MatcherType, NumberComparer, TextComparer, ExistsMatchers, DictMatchers


class TestAnythingMatcher(TestCase):
    def test_dumb(self):
        assert_that(True, equal_to(True), "Dumb test.")

    def test_record_is_match(self):
        a_matcher = AnythingMatcher("full_record")
        test_data = dict()
        assert_that(a_matcher.is_match('full_record', test_data), equal_to(True))

        test_obj = object()
        assert_that(a_matcher.is_match('full_record', test_obj), equal_to(True))

        assert_that(a_matcher.is_match('full_record', None), equal_to(True))

        assert_that(a_matcher.is_match('full_record', 1), equal_to(True))

        assert_that(a_matcher.is_match('fish', 1), equal_to(True))

        assert_that(a_matcher.is_match('dog', 'cat'), equal_to(True))


class TestEqualTo(TestCase):
    def test_is_match_single(self):
        test_data_record = {'name': 'Scarlet Shelton'}
        name_check = EqualTo('name')

        target_value = 'Scarlet Shelton'
        assert_that(name_check.is_match(target_value, test_data_record),
                    equal_to(True),
                    "Is target value in test data?")

        target_value = 'Bob Fisher'
        assert_that(name_check.is_match(target_value, test_data_record),
                    equal_to(False),
                    "Is target value in test data?")

    def test_empty_list_raises_error(self):
        test_data_record = {'name': 'Scarlet Shelton'}

        target_value = []
        name_check = EqualTo('name')

        with self.assertRaises(NotImplementedError):
            name_check.is_match(target_value, test_data_record)

    def test_is_match_list(self):
        test_data_record = {'name': 'Scarlet Shelton'}
        name_check = EqualTo('name')

        # Test a single item list
        target_value = ['Scarlet Shelton']
        self.assertTrue(name_check.is_match(target_value, test_data_record),
                        "Check against single item list")

        # Test successful, but look for one of many people
        target_value = ['Rudy Stout', 'Todd Lee', 'Scarlet Shelton']
        self.assertTrue(name_check.is_match(target_value, test_data_record),
                        "Check against multi item list")

        # Remove Scarlet and test again, should not be found
        target_value.pop(2)
        self.assertFalse(name_check.is_match(target_value, test_data_record), "Check against list")

    def test_is_key_not_in_data(self):
        test_data_record = {'full_name': 'Scarlet Shelton'}

        # Test a single item list
        target_value = ['Scarlet Shelton']
        name_check = EqualTo('name')

        self.assertFalse(name_check.is_match(target_value, test_data_record),
                         "Check against single item list")

    def test_boolean(self):
        test_data_record = {'full_name': True}

        target_value = [False]
        name_check = EqualTo('full_name')

        self.assertFalse(name_check.is_match(target_value, test_data_record),
                         "Check boolean no match")

        self.assertTrue(name_check.is_match([True], test_data_record),
                        "Check boolean does match")


    def test_obj(self):
        class MyObject(object):
            def __init__(self, something):
                self.foo = something

            def __eq__(self, other):
                return self.foo == other.foo

        a = MyObject('cad')
        test_data_record = {'full_name': [a]}
        print(test_data_record)

        b = MyObject(None)
        name_check = EqualTo('full_name')
        target_value = [b]
        print(name_check.is_match(target_value, test_data_record))
        self.assertFalse(name_check.is_match(target_value, test_data_record),
                         "Check boolean no match")

        target_value = [MyObject('cad'), MyObject('aaa')]
        print(name_check.is_match(target_value, test_data_record))








class TestTextCompareBoundaryCases(TestCase):
    def setUp(self) -> None:

        text_matcher_types = [MatcherType.STARTS_WITH, MatcherType.CONTAINS_STRING,
                              MatcherType.CONTAINS_STRING_IN_ORDER,
                              MatcherType.EQUAL_TO_IGNORE_WHITESPACE,
                              MatcherType.EQUAL_TO_IGNORE_CASE]

        self.my_text_comparer_list = list()
        for type in text_matcher_types:
            self.my_text_comparer_list.append(TextComparer('text_col', type))

    def test_empty_input_list(self):
        test_data_record = {'text_col': "some text value"}

        target_value = []
        for comparer in self.my_text_comparer_list:
            target_value = []
            with self.assertRaises(NotImplementedError, msg=f"Checking {comparer}"):
                comparer.is_match(target_value, test_data_record)

    def test_key_not_in_data_record(self):
        test_data_record = {'rating': 'Superduper'}

        # Test a single item list
        target_value = ['Super']
        for comparer in self.my_text_comparer_list:
            target_value = []
            assert_that(comparer.is_match(target_value, test_data_record),
                        equal_to(False), 'Col not present in data recrod returns FALSE')

    def test_bad_matcher_type(self):

        with self.assertRaises(NotImplementedError):
            self.comparer = TextComparer("Foo", MatcherType.GREATER_THAN_EQUAL_TO)


class TestStartsWith(TestCase):
    def test_dumb(self):
        self.assertTrue(True)

    def test_is_match_multiple_values(self):
        test_data_record = {'equipment': 'baseball'}
        ball_starts_with = TextComparer('equipment', MatcherType.STARTS_WITH)

        # Test a single item list
        target_value = ['base']
        self.assertTrue(ball_starts_with.is_match(target_value, test_data_record),
                        "find one of the balls")

        # Test a longer list
        target_value = ['foot', 'soccer', 'base']
        self.assertTrue(ball_starts_with.is_match(target_value, test_data_record),
                        "find one of the balls")

        # Test a longer list, that will fail
        target_value = ['foot', 'soccer', 'basket']
        self.assertFalse(ball_starts_with.is_match(target_value, test_data_record),
                         "No balls to find")

    def test_is_match_single_value(self):
        test_data_record = {'rating': 'Superduper'}

        # Test a single item list
        target_value = 'Super'
        rating_starts_with = TextComparer('rating', MatcherType.STARTS_WITH)

        self.assertTrue(rating_starts_with.is_match(target_value, test_data_record),
                        "looking at field not in data record")

    def test_is_match_convert_to_str(self):
        test_data_record = {'department': 11223344}
        dept_starts_with = TextComparer('department', MatcherType.STARTS_WITH)

        # Test a single item
        target_value = '1122'
        self.assertTrue(dept_starts_with.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item list
        target_value = ['1122']
        self.assertTrue(dept_starts_with.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a multiple item list
        target_value = ['2222', '1122', '3333']
        self.assertTrue(dept_starts_with.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item  -- No Match
        target_value = '122'
        self.assertFalse(dept_starts_with.is_match(target_value, test_data_record),
                         "No-Match - one of departments")


class TestEqualToIgnoreCase(TestCase):
    def test_dumb(self):
        self.assertTrue(True)

    def test_is_match_multiple_values(self):
        test_data_record = {'equipment': 'basEBAll'}
        eq_ignore_case = TextComparer('equipment', MatcherType.EQUAL_TO_IGNORE_CASE)

        # Test a single item list
        target_value = ['baseball']
        self.assertTrue(eq_ignore_case.is_match(target_value, test_data_record),
                        "find one of the balls")

        # Test a longer list
        target_value = ['football', 'baseball']
        self.assertTrue(eq_ignore_case.is_match(target_value, test_data_record),
                        "find one of the balls")

        # Test a longer list, that will fail
        target_value = ['foot', 'soccer', 'basket']
        self.assertFalse(eq_ignore_case.is_match(target_value, test_data_record),
                         "No balls to find")

    def test_ignore_whitespace(self):
        test_data_record = {'department': 11223344}
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE)

        # Test a single item
        target_value = '11223344'
        self.assertTrue(eq_ignore_whitespace.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item list
        target_value = ['11223344']
        self.assertTrue(eq_ignore_whitespace.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a multiple item list
        target_value = ['2222', '1122', '11223344']
        self.assertTrue(eq_ignore_whitespace.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item  -- No Match
        target_value = '122'
        self.assertFalse(eq_ignore_whitespace.is_match(target_value, test_data_record),
                         "No-Match - one of departments")

        test_data_record = {'department': '  11223344  '}
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE)

        # Test a single item
        target_value = '11223344'
        self.assertTrue(eq_ignore_whitespace.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item list
        target_value = ['11223344']
        self.assertTrue(eq_ignore_whitespace.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a multiple item list
        target_value = ['2222', '1122', '11223344']
        self.assertTrue(eq_ignore_whitespace.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item  -- No Match
        target_value = '122'
        self.assertFalse(eq_ignore_whitespace.is_match(target_value, test_data_record),
                         "No-Match - one of departments")


class TestNumberComparisons(TestCase):

    def setUp(self):
        self.number_gt_check = NumberComparer('my_number', MatcherType.GREATER_THAN)
        self.number_gte_check = NumberComparer('my_number', MatcherType.GREATER_THAN_EQUAL_TO)
        self.number_lt_check = NumberComparer('my_number', MatcherType.LESS_THAN)
        self.number_lte_check = NumberComparer('my_number', MatcherType.LESS_THAN_EQUAL_TO)
        self.number_close_check = NumberComparer('my_number', MatcherType.CLOSE_TO)

    def test_dumb(self):
        self.assertTrue(True)

    def test_single_value(self):
        test_data_record = {'my_number': 5}

        # Test a single item
        target_value = 4
        self.assertTrue(self.number_gt_check.is_match(target_value, test_data_record),
                        " 5 > 4 = True")
        self.assertTrue(self.number_gte_check.is_match(target_value, test_data_record),
                        " 5 >= True ")
        self.assertFalse(self.number_lt_check.is_match(target_value, test_data_record),
                         " 5 < 4 = False")
        self.assertFalse(self.number_lte_check.is_match(target_value, test_data_record),
                         " 5 <= 4 = False ")
        self.assertTrue(self.number_close_check.is_match((target_value, 2), test_data_record),
                        " 5 close to (4,2) = True")
        self.assertTrue(self.number_close_check.is_match((target_value, 1), test_data_record),
                        " 5 close to (4,2) = True")

        # Test a single item
        target_value = 10

        self.assertFalse(self.number_gt_check.is_match(target_value, test_data_record),
                         " 5 > 10 = False")
        self.assertFalse(self.number_gte_check.is_match(target_value, test_data_record),
                         " 5 >= 10 False ")
        self.assertTrue(self.number_lt_check.is_match(target_value, test_data_record),
                        " 5 < 10 = True")
        self.assertTrue(self.number_lte_check.is_match(target_value, test_data_record),
                        " 5 <= 10 = True ")
        self.assertFalse(self.number_close_check.is_match((target_value, 2), test_data_record),
                         " 5 close to (10,2) = False")
        self.assertFalse(self.number_close_check.is_match((target_value, 1), test_data_record),
                         " 5 close to (10,2) = False")


class TestNumberComparisonsWithReplacement(TestCase):

    def setUp(self):
        self.number_gt_check = NumberComparer('my_number', MatcherType.GREATER_THAN, convert_none_to=5)
        self.number_gte_check = NumberComparer('my_number', MatcherType.GREATER_THAN_EQUAL_TO, convert_none_to=5)
        self.number_lt_check = NumberComparer('my_number', MatcherType.LESS_THAN, convert_none_to=5)
        self.number_lte_check = NumberComparer('my_number', MatcherType.LESS_THAN_EQUAL_TO, convert_none_to=5)
        self.number_close_check = NumberComparer('my_number', MatcherType.CLOSE_TO, convert_none_to=5)

    def test_single_none_with_replacement(self):
        test_data_record = {'my_number': None}

        # Test a single item
        target_value = 4
        self.assertTrue(self.number_gt_check.is_match(target_value, test_data_record),
                        " 5 > 4 = True")
        self.assertTrue(self.number_gte_check.is_match(target_value, test_data_record),
                        " 5 >= True ")
        self.assertFalse(self.number_lt_check.is_match(target_value, test_data_record),
                         " 5 < 4 = False")
        self.assertFalse(self.number_lte_check.is_match(target_value, test_data_record),
                         " 5 <= 4 = False ")
        self.assertTrue(self.number_close_check.is_match((target_value, 2), test_data_record),
                        " 5 close to (4,2) = True")
        self.assertTrue(self.number_close_check.is_match((target_value, 1), test_data_record),
                        " 5 close to (4,2) = True")

        # Test a single item
        target_value = 10

        self.assertFalse(self.number_gt_check.is_match(target_value, test_data_record),
                         " 5 > 10 = False")
        self.assertFalse(self.number_gte_check.is_match(target_value, test_data_record),
                         " 5 >= 10 False ")
        self.assertTrue(self.number_lt_check.is_match(target_value, test_data_record),
                        " 5 < 10 = True")
        self.assertTrue(self.number_lte_check.is_match(target_value, test_data_record),
                        " 5 <= 10 = True ")
        self.assertFalse(self.number_close_check.is_match((target_value, 2), test_data_record),
                         " 5 close to (10,2) = False")
        self.assertFalse(self.number_close_check.is_match((target_value, 1), test_data_record),
                         " 5 close to (10,2) = False")

    def test_is_gt_list_value(self):
        test_data_record = {'my_number': 5}

        # Test a single item list
        target_value = [4]
        self.assertTrue(self.number_gt_check.is_match(target_value, test_data_record),
                        "looking at field not in data record")

        # Test a single item list
        target_value = [10]
        self.assertFalse(self.number_gt_check.is_match(target_value, test_data_record),
                         "looking at field not in data record")

    def test_empty_list_raise_error(self):
        test_data_record = {'my_number': 11223344}

        target_value = []
        with self.assertRaises(NotImplementedError):
            self.number_gt_check.is_match(target_value, test_data_record)

    def test_multiple_vals_raise_error(self):
        test_data_record = {'my_number': 11223344}

        target_value = [1, 2, 3, 4]
        with self.assertRaises(NotImplementedError):
            self.number_gt_check.is_match(target_value, test_data_record)


class AbstractTestMatcher(Matcher):
    """ A class sole for testing the Abstract Base Class """

    def __init__(self, match_key_col):
        super().__init__(match_key_col)

    def is_match(self, *args):
        raise NotImplementedError


class TestMatcher(TestCase):
    def test_reper(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        assert_that("some_key_field", is_in(abc_matcher.__repr__()), "Check output")

    def test_get_key_value(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        print(abc_matcher.get_key_val())

        test_key = frozenset(('some_key_field', MatcherType.NOTHING.value))
        assert_that(abc_matcher.get_key_val(), equal_to(test_key))

    def test_str(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        assert_that("some_key_field", is_in(abc_matcher.__str__()), "Check output")
        print(abc_matcher.__str__())

    def test_match(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        with self.assertRaises(NotImplementedError):
            abc_matcher.is_match("target", "data_record")


class TestNumberMatcherBoundaryCases(TestCase):
    def setUp(self) -> None:

        number_matcher_types = [MatcherType.GREATER_THAN, MatcherType.GREATER_THAN_EQUAL_TO,
                                MatcherType.LESS_THAN, MatcherType.LESS_THAN_EQUAL_TO,
                                MatcherType.CLOSE_TO]

        self.my_number_comparere_list = list()
        for m_type in number_matcher_types:
            self.my_number_comparere_list.append(NumberComparer('number_col', m_type))

    def test_empty_input(self):
        test_data_record = {'number_col': 11223344}

        for comparer in self.my_number_comparere_list:
            target_value = []
            with self.assertRaises(NotImplementedError, msg=f"Checking {comparer}"):
                comparer.is_match(target_value, test_data_record)

    def test_key_not_in_data_record(self):
        test_data_record = {'some_other_columns': 11223344}

        for comparer in self.my_number_comparere_list:
            target_value = []

            assert_that(comparer.is_match(target_value, test_data_record),
                        equal_to(False), "Return False when field not available.")

    def test_reject_multiple_inputs(self):
        test_data_record = {'number_col': 11223344}

        for comparer in self.my_number_comparere_list:
            target_value = [1, 2, 3, 4]
            with self.assertRaises(NotImplementedError, msg=f"Checking {comparer}"):
                comparer.is_match(target_value, test_data_record)

    def test_bad_matcher_type(self):
        with self.assertRaises(NotImplementedError):
            self.comparer = NumberComparer("Foo", MatcherType.STARTS_WITH)


class TestExistenceMatcherBoundaryCases(TestCase):
    def setUp(self) -> None:

        exists_matcher_types = [MatcherType.NONE, MatcherType.NONE_OR_EMPTY,
                                MatcherType.NOT_NONE, MatcherType.NOT_NONE_OR_EMPTY]

        self.my_exists_comparer_list = list()
        for m_type in exists_matcher_types:
            self.my_exists_comparer_list.append(ExistsMatchers('number_col', m_type))

    def test_key_not_in_data_record(self):
        test_data_record = {'some_other_columns': 11223344}

        for comparer in self.my_exists_comparer_list:
            target_value = []

            assert_that(comparer.is_match(test_data_record),
                        equal_to(False), "Return False when field not available.")

    def test_bad_matcher_type(self):
        with self.assertRaises(NotImplementedError):
            self.comparer = NumberComparer("Foo", MatcherType.STARTS_WITH)


class TestExistsMatchers(TestCase):

    def test_is_none(self):
        my_is_none = ExistsMatchers('some_col', MatcherType.NONE)

        test_data_record = {'some_col': None}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

    def test_not_none(self):
        my_not_none = ExistsMatchers('some_col', MatcherType.NOT_NONE)

        test_data_record = {'some_col': None}
        assert_that(my_not_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_not_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_not_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_not_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

    def test_is_none_or_empty(self):
        my_is_none = ExistsMatchers('some_col', MatcherType.NONE_OR_EMPTY)

        test_data_record = {'some_col': None}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': {}}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': ()}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

    def test_not_none_or_empty(self):
        my_is_none = ExistsMatchers('some_col', MatcherType.NOT_NONE_OR_EMPTY)

        test_data_record = {'some_col': None}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': {}}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': ()}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")


class TestDictMatchers(TestCase):

    def test_has_entries(self):
        operator = DictMatchers('dumb', MatcherType.HAS_ENTRIES)
        assert_that(operator.is_match('a', 'b', data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(operator.is_match({'a': 'b'}, data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(operator.is_match({'foo': 'bar'}, data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))
        assert_that(operator.is_match('foo', 'bar', data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(operator.is_match('a', 'b', 'c', 'd',
                                      data_record={'dumb': {'c': 'd', 'a': 'b'}}),
                    equal_to(True))

        assert_that(operator.is_match('a', 'b',
                                      data_record={'dumb': [
                                          {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))

        assert_that(operator.is_match([{'a': 'b'}, {'1': '2'}],
                                      data_record={'dumb': [
                                          {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))

        assert_that(operator.is_match([{'a': 'g'}, {'1': 'g'}],
                                      data_record={'dumb': [
                                          {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(False))

        assert_that(operator.is_match([{'a': 'g'}, {'1': 'g'}],
                                      data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(operator.is_match([{'a': 'b'}, {'1': '2'}],
                                      data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(operator.is_match([{'a': 'b'}, {'1': '2'}, {'id': 'asdf', 'identifier': 'foo'}],
                                      data_record={'dumb': [{'a': 'b'}, {'id': 'asdf', 'identifier': 'foo'}]}),
                    equal_to(True))

        assert_that(operator.is_match([{'a': 'b'}, {'1': '2'}],
                                      data_record={'dumb': None}),
                    equal_to(False))



    def test_has_entry(self):
        operator = DictMatchers('dumb', MatcherType.HAS_ENTRY)
        assert_that(operator.is_match('a', 'b', data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(operator.is_match({'a': 'b'}, data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(operator.is_match({'foo': 'bar'}, data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))
        assert_that(operator.is_match('foo', 'bar', data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(operator.is_match('a', 'b',
                                      data_record={'dumb': [
                                          {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))

        assert_that(operator.is_match([{'a': 'b'}, {'1': '2'}],
                                      data_record={'dumb': [
                                          {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))


        assert_that(operator.is_match([{'a': 'g'}, {'1': 'g'}],
                                      data_record={'dumb': [
                                          {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(False))

        assert_that(operator.is_match([{'a': 'g'}, {'1': 'g'}],
                                      data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(operator.is_match([{'a': 'b'}, {'1': '2'}],
                                      data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(operator.is_match([{'a': 'b'}, {'1': '2'}],
                                      data_record={'dumb': None}),
                    equal_to(False))



    def test_has_entry_bad_input(self):
        operator = DictMatchers('dumb', MatcherType.HAS_ENTRY)

        with self.assertRaises(ValueError):
            assert_that(operator.is_match('a', 'b', 'c', 'd',
                                          data_record={'dumb': {'c': 'd', 'a': 'b'}}),
                        equal_to(True))

    def test_this(self):
        target_skills = [{'id': '61d8923376841a071b5fb398', 'identifier': 'Alto Sax'}, {'id': '61d8923376841a071b5fb39a', 'identifier': 'Tenor Sax'}, {'id': '61d8923376841a071b5fb39c', 'identifier': 'Bari Sax'}, {'id': '61d8923376841a071b5fb39e', 'identifier': 'Trumpet'}, {'id': '61d8923376841a071b5fb3a0', 'identifier': 'Trombone'}, {'id': '6223aa9d10a7d3001e006f66', 'identifier': '2nd Trumpet'}]


