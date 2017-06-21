from flask import Flask, url_for, render_template, request, redirect, flash
from Global import *
from Deck import *
from IndividualPlay import *

app = Flask(__name__)
app.secret_key = 'some secret'


@app.route('/layout', methods=['POST', 'GET'])
def index():
    set_chip_pool(pool_value=500)
    if request.method == 'POST':
        return redirect(url_for('intro'))
    else:
        return redirect(url_for('intro'))


result = ""
statement = '''Welcome to BlackJack! Get as close to 21 as you can without going over!
    Dealer hits until she reaches 17. Aces count as 1 or 11.'''


@app.route('/bet', methods=['POST', 'GET'])
def make_bet():

    error = None
    set_bet(bet_amount=0)

    if request.method == 'POST':

        while get_bet() == 0:
            bet_amount = request.form['bet_amt']

            if bet_amount == "":
                error = "No Bet Amount Entered... Please Enter an amount"
                return render_template('start.html', result=statement, chip=get_chip_pool(), error=error)
            try:
                bet_amount = int(bet_amount)
            except ValueError:
                error = "Integer value not Entered... Please Enter an Integer Value"
                return render_template('start.html', result=statement, chip=get_chip_pool(), error=error)

            if bet_amount >= 1 and get_chip_pool() >= bet_amount:
                set_bet(bet_amount=bet_amount)
            else:
                error = 'Invalid Bet, you only have '+str(get_chip_pool())+' chips remaining'
                return render_template('start.html', result=statement, chip=get_chip_pool(), error=error)

        return redirect(url_for('deal'))


def hit():

    global player_hand, dealer_hand, deck, result

    if get_playing():
        if player_hand.calculate_value() <= 21:
            player_hand.add_card(deck.deal())

        if player_hand.calculate_value() > 21:
            flash("Busted! You Lost!! \n Please Click on New Deal to Continue")

            set_chip_pool(pool_value=get_chip_pool()-get_bet())
            set_playing(play=False)

            return redirect(url_for('game'))

    else:
        flash("Click on New Deal to Continue")

    return redirect(url_for('game'))


def stand():
    global player_hand, dealer_hand, deck, result

    if get_playing() == False:
        if player_hand.calculate_value() > 0:
            flash("Click on New Deal to Continue")

    else:
        while dealer_hand.calculate_value() < 17:
            dealer_hand.add_card(deck.deal())

        if dealer_hand.calculate_value() > 21:
            flash("Dealer Busts! You Win!!! \n Please Click on New Deal to Continue")
            set_chip_pool(pool_value=get_chip_pool()+get_bet())
            set_playing(play=False)

        elif player_hand.calculate_value() > dealer_hand.calculate_value():
            flash("You Beat the Dealer! You Win!!! \n Please Click on New Deal to Continue")
            set_chip_pool(pool_value=get_chip_pool() + get_bet())
            set_playing(play=False)

        elif player_hand.calculate_value() == dealer_hand.calculate_value():
            flash("Round Tied!! \n Please Click on New Deal to Continue")
            set_playing(play=False)

        else:
            flash("Dealer Wins!!! \n Please Click on New Deal to Continue")
            set_chip_pool(pool_value=get_chip_pool() - get_bet())
            set_playing(play=False)

    return redirect(url_for("game"))


@app.route('/player', methods=['POST', 'GET'])
def player():
    """Function takes Player input"""

    if request.method == 'POST':

        if request.form['game_submit'] == 'Hit':
            return hit()
        elif request.form['game_submit'] == 'Stand':
            return stand()
        elif request.form['game_submit'] == 'New Deal':
            return redirect(url_for('intro'))
        elif request.form['game_submit'] == 'Double the Bet':
            if get_playing() == True:
                if (get_bet()*2) > get_chip_pool():
                    flash("You cannot Double your Bet as do not have sufficient Chips Left")
                else:
                    set_bet(bet_amount=(get_bet()*2))
            else:
                flash("Click on New Deal to Continue")
            return redirect(url_for('game'))


@app.route('/game', methods=['POST', 'GET'])
def game():
    """Function to print game step/status on output"""
    player_cards = []
    dealer_cards = []

    # Display Player Hand
    player_cards = player_hand.draw(hidden=False)
    player_total = player_hand.calculate_value()

    # Display Dealer Hand
    dealer_cards = dealer_hand.draw(hidden=True)
    dealer_total = dealer_hand.calculate_value()

    # If game round is over
    if get_playing() == False:
        print(" --- for a total of " + str(dealer_hand.calculate_value()))
        print("Chip Total: ", str(get_chip_pool()))
    # Otherwise, don't know the second card yet
    else:
        print(" with another card hidden upside down")

    return render_template('game.html', playCard=player_cards, playTotal=player_total, dealerCard=dealer_cards, dealerTotal=dealer_total, bet=get_bet())


@app.route('/deal', methods=['POST', 'GET'])
def deal():

    global deck, result, player_hand, dealer_hand

    deck = Deck()

    deck.shuffle_cards()

    player_hand = IndividualPlay()
    dealer_hand = IndividualPlay()

    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    result = 'Hit or Stand? Press either h or s:'

    if get_playing() == True:
        print('Fold, Sorry!!')
        set_chip_pool(pool_value=get_chip_pool()-get_bet())

    set_playing(play=True)
    return redirect(url_for('game'))


@app.route('/intro')
def intro():
    if get_chip_pool() == 0 or get_chip_pool() < 0:
        flash("You don't have any Chips left. Adding 100 Chips to your Chip Pool")
        set_chip_pool(pool_value=100)
    return render_template('start.html', result=statement, chip=get_chip_pool())


if __name__ == '__main__':
    deck = Deck()
    player_hand = IndividualPlay()
    dealer_hand = IndividualPlay()
    app.run(debug=True)
