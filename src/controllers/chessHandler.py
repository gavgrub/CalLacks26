import chess
import chess.engine

class ChessHandler:
    def __init__(self, enginePath):
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(enginePath)
        except Exception as e:
            raise Exception(f"Could not start Stockfish: {e}")

        self.board = chess.Board()
        self.lastEval = 0

    def getVolumeMultiplier(self, timeLimit=0.05):
        try:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=timeLimit))
            score = info["score"].relative
            
            if score.is_mate():
                rawScore = 1000 if score.mate() > 0 else -1000
            else:
                rawScore = score.score()

            self.lastEval = rawScore
            volume = (rawScore + 500) / 1000
            return max(0.0, min(1.0, volume))
            
        except chess.engine.EngineTerminatedError:
            return 0.5

    def makeAiMove(self, timeLimit=0.1):
        result = self.engine.play(self.board, chess.engine.Limit(time=timeLimit))
        self.board.push(result.move)

    def closeEngine(self):
        self.engine.quit()