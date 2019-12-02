
 class Fireball(pygame.sprite.Sprite):
    def _init_(self, x,y,facing):
        self.images=(pygame.image.load('resources/images/Fireball/fireball.png'))
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing
        



    fireballs = []


if event.type == pygame.KEYDOWN:
    if event.key == event.key == pygame.K_RIGHT:
        if len(fireballs) < 5:
            fireballs.append(Fireball(round(MySprite.x + MySprite.width // 2)),
                             round(MySprite.y + MySprite.height // 2, ))