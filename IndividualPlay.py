from Global import card_value, playing


class IndividualPlay:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace_case = False

    def __str__(self):
        composition = ""

        for card in self.cards:
            card_name = card.__str__()
            composition = " " + card_name

        return "Your Current Cards: " + composition

    def add_card(self, card):
        self.cards.append(card)

        if card.rank == 'Ace':
            self.ace_case = True

        self.value += card_value[card.rank]

    def calculate_value(self):
        if self.ace_case == True and self.value < 11:
            return self.value + 10
        else:
            return self.value

    def draw(self, hidden):
        current_cards = []
        if hidden == True and playing == True:
            start = 1
        else:
            start = 0

        for card in range(start, len(self.cards)):
            current_cards.append(self.cards[card].drawCard())

        return current_cards
