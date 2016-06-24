# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import math
import random

# initialize global variables used in your code here
num_range = 100
secret_number = random.randrange(0, 100)
remaining_guesses = 7


# helper function to start and restart the game
def new_game(): 
    frame.start() 
    print "New Game - Range is 0 - 100"
	print "Secret_number is " + str(secret_number)
    print "Number of remaining guesses is", str(remaining_guesses)
    # remove this when you add your code   
    """
    if (num_range == 100):
        print "New Game - Range is 0 - 100"
        print "Number of remaining guesses is", remaining_guesses
    else:
        print "New Game - Range is 0 - 100"
        print "Number of remaining guesses is", remaining_guesses
    """



# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    # remove this when you add your code    
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    
    pass
    
def input_guess(guess):
    # main game logic goes here	
    global remaining_guesses
    remaining_guesses -= 1
    
    if remaining_guesses == 0:
        print "You lost! You are out of guesses."
        if num_range == 100:
            print "A new game has started with range 0 - 100.  Make a guess again."
        elif num_range == 1000:
            print "A new game has started with range 0 - 1000.  Make a guess again."
    else:
        print "Guess was " + str(guess)

        if int(guess) > secret_number:
            print "Guess lower."
            print "You have", str(remaining_guesses), "remaining guesses"
        elif int(guess) < secret_number:
            print "Guess higher."
            print "You have", str(remaining_guesses), "remaining guesses"
        elif int(guess) == secret_number:
            print "Correct!!! You've won!!!"

    # remove this when you add your code


    
# create frame
frame = simplegui.create_frame("Guess a Number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100) ", range100, 200)
frame.add_button("Range is [0, 1000) ", range1000, 200)
frame.add_input("Make a Guess", input_guess, 100)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
