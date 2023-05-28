import pygame as pg 
# import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    def __init__(self, game): 
        self.game = game
        self.score = 0
        self.level = 1
        self.high_scores = []
        self.read_highscores()
        self.high_score = self.high_scores[0]
        self.ships_left = game.settings.ship_limit
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (0, 0, 0)
        self.font = pg.font.SysFont(None, 48)

        self.ship_image = pg.transform.rotozoom(pg.image.load(f'images/ship.png'), 0, 2.5)

        self.score_image = None 
        self.score_rect = None
        self.alien_score_image = None
        self.alien_score_image = None
        self.alien_points = [10, 20, 30, "??"]
        self.alien_points_y = [250, 150, 50, -50]
        self.alien1_image = pg.transform.rotozoom(pg.image.load(f'images/alien_20.png'), 0, 2.5)
        self.alien2_image = pg.transform.rotozoom(pg.image.load(f'images/alien_10.png'), 0, 2.5)
        self.alien3_image = pg.transform.rotozoom(pg.image.load(f'images/alien_30.png'), 0, 2.5)
        self.alien4_image = pg.transform.rotozoom(pg.image.load(f'images/UFO_0.png'), 0, 5)



        self.ships = Group()
        self.prep_score()
        self.prep_level()
        self.prep_high_score()
        # self.prep_ships()


    def increment_score(self, points): 
        self.score += points
        self.prep_score()
        self.check_high_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        self.high_score = int(round(self.high_score, -1))
        self.high_score_str = "{:,}".format(self.high_score)
        self.high_score_image = self.font.render(self.high_score_str, True,
                                                self.text_color, self.game.settings.bg_color)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.prep_high_score()

    def read_highscores(self):
        with open("high_score.txt") as file:
            for line in file:
                self.high_scores.append(int(line))

        self.high_scores.sort(reverse=True)
        print(self.high_scores)

    def update_highscores(self):
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        file = open("high_score.txt", "w")
        if len(self.high_scores) > 10:
            for num in range(10):
                file.write(f"{self.high_scores[num]}\n")
            file.close()
        else:
            for score in self.high_scores:
                file.write(f"{score}\n")
            file.close()


    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.level), True,
                self.text_color, self.settings.bg_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        for ship_number in range(self.settings.ships_left):
            self.ship_rect = self.ship_image.get_rect()
            self.ship_rect.x = 10 + ship_number * self.ship_rect.width
            self.ship_rect.y = 5
            self.screen.blit(self.ship_image, self.ship_rect)
            

    def prep_aliens_start(self):
        self.alien1_rect = self.alien1_image.get_rect()
        self.alien1_rect.center = self.screen_rect.center
        self.alien1_rect.y -= 250
        self.alien1_rect.x -= 50

        self.alien2_rect = self.alien2_image.get_rect()
        self.alien2_rect.center = self.screen_rect.center
        self.alien2_rect.y -= 150
        self.alien2_rect.x -= 50

        self.alien3_rect = self.alien3_image.get_rect()
        self.alien3_rect.center = self.screen_rect.center
        self.alien3_rect.y -= 50
        self.alien3_rect.x -= 50

        self.alien4_rect = self.alien4_image.get_rect()
        self.alien4_rect.center = self.screen_rect.center
        self.alien4_rect.y += 50
        self.alien4_rect.x -= 50

        self.screen.blit(self.alien1_image, self.alien1_rect)
        self.screen.blit(self.alien2_image, self.alien2_rect)
        self.screen.blit(self.alien3_image, self.alien3_rect)
        self.screen.blit(self.alien4_image, self.alien4_rect)

    def prep_alien_score(self):
        it = 0
        for el in self.alien_points:
            alien_point_str = str(f"= {self.alien_points[it]}")
            self.alien_score_image = self.font.render(alien_point_str, True, self.text_color, self.settings.bg_color)
            self.alien_score_rect = self.score_image.get_rect()
            self.alien_score_rect.center = self.screen_rect.center
            self.alien_score_rect.x += 20
            self.alien_score_rect.y -= self.alien_points_y[it]
            it += 1
            self.screen.blit(self.alien_score_image, self.alien_score_rect)
    

    def prep_title(self, msg):
        self.title_image = self.font.render(msg, True, (255, 255, 0),
            self.settings.bg_color)
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.center = self.screen_rect.center
        self.title_image_rect.y -= 500
        self.screen.blit(self.title_image, self.title_image_rect)


    def highscore_screen(self):
        print("highscore screen")
        self.screen.fill(self.settings.bg_color)
        it = 1
        self.prep_title("High Scores:")
        for score in self.high_scores:
            score_str = str(score)
            self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
            self.score_image_rect = self.score_image.get_rect()
            self.score_image_rect.x = 600
            self.score_image_rect.y = 100 + it * 50
            self.screen.blit(self.score_image, self.score_image_rect)
            it += 1

        pg.display.flip()
        


            


    def reset(self): 
        self.score = 0
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.ships.draw(self.screen)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.prep_ships()