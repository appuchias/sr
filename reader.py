#!/usr/bin/env python3

import json, sys, zipfile

import numpy as np
from compression import zstd
from scipy.sparse import csr_matrix, load_npz, save_npz
from tqdm import tqdm


def zip_a_npz(zip_path: str, npz_path: str, songs_path: str) -> None:
    """Convierte los archivos contenidos en un zip a una matriz dispersa en npz"""

    songs = dict()
    rows, cols, values = list(), list(), list()

    with zipfile.ZipFile(zip_path, "r") as zipf:
        for file in tqdm(zipf.namelist()):
            if file.endswith(".json"):
                with zipf.open(file) as f:
                    file_data = json.loads(f.read())

                    for playlist in file_data["playlists"]:
                        playlist_id = playlist["pid"]

                        for song in playlist["tracks"]:
                            song_id = song["track_uri"]

                            # Si ya hemos visto la canción usamos la columna asignada
                            # Si no, la añadimos al diccionario con el índice de la
                            # columna correspondiente.
                            if (song_col := songs.get(song_id)) is None:
                                song_col = len(songs.keys())
                                songs[song_id] = song_col

                            # Guardamos un 1 en la fila-columna que corresponde.
                            rows.append(playlist_id)
                            cols.append(song_col)
                            values.append(1)

    # Construir la matriz compriida por filas
    matrix = csr_matrix((values, (rows, cols)), shape=(len(rows), len(songs)))

    # Guardar a NPZ
    save_npz(npz_path, matrix, compressed=False)
    print(f"Matriz CSR creada y guardada en '{npz_path}'.")

    # Guardar la relación de columnas a canciones
    with zstd.open(songs_path, "w") as f:
        f.write(json.dumps(songs).encode("utf8"))
    print(
        f"Guardada la correspondencia de canciones a columnas de la matriz en '{songs_path}'"
    )


if __name__ == "__main__":

    zip_path = sys.argv[1]
    try:
        npz_path = sys.argv[2]
    except IndexError:
        npz_path = "./dataset/sparse_matrix.npz"

    if not zip_path:
        print(f"Uso: {sys.argv[0]} <archivo.zip> [archivo_salida.npz]")
        exit(1)

    songs_path = "./dataset/correspondencia_canciones.json"

    zip_a_npz(zip_path, npz_path, songs_path)
