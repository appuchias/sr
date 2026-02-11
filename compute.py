#!/usr/bin/env python3
"""
Compute popularity scores for tracks in the training dataset.
"""

import json
import sys
import numpy as np
from scipy.sparse import load_npz
from typing import Dict, List, Tuple


def compute_popularity(matrix, songs: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Compute popularity of each track based on the number of playlists it appears in.
    
    Args:
        matrix: Sparse matrix where rows are playlists and columns are songs
        songs: Dictionary mapping song URIs to column indices
    
    Returns:
        List of tuples (song_uri, popularity_count) sorted by popularity (descending)
    """
    # Count occurrences of each song across all playlists
    # Sum over rows (axis=0) to get total count per song (column)
    popularity_counts = np.array(matrix.sum(axis=0)).flatten()
    
    # Create inverse mapping: column index -> song URI
    inverse_songs = {col_idx: uri for uri, col_idx in songs.items()}
    
    # Create list of (song_uri, count) tuples
    popularity_list = []
    for col_idx in range(len(popularity_counts)):
        if col_idx in inverse_songs:
            song_uri = inverse_songs[col_idx]
            count = int(popularity_counts[col_idx])
            popularity_list.append((song_uri, count))
    
    # Sort by popularity (descending)
    popularity_list.sort(key=lambda x: x[1], reverse=True)
    
    return popularity_list


def save_popularity_ranking(popularity_list: List[Tuple[str, int]], output_path: str = "./results/popularity_ranking.json"):
    """
    Save popularity ranking to a JSON file.
    
    Args:
        popularity_list: List of (song_uri, count) tuples
        output_path: Path to save the JSON file
    """
    # Convert to dictionary for easier lookup
    popularity_dict = {uri: count for uri, count in popularity_list}
    
    with open(output_path, "w") as f:
        json.dump(popularity_dict, f)
    
    print(f"Popularity ranking saved to '{output_path}'")
    print(f"Total unique tracks: {len(popularity_list)}")
    print(f"Most popular track: {popularity_list[0][0]} with {popularity_list[0][1]} appearances")
    print(f"Least popular track: {popularity_list[-1][0]} with {popularity_list[-1][1]} appearances")


if __name__ == "__main__":
    # Load the song-to-column mapping
    with open("./dataset/correspondencia_canciones.json") as f:
        songs = json.load(f)
    
    # Load the sparse matrix
    matrix = load_npz("./dataset/sparse_matrix.npz")
    
    print(f"Matrix shape: {matrix.shape}")
    print(f"Number of playlists: {matrix.shape[0]}")
    print(f"Number of unique tracks: {len(songs)}")
    
    # Compute popularity
    popularity_list = compute_popularity(matrix, songs)
    
    # Save the ranking
    save_popularity_ranking(popularity_list)
    
    # Show some statistics
    print("\nTop 10 most popular tracks:")
    for i, (uri, count) in enumerate(popularity_list[:10], 1):
        print(f"{i}. {uri}: {count} playlists")