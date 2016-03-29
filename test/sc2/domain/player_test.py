from app.sc2.domain import player

from unittest import TestCase


class PrettifyNameTests(TestCase):
    def test_returns_single_name_as_is(self):
        expect = 'Macho'
        self.assertEqual(expect, player.prettify_name(expect))

    def test_removes_whitespace(self):
        expect = 'Macho'
        self.assertEqual(expect, player.prettify_name('Macho '))

    def test_returns_firstname_last_initial(self):
        expect = 'Randy S'
        self.assertEqual(expect, player.prettify_name('Randy Savage'))
