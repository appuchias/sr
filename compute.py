#!/usr/bin/env python3

import gzip, json
from typing import Dict, List, Tuple

import numpy as np
from scipy.sparse import load_npz


def compute_popularity(matrix, songs: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Obtener la popularidad de las canciones como recuento del número de playlists en las que aparecen

    Args:
        matrix: Matriz dispersa con playlists en filas y canciones en columnas
        songs: Correspondencia de los track_uris de las canciones a las columnas

    Returns:
        Lista de tuplas (track_uri, recuento) ordenado por popularidad descendente
    """

    # Suma las columas para agregar el número de playlsits que contienen la canción
    popularity_counts = np.array(matrix.sum(axis=0)).flatten()

    # Crear correspondencia de columna a uri de la canción
    inverse_songs = {col_idx: uri for uri, col_idx in songs.items()}

    # Crea lista de tuplas (track_uri, popularidad)
    popularity_list = []
    for col_idx in range(len(popularity_counts)):
        if col_idx in inverse_songs:
            song_uri = inverse_songs[col_idx]
            count = int(popularity_counts[col_idx])
            popularity_list.append((song_uri, count))

    # Ordenar por popularidad descendente
    popularity_list.sort(key=lambda x: x[1], reverse=True)

    return popularity_list


def save_popularity_ranking(
    popularity_list: List[Tuple[str, int]], popularity_path: str
):
    """
    Guardar el ranking de popularidad a un archivo JSON.

    Args:
        popularity_list: Lista de tuplas (track_uri, recuento)
        popularity_path: Ruta al archivo de salida de popularidad
    """
    # Convert to dictionary for easier lookup
    popularity_dict = {uri: count for uri, count in popularity_list}

    with gzip.open(popularity_path, "wt", encoding="utf-8") as f:
        json.dump(popularity_dict, f)
    print(f"Ranking de popularidad guardado en '{popularity_path}'")

    # print(f"Total unique tracks: {len(popularity_list)}")
    # print(f"Most popular track: {popularity_list[0][0]} with {popularity_list[0][1]} appearances")
    # print(f"Least popular track: {popularity_list[-1][0]} with {popularity_list[-1][1]} appearances")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

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
    parser.add_argument(
        "--popularity_path",
        nargs="?",
        default="./results/popularity_ranking.json.gz",
        help="Ruta de salida del json comprimido con la popularidad de las canciones",
    )

    args = parser.parse_args()

    # Cargar la correspondencia de canciones a columnas
    with gzip.open(args.songs_path, "rt", encoding="utf-8") as f:
        songs = json.load(f)

    # Cargar la matriz dispersa de playlist-canciones
    matrix = load_npz(args.npz_path)

    assert matrix.shape[1] == len(songs)

    print(f"Número de playlists: {matrix.shape[0]}")
    print(f"Número de canciones: {matrix.shape[1]}")

    # Compute popularity
    popularity_list = compute_popularity(matrix, songs)

    # Save the ranking
    save_popularity_ranking(popularity_list, args.popularity_path)

    # Show some statistics
    print("\nTop 10 canciones más populares:")
    for i, (uri, count) in enumerate(popularity_list[:10], 1):
        print(f"{i}. {uri}: {count} playlists")
