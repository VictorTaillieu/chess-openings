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


def pgn_to_board(pgn):
    san_moves = re.sub(r"\d+\.\s", "", pgn)

    board = chess.Board()

    if san_moves:
        for san_move in san_moves.split(" "):
            board.push_san(san_move)

    svg = chess.svg.board(board)
    png = svg2png(svg)

    return f"data:image/png;base64,{base64.b64encode(png).decode()}"
