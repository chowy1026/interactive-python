# http://www.codeskulptor.org/#user41_ACvp4DSO89_0.py

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0



# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:

    def __init__(self):
        self.cards = [] # create Hand object

    def __str__(self):
        strhand = "Hands contains "
        for c in self.cards:
            strhand += str(c) + " "
        return strhand  # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card) # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        intvalue = 0
        has_a = False
        for c in self.cards:
            rank = c.get_rank()
            if rank == "A":
                has_a = True
            print "card.get_rank is", rank
            print "lookup value is", VALUES[rank]
            intvalue += int(VALUES[rank])
            
        if has_a == True and intvalue <= 11:
            intvalue += 10
        return intvalue
    
    def draw(self, canvas, pos):
        i = 0
        for c in self.cards:
            pos[0] += 1.5 * CARD_SIZE[0]
            c.draw(canvas, [pos[0], pos[1]])
            i += 1 # draw a hand on the canvas, use the draw method for cards
             
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [] # create a Deck object
        for suit in SUITS: 
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        deal = random.choice(self.cards)
        self.cards.remove(deal)
        return deal
        # deal a card object from the deck
    
    def __str__(self):
        strdeck = "Decks contains "
        for c in self.cards:
            strdeck += str(c) + " "
        return strdeck      # return a string representing the deck




#define event handlers for buttons
def deal():
    global outcome, score, in_play, my_deck, my_hand, dealer_hand
    
    if in_play == False:
        outcome = "Hit or Stand?"
        in_play = True
    else: #Deal hit in the middle of play
        outcome = "You folded previous round.  New Deal?"
        score -= 1
    
    my_deck = Deck()
    my_deck.shuffle()
    
    my_hand = Hand()
    dealer_hand = Hand()
    my_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    my_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    
    print my_hand
    print dealer_hand
    print my_deck
    


def hit():
    # replace with your code below
    global score, outcome, in_play, my_deck, my_hand   # replace with your code below
    if in_play == True :
        my_hand.add_card(my_deck.deal_card())
        if my_hand.get_value() == 21:
            score += 1
            outcome = "You scored!! New Deal?"
            in_play = False
        elif my_hand.get_value() > 21:
            score -= 1
            outcome = "You have busted! New Deal?"
            in_play = False
            
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    # replace with your code below
    global score, outcome, in_play, my_deck, dealer_hand, my_hand   # replace with your code below
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
            if dealer_hand.get_value() > 21:
                score += 1
                outcome = "Dealer busted!! New Deal?"
                in_play = False
                return
            
        if dealer_hand.get_value() >= my_hand.get_value():
            #score -= 1
            outcome = "Dealer won!!  New Deal?"
            in_play = False
        elif dealer_hand.get_value() < my_hand.get_value():
            score += 1
            outcome = "You won!! New Deal?"
            in_play = False

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    pos_dealer = [50, 200]
    pos_my = [50, 400]
    dealer_hand.draw(canvas, pos_dealer)
    my_hand.draw(canvas, pos_my)
    
    canvas.draw_text('Blackjack Game', (200, 100), 34, 'Black')
    canvas.draw_text('Dealer\'s Hand', (100, 180), 34, 'Blue')
    canvas.draw_text('My Hand', (100, 380), 34, 'Yellow')
    canvas.draw_text('Score:  ' + str(score), (450, 50), 34, 'Red')
    canvas.draw_text('Outcome: ' + str(outcome), (200, 550), 24, 'Red')
    
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos_dealer[0] + CARD_BACK_CENTER[0], pos_dealer[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")
lblgame = frame.add_label('Blackjack Game', 400)

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric