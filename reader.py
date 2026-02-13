#!/usr/bin/env python3

import gzip, json, zipfile

from scipy.sparse import csr_matrix, save_npz
from tqdm import tqdm


def zip_a_npz(zip_path: str, npz_path: str, songs_path: str) -> None:
    """Convierte los archivos contenidos en un zip a una matriz dispersa en npz"""

    songs = dict()
    rows, cols = list(), list()

    with zipfile.ZipFile(zip_path, "r") as zipf:
        for file in tqdm(zipf.namelist()):
            if file.endswith(".json"):
                with zipf.open(file) as f:
                    file_data = json.load(f)

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

    assert len(rows) == len(
        cols
    ), f"El número de filas ({len(rows)}) y columnas ({len(cols)}) debe coincidir."

    values = [1] * len(rows)

    # Construir la matriz compriida por filas
    matrix = csr_matrix((values, (rows, cols)), shape=(max(rows) + 1, len(songs)))

    # Guardar a NPZ
    save_npz(npz_path, matrix, compressed=False)
    print(f"Matriz CSR creada y guardada en '{npz_path}'.")

    # Guardar la relación de columnas a canciones
    with gzip.open(songs_path, "wt", encoding="utf-8") as f:
        json.dump(songs, f)
    print(
        f"Guardada la correspondencia de canciones a columnas de la matriz en '{songs_path}'"
    )


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument(
        "--zip_path",
        nargs="?",
        default="./dataset/spotify_train_dataset.zip",
        help="Ruta al zip de spotify de entrenamiento",
    )
    parser.add_argument(
        "--npz_path",
        nargs="?",
        default="./dataset/sparse_matrix.npz",
        help="Ruta del archivo .npz de salida de la matriz dispersa de playlists-canciones",
    )
    parser.add_argument(
        "--songs_path",
        nargs="?",
        default="./dataset/correspondencia_canciones.json.gz",
        help="Ruta de salida del json comprimido con la correspondencia de canciones a columnas",
    )

    args = parser.parse_args()

    zip_a_npz(args.zip_path, args.npz_path, args.songs_path)
