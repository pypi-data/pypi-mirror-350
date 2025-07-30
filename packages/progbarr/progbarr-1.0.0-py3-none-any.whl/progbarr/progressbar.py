"""Defines the `ProgressBar` class."""

from typing import Optional, Self
from printly import style as apply_color
from printly.types import Color


class ProgressBar:  # pylint: disable=too-many-instance-attributes
    """Represents a progress bar."""

    _pointer: int
    _pace: float
    _fill_char: str
    _place_holder: str
    _left_char: str
    _right_char: str

    def __init__(  # pylint: disable=too-many-arguments
        self: Self,
        job: str,
        tasks: int,
        length: int,
        chars: str,
        color: Optional[Color] = None,
        bgcolor: Optional[Color] = None,
    ) -> None:
        self.job: str = job
        self.tasks: int = tasks
        self.length: int = length
        self.chars: str = chars
        self.color: Optional[Color] = color
        self.bgcolor: Optional[Color] = bgcolor

    def __enter__(self: Self) -> "ProgressBar":
        self._pointer = 0
        self._pace = self.length / self.tasks
        self._fill_char = self.chars[0:1]
        self._place_holder = self.chars[1:2] or " "
        self._left_char = self.chars[2:3]
        self._right_char = self.chars[3:4]
        self.advance()
        return self

    def __exit__(self: Self, exc_type, exc_value, exc_tb) -> None:
        self._pointer = 0
        print()

    def advance(self: Self) -> None:
        """Moves the progress bar to next position."""
        bar = self._fill_char * int(self._pointer * self._pace)
        bar = bar.ljust(self.length, self._place_holder)
        bar = self._left_char + bar + self._right_char
        bar = apply_color(bar, fg=self.color, bg=self.bgcolor)
        percent = int(self._pointer / self.tasks * 100)
        print(f"\r{self.job} {bar} {percent}%", end="")
        self._pointer += 1
