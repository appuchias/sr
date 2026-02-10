#!/usr/bin/env python3

import json, sys, zipfile

import numpy as np
from scipy.sparse import csr_matrix, load_npz, save_npz
from tqdm import tqdm


def popularity(songs: dict, matrix: ...) -> ...:
    # inverse_songs = dict(zip(songs.values(), songs.keys()))
    inverse_songs = list(songs.keys())

    # print(json.dumps(inverse_songs, indent=4))

    kendrik = songs["spotify:track:7KXjTSCq5nL1LoYtL7XAwS"]
    print(kendrik)

    print(np.sum(matrix[:, kendrik]))


if __name__ == "__main__":

    with open("correspondencia_canciones.json") as f:
        songs = json.load(f)
    matrix = load_npz("sparse_matrix.npz")

    # popularity({"cancion1": 0, "cancion2": 1}, matrix)
    popularity(songs, matrix)

    # zip_path = sys.argv[1]
    # npz_path = sys.argv[2]
    #
    # if not zip_path:
    #     print(f"Uso: {sys.argv[0]} <archivo.zip> [archivo_salida.npz]")
    #     exit(1)
    #
    # if not npz_path:
    #     npz_path = "sparse_matrix.npz"
    #
    # zip_a_npz(zip_path, npz_path)
