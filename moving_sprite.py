import pygame
import random
import testingMaps
 
 
SIZE = WIDTH, HEIGHT = 1200, 800 #the width and height of our screen
BACKGROUND_COLOR = pygame.Color('pink') #The background colour of our window
FPS = 20 #Frames per second
number_of_coins = 100
 
class MySprite(pygame.sprite.Sprite):
    def __init__(self, lower,upper, position_x, position_y):
        super(MySprite, self).__init__()
        self.images = []
        for j in range(lower,upper):
            self.images.append(pygame.image.load('resources/images/Hero_Sprite/tile'+str(j)+'.png'))
 
    #Initialisation of variables used to create the image list
    #This list is iterated through (like a flipbook) to generate animations
        self.index = 0
        self.image = self.images[self.index]
        #self.rect = pygame.Rect(position_x, position_y, 24, 32)
        self.rect = pygame.Rect(position_x, position_y, 30, 30)
        
        #self.movex = 0
        #self.movey = 0
        #self.frame = 0
        
    def update(self, direction):
        
        
        if direction == "left":
            self.rect.x -= 10
            self.index+=1
            if self.index <15 or self.index >23:
                self.index = 16
            self.image = self.images[self.index]
        if direction == "right":
            self.index+=1
            self.rect.x += 10
            if self.index <24 or self.index >30:
                self.index = 24
            self.image = self.images[self.index]
        if direction == "up":
            self.rect.y -= 10
            self.index+=1
            if self.index <8 or self.index >15:
                self.index = 8
            self.image = self.images[self.index]
        if direction == "down":
            self.rect.y += 10
            self.index+=1
            if self.index <0 or self.index >7:
                self.index = 0
            self.image = self.images[self.index]
            
class coins(pygame.sprite.Sprite):
    
    def __init__ (self,upper,lower,position_x,position_y):
        super(coins, self).__init__()
        self.images = []
        for j in range (upper,lower):
            self.images.append(pygame.image.load("resources/images/Coin_Sprite/Coin"+str(j)+".png"))
            
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(position_x, position_y, 30, 30)
    
    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

"""        
class projectile(pygame.sprite.Sprite):
    def __init__(self, x,y,radius,color,facing):
        super(projectile, self).__init__()
        self.x = x
        self.y = y 
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
"""
        
"""
class enemies(pygame.sprite.Sprite):
    
    def __init__(self, upper,lower, position_x, position_y):
        super(self).__init__()
        self.images = []
        for j in range (upper, lower)
            
"""
            
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    my_sprite = MySprite(0,31,random.randrange(1200),random.randrange(800))
    #coin_1 = coins(1,6,50,50)
    all_sprites = pygame.sprite.Group(my_sprite)
    all_coins = pygame.sprite.Group()
    #test_projectile = projectile(50,50,50,"blue","left")
    font = pygame.font.SysFont("Courier New", 40)
    coin_number = number_of_coins
    #all_sprites.add(test_projectile)
    
    for i in range(number_of_coins):
    # This represents a block
        block = coins(1,6,random.randrange(1200),random.randrange(800))
 
    # Add the block to the list of objects
        all_coins.add(block)
        all_sprites.add(block)
    
    clock = pygame.time.Clock()
 
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                    my_sprite.update("left")
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    my_sprite.update("right")
            if event.key == pygame.K_UP or event.key == ord('w'):
                    my_sprite.update("up")
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                    my_sprite.update("down")
        
       # blocks_hit_list = pygame.sprite.spritecollide(my_sprite, all_coins, True)
        if pygame.sprite.spritecollide(my_sprite, all_coins, True):
            print("coin collected")
            #coin_number -= coin_number
            #print(coin_number)
        
        #coin_counter = font.render(str(coin_number), False, (0, 0, 0))
        
        #for block in blocks_hit_list:
            #score +=1
            #print(score)
                    
        

        all_coins.update()
                    
        #myGroup.update("do whatever")
        screen.fill(BACKGROUND_COLOR)
        #screen.blit(coin_counter,(HEIGHT//2,WIDTH//2))
        all_sprites.draw(screen)

        pygame.display.update()
        clock.tick(FPS)
 
#if __name__ == '__main__':
    #main()
main()