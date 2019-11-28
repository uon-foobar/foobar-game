import pygame
 
 
SIZE = WIDTH, HEIGHT = 600, 400 #the width and height of our screen
BACKGROUND_COLOR = pygame.Color('green') #The background colod of our window
FPS = 10 #Frames per second
 
class MySprite(pygame.sprite.Sprite):
    def __init__(self, lower,upper, position_x, position_y):
        super(MySprite, self).__init__()
        self.images = []
        for j in range(lower,upper):
            self.images.append(pygame.image.load('resources/images/Hero_Sprite/tile'+str(j)+'.png'))
 
        self.index = 0
 
        self.image = self.images[self.index]
 
        self.rect = pygame.Rect(position_x, position_y, 24, 32)
        
        self.movex = 0
        self.movey = 0
        self.frame = 0
        
   
 
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
            
            
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    #my_sprite_down = MySprite(0,7,5,5)
    #my_group_down = pygame.sprite.Group(my_sprite_down)
    #my_sprite_up = MySprite(8,15,20,20)
    #my_group_up = pygame.sprite.Group(my_sprite_up)
    #my_sprite_left = MySprite(16,23,50,50)
    #my_group_left = pygame.sprite.Group(my_sprite_left)
    #my_sprite_right = MySprite(24,31,80,80)
    #my_group_right = pygame.sprite.Group(my_sprite_right)
    my_sprite = MySprite(0,31,5,5)
    myGroup = pygame.sprite.Group(my_sprite)
    clock = pygame.time.Clock()
 
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
        
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                    myGroup.update("left")
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    myGroup.update("right")
            if event.key == pygame.K_UP or event.key == ord('w'):
                    myGroup.update("up")
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                    myGroup.update("down")
          
            
        
        myGroup.update("do whatever")
        screen.fill(BACKGROUND_COLOR)
        myGroup.draw(screen)

        pygame.display.update()
        clock.tick(10)
 
if __name__ == '__main__':
    main()
    
 