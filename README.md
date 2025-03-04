# Noyau minimal du projet :
## Lecture et traitement des fichiers :
* Lire des fichiers binaires contenant des données atomiques sous forme de flottants (x, y, z, m).
* Traiter ces données pour les rendre exploitables.
## Exploitation des données :
* Sélectionner une portion des données selon :
  * Une coupe définie par un plan et une épaisseur.
  * Un intervalle de valeurs pour les masses atomiques.
* Visualisation des données :
  * Générer des représentations graphiques :
    * Histogrammes des masses atomiques.
    * Projections des points atomiques sur un plan avec une coloration par masse (selon un fichier ppng fourni).
# Fonctionnalités à implémenter :

## Lecture des fichiers :
  * Gérer l'importation des fichiers binaires en format big-endian.
  * Décoder les données en coordonnées spatiales (x, y, z) et masses (m).

## Filtrage des données :
  * Une coupe géométrique (plan et épaisseur).
  * Une plage de masses atomiques.

## Visualisation graphique :
  * Des histogrammes montrant la répartition des masses.  
  * Des nuages de points en 2D représentant des projections sur un plan choisi, avec coloration selon les masses.

# Optionel 
* Export des résultats :
    * Enregistrer les données traitées et les graphiques.
* Interface graphique :
  * Interface qui permet de sélectionner un fichier et de cocher les options voulues.
* Optimisation du code (si possible, passer par des array Numpy ou des DataFrames Pandas)

# Librairies :

`os`:
    Pour la gestion des chemins et des fichiers.

`numpy`:
    Pour les calculs et les tableaux

`pandas`:
    Pour les dataframes et les opérations

`matplotlib`:
    Pour visualiser les données (nuages, histogrammes ...)

`argparse`:
    Pour passer les arguments du terminal au programme

`xmlrpc.client`: pour les booléens

`time`: pour afficher le temps écoulé

`datetime`: pour les opération sur les temps UNIX

`scipy` : pour la courbe gaussienne 

# Fonctionnement du programme :

`chemin`-> Charger le fichier fichier.pos.

`plan`-> Sélection du plan xy ou xz ou yz ...

`graph`-> Sélection du type de graphique "nuage de points" , " histogramme"... avec une coloration basée sur les masses atomiques.

 `ext`-> Sauvegarde le graphique au format .png dans le dossier AnalyseTomographique/plots. 

`mn mx`->Filtre les masses atomiques dans l'intervalle donné .

Filtre les valeurs sur les axes :

* X entre  un intervalle. `xmin xmax`
* Y entre  un intervalle. `ymin ymax`
* Z entre  un intervalle . `zmin zmax`

exemple de commande a mettre dans le terminal pour lancer le code :
`python .\AnalyseTomographique\main.py chemin\vers\fichier.pos xy nuage png -mn 10 -mx 100 -xmin -50 -xmax 50 -zmin 0 -zmax 100` Windows

`python3 AnalyseTomographique/main.py  Chemin/vers/fichier.pos xz nuage png -xmin=0 -xmax=50 -ymin=0 -ymax=50 -zmin=0 -zmax=50 -mn=30 -mx=100` Linux

# Répartition du travail : 

Tony : `afficher`, `bounds`, `process`, `main`

Paul : `unpack_floats`, `afficher`, `process`, `main`
