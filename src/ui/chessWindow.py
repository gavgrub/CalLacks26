# This is all AI slop but I want to be done this project
import os
import warnings

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

import pygame
import sys
import chess

# --- PATH SETUP ---
currentDir = os.path.dirname(os.path.abspath(__file__))
projectRoot = os.path.abspath(os.path.join(currentDir, "../../"))
sys.path.append(projectRoot)

from src.controllers.chessHandler import ChessHandler

# --- CONFIGURATION ---
WIDTH = 480
HEIGHT_OFFSET = 480 # Board height
UI_HEIGHT = 40
SQUARE_SIZE = WIDTH // 8

# Colors
LIGHT_RED = (140, 0, 0)
DARK_RED = (60, 0, 0)
HIGHLIGHT = (200, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PIECE_SYMBOLS = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

def getSquareFromMouse(pos):
    column = pos[0] // SQUARE_SIZE
    row = 7 - (pos[1] // SQUARE_SIZE)
    return chess.square(column, row)

def drawBoard(screen, selectedSquare, board):
    for row in range(8):
        for col in range(8):
            color = LIGHT_RED if (row + col) % 2 == 0 else DARK_RED
            currentSquare = chess.square(col, 7 - row)
            if currentSquare == selectedSquare:
                color = HIGHLIGHT
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    # Using a generic font if Segoe UI Symbol isn't available
    try:
        font = pygame.font.SysFont("Segoe UI Symbol", 50)
    except:
        font = pygame.font.SysFont("Arial", 50)
        
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = PIECE_SYMBOLS[piece.symbol()]
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            img = font.render(symbol, True, WHITE)
            rect = img.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2))
            screen.blit(img, rect)

def drawUI(screen, evaluation, volume, board):
    """Draws points or CHECKMATE and volume percentage."""
    overlay = pygame.Surface((WIDTH, UI_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, HEIGHT_OFFSET))

    font = pygame.font.SysFont("Arial", 22, bold=True)
    
    if board.is_checkmate():
        evalText = "CHECKMATE"
    else:
        # Convert raw centipawn score to displayable points
        evalText = f"Points: {evaluation/100:+.1f}"

    # Handle cases where volume might be None
    displayVol = volume if volume is not None else 0.5
    if not (sys.argv[1] == "PLAY"):
        volText = f"{sys.argv[1].lower().capitalize()}: {int(displayVol * 100)}%"
    else:
        volText = f"{sys.argv[1].lower().capitalize()}: {int(displayVol * 100) > 30}"

    evalImg = font.render(evalText, True, WHITE)
    volImg = font.render(volText, True, WHITE)

    screen.blit(evalImg, (20, HEIGHT_OFFSET + 8))
    screen.blit(volImg, (WIDTH - 150, HEIGHT_OFFSET + 8))

def runChessGame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH + UI_HEIGHT))
    pygame.display.set_caption("Play well to affect UI")
    
    # Get argument from main.py (VOLUME or TIME)
    var_type = sys.argv[1] if len(sys.argv) > 1 else "VOLUME"
    
    # Ensure this path matches your project structure
    chessGame = ChessHandler("src/engine/stockfish.exe", var_type)
    clock = pygame.time.Clock()
    
    selectedSquare = None
    
    # Initial calculation
    currentData = chessGame.setData()
    currentEval = chessGame.lastEval

    while True:
        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chessGame.closeEngine()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < HEIGHT_OFFSET: 
                    clickedSquare = getSquareFromMouse(event.pos)
                    
                    if selectedSquare is None:
                        piece = chessGame.board.piece_at(clickedSquare)
                        if piece and piece.color == chess.WHITE:
                            selectedSquare = clickedSquare
                    else:
                        # Attempt to move
                        move = chess.Move(selectedSquare, clickedSquare)
                        
                        # Auto-promotion to Queen
                        piece = chessGame.board.piece_at(selectedSquare)
                        if piece and piece.piece_type == chess.PAWN:
                            if chess.square_rank(clickedSquare) in [0, 7]:
                                move.promotion = chess.QUEEN

                        if move in chessGame.board.legal_moves:
                            # 1. Player Move
                            chessGame.board.push(move)
                            selectedSquare = None

                            # Visual update before AI thinks
                            screen.fill((20, 0, 0))
                            drawBoard(screen, None, chessGame.board)
                            drawPieces(screen, chessGame.board)
                            drawUI(screen, currentEval, currentData, chessGame.board)
                            pygame.display.flip()
                            
                            if not chessGame.board.is_game_over():
                                # 2. AI Move
                                chessGame.makeAiMove()
                                
                                # 3. Update scores and send to main.py
                                currentData = chessGame.setData() 
                                currentEval = chessGame.lastEval
                        else:
                            # Selection logic
                            piece = chessGame.board.piece_at(clickedSquare)
                            if piece and piece.color == chess.WHITE:
                                selectedSquare = clickedSquare
                            else:
                                selectedSquare = None

        # --- DRAWING ---
        screen.fill((20, 0, 0)) 
        drawBoard(screen, selectedSquare, chessGame.board)
        drawPieces(screen, chessGame.board)
        drawUI(screen, currentEval, currentData, chessGame.board)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    runChessGame()