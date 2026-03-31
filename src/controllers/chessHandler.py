import sys
import chess
import chess.engine

class ChessHandler:
    def __init__(self, enginePath, varType):
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(enginePath)
        except Exception as e:
            raise Exception(f"Could not start Stockfish: {e}")

        self.board = chess.Board()
        self.lastEval = 0
        self.varType = varType

    def setData(self, timeLimit=0.05):
        try:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=timeLimit))
            score_obj = info["score"].relative

            if score_obj.is_mate():
                rawScore = 1000 if score_obj.mate() > 0 else -1000
            else:
                rawScore = score_obj.score()
                if rawScore is None: rawScore = 0

            self.lastEval = rawScore
            fixedScore = (rawScore + 500) / 1000
            finalVal = max(0.0, min(1.0, fixedScore))

            print(f"{self.varType}:{finalVal}", flush=True)
            
            return finalVal
        except Exception as e:
            return 0.5

    def makeAiMove(self, timeLimit=0.1):
        result = self.engine.play(self.board, chess.engine.Limit(time=timeLimit))
        self.board.push(result.move)

    def closeEngine(self):
        self.engine.quit()