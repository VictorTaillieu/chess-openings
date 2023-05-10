import re
import time
from pathlib import Path

import chess
import pandas as pd
import requests
from tqdm import tqdm


def results_to_prop(white, draws, black):
    total = white + draws + black
    white_prop = round(white / total * 100)
    draws_prop = round(draws / total * 100)
    black_prop = round(black / total * 100)

    return white_prop, draws_prop, black_prop, total


def pgn_to_uci(pgn):
    san_moves = re.sub(r"\d+\.\s", "", pgn)

    board = chess.Board()

    uci_moves = []
    for san_move in san_moves.split(" "):
        uci_move = board.push_san(san_move).uci()
        uci_moves.append(uci_move)

    return ",".join(uci_moves)


root = "https://explorer.lichess.ovh/"
query = "?play="

df = pd.read_csv("data/openings.csv")

res_file = "data/openings_stats.csv"

if not Path(res_file).is_file():
    with open(res_file, "w") as out_file:
        out_file.write("name,color,variation,pgn,white_masters,draws_masters,black_masters,total_masters,white_lichess,draws_lichess,black_lichess,total_lichess\n")
else:
    with open(res_file, "r") as out_file:
        next_idx = len(out_file.readlines()) - 1
    df = df[next_idx:]

for idx in tqdm(range(len(df))):
    line = df.iloc[idx]
    pgn = pgn_to_uci(line["pgn"])

    res_masters = requests.get(root + "masters" + query + pgn).json()
    res_lichess = requests.get(root + "lichess" + query + pgn).json()

    time.sleep(1)

    white_m, draws_m, black_m, total_m = results_to_prop(res_masters["white"], res_masters["draws"], res_masters["black"])
    white_l, draws_l, black_l, total_l = results_to_prop(res_lichess["white"], res_lichess["draws"], res_lichess["black"])

    with open(res_file, "a") as out_file:
        out_file.write(f"{line['name']},{line['color']},{line['variation']},{line['pgn']},{white_m},{draws_m},{black_m},{total_m},{white_l},{draws_l},{black_l},{total_l}\n")
