from xmlrpc.client import boolean
import os
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime
import argparse
import scipy

def unpack_floats(file_path):  # Paul
    with open(file_path, 'rb') as f:
        byte_data = f.read()
    num_floats = len(byte_data) // 4
    float_data = np.frombuffer(byte_data, dtype='>f').astype(np.float32)
    num_floats_trimmed = (num_floats // 4) * 4
    float_data = float_data[:num_floats_trimmed]
    reshaped_data = float_data.reshape(-1, 4)
    df = pd.DataFrame(reshaped_data, columns=['x', 'y', 'z', 'm'])
    return df


def afficher(df, name, ext, mn, mx, projection='xy', taille_points=0.5, type="nuage"):
    df = df[(df['m'] >= mn) & (df['m'] <= mx)]

    if df.empty:
        print("Aucune donnée ne correspond à la plage spécifiée des masses.")
        return

    if projection == 'xy':
        x, y, masses = df['x'], df['y'], df['m']
    elif projection == 'xz':
        x, y, masses = df['x'], df['z'], df['m']
    elif projection == 'yz':
        x, y, masses = df['y'], df['z'], df['m']

    match type:
        case "histogramme":
            norm = mcolors.Normalize(vmin=masses.min(), vmax=masses.max())
            cmap = plt.cm.viridis
            colors = [mcolors.to_hex(cmap(norm(m))) for m in masses]
            n, bins, patches = plt.hist(masses, bins=50, edgecolor='black')
            for patch, color in zip(patches, colors[:len(patches)]):  #
                patch.set_facecolor(color)
            title = "Histogramme des Masses Atomiques"
            plt.xlabel("Masses Atomiques")
            plt.ylabel("Fréquence")
            plt.title(title + f" {projection.upper()}  (" + name + ".pos)")
        case "nuage":
            scatter = plt.scatter(x, y, marker='.', s=taille_points, c=masses, cmap="magma", alpha=0.075)
            title = "Projection"
            plt.xlabel("X" if projection != 'yz' else "Y")
            plt.ylabel("Y" if projection != 'xz' else "Z")
            plt.colorbar(scatter, label="Masses Atomiques")
            plt.title(title + f" {projection.upper()}  (" + name + ".pos)")
        case "distribution":
            s = pd.Series(df["m"])
            s.plot.kde()
            title = "Histogramme de Densité de Masses Atomiques"
            plt.title(title)

    output_folder = "AnalyseTomographique/plots"
    file_name = f"{name}-{type}.{ext}"
    output_path = os.path.join(output_folder, file_name)
    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(output_path)
    print(f"Figure saved at location: {output_path}")


def process(path, name, plane, gtype, ext, csv, mn, mx, bounds):
    df = unpack_floats(path)
    df = df[(df['m'] >= mn) & (df['m'] <= mx)]
    if bounds:
        for axis, (min_val, max_val) in bounds.items():
            if min_val is not None:
                df = df[df[axis] >= min_val]
            if max_val is not None:
                df = df[df[axis] <= max_val]

    if df.empty:
        print("Le dataframe est vide")
        return

    if csv:
        csv_file = f"{name}.csv"
        df.to_csv(csv_file, index=False)
        print(f"Données sauvegardées en CSV : {csv_file}")

    afficher(df, name, ext, mn, mx, projection=plane, taille_points=0.5, type=gtype)


def bounds(data):
    minX = data['x'].min()
    maxX = data['x'].max()
    minY = data['y'].min()
    maxY = data['y'].max()
    minZ = data['z'].min()
    maxZ = data['z'].max()
    return f"Min-Max : X: {minX}, {maxX}; Y: {minY}, {maxY}; Z: {minZ}, {maxZ}"


def main(args):
    print(args)
    start = time.time()
    standardStart = datetime.datetime.fromtimestamp(start)
    print(str(standardStart) + " : astartes time")

    if '/' in args.chemin:
        nom = ((args.chemin).split('/')[-1]).split('.')[0]
    else:
        nom = args.chemin.split('.')[0]

    if args.b:
        df = unpack_floats(args.chemin)
        print(bounds(df))
        exit(0)
    axes_bounds = {
        'x': (args.xmin, args.xmax),
        'y': (args.ymin, args.ymax),
        'z': (args.zmin, args.zmax)
    }
    process(args.chemin, nom, args.plan, args.graph, args.ext, args.csv, args.mn, args.mx, axes_bounds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse tomographique avec découpe des axes et filtrage par masse."
    )
    parser.add_argument("chemin", type=str, help="Chemin vers le fichier à analyser", default=None)
    parser.add_argument("plan", type=str, default="xy", help="Type de projection pour le plan")
    parser.add_argument("graph", type=str, help="Type de graphe", default="nuage")
    parser.add_argument("ext", type=str, default="png", help="Type de fichier d'image pour le graph (png, svg, pdf)")
    parser.add_argument("-mx", type=float, help="Limite supérieure de la masse", default=1000.0)
    parser.add_argument("-mn", type=float, help="Limite inférieure de la masse", default=0.0)
    parser.add_argument("-csv", type=boolean, help="Exporte les données de l'échantillon en CSV", default=False)
    parser.add_argument("-b", type=boolean, help="Renvoie les valeurs min/max de l'échantillon pour chaque axe",default=False)
    parser.add_argument("-xmin", type=float, help="Limite minimale sur X", default=None)
    parser.add_argument("-xmax", type=float, help="Limite maximale sur X", default=None)
    parser.add_argument("-ymin", type=float, help="Limite minimale sur Y", default=None)
    parser.add_argument("-ymax", type=float, help="Limite maximale sur Y", default=None)
    parser.add_argument("-zmin", type=float, help="Limite minimale sur Z", default=None)
    parser.add_argument("-zmax", type=float, help="Limite maximale sur Z", default=None)

    args = parser.parse_args()
    main(args)