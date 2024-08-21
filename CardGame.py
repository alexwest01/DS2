class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]

        
    def shuffle(self):
        self.cards = self.cards[::-1]
        
    def deal(self):
        return self.cards.pop()
    
class Game:
    def __init__(self, players, rounds, starting_funds):
        self.players = players
        self.rounds = rounds
        self.starting_funds = starting_funds
        self.deck = Deck()
        
    def play_round(self):
        self.deck.shuffle()
        for p in range(self.players):
            player_card = self.deck.deal()
            print(f"Player {p+1} draws: {player_card}")
            
    def start_game(self):
        for r in range(self.rounds):
            print(f"Round {r+1}")
            self.play_round()
            if len(self.deck.cards) < self.players:
                print("Reshuffling deck")
                self.deck = Deck()
                self.deck.shuffle()
                
def main():
    rounds = int(input("Enter the number of rounds to play: "))
    players = int(input("How many players? "))
    starting_funds = int(input("Enter starting funds for each player: "))
    
    game = Game(players, rounds, starting_funds)
    game.start_game()
    
if __name__ == "__main__":
    main()