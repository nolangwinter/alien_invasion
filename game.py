import pygame as pg
from pygame.sprite import GroupSingle
from settings import Settings
from laser import Lasers, LaserType
from alien import Aliens, Extra
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from barrier import Barriers
from button import Button
from random import randint
import sys 


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")
        self.playing = False
        self.extra_spawn_time = randint(1200,2400)


        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)
        self.play_button = Button(game=self, msg="Play")
        self.hc_button = Button(game=self, msg="High Scores")

        self.ship_lasers = Lasers(game=self, settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(game=self, settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.extra = GroupSingle()
        self.settings.initialize_speed_settings()

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT: self.game_over()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.play_button.check_button(self.play_button.msg, mouse_x, mouse_y)
                self.hc_button.check_button(self.hc_button.msg, mouse_x, mouse_y)


    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()    # handled by ship for ship_lasers and by aliens for alien_lasers
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def start_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.play_button.draw_button()
        self.hc_button.draw_button()
        self.scoreboard.prep_aliens_start()
        self.scoreboard.prep_alien_score()
        self.scoreboard.prep_title("Space Invaders")
        pg.display.flip()
        while not self.playing:
            self.handle_events()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(game=self))
            self.extra_spawn_time = randint(4000,8000)



    def play(self):
        self.sound.play_bg()
        while True:     
            self.handle_events() 
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.aliens.update()
            self.extra_alien_timer()
            self.extra.update()
            self.barriers.update()
            # self.lasers.update()    # handled by ship for ship_lasers and by alien for alien_lasers
            self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    g.start_screen()
    # g.play()

if __name__ == '__main__':
    main()
