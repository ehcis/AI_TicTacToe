from GameStatus_5120 import GameStatus

def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    print("in multi:",type(game_state))
    #temp = GameStatus([], 1)
    #terminal = temp.is_terminal()
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, None
    
    #Checking if the player is the maximizing player 
    if maximizingPlayer:
        value = float('-inf')
        pos_moves = game_state.get_moves()
        
        for move in pos_moves:
          
           best_score = minimax(game_state, depth-1, False, alpha, beta)[0]
           if best_score > value:
               value = best_score
               best_move = move
               
           if value >= beta:
                break
           alpha = max(alpha, value)
            
            
    #for minimizing player    
    else:
        value = float('inf')
        pos_moves = game_state.get_moves()
        
        for move in pos_moves:
            
            min_score = minimax(game_state, depth-1, True, alpha, beta)[0]
            if min_score < value:
                value = min_score
                best_move = move
                
            if value <= alpha:
                break
            beta = min(beta, value)
            
            
    return value, best_move
    
    """
   FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
   YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
   1. VALUE
   2. BEST_MOVE
   
   THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
   """
   
   #return value, best_move



def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth==0) or (terminal):
        scores = game_status.get_negamax_scores(terminal)
        return scores, None
    
    value = float('-inf')
    pos_moves = game_status.get_moves()
    best_move = pos_moves[0]
    
    for moves in pos_moves:
        new_game_state = game_status.get_new_state(moves)
        
        best_value = -negamax(new_game_state, depth-1, -turn_multiplier, -alpha, -beta)[0]
        
        if best_value < value:
            value = best_value
            best_move = moves
            
        if alpha < best_value:
            alpha = best_value
            
            if alpha >= beta:
                break
            
    return value, best_move
    
    """
   YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
   PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
   YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
   IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
   RETURN THE FOLLOWING TWO ITEMS
   1. VALUE
   2. BEST_MOVE
   
   THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
   
   """
   #return value, best_move