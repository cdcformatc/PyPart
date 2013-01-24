import pygame,math
from vec2d import Vec2d
RED = (255, 0, 0)
ZERO_THRESHOLD = 2

class Particle:
    def __init__(self, bound, max_speed, size=10):
        print "init"
        self.bound = bound
        r,g,b = RED
        self.color = pygame.Color(r,g,b)
        self.rect = pygame.Rect(bound.right / 2, bound.bottom / 2, size, size)
        self.radius = size
        self.child = None
        self.max_speed = max_speed
        # if size>1:
            # self.child = myPlayer(bound,size-1)
        # else:
            # self.child = None
        self.reset()
    
    def set(self,x,y):
        self.rect.center = x,y
        self.x, self.y = self.rect.center
        
        if self.child:
            self.child.set(x, y)
        
    def reset(self):
        self.set(self.bound.right / 2, self.bound.bottom / 2)
        self.speed = Vec2d(0, 0)
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
        if self.child:
            self.child.draw(screen)
        
    def fix_speed(self):
        speed = self.speed.get_length()
        if speed > self.max_speed:
            self.speed *= self.max_speed / speed
        if(round(self.speed[0], ZERO_THRESHOLD) == 0):
            self.speed[0] = 0
        
        if(round(self.speed[1], ZERO_THRESHOLD) == 0):
            self.speed[1] = 0
        
    def friction(self, c):
        self.speed *= c
        self.fix_speed()
            
    def gravity(self, grav):
        self.speed[1] += grav
        self.fix_speed()
    
    def move(self, c, mode = 1):
        self.friction(c)
        
        oldcenter = (self.x, self.y)
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect.center = (self.x, self.y)
        
        if mode==1:#wrap
            if self.x < self.bound.left:
                self.x = self.bound.right
            elif self.x > self.bound.right:
                self.x = self.bound.left
            
            if self.y < self.bound.top:
                self.y = self.bound.bottom
            elif self.y > self.bound.bottom:
                self.y = self.bound.top
        elif mode==0:
            if self.x + self.radius < self.bound.left:
                self.x = self.bound.left+ self.radius 
                self.speed[0] *= -1.95
            elif self.x - self.radius > self.bound.right:
                self.x = self.bound.right - self.radius 
                self.speed[0] *= -1.95
            
            if self.y - self.radius < self.bound.top:
                self.y = self.bound.top + self.radius
                self.speed[1] *= -1.95
            elif self.y + self.radius  > self.bound.bottom:
                self.y = self.bound.bottom - self.radius
                self.speed[1] *= -1.95
                
        if self.child:
            self.child.movecenter(oldcenter)
            
            
    def movecenter(self, center):
        oldcenter = (self.x, self.y)
        self.x, self.y = center
        self.rect.center = center
        if self.child:
            self.child.movecenter(oldcenter)
        
        #self.set(center[0],center[1])
        
    def collide(self, other):
        return self.rect.colliderect(other.rect)
    
    def movetowards(self, target_pos, accel, friction):
        target_x, target_y = target_pos[0], target_pos[1]
        
        dist_right = self.bound.right - self.x
        dist_left = self.x - self.bound.left
        dist_top = self.y - self.bound.top
        dist_bottom = self.bound.bottom - self.y
        
        enemy_dist_right = self.bound.right - target_x
        enemy_dist_left = target_x - self.bound.left
        enemy_dist_top = target_y - self.bound.top
        enemy_dist_bottom = self.bound.bottom - target_y
        
        x_accel = 0
        y_accel = 0
        
        #am i to the right of enemy?
        if self.x > target_x:
            #what is closer? the enemy or the right wall?
            if self.x - target_x < dist_right + enemy_dist_left: 
                #go left
                x_accel =- accel
            elif self.x - target_x > dist_right + enemy_dist_left:
                #go right
                x_accel = accel
        
        #am i to the left of enemy?
        elif self.x < target_x:
            #what is closer? the enemy or the left wall?
            if target_x - self.x > dist_left + enemy_dist_right:
                #go left
                x_accel =- accel
            elif target_x - self.x < dist_left + enemy_dist_right:
                #go right
                x_accel = accel

        #am i underneath enemy?
        if self.y > target_y:
            #what is closer? the enemy or the bottom wall?
            if self.y - target_y < dist_bottom + enemy_dist_top:
                #go up
                y_accel =- accel
            elif self.y - target_y > dist_bottom + enemy_dist_top:
                #go down
                y_accel = accel
        #am i above enemy?
        elif self.y < target_y:
            #what is closer? the enemy or the top wall?
            if target_y - self.y > dist_top + enemy_dist_bottom:
                #go up
                y_accel =- accel
            elif target_y - self.y < dist_top + enemy_dist_bottom:
                #go down
                y_accel = accel
        
        self.speed += [x_accel, y_accel]
    
        self.move(friction)    
            