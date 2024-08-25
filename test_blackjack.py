import unittest
from CardGameLocal_FINAL import Card, Hand

class TestHand(unittest.TestCase):
    
    def setUp(self):
        self.hand = Hand()
    
    def test_add_card(self):
        card = Card('Hearts', '10')
        self.hand.add_card(card)
        self.assertEqual(self.hand.value, 10, "Hand value should be 10 after adding a 10 card.")

    def test_add_card_with_ace(self):
        card = Card('Spades', 'Ace')
        self.hand.add_card(card)
        self.assertEqual(self.hand.value, 11, "Hand value should be 11 after adding an Ace.")

    def test_adjust_for_aces(self):
        # Adding an Ace to the hand
        card1 = Card('Spades', 'Ace')
        # Adding another Ace to the hand
        card2 = Card('Diamonds', 'Ace')
        # Adding a 10 to the hand
        card3 = Card('Hearts', '10')
        
        self.hand.add_card(card1)  # Ace, value should be 11
        self.hand.add_card(card2)  # Another Ace, value should be 12 (11 + 1)
        self.hand.add_card(card3)  # Adding a 10 should adjust one Ace to 1, total should be 12 + 10 = 22 and Ace adjustment -> 12

        self.assertEqual(self.hand.value, 12, "Hand value with two Aces and a 10 should be 12 due to adjustment of one Ace.")

    def test_multiple_cards(self):
        card1 = Card('Hearts', '9')
        card2 = Card('Spades', '7')
        card3 = Card('Diamonds', '5')

        self.hand.add_card(card1)
        self.hand.add_card(card2)
        self.hand.add_card(card3)

        self.assertEqual(self.hand.value, 21, "Hand value should be 21 after adding 9, 7, and 5.")

    def test_bust_scenario(self):
        card1 = Card('Hearts', '10')
        card2 = Card('Spades', '8')
        card3 = Card('Diamonds', '5')

        self.hand.add_card(card1)
        self.hand.add_card(card2)
        self.hand.add_card(card3)

        self.assertEqual(self.hand.value, 23, "Hand value should be 23 after adding 10, 8, and 5.")

if __name__ == '__main__':
    unittest.main()
