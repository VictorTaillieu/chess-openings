import base64
import re

import chess
import chess.svg
from cairosvg import svg2png


def pgn_to_uci(pgn):
    san_moves = re.sub(r"\d+\.\s", "", pgn)

    board = chess.Board()

    uci_moves = []
    for san_move in san_moves.split(" "):
        uci_move = board.push_san(san_move).uci()
        uci_moves.append(uci_move)

    return ",".join(uci_moves)
