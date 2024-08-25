import time
import random
from CardGameLocal_FINAL import Deck

def fisher_yates_shuffle(deck):
    # Fisher-Yates shuffle implementation
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def test_shuffle_performance():
    # Initialize deck and perform the Fisher-Yates shuffle 1000 times
    deck = Deck()
    shuffle_times = 1000

    # We will directly shuffle the list of cards in the Deck instance
    deck_list = deck.cards

    start_time = time.time()
    for _ in range(shuffle_times):
        fisher_yates_shuffle(deck_list)
    end_time = time.time()

    print(f"Time taken to shuffle a 52-card deck {shuffle_times} times using Fisher-Yates: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    test_shuffle_performance()
