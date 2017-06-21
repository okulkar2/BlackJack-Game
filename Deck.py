import random
from Global import suits, rankings
from Card import Card


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in rankings:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += " " + card.__str__()

        return "The deck has" + deck_comp

    def shuffle_cards(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

