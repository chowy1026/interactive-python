# http://www.codeskulptor.org/#user41_nBAtRckNrnkfDPj_0.py

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600

VEL_UPPER = 2.0
VEL_LOWER = -2.0
ANG_VEL_UPPER = 0.4
ANG_VEL_LOWER = -0.4

ROCK_LIMITS = 5

score = 0
lives = 3
time = 0
c = 0.1 #friction
ship_speed = 3
missile_speed = 6

game_on = False

rock_group = set([])
missile_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
    def set_center(self, lst_center):
        self.center = lst_center

    def set_size(self, lst_size):
        self.size = lst_size

    def set_radius(self, flt_radius):
        self.radius = flt_radius

    def set_animated(self, bool_animated):
        self.animated = bool_animated 

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

### SOUND Assets ###
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.4)

missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)

ship_thrust_sound = simplegui.load_sound("http://giladayalonvegan.vkav.org/Python/thrust.mp3")
ship_thrust_sound.set_volume(.6)

explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.6)

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# get random float number
def rand_float(upper, lower):
    rand_range = upper - lower
    return random.random() * rand_range + lower


    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_info = info
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def __str__(self):
        s = "Ship Object: "
        s += "\n Pos: " + str(self.pos)
        s += "\n Vel: " + str(self.vel)
        s += "\n Thrust: " + str(self.thrust)
        s += "\n Angle: " + str(self.angle)
        s += "\n Angle_vel: " + str(self.angle_vel)
        s += "\n Image_center: " + str(self.image_center)
        s += "\n Image_size: " + str(self.image_size)
        s += "\n Radius: " + str(self.radius)
        return s
        
    def set_vel(self, lst_velocity):
        self.vel[0] = lst_velocity[0]
        self.vel[1] = lst_velocity[1]

    def set_thrust(self, bool_thrust):
        self.thrust = bool_thrust
        # play sound when ship thrusting
        if bool_thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def set_angle_vel(self, flt_angle_vel):
        if flt_angle_vel != 0:
            self.angle_vel = float(flt_angle_vel)
        else:
            self.angle_vel = 0

    def get_position(self):
        return self.pos

    def get_center_pos(self):
        center_pos = [(self.pos[0] + self.image_center[0]), (self.pos[1] + self.image_center[1])]
        return center_pos

    def get_radius(self):
        return self.radius

    def shoot(self):
        #print my_ship
        global a_missile
        
        # calculate the starting position of a missile
        pos = [self.pos[0] + self.radius * math.cos(self.angle), self.pos[1] + self.radius * math.sin(self.angle)]
        missle_vector = angle_to_vector(self.angle)
        vel = [missle_vector[0] * missile_speed, missle_vector[1] * missile_speed]
        # initiazion of a missle
        a_missile = Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        # play missile sound while shooting
        missile_sound.play()
        
        
    def stop_shoot(self):
        #missile_sound.rewind()
        pass


    def draw(self,canvas):
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White"
        if self.thrust:
            self.image_center = [135, 45]
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            self.image_center = [45, 45]
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # adjust angle by angular velocity
        self.angle += self.angle_vel

        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
        # calculate the vector based on the current angle. 
        ship_vector = angle_to_vector(self.angle)

        # if ship is thrusting
        if self.thrust:
            # switch to ship with thrust flame
            # self.image_center[0] += self.image_size[0] / 2
            # adjust velocity if thrusting
            self.vel[0] += ship_vector[0] * ship_speed 
            self.vel[1] += ship_vector[1] * ship_speed 

        self.pos[0] += self.vel[0]
        self.pos[0] = float(self.pos[0] % WIDTH)
        self.pos[1] += self.vel[1]
        self.pos[1] = float(self.pos[1] % HEIGHT)


    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            #sound.play()
   
    def __str__(self):
        s = "Sprite Object: "
        s += "\n Pos: " + str(self.pos)
        s += "\n Vel: " + str(self.vel)
        s += "\n Angle: " + str(self.angle)
        s += "\n Angle_vel: " + str(self.angle_vel)
        s += "\n Image_center: " + str(self.image_center)
        s += "\n Image_size: " + str(self.image_size)
        s += "\n Radius: " + str(self.radius)
        s += "\n Lifespan: " + str(self.lifespan)
        s += "\n Animated: " + str(self.animated)
        return s
    
    def set_vel(self, lst_velocity):
        self.vel[0] = lst_velocity[0]
        self.vel[1] = lst_velocity[1]
        
    def set_angle_vel(self, flt_angle_vel):
        if flt_angle_vel != 0:
            self.angle_vel = float(flt_angle_vel)
    
    def set_pos(self, lst_pos):
        self.pos[0] = lst_pos[0]
        self.pos[1] = lst_pos[1]
        
    def set_angle(self, flt_angle):
        self.angle = float(flt_angle)

    def get_position(self):
        return self.pos
    
    def get_center_pos(self):
        center_pos = [(self.pos[0] + self.image_center[0]), (self.pos[1] + self.image_center[1])]
        return center_pos

    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        # canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # increment age
        self.age += 0.5
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[0] = float(self.pos[0] % WIDTH)
        self.pos[1] += self.vel[1]    
        self.pos[1] = float(self.pos[1] % WIDTH)
        # pass
        if (self.lifespan != None) and (self.age >= self.lifespan):
            return True
        else:
            return False
        

    def collide(self, other_object):
        obj_distance = dist(self.get_center_pos(), other_object.get_center_pos())    
        if (obj_distance <= (self.get_radius() + other_object.get_radius())):
            return True
        else:
            return False

           
def draw(canvas):
    global time, game_on, lives, score
    print "game_on", game_on
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    #canvas.draw_polygon([(0, 0), (WIDTH, 0), (WIDTH, HEIGHT),  (0, HEIGHT)], 5, 'Black', 'Black')
        
    # scores and lives
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # ship draw and update
    my_ship.draw(canvas)
    my_ship.update()

    # rock_group draw and update
    if (len(rock_group) > 0):
        process_sprite_group(rock_group, canvas)
    
    # missile_group draw and update
    if (len(missile_group) > 0):
        process_sprite_group(missile_group, canvas)

    # see if ship collide with rock_group
    if (group_collide(rock_group, my_ship) == True): 
        lives -= 1
        
    # see if missiles hit any rocks, score updated within
    hits = group_group_collide(missile_group, rock_group)
    score += hits
   
    # when game first started
    if game_on == False:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2),splash_info.get_size())
    # when runs out of lives
    elif game_on == True and (lives <= 0):
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2),splash_info.get_size())
        game_on = False
        stop_game()

    
    
def group_group_collide(sprite_group, other_sprite_group):
    # loop through group missiles
    hits = 0
    for sprite in sprite_group:
        ishit = group_collide(other_sprite_group, sprite)
        if (ishit == True):
            hits += 1
            sprite_group.discard(sprite)
    return hits

def group_collide(sprite_group, other_object):
    #print type(other_object)
    remove_sprite = set([])
    for sprite in sprite_group:
        collide = sprite.collide(other_object)
        if collide:
            print "collide"
            remove_sprite.add(sprite)
    sprite_group.difference_update(remove_sprite)
    if len(remove_sprite) > 0:
        return True
    else:
        return False
    
def process_sprite_group(sprite_group, canvas):
    remove_sprite = set([])
    for sprite in sprite_group:
        sprite.draw(canvas)
        if sprite.update():
            remove_sprite.add(sprite)
    sprite_group.difference_update(remove_sprite)
    

def rock_spawn_pos(pos):
    ship_pos = my_ship.get_position()
    if dist(pos, ship_pos) < 100:
        pos[0] += 90
        pos[1] += 90
    return pos
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, lives
    spawn_pos = rock_spawn_pos([int(rand_float(0, WIDTH)), int(rand_float(0, HEIGHT))])
    #spawn_pos = rock_spawn_pos([400, 300])
    if len(rock_group) < ROCK_LIMITS:
        rand_pos = [0,0]
        rand_vel = [0.0, 0.0]
        rand_vel[0] = rand_float(VEL_UPPER, VEL_LOWER)
        rand_vel[1] = rand_float(VEL_UPPER, VEL_LOWER)
        rand_angle_vel = rand_float(ANG_VEL_UPPER, ANG_VEL_LOWER)
        a_rock = Sprite(spawn_pos, rand_vel, 0, rand_angle_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)           

def stop_game():
    global game_on, lives, score, missile_group, rock_group
    timer.stop()
    soundtrack.rewind()
    missile_group = set([])
    rock_group = set([])
    
# reset game helper function
def restart_game():
    global lives, score
    lives = 3
    score = 0
    timer.start()
    soundtrack.play()
    
# mouse click handler
def mouseclick_handler(pos):
    global game_on
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    #print "game_on", game_on
    if (not game_on) and inwidth and inheight:
        game_on = True
        restart_game()

# keydown handler and functions
def keydown(key):
    for i in keyinputs:
        if key == simplegui.KEY_MAP[i]:
            keyinputs[i][0]()

def keyup(key):
    for i in keyinputs:
        if key == simplegui.KEY_MAP[i]:
            keyinputs[i][1]()

def turn_counterclockwise():
    my_ship.set_angle_vel(float(-0.05))

def turn_clockwise():
    my_ship.set_angle_vel(float(0.05))

def thrustfwd():
    my_ship.set_thrust(True) 

def stop_turning():
    my_ship.set_angle_vel(0)

def stop_thrust():
    my_ship.set_thrust(False) 

def shoot_missile():
    my_ship.shoot()

def stop_missle():
    my_ship.stop_shoot()

keyinputs = {"left" : [turn_counterclockwise, stop_turning],
    "right" : [turn_clockwise, stop_turning],
    "up" : [thrustfwd, stop_thrust], 
    "space" : [shoot_missile, stop_missle]}

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# ship initialization
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouseclick_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
#timer.start()