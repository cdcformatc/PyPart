import sys, pygame,math,os
from Particle import Particle
os.environ['SDL_VIDEO_CENTERED'] = '1'

#admin settings
FIELD_SIZE = 300
MAX_LEVELS = 1000

#difficulty settings
GAME_LENGTH = 10
PLAYER_LIVES = 5

#physics settings
FRICTION_COEFFICIENT = 0.995
GRAVITY = 0.25
KEY_ACCEL = 0.5
MAX_SPEED = 15

def read_keyboard(accel):
    x_accel = 0
    y_accel = 0
    
    x = pygame.key.get_pressed()
    if x[pygame.K_UP] or x[pygame.K_w]:
        y_accel+=-accel
    if x[pygame.K_DOWN] or x[pygame.K_s]:
        y_accel+=accel
    if x[pygame.K_RIGHT] or x[pygame.K_d]:
        x_accel+=accel
    if x[pygame.K_LEFT] or x[pygame.K_a]:
        x_accel+=-accel
    if x[pygame.K_ESCAPE] or x[pygame.K_q] or x[pygame.K_BREAK]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    mag =  math.hypot(x_accel, y_accel)
    if mag > accel:
        x_accel *= accel / mag
        y_accel *= accel / mag
        
    return x_accel, y_accel

def main():
    pygame.init()
    clock = pygame.time.Clock()  
    pygame.key.set_repeat(1, 50)
    size = FIELD_SIZE, FIELD_SIZE
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("Courier New", 18)
    black = 0, 0, 0
    
    ball = Particle(screen.get_rect(), max_speed=15, color=(125,5,230))
    # ball.reset()
    ball.set_gravity(GRAVITY)
    ball.set_friction(FRICTION_COEFFICIENT)
    
    done = False
    
    while not done:
        dt = clock.tick(120) #limit to 120 fps
        screen.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        ball.speed +=  read_keyboard(KEY_ACCEL)
        
        ball.move(0)
        ball.draw(screen)  
        
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