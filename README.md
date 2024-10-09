# TP Big Data Vélib

Ce projet analyse les données Vélib en utilisant MongoDB et Python pour effectuer des opérations de map-reduce.

## Prérequis

- Docker
- Python 3.x
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez ce répertoire :
   ```
   git clone https://github.com/AxelSELEBRANTSF/tp-big-data-Axel-SELEBRAN-MLV.git
   cd tp-big-data-Axel-SELEBRAN-MLV
   ```

2. Installez les dépendances Python :
   ```
   pip install -r requirements.txt
   ```

## Lancement du projet

### 1. Démarrer MongoDB avec Docker

Lancez MongoDB sur le port 27017 avec Docker en utilisant les commandes suivantes :

```bash
# Créez un volume Docker pour persister les données
docker volume create mongodb_data

# Lancez le conteneur MongoDB
docker run -d -p 27017:27017 --name mongodb \
  -v mongodb_data:/data/db \
  mongo:latest
```

Ces commandes vont :
- Créer un volume Docker nommé `mongodb_data` pour stocker les données de manière persistante.
- Lancer un conteneur MongoDB nommé `mongodb`, en mappant le port 27018 de l'hôte au port 27017 du conteneur.

### 2. Exécuter le script principal

Une fois MongoDB en cours d'exécution, vous pouvez lancer le script principal :

```bash
python main.py
```

Ce script va se connecter à la base de données MongoDB, effectuer l'opération de map-reduce sur les données Vélib, et afficher les résultats.


Par la suite, vous pouvezz lancer le script pour lancer la map avec les quinze points les plus proche:

```bash
python index.py
```

## Arrêt du projet

Pour arrêter le conteneur MongoDB après utilisation :

```bash
docker stop mongodb
```

Pour supprimer le conteneur (tout en conservant les données dans le volume) :

```bash
docker rm mongodb
```

## Remarques

- Assurez-vous que le port 27018 est libre sur votre machine avant de lancer le conteneur MongoDB.
- Si vous modifiez le port dans la commande Docker, n'oubliez pas de mettre à jour la configuration de connexion dans le script Python.
