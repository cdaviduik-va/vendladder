from app.sc2.utils import match_utils

from unittest import TestCase


class GetVsStringFromNamesTests(TestCase):
    def test_single_player_match_formats_correctly(self):
        expect = "Randy S @ Steve A"
        result = match_utils.get_vs_string_from_names(['Randy Savage'], ['Steve Austin'])
        self.assertEqual(expect, result)

    def test_two_player_match_formats_correctly(self):
        expect = "Randy S & Steve A @ Ric F & Vince M"
        result = match_utils.get_vs_string_from_names(['Randy Savage', 'Steve Austin'], ['Ric Flair', 'Vince McMahon'])
        self.assertEqual(expect, result)

    def test_three_player_match_formats_correctly(self):
        expect = 'Randy S & Steve A & Undertaker @ Ric F & Vince M & Triple H'
        result = match_utils.get_vs_string_from_names(['Randy Savage', 'Steve Austin', 'Undertaker'],
                                                ['Ric Flair', 'Vince McMahon', ' Triple H'])
        self.assertEqual(expect, result)

    def test_match_string_works_with_mixed_length_names(self):
        expect = 'Sting & Hulk H @ Stone C & Undertaker'
        result = match_utils.get_vs_string_from_names(['Sting', 'Hulk Hogan'], ['Stone Cold', 'Undertaker'])
        self.assertEqual(expect, result)
