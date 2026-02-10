#!/usr/bin/env python3

def recommender(...) -> ...:
    ...


if __name__ == "__main__":

    test_zip_path = sys.argv[1]
    npz_path = sys.argv[2]

    if not zip_path:
        print(f"Uso: {sys.argv[0]} <archivo.zip> [archivo_salida.npz]")
        exit(1)

    if not npz_path:
        npz_path = "sparse_matrix.npz"

    recommender(zip_path, npz_path)
