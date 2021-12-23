# 2048 Clone for Max

This is a library that implements 2048. It's playable from the console, but the real point is to use as a library for an game playing agent. 

## Usage

1. Create a board
```
b = Board()
```
2.  Each move is just a call to the four move functions. 
```
left(b)
right(b)
up(b)
down(b)
```
3. After each move check check the game state. The values are `WON`, `LOST`, and `PLAYING`.
```
game = game_state(board)
if game == 'WON':
    game_over = True
    print('You won :-)')
elif game == 'LOST':
    game_over = True
    print('You lost :-(')
else:
    board.assign_tile_to_board()
```

## Improvements
Should the game continue beyond the 2048 tile?

