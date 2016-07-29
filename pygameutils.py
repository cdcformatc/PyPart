import pygame

def read_keyboard():
    x = pygame.key.get_pressed()
    if x[pygame.K_ESCAPE] or x[pygame.K_q] or x[pygame.K_BREAK]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        
def init(fieldw,fieldh):
    pygame.init()
    clock = pygame.time.Clock()  
    pygame.key.set_repeat(1, 50)
    size = fieldw, fieldh
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("Courier New", 18)
    black = 0, 0, 0
    return screen,clock,font
    
def frame(screen, clock, rate):
    dt = clock.tick(rate) #limit fps
    read_keyboard()
    pygame.display.flip()
    screen.fill((0,0,0))
    done = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    return dt,done
    