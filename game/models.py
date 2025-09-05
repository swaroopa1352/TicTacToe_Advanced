# game/models.py
import uuid
import random
from django.db import models

class Game(models.Model):
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    STATUS_CHOICES = [(IN_PROGRESS, "In progress"), (FINISHED, "Finished")]

    DIFF_EASY = "EASY"
    DIFF_MED = "MEDIUM"
    DIFF_HARD = "HARD"
    DIFF_CHOICES = [(DIFF_EASY, "Easy"), (DIFF_MED, "Medium"), (DIFF_HARD, "Hard")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.CharField(max_length=9, default="---------")   # '-', 'X', 'O'
    current_player = models.CharField(max_length=1, default="X")  # 'X' | 'O'
    winner = models.CharField(max_length=1, null=True, blank=True)  # 'X' | 'O' | None
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=IN_PROGRESS)

    # AI configuration
    ai_enabled = models.BooleanField(default=False)
    ai_player = models.CharField(max_length=1, default="O")  # AI mark
    ai_difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES, default=DIFF_HARD)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---------- Public helpers ----------
    def as_dict(self):
        return {
            "id": str(self.id),
            "board": list(self.board),
            "player": self.current_player,
            "winner": self.winner,
            "status": self.status,
            "ai_enabled": self.ai_enabled,
            "ai_player": self.ai_player,
            "ai_difficulty": self.ai_difficulty,
        }

    def restart(self):
        self.board = "---------"
        self.current_player = "X"
        self.winner = None
        self.status = self.IN_PROGRESS
        self.save(update_fields=["board","current_player","winner","status","updated_at"])

    def make_move(self, pos: int):
        """Apply a move for the current player (human or AI)."""
        if self.status == self.FINISHED or not (0 <= pos <= 8) or self.board[pos] != "-":
            return
        b = list(self.board)
        b[pos] = self.current_player
        self.board = "".join(b)

        w = self._winner_of(self.board)
        if w:
            self.winner = None if w == "T" else w
            self.status = self.FINISHED
            self.save(update_fields=["board","winner","status","updated_at"])
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.save(update_fields=["board","current_player","updated_at"])

    def ai_move(self):
        """If it's AI's turn, choose and apply a move according to difficulty."""
        if not self.ai_enabled or self.status == self.FINISHED:
            return
        if self.current_player != self.ai_player:
            return

        move = self._choose_ai_move(self.board, self.ai_player, self.ai_difficulty)
        if move is not None:
            self.make_move(move)

    # ---------- AI internals ----------
    @staticmethod
    def _winner_of(board_str: str):
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in lines:
            if board_str[a] != "-" and board_str[a] == board_str[b] == board_str[c]:
                return board_str[a]
        return "T" if "-" not in board_str else None

    @staticmethod
    def _available_moves(board_str: str):
        return [i for i, v in enumerate(board_str) if v == "-"]

    def _choose_ai_move(self, board_str: str, ai: str, difficulty: str):
        if difficulty == self.DIFF_EASY:
            # random legal move
            moves = self._available_moves(board_str)
            return random.choice(moves) if moves else None

        if difficulty == self.DIFF_MED:
            # 1) win if possible  2) block if needed  3) center  4) corner  5) side
            human = "O" if ai == "X" else "X"
            # try win
            for i in self._available_moves(board_str):
                test = board_str[:i] + ai + board_str[i+1:]
                if self._winner_of(test) == ai:
                    return i
            # try block
            for i in self._available_moves(board_str):
                test = board_str[:i] + human + board_str[i+1:]
                if self._winner_of(test) == human:
                    return i
            # center
            if board_str[4] == "-":
                return 4
            # corners
            for i in [0,2,6,8]:
                if board_str[i] == "-":
                    return i
            # sides
            for i in [1,3,5,7]:
                if board_str[i] == "-":
                    return i
            return None

        # HARD → minimax
        return self._best_move_minimax(board_str, ai)

    def _best_move_minimax(self, board_str: str, ai: str):
        human = "O" if ai == "X" else "X"

        def minimax(b: str, player: str, depth: int):
            w = self._winner_of(b)
            if w == ai:
                return 10 - depth, None
            if w == human:
                return depth - 10, None
            if w == "T":
                return 0, None

            best_score = float("-inf") if player == ai else float("inf")
            best_mv = None
            for i in self._available_moves(b):
                nb = b[:i] + player + b[i+1:]
                score, _ = minimax(nb, "O" if player == "X" else "X", depth + 1)
                if player == ai:
                    if score > best_score:
                        best_score, best_mv = score, i
                else:
                    if score < best_score:
                        best_score, best_mv = score, i
            return best_score, best_mv

        _, mv = minimax(board_str, ai, 0)
        return mv


