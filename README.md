# Proceso

i7-12650H
16GB RAM
1TB SSD

```
python reader.py && python compute.py && python recommender.py --recommendations_path ./results/submission_it0.csv.gz
```

```bash
❯ python reader.py
100%|█████████████████████████████████████████████████████| 1011/1011 [03:08<00:00,  5.36it/s]
Matriz CSR creada y guardada en './dataset/sparse_matrix.npz'.
Guardada la correspondencia de canciones a columnas de la matriz en './dataset/correspondencia_canciones.json.zst'
```

```bash
❯ python compute.py
Número de playlists: 1000000
Número de canciones: 2262292
Ranking de popularidad guardado en './results/popularity_ranking.json.gz'

Top 10 canciones más populares:
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
❯ python recommender.py --recommendations_path ./results/submission_it0.csv.gz

Cargando ránkings de popularidad...
Cargadas 2262292 canciones

Obteniendo los items semilla de las playlsits...
Cargadas 10000 playlists

Obteniendo recomendaciones...
Obtenidas recomendaciones para 10000 playlists

Guardando las recomendaciones con el formato de salida...
Archivo de salida guardado en './results/submission_it0.csv.gz'
Total de playlists con recomendaciones: 10000
```
