
playing = False
bet = 0
chip_pool = 500
suits = ('hearts', 'diamonds', 'clubs', 'spades')
rankings = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
card_value = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}


def set_playing(play):
    global playing
    playing = play

def get_playing():
    return playing


def set_bet(bet_amount):
    global bet
    bet = bet_amount


def get_bet():
    return bet


def set_chip_pool(pool_value):
    global chip_pool
    chip_pool = pool_value


def get_chip_pool():
    return chip_pool