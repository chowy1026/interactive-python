#http://www.codeskulptor.org/#user41_tiuem3bZK69rGjo.py

# template for "Stopwatch: The Game"
import simplegui

# define global variables
interval = 100
count = 0
display = "0:00.0"
score = [0,0]

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global display
    min = t // 600
    sec = round(((float(t) % 600)/10),1)
    if (sec < 10):
        display = str(min) + ":0" + str(sec)
    else:
        display = str(min) + ":" + str(sec)

    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    print "Start Clicked"
    timer.start()

def stop_timer():
    print "Stop Clicked"
    if (timer.is_running()):
        timer.stop()
        score[1] +=1
        if (display[-1] == "0"):
            score[0] +=1
    else:
        pass

def reset_timer():
    print "Reset Clicked"
    timer.stop()  
    global count, display
    count = 0
    format(0)
    score[0] = 0
    score[1] = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global count, display
    count += 1
    format(count)
 

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(display, [135, 115], 36, "White")
    canvas.draw_text(str(score[0]) + " / " + str (score[1]), [280,40], 28,"White")

# create frame
frame = simplegui.create_frame("Cute Timer", 360, 200)
btnstart = frame.add_button("Start", start_timer, 100)
btnstop = frame.add_button("Stop", stop_timer, 100)
btnreset = frame.add_button("Reset", reset_timer, 100)


# register event handlers
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(interval, timer_handler)

# start frame
frame.start()


# Please remember to review the grading rubric
