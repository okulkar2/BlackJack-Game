class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit + self.rank

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def drawCard(self):
        return self.suit + self.rank