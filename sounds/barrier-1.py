import pygame as pg
from pygame.sprite import Sprite, Group

class BarrierPiece(Sprite):
    def __init__(self, game, rect):
        self.rect = rect
        self.game = game
        self.screen = game.screen
    def hit(self): self.kill()
    def update(self): pass
    def draw(self):
        pg.draw.rect(self.screen, pg.Color(0, 255, 0), self.rect)


class Barrier(Sprite):    # not a real Barrier class -- should be made up of many tiny Sprites
                          # you will not get credit for this class unless it is updated to tiny Sprites
    color = 255, 0, 0
    black = 0, 0, 0
    health_colors = {4: pg.Color(0, 255, 0),
                     3: pg.Color(0, 255, 255),
                     2: pg.Color(255, 255, 0),
                     1: pg.Color(255, 125, 0),
                     0: pg.Color(0, 0, 255)}


    def __init__(self, game, rect):
        super().__init__()
        self.screen = game.screen
        self.rect = rect
        self.settings = game.settings
        self.health = 4
        self.pieces = Group()
        self.width, self.height = 40, 20
        self.left, self.top = 0, 0
        # for i in range(3):
        #     for j in range(3):
        #         self.pieces.add(pg.rect(self.left + i * self.width, self.top + j * self.height, self.width, self.height))
        
    def hit(self): # TODO: change to use tiny Sprites
       # if self.health == 0: return
        self.health -= 1
        if self.health == 0: 
            self.kill()
            print("barrier destroyed")

    def is_dead(self): return self.health == 0

    def update(self): 
        # TODO: change to use tiny Sprites to decide if a collision occurred
        self.draw()

    def draw(self): 
        # TODO: change to use tiny Sprites
        for bp in self.pieces:
            bp.draw()

        pg.draw.rect(self.screen, Barrier.health_colors[self.health], self.rect, 0, 20)
        pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width/6)


class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.ship_lasers = game.ship_lasers
        self.alien_lasers = game.alien_lasers
        self.barriers = Group()
        self.create_barriers()

    def create_barriers(self):     
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
        rects = [pg.Rect(x * 2 * width + 1.5 * width, top, width, height) for x in range(4)]   # SP w  3w  5w  7w  SP
        self.barriers = [Barrier(game=self.game, rect=rects[i]) for i in range(4)]
        # for i in range(4):
        #    self.barriers.add(Barrier(game=self.game, rect=rects[i]))

    def hit(self): pass 
    
    def reset(self):
        self.create_barriers()

    def update(self):
        collisions = pg.sprite.groupcollide(self.barriers, self.ship_lasers.lasers, False, True) 
        for barrier in collisions:
            barrier.hit()

        collisions = pg.sprite.groupcollide(self.barriers, self.alien_lasers.lasers, False, True) 
        for barrier in collisions:
            barrier.hit() 
 
        for barrier in self.barriers.sprites():
            if barrier.is_dead():
                barrier.remove()
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers: 
            barrier.draw()

