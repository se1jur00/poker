from Player import Player
from Game import Game
from Combinations import Combinations
from Card import Card

player1 = Player(id = 0, balance=1000, name='Player1')
player2 = Player(id = 0, balance=1000, name='Player2')
player3 = Player(id = 0, balance=1000, name='Player3')
player4 = Player(id = 0, balance=1000, name='Player4')
player5 = Player(id = 0, balance=1000, name='Player5')
game = Game()
game.join(player1)
game.join(player2)
game.join(player3)
game.join(player4)
game.join(player5)
game.start_round()


for i in range(2):
    game.lay_card()

game.table = [Card('Diamonds', '9'), Card('Spades', '10'), Card('Diamonds', 'Queen'), Card('Diamonds', 'King'), Card('Diamonds', '7')]
player1.cards = [Card('Diamonds', '10'), Card('Diamonds', 'Jack')]
player2.cards = [Card('Diamonds', '8'), Card('Hearts', 'Jack')]
print(game.table)
print(game.check_winner())
for player in game.players:
    print(player.cards)
print(Combinations.sort_cards(player1.cards+game.table))
