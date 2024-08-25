import random

class Card:
    # Represents a single playing card.
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    def get_value(self):
        # Returns the Blackjack value of the card.
        # Face cards (Jack, Queen, King) are worth 10.
        # Ace is worth 11 (to be adjusted later in hand calculation).
        if self.value in ['Jack', 'Queen', 'King']:
            return 10
        elif self.value == 'Ace':
            return 11
        else:
            return int(self.value)

class Deck:
    # Represents a deck of 52 cards.
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]
        self.shuffle()  # Shuffle the deck upon initialization

    def shuffle(self):
        # Shuffles the deck using the Fisher-Yates algorithm.
        n = len(self.cards)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def deal(self):
        # Deals a single card from the deck.
        if self.cards:  # Ensure there are cards left to deal
            return self.cards.pop()
        else:
            raise ValueError("All cards have been dealt, the deck is empty.")

class Hand:
    # Represents a player's hand or the dealer's hand.
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Track aces to adjust value if needed
    
    def add_card(self, card):
        # Adds a card to the hand and adjusts the hand's value.
        self.cards.append(card)
        self.value += card.get_value()
        if card.value == 'Ace':
            self.aces += 1
        self.adjust_for_aces()
    
    def adjust_for_aces(self):
        # Adjusts the hand value if there are aces and the hand is over 21.
        # Each ace can be worth 1 or 11, so we reduce the value if necessary.
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __repr__(self):
        return f"Hand: {self.cards}, Value: {self.value}"

class Game:
    # Represents the Blackjack game.
    def __init__(self, players, starting_funds):
        self.players = [{'hand': Hand(), 'funds': starting_funds, 'bet': 0} for _ in range(players)]
        self.dealer = Hand()
        self.deck = Deck()

    def start_game(self):
        # Starts and manages the game loop.
        print("Starting a game of Blackjack!")
        while self.players:
            # Filter out players with zero funds before starting a round
            self.players = [player for player in self.players if player['funds'] > 0]
            if not self.players:
                print("No players have enough funds to continue. Game over.")
                break

            self.collect_bets()
            if not self.players:
                print("No players have enough funds to continue. Game over.")
                break

            self.initial_deal()
            self.show_hands(initial=True)

            for i, player in enumerate(self.players):
                if player['funds'] > 0:
                    print(f"\nPlayer {i + 1}'s turn:")
                    self.player_turn(player)

            print("\nDealer's turn:")
            self.dealer_turn()
            self.show_hands()

            self.determine_winners()

            if not self.play_again():
                break

    def collect_bets(self):
        # Collects bets from each player. Ensures bets are within their funds and positive.
        for i, player in enumerate(self.players):
            if player['funds'] > 0:
                while True:
                    try:
                        bet = get_valid_integer_input(f"Player {i + 1}, enter your bet (current funds: {player['funds']}): ", min_value=1, max_value=player['funds'])
                        player['bet'] = bet
                        player['funds'] -= bet
                        break
                    except ValueError as e:
                        print(f"Invalid input. {e}")

    def initial_deal(self):
        # Deals two cards to each player and two cards to the dealer (one face down).
        for player in self.players:
            player['hand'] = Hand()
            player['hand'].add_card(self.deck.deal())
            player['hand'].add_card(self.deck.deal())
        self.dealer = Hand()
        self.dealer.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def show_hands(self, initial=False):
        # Displays the hands of all players and the dealer.
        for i, player in enumerate(self.players):
            print(f"Player {i + 1}'s hand: {player['hand']} (Bet: {player['bet']}, Funds: {player['funds']})")
        if initial:
            print(f"Dealer's hand: [{self.dealer.cards[0]}, ?]")
        else:
            print(f"Dealer's hand: {self.dealer}")

    def player_turn(self, player):
        # Handles a player's turn. The player can choose to hit or stand.
        while True:
            print(player['hand'])
            if player['hand'].value == 21:
                print("Blackjack!")
                break
            elif player['hand'].value > 21:
                print("Bust!")
                break

            move = self.get_valid_input("Do you want to hit or stand? (h/s): ", ['h', 's', 'hit', 'stand'])
            if move in ['h', 'hit']:
                player['hand'].add_card(self.deck.deal())
                if player['hand'].value > 21:
                    print("Bust!")
                    break
            else:
                break

    def dealer_turn(self):
        # Handles the dealer's turn. The dealer hits until their hand value is at least 17.
        while self.dealer.value < 17:
            self.dealer.add_card(self.deck.deal())
        if self.dealer.value > 21:
            print("Dealer busts!")

    def determine_winners(self):
        # Compares each player's hand to the dealer's hand and determines the winners.
        dealer_value = self.dealer.value
        print(f"\nDealer's final hand: {self.dealer}")

        for i, player in enumerate(self.players):
            player_value = player['hand'].value
            if player_value > 21:
                print(f"Player {i + 1} busts and loses their bet of {player['bet']}.")
            elif dealer_value > 21 or player_value > dealer_value:
                winnings = player['bet'] * 2
                player['funds'] += winnings
                print(f"Player {i + 1} wins! They receive {winnings} (total funds: {player['funds']}).")
            elif player_value == dealer_value:
                player['funds'] += player['bet']  # Return bet
                print(f"Player {i + 1} ties with the dealer and gets their bet back (total funds: {player['funds']}).")
            else:
                print(f"Player {i + 1} loses their bet of {player['bet']} (total funds: {player['funds']}).")

    def play_again(self):
        # Asks if the players want to play another round and returns True or False.
        choice = self.get_valid_input("Do you want to play another round? (y/n): ", ['y', 'n', 'yes', 'no'])
        return choice in ['y', 'yes']

    def get_valid_input(self, prompt, valid_inputs):
        # Prompts the user for input until a valid choice is made.
        while True:
            user_input = input(prompt).lower()
            if user_input in valid_inputs:
                return user_input
            print(f"Invalid input. Please enter one of {valid_inputs}.")

def get_valid_integer_input(prompt, min_value, max_value):
    # Prompts the user for an integer input within a specified range.
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Input must be between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Main function to run the game.
    print("Welcome to Blackjack!")
    players = get_valid_integer_input("How many players? (1-5): ", min_value=1, max_value=5)
    starting_funds = get_valid_integer_input("Enter starting funds for each player (max 1000): ", min_value=1, max_value=1000)

    game = Game(players, starting_funds)
    game.start_game()

if __name__ == "__main__":
    main()
