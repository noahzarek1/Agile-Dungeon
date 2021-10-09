"""Class representing the audio capabilities of Agile Dungeon"""
from enum import Enum
import pygame
from common import util


class Music():
    """Background music object

    Attributes:
        _current_song: Enumerated Song object representing the song being played
        _loops: Integer representing the number of loops to play the music
                Default is -1 (loops indefinitely)
        _current_song_path: String representing the full path of the current song
    """
    class Song(Enum):
        """Songs available to play

        Args:
            Enum (str): Song to play
        """
        DUNGEON01 = "dungeon01.ogg"
        DUNGEON02 = "dungeon02.ogg"
        GAMEOVER = "gameover.ogg"

    def __init__(self, song: Song, loops: int = -1) -> None:
        self._current_song = song
        self._loops = loops

        self._current_song_path = util.get_absolute_path_of_asset("audio", "music", song.value)

    def play(self) -> None:
        """Play the object's music"""
        pygame.mixer.music.load(self._current_song_path)
        pygame.mixer.music.play(self._loops)

    def get_current_song(self) -> Song:
        """Get the current song

        Returns:
            Song: Song enum representing the current song
        """
        return self._current_song

    def get_current_song_path(self) -> str:
        """Get the current song path

        Returns:
            str: Sring representing the current song's full path
        """
        return self._current_song_path

    def get_loops(self) -> int:
        """Get the number of loops for the current song

        Returns:
            int: Number of loops
        """
        return self._loops


class SoundEffect():
    """Sound Effect objects

    Attributes:
        _sound_effect : Sound effect to play
        _full_path = Full path of the sound effect
        _sound_object = pygame.mixer.Sound object for the sound effect
    """
    class Effect(Enum):
        """Sound effects available to play

        Args:
            Enum (str): Sound effect to play
        """
        ARROW = "arrow.ogg"
        LASER01 = "laser01.wav"
        LASER02 = "laser02.wav"
        PAIN01 = "pain01.ogg"
        HEAL01 = "heal01.ogg"

    def __init__(self, sound_effect: Effect):
        self._sound_effect = sound_effect
        self._full_path = util.get_absolute_path_of_asset("audio", "effects", sound_effect.value)
        self._sound_object = pygame.mixer.Sound(self._full_path)

    def play(self) -> None:
        """Play the current sound effect"""
        self._sound_object.play()
