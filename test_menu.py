import unittest

from menu import analyze_menu, detect_dietary_tags, keyword_present, normalize_menu_text, parse_dishes


class MenuDecoderTests(unittest.TestCase):
    def test_keyword_present_uses_whole_words(self):
        self.assertFalse(keyword_present("champagne reduction", ["ham"]))
        self.assertTrue(keyword_present("fish sauce", ["fish"]))

    def test_detect_dietary_tags_handles_hidden_ingredients(self):
        self.assertIn("contains-meat", detect_dietary_tags("Chicken broth risotto"))
        self.assertNotIn("contains-meat", detect_dietary_tags("Champagne sorbet"))
        self.assertIn("contains-fish", detect_dietary_tags("Tofu with fish sauce"))
        self.assertIn("vegetarian", detect_dietary_tags("Roasted vegetables with olive oil"))

    def test_detect_dietary_tags_distinguishes_meat_and_fish_menus(self):
        self.assertEqual(detect_dietary_tags("Grilled salmon with lemon"), ["pescatarian-friendly", "contains-fish"])
        self.assertEqual(detect_dietary_tags("BBQ brisket with sauce"), ["contains-meat"])

    def test_parse_dishes_extracts_sample_menu(self):
        sample = normalize_menu_text(
            """
            STARTERS
            Bruschetta - tomato, basil, garlic, olive oil 8.50
            Shrimp Cocktail $12.00

            MAINS
            Salmon Teriyaki $21.99
            served with rice, sesame, soy glaze
            Margherita Pizza 15.00
            mozzarella, tomato, basil
            """
        )
        dishes = parse_dishes(sample)
        self.assertEqual([dish["name"] for dish in dishes], ["Bruschetta", "Shrimp Cocktail", "Salmon Teriyaki", "Margherita Pizza"])
        self.assertEqual([dish["price"] for dish in dishes], ["$8.50", "$12.00", "$21.99", "$15.00"])

    def test_analyze_menu_marks_small_menu_as_friendly_when_it_has_options(self):
        sample = normalize_menu_text(
            """
            STARTERS
            Bruschetta - tomato, basil, garlic, olive oil 8.50
            Shrimp Cocktail $12.00

            MAINS
            Salmon Teriyaki $21.99
            served with rice, sesame, soy glaze
            Margherita Pizza 15.00
            mozzarella, tomato, basil
            """
        )
        result = analyze_menu(sample)
        summary = result["restaurant_summary"]
        self.assertTrue(summary["vegetarian_friendly"])
        self.assertTrue(summary["pescatarian_friendly"])


if __name__ == "__main__":
    unittest.main()
