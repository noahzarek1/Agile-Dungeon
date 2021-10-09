"""Implements the Menu that appears at the start of the game and while paused."""
import os
import pygame
from common import util

class Menu():

    """Class representing a starting and pause menu during gameplay"""
    def __init__(self, screen_dimensions):
        # Hang on to screen size for a sec
        self._screen_dimensions = screen_dimensions

        pygame.sprite.Sprite.__init__(self)

        self._font_text = pygame.freetype.Font(util.get_absolute_path_of_asset("other", "fonts", "Macondo-Regular.ttf"))

        # Fetch images from the dir
        img_path = util.get_absolute_path_of_asset("images", "screens", "main.png")
        self._image = pygame.image.load(img_path)

        paused_img_path = util.get_absolute_path_of_asset("images", "screens", "paused.png")
        self._paused_image = pygame.image.load(paused_img_path)

        game_over_img_path = util.get_absolute_path_of_asset("images", "screens", "gameover.png")
        self._game_over_image = pygame.image.load(game_over_img_path)

        #self._score = pygame.

    def draw_main_menu(self):
        # Display image loaded in init
        scene = pygame.display.set_mode(self._screen_dimensions)
        scene.blit(self._image, (0, 0))

        x_pos = 525
        y_pos = 500
        score_list = self.read_high_scores()
        self._font_text.render_to(scene, (x_pos, y_pos - 1), "High Scores: ", size=24)
                
        self._font_text.render_to(scene, (x_pos + 130, y_pos), str(score_list[0]), size=24)
        self._font_text.render_to(scene, (x_pos + 130, y_pos + 30), str(score_list[1]), size=24)
        self._font_text.render_to(scene, (x_pos + 130, y_pos + 60), str(score_list[2]), size=24)

        self._font_text.render_to(scene, (300, 660), "wasd to move - click to shoot arrows - number keys to use items", size=24)
        self._font_text.render_to(scene, (500, 690), "Press any key to continue ", size=24)

    def draw_pause_menu(self):
        scene = pygame.display.set_mode(self._screen_dimensions)
        scene.blit(self._image, (0, 0))
        pygame.display.set_mode(self._screen_dimensions).blit(self._paused_image, (0, 0))

        self._font_text.render_to(scene, (500, 500), "Paused", size=30)
        self._font_text.render_to(scene, (500, 600), "Press 'p' to resume game", size=24)

    def draw_game_over(self):
        scene = pygame.display.set_mode(self._screen_dimensions)
        scene.blit(self._image, (0, 0))
        pygame.display.set_mode(self._screen_dimensions).blit(self._game_over_image, (0, 0))

    def read_high_scores(self):
        temp_d = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(temp_d, 'high_scores.txt')

        score_file = open(filename,"rt+")
        scores = score_file.readline()
        score_list = scores.split(",")
        score_int_list = list(map(int, score_list))
        score_file.close()
        return score_int_list

    def update_high_scores(self, new_score):
        score_changed = False
        temp_d = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(temp_d, 'high_scores.txt')

        score_file = open(filename,"rt+")
        scores = score_file.readline()
        score_list = scores.split(",")
        score_int_list = list(map(int, score_list))
        temp = 0
        for i in range(len(score_int_list)):
            if new_score >= score_int_list[i]:
                score_changed = True
                temp = score_int_list[i]
                score_int_list[i] = new_score
                score_str_list = list(map(str, score_int_list))
                glue = ","
                score_write_out = glue.join(score_str_list)
                new_score = temp

        if score_changed:
            score_file.seek(0)
            score_file.write(score_write_out)
            score_file.truncate()
            score_file.close()
