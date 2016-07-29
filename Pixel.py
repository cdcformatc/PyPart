import pygame,math,pygameutils
from Particle import Particle

#admin settings
FIELD_SIZE = 900
FRAME_RATE = 120

class Pixel(Particle):
    def __init__(self, bound, max_speed=15, 
        color = pygame.Color(255,0,0), size=10, gravity=0, friction=1 ):
        super(Pixel, self).__init__(bound,max_speed,color,size,gravity,friction)
        if size>1:
            r = int(self.color.r-self.color.r*.15)
            g = int(self.color.g-self.color.g*.15)
            b = int(self.color.b-self.color.b*.15)
        
            self.child = Pixel(self.bound,size=self.radius-1,color=(r,g,b))
        else:
            self.child = None
        
    def draw(self, screen):
        if self.child:
            self.child.draw(screen)
        pygame.draw.rect(screen, self.color, self.rect)
        
def main():
    screen,clock,font = pygameutils.init(FIELD_SIZE,FIELD_SIZE)
    
    square = Pixel(screen.get_rect(), color=(255,0,0))
    
    done = False
    
    while not done:
        dt,done = pygameutils.frame(screen, clock, FRAME_RATE)
        square.draw(screen)
        
    pygame.quit()

if __name__ == "__main__":
    main()
