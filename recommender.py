#!/usr/bin/env python3

import gzip, json, zipfile
from typing import Dict, List, Set


def get_playlist_seeds(test_zip_path: str) -> Dict[int, Set[str]]:
    """
    Obtener las semillas de las playlists de test_input_playlists.json dentro del zip
    """
    playlist_seeds = dict()

    with zipfile.ZipFile(test_zip_path, "r") as zipf:
        with zipf.open("test_input_playlists.json") as f:
            file_data = json.load(f)

            for playlist in file_data["playlists"]:
                # Tolerar playlists vacías
                seed_tracks = {
                    track["track_uri"] for track in playlist.get("tracks", list())
                }

                playlist_seeds[playlist["pid"]] = seed_tracks

    return playlist_seeds


def generate_popularity_recommendations(
    seed_tracks: Set[str],
    popular_tracks: List[str],
    num_recommendations: int = 500,
) -> List[str]:
    """
    Generar recomendaciones para una playlist por popularidad.

    Args:
        seed_tracks: track_uris de las canciones ya en la playlist
        popular_tracks: Lista de canciones ordenadas por popularidad
        num_recommendations: Número de canciones a recomendar

    Returns:
        Lista de track_uris de las recomendaciones
    """

    recommendations = list()

    for track_uri in popular_tracks:
        if track_uri not in seed_tracks:
            recommendations.append(track_uri)

            # Parar el bucle cuando se consigan todas las canciones que recomendar
            if len(recommendations) >= num_recommendations:
                break
    else:
        raise Exception("No se pudo llegar a las recomendaciones requeridas")

    return recommendations


def format_submission(
    recommendations_dict: Dict[int, List[str]],
    recommendations_path: str,
    team_name: str,
    contact_email: str,
):
    """
    Exportar las recomendaciones con el formato de la submission.

    Sigue la especificacion oficial de Spotify Million Playlist Challenge
    - Línea 1: team_info, team_name, contact_email
    - Líneas consecutivas: pid, track_uri_1, track_uri_2, ..., track_uri_n
    - Exactamente 500 canciones por playlist (sin duplicados ni seeds)
    - Salida como CSV comprimido con GZIP

    Args:
        recommendations_dict: Diccionario con las recomendaciones para las playlists
        output_path: Ruta de salida del archivo de recomendaciones (.csv.gz)
        team_name: Nombre del equipo o método
        contact_email: Correo de contacto
    """

    # # Asegurar que la salida termina en .csv.gz
    # if not recommendations_path.endswith(".csv.gz"):
    #     if recommendations_path.endswith(".csv"):
    #         recommendations_path = recommendations_path + ".gz"
    #     else:
    #         recommendations_path = recommendations_path + ".csv.gz"

    # # Validar recomendaciones
    # invalid_count = 0
    # for pid, tracks in recommendations_dict.items():
    #     if len(tracks) != 500:
    #         print(f"Warning: Playlist {pid} has {len(tracks)} tracks instead of 500")
    #         invalid_count += 1
    #
    #     # Check for duplicates
    #     if len(tracks) != len(set(tracks)):
    #         print(f"Warning: Playlist {pid} contains duplicate tracks")
    #         invalid_count += 1
    #
    # if invalid_count > 0:
    #     print(f"Found {invalid_count} playlists with validation issues")

    total_playlists = len(recommendations_dict)

    # Escribir el CSV comprimido
    with gzip.open(recommendations_path, "wt", encoding="utf-8") as f:
        # Cabecera con info
        f.write(f"team_info,{team_name},{contact_email}\n")

        # Recomendacionea para las playlists de test (ordenadas por pid)
        for pid in sorted(recommendations_dict.keys()):
            tracks = recommendations_dict[pid]

            # Formato: pid,track_uri_1,track_uri_2,...,track_uri_500
            line = f"{pid}," + ",".join(tracks)
            f.write(line + "\n")

    print(f"Archivo de salida guardado en '{recommendations_path}'")
    print(f"Total de playlists con recomendaciones: {total_playlists}")


def _get_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument(
        "--test_zip_path",
        default="./dataset/spotify_test_playlists.zip",
        help="Ruta al zip de spotify de test",
    )
    parser.add_argument(
        "--popularity_path",
        default="./results/popularity_ranking.json.gz",
        help="Ruta de salida del json comprimido con la popularidad de las canciones",
    )
    parser.add_argument(
        "--recommendations_path",
        default="./results/submission.csv.gz",
        help="Ruta del archivo .csv.gz con las recomendaciones obtenidas",
    )
    parser.add_argument(
        "--num_recommendations",
        type=int,
        default=500,
        help="Número de recomendaciones por playlist",
    )
    parser.add_argument(
        "--team_name",
        default="EXP",
        help="Número de recomendaciones por playlist",
    )
    parser.add_argument(
        "--contact_email",
        default="enrique.pardo.garcia@udc.es,xoel.maestu@udc.es,p.fernandezf@udc.es",
        help="Número de recomendaciones por playlist",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()

    print("Cargando ránkings de popularidad...")
    with gzip.open(args.popularity_path) as f:
        popularity_dict = json.loads(f.read().decode("utf8"))
    print(f"Cargadas {len(popularity_dict)} canciones")
    print()

    print("Obteniendo los items semilla de las playlsits...")
    playlist_seeds = get_playlist_seeds(args.test_zip_path)
    print(f"Cargadas {len(playlist_seeds)} playlists")
    print()

    print("Obteniendo recomendaciones...")
    recommendations_dict = dict()
    for playlist_id, seed_tracks in playlist_seeds.items():
        recommendations_dict[playlist_id] = generate_popularity_recommendations(
            seed_tracks,
            popularity_dict,
            num_recommendations=args.num_recommendations,
        )
    print(f"Obtenidas recomendaciones para {len(recommendations_dict)} playlists")
    print()

    print("Guardando las recomendaciones con el formato de salida...")
    format_submission(
        recommendations_dict,
        args.recommendations_path,
        args.team_name,
        args.contact_email,
    )
