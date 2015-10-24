import pygame,math
from vec2d import Vec2d
ZERO_THRESHOLD = 2

class Particle:
    def __init__(self, bound, max_speed=15, 
        color = pygame.Color(255,0,0), size=10, gravity=0, friction=1 ):
        self.bound = bound
        if isinstance(color,list) or isinstance(color,tuple):
            try:
                r,g,b = color
                self.color = pygame.Color(r,g,b)
            except:
                print "Invalid color object",color
                self.color = pygame.Color(255,0,0)
        elif isinstance(color,pygame.Color):
            self.color = color
        else:
            try:
                self.color = pygame.Color(color)
            except:
                print "Invalid color object",color
                self.color = pygame.Color(255,0,0)
            
        self.rect = pygame.Rect(bound.right / 2, bound.bottom / 2, size, size)
        self.radius = size
        self.child = None
        self.max_speed = max_speed
        self.set_gravity(gravity)
        self.set_friction(friction)
        if size>1:
            r = int(self.color.r-self.color.r*.15)
            g = int(self.color.g-self.color.g*.15)
            b = int(self.color.b-self.color.b*.15)
        
            self.child = Particle(self.bound,size=self.radius-1,color=(r,g,b))
        else:
            self.child = None
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
        if self.child:
            self.child.draw(screen)
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
        
    def limit_speed(self):
        speed = self.speed.get_length()
        if speed > self.max_speed:
            self.speed *= self.max_speed / speed
        if(round(self.speed[0], ZERO_THRESHOLD) == 0):
            self.speed[0] = 0
        
        if(round(self.speed[1], ZERO_THRESHOLD) == 0):
            self.speed[1] = 0
        
    def set_friction(self, mu):
        self.friction = mu
    
    def apply_friction(self):
        self.speed *= self.friction
    
    def set_gravity(self, gravity):
        self.gravity = gravity
    
    def apply_gravity(self):
        self.speed[1] += self.gravity
    
    def move_wrap(self):
        self.move_gen(1)
        
    def move(self):
        self.move_gen(0)
    
    def move_gen(self, mode = 1):
        self.apply_friction()
        self.apply_gravity()
        
        oldcenter = (self.x, self.y)
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect.center = (self.x, self.y)
        
        if mode == 1:#wrap
            if self.x < self.bound.left:
                self.x = self.bound.right
            elif self.x > self.bound.right:
                self.x = self.bound.left
            if self.y < self.bound.top:
                self.y = self.bound.bottom
            elif self.y > self.bound.bottom:
                self.y = self.bound.top
        elif mode == 0:
            if self.x - self.radius <= self.bound.left:
                self.x = self.bound.left+self.radius
                self.speed *= [-.95,.95]
            elif self.x + self.radius >= self.bound.right:
                self.x = self.bound.right - self.radius 
                self.speed *= [-.95,.95]
            if self.y - self.radius < self.bound.top:
                self.y = self.bound.top + self.radius
                self.speed *= [0.95,-.95]
            elif self.y + self.radius  > self.bound.bottom:
                self.y = self.bound.bottom - self.radius
                self.speed*=[0.95,-.95]
                
        self.limit_speed()
        
        if self.child:
            self.child.movecenter(oldcenter)
            
    def movecenter(self, center):
        oldcenter = (self.x, self.y)
        self.x, self.y = center
        self.rect.center = center
        if self.child:
            self.child.movecenter(oldcenter)
        
    def collide(self, other):
        return self.rect.colliderect(other.rect)
    
    def movetowards_wrap(self, target_pos, accel):
        target_x, target_y = target_pos[0], target_pos[1]
        
        dist_right = self.bound.right - self.x
        dist_left = self.x - self.bound.left
        dist_top = self.y - self.bound.top
        dist_bottom = self.bound.bottom - self.y
        
        target_dist_right = self.bound.right - target_x
        target_dist_left = target_x - self.bound.left
        target_dist_top = target_y - self.bound.top
        target_dist_bottom = self.bound.bottom - target_y
        
        x_accel = 0
        y_accel = 0
        
        #am i to the right of target?
        if self.x > target_x:
            #what is closer? the target or the right wall?
            if self.x - target_x < dist_right + target_dist_left: 
                #go left
                x_accel =- accel[0]
            elif self.x - target_x > dist_right + target_dist_left:
                #go right
                x_accel = accel[0]
        
        #am i to the left of target?
        elif self.x < target_x:
            #what is closer? the target or the left wall?
            if target_x - self.x > dist_left + target_dist_right:
                #go left
                x_accel =- accel[0]
            elif target_x - self.x < dist_left + target_dist_right:
                #go right
                x_accel = accel[0]

        #am i underneath target?
        if self.y > target_y:
            #what is closer? the target or the bottom wall?
            if self.y - target_y < dist_bottom + target_dist_top:
                #go up
                y_accel =- accel[1]
            elif self.y - target_y > dist_bottom + target_dist_top:
                #go down
                y_accel = accel[1]
        #am i above target?
        elif self.y < target_y:
            #what is closer? the target or the top wall?
            if target_y - self.y > dist_top + target_dist_bottom:
                #go up
                y_accel =- accel[1]
            elif target_y - self.y < dist_top + target_dist_bottom:
                #go down
                y_accel = accel[1]
        
        self.speed += [x_accel, y_accel]
    
        self.move_wrap()
        
    def movetowards(self, target_pos, accel):
        target_x, target_y = target_pos[0], target_pos[1]
        
        dist_right = self.bound.right - self.x
        dist_left = self.x - self.bound.left
        dist_top = self.y - self.bound.top
        dist_bottom = self.bound.bottom - self.y
        
        target_dist_right = self.bound.right - target_x
        target_dist_left = target_x - self.bound.left
        target_dist_top = target_y - self.bound.top
        target_dist_bottom = self.bound.bottom - target_y
        
        x_accel = 0
        y_accel = 0
        
        #am i to the right of target?
        if self.x > target_x:
            #go left
            x_accel =- accel[0]

        #am i to the left of target?
        elif self.x < target_x:
            #go right
            x_accel =+ accel[0]

        #am i underneath target?
        if self.y > target_y:
            #go up
            y_accel =- accel[1]
        #am i above target?
        elif self.y < target_y:
            #go up
            y_accel =+ accel[1]
        
        self.speed += [x_accel, y_accel]
    
        self.move()
        
    def move_keyboard(self, pressed, accel):
        x_accel = 0
        y_accel = 0
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            y_accel-=accel[1]
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            y_accel+=accel[1]
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            x_accel+=accel[0]
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            x_accel-=accel[0]
        
        self.speed += x_accel,y_accel
        
    def move_mouse(self,per_frame):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            ballpos = self.x, self.y
            self.speed[0] = (pos[0]-self.x)*per_frame
            self.speed[1] = (pos[1]-self.y)*per_frame
            
    def draw_line(self, screen, pos, thresh):
        if thresh==0 or (self.x-pos[0])**2 + (self.y-pos[1])**2 < thresh**2:
            pygame.draw.line(screen, self.color, self.rect.center, pos, self.radius)
