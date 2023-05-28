import pygame.font

class Button():

    def __init__(self, game, msg):
        self.game = game
        self.screen = self.game.screen
        self.scoreboard = self.game.scoreboard
        self.screen_rect = self.screen.get_rect()
        self.msg = msg
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (118, 238, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Build the button's rect object and center it.
       # self.rect = pygame.Rect(0, 0, self.width, self.height)
        # self.rect.center = self.screen_rect.center
        # The button message needs to be prepped only once.
        self.button_loc(msg)
        self.prep_msg(msg)

    def button_loc(self, msg):
        if msg == "Play":
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.center = self.screen_rect.center
            self.rect.y += 200
        elif msg == "High Scores":
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.center = self.screen_rect.center
            self.rect.y += 300



    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def check_button(self, msg, mouse_x, mouse_y):
        """Start a new game when the player clicks Play."""
        if self.rect.collidepoint(mouse_x, mouse_y):
            if msg == "Play":
                print("play")
                self.game.playing = True
                self.game.play()
            elif msg == "High Scores":
                print('highscore')
                self.scoreboard.highscore_screen()


    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
