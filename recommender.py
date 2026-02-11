#!/usr/bin/env python3
"""
Popularity-based recommender system for Spotify Million Playlist Challenge.
Iteration 0: Baseline using most popular tracks.
"""

import json
import sys
import zipfile
from typing import List, Dict, Set
import gzip

def load_popularity_ranking(popularity_path: str = "./results/popularity_ranking.json") -> List[str]:
    """
    Load pre-sorted popularity ranking from JSON file.
    """
    with open(popularity_path, "r") as f:
        popularity_dict = json.load(f)
    
    # Already descent ordered by popularity, only extract URIs
    return list(popularity_dict.keys())


def get_playlist_seeds(test_zip_path: str) -> Dict[int, Set[str]]:
    """
    Extract playlist seeds from test_input_playlists.json in test dataset.
    """
    playlist_seeds = {}
    
    with zipfile.ZipFile(test_zip_path, "r") as zipf:
        # Leer SOLO test_input_playlists.json (seeds vacíos)
        with zipf.open("test_input_playlists.json") as f:
            file_data = json.loads(f.read())
            
            for playlist in file_data["playlists"]:
                playlist_id = playlist["pid"]
                # Puede estar vacío → seeds vacíos es correcto para challenge
                seed_tracks = {track["track_uri"] for track in playlist.get("tracks", [])}
                playlist_seeds[playlist_id] = seed_tracks
    
    return playlist_seeds


def generate_recommendations(
    # playlist_id: int,
    seed_tracks: Set[str],
    popular_tracks: List[str],
    num_recommendations: int = 500
) -> List[str]:
    """
    Generate recommendations for a playlist based on popularity.
    
    Args:
        playlist_id: ID of the playlist
        seed_tracks: Set of track URIs already in the playlist
        popular_tracks: List of all tracks sorted by popularity
        num_recommendations: Number of tracks to recommend
    
    Returns:
        List of recommended track URIs
    """
    recommendations = []
    
    for track_uri in popular_tracks:
        # Skip tracks already in the playlist
        if track_uri not in seed_tracks:
            recommendations.append(track_uri)
            
            # Stop when we have enough recommendations
            if len(recommendations) >= num_recommendations:
                break
    
    return recommendations


def format_submission(
    recommendations_dict: Dict[int, List[str]],
    output_path: str = "./results/submission.csv.gz",
    team_name: str = "EXP",
    contact_email: str = "enrique.pardo.garcia@udc.es,xoel.maestu@udc.es,p.fernandezf@udc.es"
):
    """
    Format recommendations according to the challenge specification.
    
    The format follows the official Spotify Million Playlist Challenge specification:
    - First line: team_info, team_name, contact_email
    - Following lines: pid, track_uri_1, track_uri_2, ..., track_uri_500
    - Exactly 500 tracks per playlist (no duplicates, no seed tracks)
    - Output as gzipped CSV (.csv.gz)
    
    Args:
        recommendations_dict: Dictionary mapping playlist_id to list of recommended tracks
        output_path: Path to save the submission file (will be saved as .csv.gz)
        team_name: Name of the team/approach
        contact_email: Contact email address
    """    
    # Ensure output path ends with .csv.gz
    if not output_path.endswith('.csv.gz'):
        if output_path.endswith('.csv'):
            output_path = output_path + '.gz'
        else:
            output_path = output_path + '.csv.gz'
    
    # Validate recommendations
    total_playlists = len(recommendations_dict)
    invalid_count = 0
    
    for pid, tracks in recommendations_dict.items():
        # Check for exactly 500 tracks
        if len(tracks) != 500:
            print(f"Warning: Playlist {pid} has {len(tracks)} tracks instead of 500")
            invalid_count += 1
        
        # Check for duplicates
        if len(tracks) != len(set(tracks)):
            print(f"Warning: Playlist {pid} contains duplicate tracks")
            invalid_count += 1
    
    if invalid_count > 0:
        print(f"Found {invalid_count} playlists with validation issues")
    
    # Write compressed CSV file
    with gzip.open(output_path, 'wt', encoding='utf-8') as f:
        # Write header with team info (no extra spaces as per spec)
        f.write(f"team_info,{team_name},{contact_email}\n")
        
        # Write recommendations for each playlist (sorted by playlist ID)
        for pid in sorted(recommendations_dict.keys()):
            tracks = recommendations_dict[pid]
            
            # Format: pid,track_uri_1,track_uri_2,...,track_uri_500
            # Note: No spaces after commas as per spec
            line = f"{pid}," + ",".join(tracks)
            f.write(line + "\n")
    
    print(f"Submission file saved to '{output_path}'")
    print(f"Total playlists: {total_playlists}")
    print(f"Format: gzipped CSV (.csv.gz)")


def recommender(test_zip_path: str, output_path: str = "./results/submission.csv.gz"):
    """
    Main recommender function.
    
    Args:
        test_zip_path: Path to the test playlists ZIP file
        output_path: Path to save the submission file (.csv.gz)
    """
    print("Loading popularity ranking...")
    popular_tracks = load_popularity_ranking()
    print(f"Loaded {len(popular_tracks)} tracks")
    
    print("\nExtracting playlist seeds from test dataset...")
    playlist_seeds = get_playlist_seeds(test_zip_path)
    print(f"Found {len(playlist_seeds)} test playlists")
    
    print("\nGenerating recommendations...")
    recommendations_dict = {}
    
    for playlist_id, seed_tracks in playlist_seeds.items():
        recommendations = generate_recommendations(
            # playlist_id,
            seed_tracks,
            popular_tracks,
            num_recommendations=500
        )
        recommendations_dict[playlist_id] = recommendations
    
    print(f"Generated recommendations for {len(recommendations_dict)} playlists")
    
    print("\nFormatting submission file...")
    format_submission(recommendations_dict, output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <test_playlists.zip> [output.csv.gz]")
        print(f"Example: {sys.argv[0]} ./dataset/spotify_test_playlists.zip ./results/submission.csv.gz")
        sys.exit(1)
    
    test_zip_path = sys.argv[1]
    
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = "./results/submission.csv.gz"
    
    recommender(test_zip_path, output_path)