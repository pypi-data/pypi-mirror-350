from dataclasses import dataclass
from typing import Any, Callable, Protocol, TypeAlias

from tic_tac_toe_3x3.game.players import AsyncPlayer, Player
from tic_tac_toe_3x3.game.renderers import AsyncRenderer, Renderer
from tic_tac_toe_3x3.logic.exceptions import InvalidMove
from tic_tac_toe_3x3.logic.models import GameState, Grid, Mark
from tic_tac_toe_3x3.logic.validators import validate_players


class AsyncCallable(Protocol):
    async def __call__(self, param: Exception) -> Any:
        ...


ErrorHandler: TypeAlias = Callable[[Exception], None]
AsyncErrorHandler: TypeAlias = AsyncCallable


@dataclass(frozen=True)
class TicTacToe:
    """Creates a game and implements the main game loop.
    Parameters:
    - player1, player2 - players, whose implementation must correspond to the
    abstract class Player and specify this class for specific conditions
    - renderer - implementation of a class that inherits the abstract class
    Renderer to display the current state of the game under specific conditions.
    """

    player1: Player
    player2: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None

    def __post_init__(self):
        validate_players(self.player1, self.player2)

    def play(self, starting_mark: Mark = Mark("X")) -> None:
        """Implements the main game cycle."""
        game_state = GameState(Grid(), starting_mark)
        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)
            try:
                game_state = player.make_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    self.error_handler(ex)

    def get_current_player(self, game_state: GameState) -> Player:
        """Returns the player whose turn it is to make a move."""
        if game_state.current_mark is self.player1.mark:
            return self.player1
        else:
            return self.player2


@dataclass(frozen=True)
class AsyncTicTacToe(TicTacToe):
    """Creates a game and implements the main game loop for asynchronous players.
    Parameters:
    - player1, player2 - players, whose implementation must correspond to the abstract class AsuncPlayer
    and specify this class for specific conditions
    - renderer - implementation of a class that inherits the abstract class AsyncRenderer to display the current state
    of the game under specific conditions.
    """

    player1: AsyncPlayer
    player2: AsyncPlayer
    renderer: AsyncRenderer
    error_handler: AsyncErrorHandler | None = None

    async def play(self, starting_mark: Mark = Mark("X")) -> None:
        """Implements the main game cycle for asynchronous players."""
        game_state = GameState(Grid(), starting_mark)
        while True:
            await self.renderer.render(game_state)
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)
            try:
                game_state = await player.make_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    await self.error_handler(ex)

    def get_current_player(self, game_state: GameState) -> AsyncPlayer:
        """Returns the player whose turn it is to make a move."""
        if game_state.current_mark is self.player1.mark:
            return self.player1
        else:
            return self.player2
