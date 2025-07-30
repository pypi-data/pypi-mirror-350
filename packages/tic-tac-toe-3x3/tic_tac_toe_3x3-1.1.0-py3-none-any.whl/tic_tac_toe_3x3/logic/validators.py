from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tic_tac_toe_3x3.game.players import Player
    from tic_tac_toe_3x3.logic.models import Grid, GameState, Mark

import re

from tic_tac_toe_3x3.logic.exceptions import InvalidGameState


def validate_grid(grid: Grid) -> None:
    """Validates the grid state.

    valid grid elements: space, X, O. Total number of elements - 9.
    If any of these requirements are violated - a ValueError exception is generated.
    """
    if not re.match(r"^[\sX0]{9}$", grid.cells):
        raise ValueError("Must contain 9 cells of: X, 0(null), or space")


def validate_game_state(game_state: GameState) -> None:
    """Validates the game state: consolidates game state validation with other validators"""
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.starting_mark)
    validate_winner(game_state.grid, game_state.starting_mark, game_state.winner)


def validate_number_of_marks(grid: Grid) -> None:
    """Validates the game state based on an analysis of the numbers of players' marks on the grid:
    for a real game, the number of players' marks cannot differ by more than one or be the same.
    """
    if abs(grid.x_count - grid.o_count) > 1:
        raise InvalidGameState("Wrong number of Xs and Os")


def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
    """Validates the game state by checking the player who started:
    for a correct state, the marks on the field that predominate in number can only be the marks
    of the player who made the first move.
    """
    if grid.x_count > grid.o_count:
        if starting_mark != "X":
            raise InvalidGameState("Wrong starting mark")
    elif grid.o_count > grid.x_count:
        if starting_mark != "0":
            raise InvalidGameState("Wrong starting mark")


def validate_winner(grid: Grid, starting_mark: Mark, winner: Mark | None) -> None:
    """Validates the game state based on winner analysis:
    if the player who started the game won, then his marks must be more than
    the opposing marks,
    if the other player won, then there must be the same number of
    marks on the field.
    """
    if winner == "X":
        if starting_mark == "X":
            if grid.x_count <= grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
        else:
            if grid.x_count != grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
    elif winner == "0":
        if starting_mark == "0":
            if grid.o_count <= grid.x_count:
                raise InvalidGameState("Wrong number of 0s")
        else:
            if grid.o_count != grid.x_count:
                raise InvalidGameState("Wrong number of 0s")


def validate_players(player1: Player, player2: Player) -> None:
    """Validates the players' marks: the players must use different marks"""
    if player1.mark is player2.mark:
        raise ValueError("Players must use different marks")
