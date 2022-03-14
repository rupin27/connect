# connect
Programmed gameplay agents in Python for 2-player adversarial search in an unbounded version of Connect 4.
Deployed recursive variants of complete minimax, heuristic-based finite-lookahead, and alpha-beta pruning algorithms for optimal gameplay.

# GamePlay:
1) Notlimited to 6x7 boards. Games may start with one or more “obstacle” pieces already on the board which do not belong to either player. 
2) Play will always continue until the board is completely full (even after a player has achieved 4-in-a-row), at which point scores for each player will be calculated.
Points are awarded as follows: 
3) For each run of length three or greater, the player will receive points equal to the square of the length of that run. For example, 3-in-a-row is worth 9 points, 4-in-a-row 16, 5-in-a-row 25, etc.
4) When calculating the value of different moves, your game-playing agent will use the scores as utility values for the terminal games states, and seek to maximize
the delta between its score and that of its opponent using Minimax.

# Running the Game:
<p>
To play a game, you run connect.py from a command line (or within an IDE) and supply it with arguments that determine the parameters of the game and which type of agents are playing. The required arguments are, in order:
player1 – one of {‘r’, ‘h’, ‘c’, ‘o’} specifying the agent type (see code for details) player2 – one of {‘r’, ‘h’, ‘c’, ‘o’}
</p>
<p>
  <i>rows</i> – the number of rows in the board <br>
  <i>columns</i> – the number of columns in the board
</p>
<br>

For example, to play against a random computer agent on a 4x5 board, you would type:
> python connect.py r h 4 5

To run your heuristic code using the evaluation function, you must supply a depth limit using the the --depth flag:
> python connect.py r c 6 7 --depth 3

Additionally, the --board flag is the only way to specify obstacle spots in the board. The value of that argument must match one of the keys of the boards dictionary defined in test_boards.py. For example, to start the game with a state labeled “samp”:
> python connect.py c h 4 5 --board samp

