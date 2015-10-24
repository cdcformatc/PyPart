from __future__ import division
import sys, pygame, math, os
from vec2d import Vec2d
from Particle import Particle
os.environ['SDL_VIDEO_CENTERED'] = '1'

#admin settings
FIELD_SIZE = 900
MAX_LEVELS = 1000
FRAME_RATE = 120

#difficulty settings
GAME_LENGTH = 10
PLAYER_LIVES = 5

#physics settings
FRICTION_COEFFICIENT = .995
GRAVITY = 0
KEY_ACCEL = 0.325,0.325
MAX_SPEED = 15

def read_keyboard():
    x = pygame.key.get_pressed()
    if x[pygame.K_ESCAPE] or x[pygame.K_q] or x[pygame.K_BREAK]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
def main():
    pygame.init()
    clock = pygame.time.Clock()  
    pygame.key.set_repeat(1, 50)
    size = FIELD_SIZE, FIELD_SIZE
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("Courier New", 18)
    black = 0, 0, 0
    
    ball = Particle(screen.get_rect(), max_speed=15, color=(125,5,230), gravity=GRAVITY, friction=FRICTION_COEFFICIENT)
    
    grid = []
    
    for i in range(100, FIELD_SIZE, 100):
        for j in range(100, FIELD_SIZE, 100):
            new = Particle(screen.get_rect(), size=1, max_speed=0, color=(255,255,255), gravity=0, friction=0)
            new.set(i,j)
            grid.append(new)
    
    done = False
    while not done:
        dt = clock.tick(FRAME_RATE) #limit to 120 fps
        screen.fill(black)
        read_keyboard()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        # ball.move_keyboard(pygame.key.get_pressed(),KEY_ACCEL)
        ball.move_mouse(50/FRAME_RATE)
        ball.movetowards((450,450),KEY_ACCEL)
        
        ball.move()
        ball.draw(screen)
        
        for dot in grid:
            dot.draw(screen)
        
        pygame.display.flip()
    pygame.quit()

def collision(a, b):
    normal = Vec2d(a.x - b.x, a.y - b.y).normalized()
    
    vab = a.speed - b.speed
    e = 1
    
    j = (-(1 + e) * vab).dot(normal) / normal.dot(2 * normal)
    
    a.speed = a.speed + j * normal
    b.speed = b.speed + j * normal
    
    print normal
    
if __name__ == "__main__":
    main()