import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

DISTANCES = '''
The distance from Earth to Mars is 78,340,000 kilometers.
The distance from Earth to Jupiter is 628,730,000 kilometers.
It is 4,140 kilometers from Moscow to Krasnoyarsk.
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    def test_integers_with_group_separator(self):
        self.assert_extract(DISTANCES, library.integers, '78,340,000', '628,730,000', '4,140')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    def test_dates(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    def test_datetimes_with_minute_precision(self):
        self.assert_extract("The plane departure is delayed from 2015-07-25 12:35 to 2015-07-25 15:10.",
                            library.dates_iso8601, '2015-07-25 12:35', '2015-07-25 15:10')

    def test_datetimes_with_second_precision(self):
        self.assert_extract("The accurate time was 2015-07-25 10:06:48.",
                            library.dates_iso8601, '2015-07-25 10:06:48')

    def test_datetimes_with_millisecond_precision(self):
        self.assert_extract("The accurate time was 2015-07-25T10:06:48.874.",
                            library.dates_iso8601, '2015-07-25T10:06:48.874')

    def test_datetimes_with_microsecond_precision_not_extracted(self):
        self.assert_extract("The accurate time was 2015-07-25T10:06:48.874012.", library.dates_iso8601)

    def test_datetimes_with_literal_timezone(self):
        self.assert_extract("The accurate time was 2015-07-25 04:06MDT.",
                            library.dates_iso8601, '2015-07-25 04:06MDT')

    def test_datetimes_with_too_short_literal_timezone_not_extracted(self):
        self.assert_extract("The accurate time was 2015-07-25 04:06MD.", library.dates_iso8601)

    def test_datetimes_with_too_long_literal_timezone_not_extracted(self):
        self.assert_extract("The accurate time was 2015-07-25 04:06MDTX.", library.dates_iso8601)

    def test_datetimes_with_utc_timezone(self):
        self.assert_extract("The accurate time was 2015-07-25T10:06:48.874Z.",
                            library.dates_iso8601, '2015-07-25T10:06:48.874Z')

    def test_datetimes_with_positive_timezone_offset(self):
        self.assert_extract("The accurate time was 2015-07-25 14:36:48+0430.",
                            library.dates_iso8601, '2015-07-25 14:36:48+0430')

    def test_datetimes_with_negative_timezone_offset(self):
        self.assert_extract("The accurate time was 2015-07-25 02:06:48-0800.",
                            library.dates_iso8601, '2015-07-25 02:06:48-0800')

    def test_datetimes_with_space_as_date_time_separator(self):
        self.assert_extract("The accurate time was 2015-07-25 14:36:48.874+0430.",
                            library.dates_iso8601, '2015-07-25 14:36:48.874+0430')

    def test_datetimes_with_t_as_date_time_separator(self):
        self.assert_extract("The accurate time was 2015-07-25T14:36:48.874+0430.",
                            library.dates_iso8601, '2015-07-25T14:36:48.874+0430')

    def test_no_dates(self):
        self.assert_extract('2015-13-25 is not a date and 2015-07-32 is not a date too.', library.dates_iso8601)

    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    def test_dates_fmt2_with_comma(self):
        self.assert_extract('I was born on 25 Jan, 2017.', library.dates_fmt2, '25 Jan, 2017')

if __name__ == '__main__':
    unittest.main()
