"""Class which runs the game"""

import pygame
from common.scene import Scene
from common.state import State


class Game:
    """Class representing the game
    Attributes:
        scene (Scene): Scene represening the game window
        state (State): The current state of the game
        fps (int): Frames per second
        running (bool): Whether the game is running or not
    """
    def __init__(self) -> None:
        self._scene = Scene(1280, 768)

        self._state = State()
        self._fps = 60
        self._running = False
        # self._started = False

    def run_game(self) -> None:
        """Start the game"""
        pygame.init()
        self._running = True

        # Set the window title
        pygame.display.set_caption("Agile Dungeon")

        # Display menu
        # main_menu = menu.Menu((1280, 768))

        # Main game loop
        while self._running:
            # Tick the clock forward how ever many fps
            pygame.time.Clock().tick(self._fps)

            self._state.update()
            self._scene.draw_state(self._state)

            # Flip the display
            pygame.display.flip()

            # Check for start, quit, or pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if self._state.started is False:
                        self._state.started = True
                        self._state.paused = False
                    if self._state.game_is_over():
                        self._scene.menu.update_high_scores(self._state.get_score())
                        self._state.paused = False
                        self._state.spawn()
                        self._state.enter_new_dungeon()
                    if event.key == pygame.K_p:
                        self._state.paused = not self._state.paused
        self._scene.menu.update_high_scores(self._state.get_score())
        pygame.quit()

    def has_started(self) -> bool:
        """Check if the game has started.
        Returns:
            bool: Whether the game has started
        """
        return self._started
