from typing import Literal

PlayerID = Literal['X', 'O', 1, 0]

def player_int(player: PlayerID) -> Literal[0, 1]:
    if player in (1, 'X'):
        return 1
    elif player in (0, 'O'):
        return 0
    else:
        raise ValueError(f'{player = } is not valid')

def change_player(player: PlayerID) -> Literal[0, 1]:
    """returns the other player"""
    if player in (1, 'X'):
        return 0
    elif player in (0, 'O'):
        return 1
    else:
        raise ValueError(f'{player = }is not valid')