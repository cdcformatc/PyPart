from __future__ import division
import pygame,math,pygameutils
from Particle import Particle

#admin settings
FIELD_SIZE = 900
FRAME_RATE = 120

COLOR_CYCLE_RATE = 100
MOVE_RATE = 100
MOVE_AMPLITUDE = 450
DECAY_RATE = 1000

class Pixel(Particle):
    def __init__(self, bound, max_speed=15, 
        color = (255,255,0), size=100, gravity=0, friction=1, children=0):
        super(Pixel, self).__init__(bound,max_speed,color,size,children,gravity,friction)
                
        if children>0:
            self.child = Pixel(self.bound,size=size,color=(red,green,blue), children=children-1)
        else:
            self.child = None
        
    def draw(self, screen):
        if self.child:
            self.child.draw(screen)
        
        pygame.draw.rect(screen, self.color, self.rect)
        
    def movecenter(self, center):
        oldcenter = (self.x, self.y)
        self.x, self.y = center
        self.rect.center = center
        if self.child:
            self.child.movecenter(oldcenter)
            
def damped_spring(t,phi=0):

    a = MOVE_AMPLITUDE
    g = 1/DECAY_RATE
    w = 1/MOVE_RATE
    
    return a * math.e**(-g * t) * math.cos(w * t-phi*2*math.pi)
        
def main():
    screen,clock,font = pygameutils.init(FIELD_SIZE,FIELD_SIZE)
    size=100
    num = int(FIELD_SIZE*2/size)
    squares=[]
    
    for i in range(num):
        square = Pixel(screen.get_rect(), size=size, children=0)
        
        square.x = i * size/2 + size/2
        square.phi = i/num
        square.color.hsla =(square.phi * 360,100,50,100)
        
        print square.color
        
        squares.append(square)
    
    done = False
    elapsed = 0
    amp=1
    while not done:
        dt,done = pygameutils.frame(screen, clock, FRAME_RATE)
        elapsed += dt
        
        for square in squares:
            square.draw(screen)
            # square.color.hsla =((elapsed*COLOR_CYCLE_RATE/1000)%360,100,50,100)
            
            if amp != 0:
                amp = round(damped_spring(elapsed,square.phi),4)
            
            
            y = screen.get_rect().height/2 + amp
            square.movecenter((square.x,int(y)))
        
    pygame.quit()

if __name__ == "__main__":
    main()
