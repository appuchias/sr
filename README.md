# Proceso

i7-12650H
16GB RAM
1TB SSD

```bash
❯ python reader.py dataset/spotify_train_dataset.zip
100%|█████████████████████████████████████████████████████| 1011/1011 [03:08<00:00,  5.36it/s]
Matriz CSR creada y guardada en './dataset/sparse_matrix.npz'.
Guardada la correspondencia de canciones a columnas de la matriz en './dataset/correspondencia_canciones.json.zst'
```

```bash
❯ python compute.py
Matrix shape: (65640000, 2262292)
Number of playlists: 65640000
Number of unique tracks: 2262292
Popularity ranking saved to './results/popularity_ranking.json'
Total unique tracks: 2262292
Most popular track: spotify:track:7KXjTSCq5nL1LoYtL7XAwS with 45921 appearances
Least popular track: spotify:track:5DvykFHB6utG6Hozpt5eNK with 1 appearances

Top 10 most popular tracks:
1. spotify:track:7KXjTSCq5nL1LoYtL7XAwS: 45921 playlists
2. spotify:track:1xznGGDReH1oQq0xzbwXa3: 42854 playlists
3. spotify:track:7yyRTcZmCiyzzJlNzGC9Ol: 40680 playlists
4. spotify:track:7BKLCZ1jbUBVqRi2FVlTVw: 40511 playlists
5. spotify:track:3a1lNhkSLSkpJE4MSHpDu9: 39415 playlists
6. spotify:track:5hTpBe8h35rJ67eAWHQsJx: 34663 playlists
7. spotify:track:2EEeOnHehOozLq4aS0n6SL: 34631 playlists
8. spotify:track:4Km5HrUvYTaSUfiSGPJeQR: 34496 playlists
9. spotify:track:7GX5flRQZVHRAGd6B4TmDO: 34395 playlists
10. spotify:track:152lZdxL1OR0ZMW6KquMif: 34163 playlists
```

```bash
❯ python recommender.py dataset/spotify_test_playlists.zip
Loading popularity ranking...
Loaded 2262292 tracks

Extracting playlist seeds from test dataset...
Found 10000 test playlists

Generating recommendations...
Generated recommendations for 10000 playlists

Formatting submission file...
Submission file saved to './results/submission.csv.gz'
Total playlists: 10000
Format: gzipped CSV (.csv.gz)
```
