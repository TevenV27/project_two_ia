import chess
import math
from utils import PIECE_VALUES, POSITION_VALUES
def alphabeta_pruning(boardCopy,movement,depth,alpha,beta,maximizingPlayer):
    if depth == 0:
        return evaluateBoard(boardCopy,movement)
    
    boardCopy.push(chess.Move.from_uci(movement))
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]

    if maximizingPlayer:
        value = -(math.inf)
        for move in legal_moves:
            value = max(value,alphabeta_pruning(boardCopy.copy(),move,depth-1,alpha,beta,False))
            if value >= beta:
                break
            alpha = max(alpha,value)
        return value
    else:
        value = (math.inf)
        for move in legal_moves:
            value = min(value,alphabeta_pruning(boardCopy.copy(),move,depth-1,alpha,beta,True))
            if value <= alpha:
                break
            beta = min(beta,value)
        return value

def evaluateBoard(boardCopy,movement):
    value = 0
    boardCopy.push(chess.Move.from_uci(movement))
    for i in range(8):
        for j in range(8):
            piece = str(boardCopy.piece_at(chess.Square((i*8+j))))
            pieceVal = PIECE_VALUES[piece] if piece != 'None' else 0
            posVal = POSITION_VALUES[piece][i][j] if piece != 'None' else 0
            value += pieceVal + posVal
    return value

def minMaxMax(boardCopy,movement,depth):
    if depth < 0:
        value = evaluateBoard(boardCopy,movement)
        return {"Value":value,"Movement":movement}
    
    boardCopy.push(chess.Move.from_uci(movement))
    max = -(math.inf)
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    result = {}
    for move in legal_moves:
       evaluation = minMaxMin(boardCopy.copy(),move,depth-1)
       if  evaluation["Value"] > max:
            max = evaluation["Value"]
            result = evaluation
    return result

def minMaxMin(boardCopy,movement,depth):
    if depth < 0:
        value = evaluateBoard(boardCopy,movement)
        return {"Value":value,"Movement":movement}
    
    boardCopy.push(chess.Move.from_uci(movement))
    min = math.inf
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    result = {}
    for move in legal_moves:
       evaluation = minMaxMax(boardCopy.copy(),move,depth-1)
       if  evaluation["Value"] < min:
            min = evaluation["Value"]
            result = evaluation
    return result