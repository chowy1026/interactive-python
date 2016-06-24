# http://www.codeskulptor.org/#user41_bpThEaHJhk_4.py
# http://www.codeskulptor.org/#user41_qo0KO39z6hcvQ2m.py
# implementation of card game - Memory

import simplegui
import random

lst1 = range(0,8)
lst2 = range(0,8)
lst_nums = lst1 + lst2

exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]


# helper function to initialize globals
def new_game():
    global state, idx0, idx1, turns
    state = 0
    idx0 = 0
    idx1 = 0
    turns = 0
    label.set_text("Turns = " + str(turns))
    for index, item in enumerate(exposed):
        if exposed[index]:
            exposed[index] = False
    random.shuffle(lst_nums)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, idx0, idx1, turns
    idx = pos[0] / 50
    #print str(pos[0]), ":", str(idx), ":", exposed[idx]
    if not exposed[idx]:
        if state == 0:
            state = 1
            idx0 = idx
            exposed[idx0] = True
        elif state == 1:
            state = 2
            idx1 = idx
            exposed[idx0] = True
            exposed[idx1] = True
            
            turns += 1
            label.set_text("Turns = " + str(turns))
            
        else:
            if lst_nums[idx0] == lst_nums[idx1]:
                state = 1
                idx0 = idx
                exposed[idx0] = True                
            else:
                state = 0
                exposed[idx0] = False
                exposed[idx1] = False
                exposed[idx] = False
        lblstate.set_text("State = " + str(state))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    count = 0
    card_width = 50
    card_height = 100
    for num in lst_nums:
        #print num
        x_txt = 15 + (count * card_width)
        y_txt = 65
        x_card = (card_width / 2) + (count * 50)
        y_card = 100
        if exposed[count]:
            canvas.draw_text(str(num), [x_txt, y_txt], 50, 'Yellow')
        else:
            canvas.draw_line((x_card, 0), (x_card, 100), 48, 'Green')
        count += 1


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
lblstate = frame.add_label("State = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric