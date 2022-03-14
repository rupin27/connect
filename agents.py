import random
import math


BOT_NAME = "rupi|n|agrom"


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """
        Determine the minimax utility value of the given state.
        Args: state: a connect383.GameState object representing the current board
        Returns: the exact minimax utility value of the state
        """
        next = state.next_player()
        if (state.is_full() == True):
            return state.utility()

        if (next == 1):
            bestval = -math.inf 
            for move, state_cur in state.successors(): 
                bestval = max(bestval, self.minimax(state_cur))
        else:
            bestval = math.inf
            for move, state_cur in state.successors():
                bestval = min(bestval, self.minimax(state_cur))
        return bestval


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move.
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        if (self.depth_limit is not None):
            return self.minimax_depth(state, self.depth_limit)
        else:
            next = state.next_player()
            if (state.is_full() == True):
                return state.utility()

            if (next == 1):
                bestval = -math.inf 
                for move, state_cur in state.successors(): 
                    bestval = max(bestval, self.minimax(state_cur))
            else:
                bestval = math.inf
                for move, state_cur in state.successors():
                    bestval = min(bestval, self.minimax(state_cur))
            return bestval

    def minimax_depth(self, state, depth):
        """This is just a helper method forr minimax(). Feel free to use it or not. """
        if state.is_full() == True:
            return state.utility()
        if depth == 0:
            return self.evaluation(state)

        next = state.next_player()
        best_util = -math.inf if next == 1 else math.inf
        if (next == 1):
            bestval = -math.inf 
            for move, state_cur in state.successors(): 
                bestval = max(bestval, self.minimax_depth(state_cur, depth - 1))
        else:
            bestval = math.inf
            for move, state_cur in state.successors():
                bestval = min(bestval, self.minimax_depth(state_cur, depth - 1))
        return bestval


    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.
        N.B.: This method must run in constant time for all states!
        Args:
            state: a connect383.GameState object representing the current board
        Returns: a heuristic estimate of the utility value of the state
        """
        p1_score = 0
        p2_score = 0
        for run in state.get_rows() + state.get_cols() + state.get_diags():
            for i, len in self.mstreaks(run):
                if (i == 1) and (len >= 2):
                    p1_score += 1
                elif (i == -1) and (len >= 2):
                    p2_score += 1
            for i, len in self.streaks(run):
                if (i == 1) and (len >= 3):
                    p1_score += len**2
                elif (i == -1) and (len >= 3):
                    p2_score += len**2
            
        return p1_score- p2_score

    def streaks(self,lst):  
        """Get the lengths of all the streaks of the same element in a sequence."""
        samp = []  # list of (element, length) tuples
        prev = lst[0]
        curr_len = 1
        for curr in lst[1:]:
            if curr == prev:
                curr_len += 1
            else:
                samp.append((prev, curr_len))
                prev = curr
                curr_len = 1
        samp.append((prev, curr_len))
        return samp
    
    def mstreaks(self,lst):  
        """Get the lengths of all the streaks of the same element in a sequence."""
        samp = []  
        bool = False
        stack = []
        for curr in lst:
            if(curr == 0):
                bool=True
                if len(stack) >= 2:
                    samp.append((stack[-1:][0],len(stack)))
                stack=[]
            elif(curr == 1 or curr == -1):
                if(len(stack)==0):
                    stack.append(curr)
                elif(stack[-1:][0]==curr):
                    stack.append(curr)
                else:
                    if(bool==True):
                        samp.append((stack[-1:][0],len(stack)))
                    bool=False
                    stack=[]
                    stack.append(curr)
            else:
                if(bool==True and len(stack)!=0):
                    samp.append((stack[-1:][0],len(stack)))
                    bool=False
                    stack=[] 
        
        if (bool==True and len(stack)!=0):
            samp.append((stack[-1:][0],len(stack)))  

        return samp


class MinimaxPruneAgent(MinimaxAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move.
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent should also respect the depth limit like HeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        return self.alphabeta(state, -math.inf, math.inf)

    def alphabeta(self, state,alpha, beta):
        """ This is just a helper method for minimax(). Feel free to use it or not. """
        # return 9 # change this line!
        ply = state.next_player()#gives us what player goes next 
       #if terminal node return util val right away 
        if (state.is_full() == True):
            return state.utility()
        if (ply == 1):
            bestval = -math.inf 
            for move, state_cur in state.successors(): 
                bubble = self.alphabeta(state_cur, alpha, beta) 
                bestval = max(bestval, bubble)
                alpha = max(alpha, bestval)
                if beta <= alpha:
                    break
        else:
            bestval = math.inf
            for move, state_cur in state.successors():
                bubble = self.alphabeta(state_cur, alpha, beta)
                bestval = min(bestval,bubble)
                beta = min(beta, bestval)
                if beta <=alpha:
                    break
        return bestval


class OtherMinimaxHeuristicAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state."""
        #
        # Fill this in, if it pleases you.
        #
        return 26  # Change this line, unless you have something better to do.