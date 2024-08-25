import random
import time
import cProfile

class Card: # Represents a single playing card
    
    execution_times = {'get_value': 0}

    def __init__(self, suit, value):
        self.suit = suit  # Initialize a card with a suit
        self.value = value  # Initialize a card with a value
        
    def __repr__(self):
        return f"{self.value} of {self.suit}"  # Return a string representation of the card
    
    def get_value(self):
        start_time = time.time()  # Start performance measurement
        # Face cards are worth 10, Aces are worth 11, others are worth their integer value
        result = 10 if self.value in ['Jack', 'Queen', 'King'] else 11 if self.value == 'Ace' else int(self.value)
        end_time = time.time()  # End performance measurement
        Card.execution_times['get_value'] += end_time - start_time  # Update execution time
        return result

class Deck: # Represents a deck of 52 cards
    
    execution_times = {'__init__': 0, 'shuffle': 0, 'deal': 0}

    def __init__(self):
        start_time = time.time()  # Start performance measurement
        # Create a list of Card objects for each combination of suit and value
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]
        self.shuffle()  # Shuffle the deck after initialization
        end_time = time.time()  # End performance measurement
        Deck.execution_times['__init__'] += end_time - start_time  # Update execution time

    def shuffle(self):
        start_time = time.time()  # Start performance measurement
        # Shuffle the deck using the Fisher-Yates algorithm
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]  # Swap the cards
        end_time = time.time()  # End performance measurement
        Deck.execution_times['shuffle'] += end_time - start_time  # Update execution time

    def deal(self):
        start_time = time.time()  # Start performance measurement
        if self.cards:
            card = self.cards.pop()  # Remove and return the last card in the deck
            end_time = time.time()  # End performance measurement
            Deck.execution_times['deal'] += end_time - start_time  # Update execution time
            return card
        else:
            end_time = time.time()  # End performance measurement
            Deck.execution_times['deal'] += end_time - start_time  # Update execution time
            raise ValueError("The deck is empty.")  # Raise an error if the deck is empty

class Hand: # Represents a player's hand or the dealer's hand
    
    execution_times = {'__init__': 0, 'add_card': 0, 'adjust_for_aces': 0}
    
    def __init__(self):
        start_time = time.time()  # Start performance measurement
        self.cards = []  # Initialize an empty hand
        self.value = 0  # Initialize hand value
        self.aces = 0  # Initialize ace count
        end_time = time.time()  # End performance measurement
        Hand.execution_times['__init__'] += end_time - start_time  # Update execution time
    
    def add_card(self, card):
        start_time = time.time()  # Start performance measurement
        self.cards.append(card)  # Add a card to the hand
        self.value += card.get_value()  # Update the hand's value
        if card.value == 'Ace':
            self.aces += 1  # Increment ace count
        self.adjust_for_aces()  # Adjust the value if the hand has Aces and is over 21
        end_time = time.time()  # End performance measurement
        Hand.execution_times['add_card'] += end_time - start_time  # Update execution time
    
    def adjust_for_aces(self):
        start_time = time.time()  # Start performance measurement
        while self.value > 21 and self.aces:
            self.value -= 10  # Adjust the value for Aces
            self.aces -= 1  # Decrement ace count
        end_time = time.time()  # End performance measurement
        Hand.execution_times['adjust_for_aces'] += end_time - start_time  # Update execution time

    def __repr__(self):
        return f"{', '.join(map(str, self.cards))} (Value: {self.value})"  # Return a string representation of the hand's cards and value

class Game: # Represents a game of Blackjack
    
    execution_times = {'__init__': 0, 'start_game': 0, 'collect_bets': 0, 'initial_deal': 0,
                       'show_hands': 0, 'player_turn': 0, 'handle_bust': 0, 'dealer_turn': 0,
                       'determine_winners': 0, 'play_again': 0}

    def __init__(self, players, starting_funds):
        start_time = time.time()  # Start performance measurement
        self.players = [{'hand': Hand(), 'funds': starting_funds, 'bet': 0} for _ in range(players)]  # Initialize player hands and funds
        self.dealer = Hand()  # Initialize dealer's hand
        self.deck = Deck()  # Initialize a new deck
        end_time = time.time()  # End performance measurement
        Game.execution_times['__init__'] += end_time - start_time  # Update execution time

    def start_game(self):
        start_time = time.time()  # Start performance measurement
        print("Starting a game of Blackjack!")
        while self.players:
            self.players = [player for player in self.players if player['funds'] > 0]  # Remove players who have no funds left
            if not self.players:
                print("No players have enough funds to continue. Game over.")
                break

            self.collect_bets()  # Collect bets from all players
            if not self.players:
                print("No players have enough funds to continue. Game over.")
                break

            self.initial_deal()  # Deal initial cards to players and dealer
            self.show_hands(initial=True)  # Show hands initially

            for i, player in enumerate(self.players[:]):
                if player['funds'] > 0:
                    print(f"\nPlayer {i + 1}'s turn:")
                    self.player_turn(player)  # Handle player's turn

            print("\nDealer's turn:")
            self.dealer_turn()  # Dealer's turn
            self.show_hands(final=True)  # Show final hands

            self.determine_winners()  # Determine the winners of the game

            if not self.play_again():  # Ask if players want to play again
                break
        end_time = time.time()  # End performance measurement
        Game.execution_times['start_game'] += end_time - start_time  # Update execution time

    def collect_bets(self):
        for i, player in enumerate(self.players):
            if player['funds'] > 0:
                bet = get_valid_integer_input(f"Player {i + 1}, enter your bet (current funds: {player['funds']}): ", min_value=1, max_value=player['funds'])
                player['bet'] = bet  # Set the player's bet
                player['funds'] -= bet  # Deduct the bet from the player's funds

    def initial_deal(self):
        start_time = time.time()  # Start performance measurement
        for player in self.players:
            player['hand'] = Hand()  # Reset player hand
            player['hand'].add_card(self.deck.deal())  # Deal two cards to the player
            player['hand'].add_card(self.deck.deal())
        self.dealer = Hand()  # Reset dealer hand
        self.dealer.add_card(self.deck.deal())  # Deal two cards to the dealer
        self.dealer.add_card(self.deck.deal())
        end_time = time.time()  # End performance measurement
        Game.execution_times['initial_deal'] += end_time - start_time  # Update execution time

    def show_hands(self, initial=False, final=False):
        start_time = time.time()  # Start performance measurement
        if initial:
            _ = "\nCurrent Hands: "
        elif final:
            _ = "\nDealer's final hand: "
        end_time = time.time()  # End performance measurement
        Game.execution_times['show_hands'] += end_time - start_time  # Update execution time

    def player_turn(self, player):
        while True:
            print(player['hand'])  # Show player's hand
            if player['hand'].value == 21:
                print("Blackjack!")
                break
            elif player['hand'].value > 21:
                self.handle_bust(player)  # Handle bust
                break

            move = self.get_valid_input("Do you want to hit or stand? (h/s): ", ['h', 's', 'hit', 'stand'])
            if move in ['h', 'hit']:
                player['hand'].add_card(self.deck.deal())  # Player hits
                if player['hand'].value > 21:
                    self.handle_bust(player)  # Handle bust
                    break
            else:
                break

    def handle_bust(self, player):
        print(f"You bust with {player['hand'].value}!")  # Notify bust
        input("Please enter C to continue: ")  # Pause for user input

    def dealer_turn(self):
        start_time = time.time()  # Start performance measurement
        while self.dealer.value < 17:
            self.dealer.add_card(self.deck.deal())  # Dealer hits
        if self.dealer.value > 21:
            print("Dealer busts!")  # Notify dealer bust
        end_time = time.time()  # End performance measurement
        Game.execution_times['dealer_turn'] += end_time - start_time  # Update execution time

    def determine_winners(self):
        start_time = time.time()  # Start performance measurement
        dealer_value = self.dealer.value
        print(f"\nDealer's final hand: {self.dealer}")

        for i, player in enumerate(self.players):
            player_value = player['hand'].value
            if player_value > 21:
                print(f"Player {i + 1} busts and loses their bet of {player['bet']} (Total funds: {player['funds']})")
            elif dealer_value > 21 or player_value > dealer_value:
                winnings = player['bet'] * 2
                player['funds'] += winnings  # Player wins
                print(f"Player {i + 1} wins! They receive {winnings} (total funds: {player['funds']}).")
            elif player_value == dealer_value:
                player['funds'] += player['bet']  # Tie
                print(f"Player {i + 1} ties with the dealer and gets their bet back (total funds: {player['funds']}).")
            else:
                print(f"Player {i + 1} loses their bet of {player['bet']} (total funds: {player['funds']}).")
        end_time = time.time()  # End performance measurement
        Game.execution_times['determine_winners'] += end_time - start_time  # Update execution time

    def play_again(self):
        choice = self.get_valid_input("Do you want to play another round? (y/n): ", ['y', 'n', 'yes', 'no'])
        return choice in ['y', 'yes']  # Return True if player wants to play again

    def get_valid_input(self, prompt, valid_inputs):
        while True:
            user_input = input(prompt).lower()
            if user_input in valid_inputs:
                return user_input
            print(f"Invalid input. Please enter one of {valid_inputs}.")

def get_valid_integer_input(prompt, min_value, max_value):
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
    print("Welcome to Blackjack!")
    players = get_valid_integer_input("How many players? (1-5): ", min_value=1, max_value=5)
    starting_funds = get_valid_integer_input("Enter starting funds for each player (max 1000): ", min_value=1, max_value=1000)

    game = Game(players, starting_funds)
    game.start_game()

    while True:
        reveal_metrics = input("Would you like to reveal execution time metrics? (y/n): ").lower()
        if reveal_metrics in ['y', 'yes']:
            print("\nExecution times for methods:")
            for class_name, times in [("Card", Card.execution_times), ("Deck", Deck.execution_times),
                                      ("Hand", Hand.execution_times), ("Game", Game.execution_times)]:
                for method_name, exec_time in times.items():
                    if exec_time > 0:
                        print(f"{class_name} {method_name} execution time: {exec_time:.6f} seconds")
            break
        elif reveal_metrics in ['n', 'no']:
            print("Exiting the game.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    cProfile.run('main()')  # Profile the main function to analyze performance
