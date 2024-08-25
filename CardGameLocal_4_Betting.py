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
