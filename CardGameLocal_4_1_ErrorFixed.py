import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    def get_value(self):
        if self.value in ['Jack', 'Queen', 'King']:
            return 10
        elif self.value == 'Ace':
            return 11  # We'll handle Ace as 1 or 11 in hand calculation.
        else:
            return int(self.value)

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]
        self.shuffle()  # Shuffle the deck upon initialization

    def shuffle(self):
        # Fisher-Yates Shuffle Algorithm
        n = len(self.cards)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def deal(self):
        if self.cards:  # Ensure there are cards left to deal
            return self.cards.pop()
        else:
            raise ValueError("All cards have been dealt, the deck is empty.")

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Track aces to adjust value if needed
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += card.get_value()
        if card.value == 'Ace':
            self.aces += 1
        self.adjust_for_aces()
    
    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __repr__(self):
        return f"Hand: {self.cards}, Value: {self.value}"

class Game:
    def __init__(self, players, starting_funds):
        self.players = [{'hand': Hand(), 'funds': starting_funds, 'bet': 0} for _ in range(players)]
        self.dealer = Hand()
        self.deck = Deck()

    def start_game(self):
        print("Starting a game of Blackjack!")
        while True:
            self.collect_bets()
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
        for i, player in enumerate(self.players):
            if player['funds'] > 0:
                bet = int(input(f"Player {i + 1}, enter your bet (current funds: {player['funds']}): "))
                while bet > player['funds']:
                    print("You cannot bet more than your current funds.")
                    bet = int(input(f"Player {i + 1}, enter your bet (current funds: {player['funds']}): "))
                player['bet'] = bet
                player['funds'] -= bet

    def initial_deal(self):
        for player in self.players:
            player['hand'] = Hand()
            player['hand'].add_card(self.deck.deal())
            player['hand'].add_card(self.deck.deal())
        self.dealer = Hand()
        self.dealer.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def show_hands(self, initial=False):
        for i, player in enumerate(self.players):
            print(f"Player {i + 1}'s hand: {player['hand']} (Bet: {player['bet']}, Funds: {player['funds']})")
        if initial:
            print(f"Dealer's hand: [{self.dealer.cards[0]}, ?]")
        else:
            print(f"Dealer's hand: {self.dealer}")

    def player_turn(self, player):
        while True:
            print(player['hand'])
            if player['hand'].value == 21:
                print("Blackjack!")
                break
            elif player['hand'].value > 21:
                print("Bust!")
                break

            move = input("Do you want to hit or stand? (h/s): ").lower()
            if move == 'h':
                player['hand'].add_card(self.deck.deal())
            else:
                break

    def dealer_turn(self):
        while self.dealer.value < 17:
            self.dealer.add_card(self.deck.deal())
        if self.dealer.value > 21:
            print("Dealer busts!")

    def determine_winners(self):
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
        choice = input("Do you want to play another round? (y/n): ").lower()
        return choice == 'y'

def main():
    players = int(input("How many players? "))
    starting_funds = int(input("Enter starting funds for each player: "))

    game = Game(players, starting_funds)
    game.start_game()

if __name__ == "__main__":
    main()
