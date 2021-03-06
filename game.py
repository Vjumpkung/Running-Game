import pygame
import threading
from datetime import datetime
from environment.background import Background
from environment.snail import Snail
from environment.player import Player
from utils.settings import Settings, get_fps
from utils.queries import MaximumScore, get_top_five
from key_input import KeyboardInput
from time import time

# loading every class here
settings = Settings()
background = Background()
snail = Snail()
player = Player()
maximum = MaximumScore()

'''
    loading constants from settings.py
'''

# constants
NAME = settings.NAME
FPS = 60
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT


class StartGame:

    # loading pygame

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(NAME)


class Font:

    # loading font and size.

    def __init__(self):
        self.font = pygame.font.Font('font/Minecraft.ttf', 50)
        self.fpsfont = pygame.font.Font('font/Minecraftia-Regular.ttf', 20)
        self.score = pygame.font.Font('font/Minecraft.ttf', 30)


class Screen:

    # setup screen size and clock

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()


class Drawing:
    def __init__(self):
        '''
            drawing every surface.
        '''

        font = Font()

        # drawing surface
        self.sky_surface = background.sky_surface
        background.SetSkyColor('lightblue')

        # drawing ground
        self.ground_surface = background.ground_surface
        background.SetGroundColor('lightgreen')

        # drawing font
        self.font_surface = font.font.render(NAME, False, 'Black')
        self.font_position = self.font_surface.get_rect(
            center=(WIDTH/2, (HEIGHT/2) - 300))

        # drawing game over
        self.gameover = font.font.render('GAME OVER', False, 'Black')
        self.gameover_rect = self.gameover.get_rect(
            center=(WIDTH/2, (HEIGHT/2)))

        # drawing score
        self.score_font = font.score.render(f'SCORE : 0', False, 'Black')
        self.score_font_rect = self.score_font.get_rect(topleft=(10, 50))

        # drawing username font
        self.user_font = font.fpsfont.render('GUEST', False, 'Black')
        self.user_font_rect = self.user_font.get_rect(topleft=(1280, 700))

    def username_font(self, username: str):

        font = Font()

        # drawing username
        self.user_font = font.fpsfont.render(username, False, 'Black')
        self.user_font_rect = self.user_font.get_rect(bottomright=(1270, 710))

        # drawing personal best
        self.max_font = font.score.render(
            f'PERSONAL BEST : {maximum.get_max_score(username)}', False, 'Black')
        self.max_font_rect = self.max_font.get_rect(topleft=(10, 80))

    def scoreboard(self):

        # get Top 5 score and show it in leaderboard (Top-Right screen)

        self.Top_Five = get_top_five()

        font = Font()

        for idx, val in enumerate(self.Top_Five):
            exec(
                f"self.number{idx}_font = font.fpsfont.render('{idx+1}. {val['username']} : {val['score']}', False, 'Black')")
            exec(
                f"self.number{idx}_font_rect = self.number{idx}_font.get_rect(topleft=(1050,idx*25+10))")


class Score:

    # update score and save personal best score

    def __init__(self):

        # initialize score = 0

        self.score = 0
        self.font = Font()

    def update_score(self, draw):

        # update score and draw new score into screen.

        self.score += 1
        draw.score_font = self.font.score.render(
            f'SCORE : {self.score}', False, 'Black')

    def reset_score(self, draw):

        # if player collide with snail reset score.

        self.score = 0
        draw.score_font = self.font.score.render(
            f'SCORE : {self.score}', False, 'Black')

    def update_best_score(self, draw, username, isLocal):

        # if player break new record it will update personal best score.
        if isLocal:
            draw.max_font = self.font.score.render(
                f'PERSONAL BEST : {maximum.update_local_score()}', False, 'Black')
        else:
            draw.max_font = self.font.score.render(
                f'PERSONAL BEST : {maximum.get_max_score(username)}', False, 'Black')

# loading everything goes here.


class Game:

    '''
        Loading only one time.
    '''

    def __init__(self, username):

        # game initialize
        self.start = StartGame()
        self.screen = Screen().screen
        self.clock = Screen().clock
        self.draw = Drawing()
        self.font = Font()
        self.score = Score()
        self.now_time = time()
        self.move_per_second = 60
        self.isActive = True

        # put username into lower right
        self.username = username
        self.draw.username_font(self.username)
        self.draw.scoreboard()

    '''
        Loop until you stop the game.
    '''

    def LoopFunction(self):

        running = True

        while running:
            # tick
            self.ms_frame = self.clock.tick(FPS)
            self.move_per_frame = self.move_per_second * self.ms_frame / 1000

            if self.isActive:

                '''
                    When game is still running and not end.
                '''

                # draw everything

                screen = self.screen
                screen.blit(self.draw.sky_surface, (0, 0))
                screen.blit(self.draw.ground_surface, (0, 540))
                screen.blit(self.draw.font_surface, self.draw.font_position)
                screen.blit(player.player_surface, player.player_rect)
                screen.blit(snail.snail_surface, snail.snail_rect)
                screen.blit(get_fps(self.font.fpsfont, self.clock), (10, 10))
                screen.blit(self.draw.score_font, self.draw.score_font_rect)
                screen.blit(self.draw.max_font, self.draw.max_font_rect)
                screen.blit(self.draw.user_font, self.draw.user_font_rect)

                # entities

                if(snail.move(self.move_per_frame)):

                    # updating score
                    self.score.update_score(self.draw)

                    if (maximum.update_score(self.score.score, self.username, isLocal=True)):
                        self.score.update_best_score(
                            self.draw, self.username, isLocal=True)
                        screen.blit(self.draw.max_font,
                                    self.draw.max_font_rect)
                        pygame.draw.rect(screen, "lightblue",
                                         self.draw.max_font_rect)
                        screen.blit(self.draw.max_font,
                                    self.draw.max_font_rect)
                        pygame.display.update(self.draw.max_font_rect)

                    if self.score.score % 5 == 0:
                        snail.add_acceleration()

                # player

                player.add_gravity(self.move_per_frame)
                player.move(self.move_per_frame)
                player.floor()

                # collide check

                if player.isCollide(snail.snail_rect):
                    print(f"{datetime.now()} : OOPS game over.")
                    # stopping game
                    self.isActive = False

                    # update max score
                    maximum.update_score(
                        self.score.score, self.username, isLocal=False)
                    self.score.update_best_score(
                        self.draw, self.username, isLocal=False)
                    screen.blit(self.draw.max_font, self.draw.max_font_rect)
                    pygame.draw.rect(screen, "lightblue",
                                     self.draw.max_font_rect)
                    screen.blit(self.draw.max_font, self.draw.max_font_rect)
                    pygame.display.update(self.draw.max_font_rect)
                    self.draw.scoreboard()
            else:
                '''
                    GAMEOVER when self.isActive = False
                '''
                screen.blit(self.draw.gameover, self.draw.gameover_rect)

            # scoreboard update

            for idx, val in enumerate(self.draw.Top_Five):
                exec(
                    f"screen.blit(self.draw.number{idx}_font, self.draw.number{idx}_font_rect)")

            # get keyboard input

            self.kb = KeyboardInput()

            # updating display

            pygame.display.update()

            # event handle

            for event in pygame.event.get():

                # check quit event

                if event.type == pygame.QUIT:
                    print(f"{datetime.now()} : EXIT.")
                    snail.reset_acceleration()
                    snail.move_to_default()
                    self.score.reset_score(self.draw)
                    self.isActive = False
                    pygame.quit()
                    running = False

                # using SPACE , left click button or up button to jump

                if self.kb.jump(event, pygame.K_SPACE) and 540 <= player.player_rect.bottom <= 542:
                    player.set_gravity(-27)

                # using r to retry game and reset score to 0

                if self.kb.retry(event, pygame.K_r) and not self.isActive:
                    print(f"{datetime.now()} : Retry!!!")
                    snail.reset_acceleration()
                    snail.move_to_default()
                    self.score.reset_score(self.draw)
                    self.isActive = True
                    continue

            # updating scoreboard every 10 seconds
            if(time() - self.now_time > 10):

                self.now_time = time()

                # update max score
                maximum.update_score(
                    self.score.score, self.username, isLocal=True)
                self.score.update_best_score(
                    self.draw, self.username, isLocal=True)

                self.t1 = threading.Thread(
                    target=self.draw.scoreboard(), args=())

                self.t2 = threading.Thread(target=maximum.update_score, args=(
                    self.score.score, self.username, False,))

                print(f'{datetime.now()} : update scoreboard')
                self.t1.start()
                self.t2.start()
                self.t1.join()
                self.t2.join()
