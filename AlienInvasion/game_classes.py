import thumby
import random
import math
import time
from collections import namedtuple, deque


# use namedtuples to simulate enums
ShipDirection = namedtuple("ship_direction", ("none", "left", "right", "up", "down"))
MissileDirection = namedtuple("ship_direction", ("forward", "left", "right"))
FireDirection = namedtuple("ship_direction", ("forward", "side"))
BossState = namedtuple("boss_state", ("inactive", "enter", "beam_down", "wait", "beam_up", "move", "abduct", "exit"))


# BITMAP: width: 72, height: 40
game_logo1 = bytearray([0,0,224,240,24,24,24,240,224,0,0,248,248,0,0,0,0,0,24,24,248,248,24,24,0,0,248,248,152,152,24,24,0,0,248,248,224,192,128,248,248,0,0,0,0,176,104,216,104,176,0,0,0,0,0,0,0,0,0,0,0,16,152,92,22,222,22,92,152,16,0,0,
           0,0,31,31,3,3,3,31,31,0,0,31,31,24,24,24,0,0,24,24,31,31,24,24,0,0,31,31,25,25,24,24,0,0,31,31,0,1,3,31,31,0,0,0,0,0,0,0,0,0,0,0,0,6,29,11,29,6,0,0,0,3,0,0,0,3,0,0,0,3,0,0,
           0,0,3,3,255,255,3,3,0,0,255,255,28,56,112,255,255,0,0,31,127,224,128,224,127,31,0,0,252,254,99,99,99,254,252,0,0,14,31,51,51,51,227,195,0,0,3,3,255,255,3,3,0,0,252,254,135,3,3,135,254,252,0,0,255,255,28,56,112,255,255,0,
           0,0,3,3,3,3,3,3,0,0,3,3,0,0,0,3,3,0,0,0,0,1,3,1,0,0,0,0,3,3,0,0,0,3,3,0,224,147,147,147,227,3,35,1,0,96,147,147,19,3,19,19,240,16,16,1,227,147,147,227,1,240,144,144,243,3,16,16,240,19,19,0,
           0,0,127,73,73,73,54,0,34,0,0,127,73,73,65,0,99,20,8,20,99,0,65,65,127,65,65,0,1,1,127,1,1,0,0,0,7,0,0,0,7,0,2,0,0,4,4,4,3,0,0,0,7,0,0,0,7,0,0,7,0,7,0,1,6,0,0,0,7,0,0,0])

# BITMAP: width: 72, height: 40
game_logo2 = bytearray([0,0,224,240,24,24,24,240,224,0,0,248,248,0,0,0,0,0,24,24,248,248,24,24,0,0,248,248,152,152,24,24,0,0,248,248,224,192,128,248,248,0,0,0,0,48,232,88,232,48,0,0,0,0,0,0,0,0,0,0,0,16,24,148,94,22,94,148,24,16,0,0,
           0,0,31,31,3,3,3,31,31,0,0,31,31,24,24,24,0,0,24,24,31,31,24,24,0,0,31,31,25,25,24,24,0,0,31,31,0,1,3,31,31,0,0,0,0,0,0,0,0,0,0,0,0,22,13,27,13,22,0,0,0,0,3,0,0,0,0,0,3,0,0,0,
           0,0,3,3,255,255,3,3,0,0,255,255,28,56,112,255,255,0,0,31,127,224,128,224,127,31,0,0,252,254,99,99,99,254,252,0,0,14,31,51,51,51,227,195,0,0,3,3,255,255,3,3,0,0,252,254,135,3,3,135,254,252,0,0,255,255,28,56,112,255,255,0,
           0,0,3,3,3,3,3,3,0,0,3,3,0,0,0,3,3,0,0,0,0,1,3,1,0,0,0,0,3,3,0,0,0,3,3,0,224,147,147,147,227,3,35,1,0,96,147,147,19,3,19,19,240,16,16,1,227,147,147,227,1,240,144,144,243,3,16,16,240,19,19,0,
           0,0,127,73,73,73,54,0,34,0,0,127,73,73,65,0,99,20,8,20,99,0,65,65,127,65,65,0,1,1,127,1,1,0,0,0,7,0,0,0,7,0,2,0,0,4,4,4,3,0,0,0,7,0,0,0,7,0,0,7,0,7,0,1,6,0,0,0,7,0,0,0])
          
# BITMAP: width: 1, height: 1
small_star = bytearray([1])

# BITMAP: width: 7, height: 6
ship_none = bytearray([56,28,14,15,14,28,56])

# BITMAP: width: 7, height: 6
ship_left = bytearray([48,60,31,14,14,28,24])

# BITMAP: width: 7, height: 6
ship_right = bytearray([24,28,14,14,31,60,48])

# BITMAP: width: 7, height: 6
ship_forward = bytearray([28,30,15,7,15,30,28])

# BITMAP: width: 7, height: 6
ship_back = bytearray([56,28,12,6,12,28,56])

# BITMAP: width: 7, height: 7
ship_explosion1 = bytearray([73,42,28,127,28,42,73])

# BITMAP: width: 7, height: 7
ship_explosion2 = bytearray([54,85,99,0,99,85,54])

# BITMAP: width: 3, height: 3
missile_forward = bytearray([6,3,6])

# BITMAP: width: 3, height: 3
missile_left = bytearray([2,7,5])

# BITMAP: width: 3, height: 3
missile_right = bytearray([5,7,2])

# BITMAP: width: 5, height: 5
alien1a = bytearray([22,13,27,13,22])

# BITMAP: width: 5, height: 5
alien1b = bytearray([6,29,11,29,6])

# BITMAP: width: 5, height: 5
alien2 = bytearray([19,13,7,13,19])

# BITMAP: width: 5, height: 2
missiles3 = bytearray([3,0,3,0,3])

# BITMAP: width: 5, height: 2
missiles2 = bytearray([0,0,3,0,3])

# BITMAP: width: 5, height: 2
missiles1 = bytearray([0,0,0,0,3])

# BITMAP: width: 5, height: 2
missiles0 = bytearray([0,0,0,0,0])

# BITMAP: width: 8, height: 4
abduction_aliena = bytearray([4,14,13,5,7,15,14,4])

# BITMAP: width: 8, height: 4
abduction_alienb = bytearray([4,6,15,13,5,7,14,12])

# BITMAP: width: 8, height: 4
abduction_alienc = bytearray([12,6,7,15,13,5,6,12])

# BITMAP: width: 8, height: 4
abduction_aliend = bytearray([12,14,5,7,15,13,6,4])

# BITMAP: width: 8, height: 8
beam0a = bytearray([0,0,68,136,136,68,0,0])

# BITMAP: width: 8, height: 8
beam0b = bytearray([0,0,34,68,68,34,0,0])

# BITMAP: width: 8, height: 8
beam0c = bytearray([0,0,17,34,34,17,0,0])

# BITMAP: width: 8, height: 8
beam0d = bytearray([0,0,136,17,17,136,0,0])

# BITMAP: width: 8, height: 8
beam1a = bytearray([0,64,132,136,136,132,64,0])

# BITMAP: width: 8, height: 8
beam1b = bytearray([0,32,66,68,68,66,32,0])

# BITMAP: width: 8, height: 8
beam1c = bytearray([0,16,33,34,34,33,16,0])

# BITMAP: width: 8, height: 8
beam1d = bytearray([0,136,16,17,17,16,136,0])

# BITMAP: width: 8, height: 8
beam2a = bytearray([64,132,136,136,136,136,132,64])

# BITMAP: width: 8, height: 8
beam2b = bytearray([32,66,68,68,68,68,66,32])

# BITMAP: width: 8, height: 8
beam2c = bytearray([16,33,34,34,34,34,33,16])

# BITMAP: width: 8, height: 8
beam2d = bytearray([136,16,17,17,17,17,16,136])

# BITMAP: width: 8, height: 8
beam3a = bytearray([68,136,136,136,136,136,136,68])

# BITMAP: width: 8, height: 8
beam3b = bytearray([34,68,68,68,68,68,68,34])

# BITMAP: width: 8, height: 8
beam3c = bytearray([17,34,34,34,34,34,34,17])

# BITMAP: width: 8, height: 8
beam3d = bytearray([136,17,17,17,17,17,17,136])

# BITMAP: width: 8, height: 32
full_beam = bytearray(
    [
        0,0,17,34,34,17,0,0,
        0,16,33,34,34,33,16,0,
        16,33,34,34,34,34,33,16,
        17,34,34,34,34,34,34,17
    ]
)

# BITMAP: width: 8, height: 8
explosion1 = bytearray([0,0,36,24,24,36,0,0])

# BITMAP: width: 8, height: 8
explosion2 = bytearray([0,40,38,80,26,36,24,0])

# BITMAP: width: 8, height: 8
explosion3 = bytearray([84,169,38,209,26,36,154,101])

# BITMAP: width: 8, height: 8
explosion4 = bytearray([90,169,2,128,1,66,146,37])

# BITMAP: width: 8, height: 8
explosion5 = bytearray([70,129,0,128,1,0,129,69])

class Logo():
    
    def __init__(self):
        self.sprite = thumby.Sprite(72, 40, game_logo1+game_logo2, 0, 0, 0)
        self.frame_rate = 250
        self.timer = time.ticks_ms()
            
    def update(self, t0):
        if time.ticks_diff(self.timer, t0) <= 0:
            self.sprite.setFrame((self.sprite.getFrame() + 1) % 2)
            self.timer = time.ticks_add(t0, self.frame_rate)

class Explosion():
    
    def __init__(self):
        self.sprite = thumby.Sprite(8, 8, explosion1+explosion2+explosion3+explosion4+explosion5, 0, 0, 0)
        self.frame_rate = 100
        self.timer = time.ticks_ms()
        self.done = False
        
    def __lt__(self, other):
        return int(self.done) < int(other.done)
        
    def update(self, t0):
        if time.ticks_diff(self.timer, t0) <= 0:
            # Mark explosion as done
            if self.sprite.getFrame() == 4:
                self.done = True
                self.sprite.setFrame(0)
                return
            # Move sprite to next frame, reset timer
            if not self.done:
                self.sprite.setFrame(self.sprite.getFrame() + 1)
                self.timer = time.ticks_add(t0, self.frame_rate)

    def place(self, x, y):
        self.done = False
        self.timer = time.ticks_add(time.ticks_ms(), self.frame_rate)
        self.sprite.x = x
        self.sprite.y = y
        return self
        

class Star():
    
    def __init__(self, speed, x, y):
        self.sprite = thumby.Sprite(1, 1, small_star, x, y)
        self.frame_rate = speed * 100
        self.timer = time.ticks_ms()
        
    def __lt__(self, other):
        return self.sprite.y < other.sprite.y
    
    def move(self, t0):
        if time.ticks_diff(self.timer, t0) <= 0:
            self.timer = time.ticks_add(t0, self.frame_rate)
            self.sprite.y += 1
            
class Missile():
    
    missile_direction = MissileDirection(*range(3))
    fire_direction = FireDirection(*range(2))
    
    def __init__(self):
        self.sprite = thumby.Sprite(
            3, 3, missile_forward+missile_left+missile_right, 0, 0, 0
        )
        self.direction = Missile.missile_direction.forward
        self.alive = True
        self.move_timer = time.ticks_ms()
        self.frame_rate = 20
        
    def __lt__(self, other):
        return int(not self.alive) + int(self.out_of_bounds()) < int(not other.alive) + int(other.out_of_bounds())
        
    def orient(self, direction):
        self.direction = direction
        self.sprite.setFrame(self.direction)
        self.alive = True
        
    def move(self, t0):
        if time.ticks_diff(self.move_timer, t0) >= 0:
            return
        self.move_timer = time.ticks_add(t0, self.frame_rate)
        if self.direction == Missile.missile_direction.forward:
            self.sprite.y -= 1
        elif self.direction == Missile.missile_direction.left:
            self.sprite.x -= 1
        else:
            self.sprite.x += 1
            
    def out_of_bounds(self):
        return (
            self.sprite.y <= -self.sprite.height
            or self.sprite.x <= -self.sprite.width
            or self.sprite.x > thumby.display.width
        )

class MissileHUD():
    
    def __init__(self):
        self.sprite = thumby.Sprite(5, 2, missiles0+missiles1+missiles2+missiles3, thumby.display.width - 5, thumby.display.height - 2, 0)

    def update(self, num):
        self.sprite.setFrame(num)
            
class Ship():
    
    ship_direction = ShipDirection(*range(5))
    
    def __init__(self, max_missiles):
        self.sprite = thumby.Sprite(7, 6, ship_none+ship_left+ship_right+ship_forward+ship_back, thumby.display.width/2, thumby.display.height/2, 0)
        self.explosion_sprite = thumby.Sprite(7, 6, ship_explosion1+ship_explosion1+ship_explosion2+ship_explosion2, 0, 0)
        self.alive = True
        self.explosion_frames = 10
        self.xvelocity = 0
        self.yvelocity = 0
        self.missile_queue = deque((), max_missiles)
        for _ in range(max_missiles):
            self.missile_queue.append(Missile())
        self.move_timer = time.ticks_ms()
        self.frame_rate = 25
        
        
    def move(self, l, r, u, d, t0):
        if time.ticks_diff(self.move_timer, t0) >= 0:
            return
        self.move_timer = time.ticks_add(t0, self.frame_rate)
        self.sprite.setFrame(
            Ship.ship_direction.left if l
            else Ship.ship_direction.right if r
            else Ship.ship_direction.up if u 
            else Ship.ship_direction.down if d
            else Ship.ship_direction.none
        )
        self.xvelocity = -1 if l else 1 if r else 0
        self.yvelocity = -1 if u else 1 if d else 0
        self.sprite.x += self.xvelocity
        self.sprite.y += self.yvelocity
        
        if self.sprite.x < 0:
            self.sprite.x = 0
        if self.sprite.y < 0:
            self.sprite.y = 0
        if self.sprite.x > thumby.display.width - self.sprite.width:
            self.sprite.x = thumby.display.width - self.sprite.width
        if self.sprite.y > thumby.display.height - self.sprite.height:
            self.sprite.y = thumby.display.height - self.sprite.height
            
    def fire(self, direction):
        if direction == Missile.fire_direction.forward and len(self.missile_queue) > 0:
            new_missile = self.missile_queue.popleft()
            new_missile.orient(Missile.missile_direction.forward)
            new_missile.sprite.x = self.sprite.x + 2
            new_missile.sprite.y = self.sprite.y - 3
            return (new_missile,)
        elif direction == Missile.fire_direction.side and len(self.missile_queue) > 1:
            new_left_missile = self.missile_queue.popleft()
            new_left_missile.orient(Missile.missile_direction.left)
            new_left_missile.sprite.x = self.sprite.x - new_left_missile.sprite.width
            new_left_missile.sprite.y = self.sprite.y + 2
            new_right_missile = self.missile_queue.popleft()
            new_right_missile.orient(Missile.missile_direction.right)
            new_right_missile.sprite.x = self.sprite.x + self.sprite.width - 1
            new_right_missile.sprite.y = self.sprite.y + 2
            return (new_left_missile, new_right_missile,)
        return tuple()
        
class BasicAlien():
    
    def __init__(self):
        self.sprite = thumby.Sprite(5, 5, alien1a+alien1b, 0, 0)
        self.amplitude = random.randint(3, 7)
        self.centerx = 0
        self.centery = 0
        self.move_timer = time.ticks_ms()
        self.speed = 0
        self.alive = True
        self.move_function = lambda x, y: (x + 1, y + 0)
        
    def __lt__(self, other):
        return int(not self.alive) + int(self.out_of_bounds()) < int(not self.alive) + int(other.out_of_bounds())
        
    def score(self):
        return 20 - int(self.speed/10)
        
    def initialize(self, x, y, s, mf):
        self.sprite.x = self.centerx = x
        self.sprite.y = self.centery = y
        self.speed = s
        self.move_function = mf
        
    def move(self, t0):
        if time.ticks_diff(self.move_timer, t0) >= 0:
            return
        self.move_timer = time.ticks_add(t0, self.speed)
        self.sprite.setFrame((self.sprite.getFrame() + 1) % 2)
        self.sprite.x, self.sprite.y = self.move_function(self.sprite.x, self.sprite.y)

    # Check for collision with another sprite
    def collides_with(self, other):
        return (
            other.x - self.sprite.width <= self.sprite.x <= other.x + other.width
            and other.y - self.sprite.height <= self.sprite.y <= other.y + other.height
        )
        
    def out_of_bounds(self):
        return (
            self.sprite.y > self.sprite.height + thumby.display.height
            or self.sprite.x > thumby.display.width
            or self.sprite.x < -self.sprite.width
        )
        
class BeamSegment():
    
    def __init__(self, sprite):
        self.active = False
        self.sprite = thumby.Sprite(8, 8, sprite, 0, 0, 0)
        
        
class BossAlien():
    
    boss_state = BossState(*range(8))
    
    def __init__(self, ship):
        self.ship = ship
        self.sprite = thumby.Sprite(8, 4, abduction_aliena+abduction_alienb+abduction_alienc+abduction_aliend, -4)
        self.beam_segments = [
            BeamSegment(beam) for beam in (
                beam0a+beam0b+beam0c+beam0d,
                beam1a+beam1b+beam1c+beam1d,
                beam2a+beam2b+beam2c+beam2d,
                beam3a+beam3b+beam3c+beam3d,
            )
        ]
        self.state = BossAlien.boss_state.inactive
        self.nextx = 0
        self.nexty = 0
        self.beam_timer = 0
        self.move_timer = time.ticks_ms()
        self.health = 10
        self.speed = 100
        self.animation_speed = 100
        self.animation_timer = 0

    # Place the boss alien when it spawns
    def initialize(self):
        self.sprite.x = random.randint(0, thumby.display.width - self.sprite.width)
        self.sprite.y = -self.sprite.height
        self.nextx = self.sprite.x
        self.nexty = 0
        self.state = BossAlien.boss_state.enter
    
    # Check for collision with another sprite
    def collides_with(self, other):
        return (
            other.x - self.sprite.width <= self.sprite.x <= other.x + other.width
            and other.y - self.sprite.height <= self.sprite.y <= other.y + other.height
        )
    
    # Check for beam collision with ship
    def beam_collides_with_ship(self):
        for beam in filter(lambda x: x.active, self.beam_segments):
            if (
                self.ship.sprite.x - beam.sprite.width <= beam.sprite.x <= self.ship.sprite.x + self.ship.sprite.width
                and self.ship.sprite.y - beam.sprite.height <= beam.sprite.y <= self.ship.sprite.y + self.ship.sprite.height
            ):
                return True
        
    def move(self, t0):
        if time.ticks_diff(self.animation_timer, t0) < 0:
            self.animation_timer = time.ticks_add(t0, self.animation_speed)
            self.sprite.setFrame((self.sprite.getFrame() + 1) % 4)
            for segment in self.beam_segments:
                segment.sprite.setFrame((segment.sprite.getFrame() + 1) % 4)
        if time.ticks_diff(self.move_timer, t0) >= 0:
            return
        self.move_timer = time.ticks_add(t0, self.speed)
        
        if self.state == BossAlien.boss_state.enter:
            self.speed = 100
            # Enter the screen
            self.sprite.y += 1
            if self.sprite.y >= self.nexty:
                self.speed = 200
                self.state = BossAlien.boss_state.beam_down
                
        elif self.state == BossAlien.boss_state.beam_down:
            # Extend the beam down
            for num, segment in enumerate(self.beam_segments, start=1):
                if not segment.active:
                    segment.sprite.x = self.sprite.x
                    segment.sprite.y = self.sprite.y - 4 + num * segment.sprite.height
                    segment.active = True
                    return
            self.beam_timer = time.ticks_add(2000, t0)
            self.state = BossAlien.boss_state.wait
            
        elif self.state == BossAlien.boss_state.wait:
            # Wait with the beam down
            if time.ticks_diff(self.beam_timer, t0) <= 0:
                self.speed = 200
                self.state = BossAlien.boss_state.beam_up
                
        elif self.state == BossAlien.boss_state.beam_up:
            # Retract the beam up
            for segment in reversed(self.beam_segments):
                if segment.active:
                    segment.active = False
                    return
            # Choose a new location, at least 20 pix away
            while abs(self.nextx - self.sprite.x) < 15:
                self.nextx = random.randint(0, thumby.display.width - self.sprite.width)
            self.speed = 50
            self.state = BossAlien.boss_state.move
            
        elif self.state == BossAlien.boss_state.move:
            # Move to a new location
            if self.sprite.x > self.nextx:
                self.sprite.x -= 1
            elif self.sprite.x < self.nextx:
                self.sprite.x += 1
            if self.sprite.x == self.nextx:
                self.speed = 100
                self.state = BossAlien.boss_state.beam_down
                
        elif self.state == BossAlien.boss_state.abduct:
            # Abduct the ship
            ship_moved = False
            self.speed = 100
            if self.ship.sprite.x < self.sprite.x:
                self.ship.sprite.x += 1
                ship_moved = True
            elif self.ship.sprite.x > self.sprite.x:
                self.ship.sprite.x -= 1
                ship_moved = True
            if self.ship.sprite.y > self.sprite.y + self.sprite.height:
                self.ship.sprite.y -= 1
                ship_moved = True
            
            if not ship_moved:
                for beam in self.beam_segments:
                    beam.active = False
                self.speed = 100
                self.state =  BossAlien.boss_state.exit    
                
        elif self.state == BossAlien.boss_state.exit:
            # Move offscreen with the ship
            self.sprite.y -= 1
            self.ship.sprite.y -= 1
            
            # End the game
            if self.ship.sprite.y < -self.ship.sprite.height:
                self.ship.alive = False
                self.state = BossAlien.boss_state.inactive
