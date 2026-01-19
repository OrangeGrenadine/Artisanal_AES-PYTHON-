# -- Un AES-Artisanal en Python -- 

Ce projet tente d'implémenter l'**Advanced Encryption Standard (AES)** en Python, sans l'aide d'aucune bibliothèque externe.

Les seules bibliothèques utilisées sont dans le fichier **'main.py'**', qui a pour but d'illustrer que le programme peut fonctionner sans l'utilisation de numpy et surtout de SageMath comme on l'avait fait à la base. Vous pouvez vous en défaire si vous ne comptez qu'utiliser le fichier **'MoteurAlgebre.py'** (*trop bien comme nom héhé*), sur lequel repose tout le projet.

Ce projet se base sur le document **Rijndael for algebraists**, publié le 8 avril 2002 par **H.W. Lenstra, Jr**.

---

## -- Utilisation --

Le script `main.py` à la racine permet de chiffrer et déchiffrer des fichiers en utilisant ce que j'ai appelé le *'moteur'*, situé dans `./Biblio/MoteurAlgebre.py`.

### 1. Chiffrement (Encryption)

Pour transformer un fichier clair en fichier chiffré :

```bash
python3 main.py enc <nom_du_fichier> -k <clé_hexa>

```

*Exemple :*

```bash
python3 main.py enc document.txt -k 0xb4c168612aff26221004ef626cc42811

```

> 📝 Un fichier `document.txt.enc` sera généré.

### 2. Déchiffrement (Decryption)

Pour retrouver le contenu original :

```bash
python3 main.py dec <nom_du_fichier.enc> -k <clé_hexa>

```

*Exemple :*

```bash
python3 main.py dec document.txt.enc -k 0xb4c168612aff26221004ef626cc42811

```

> 📝 Un fichier `document.txt.enc.dec` sera généré.

---

## -- Paramètres --

| Argument | Description | Défaut |
| --- | --- | --- |
| `action` | `enc` pour chiffrer, `dec` pour déchiffrer | (Obligatoire) |
| `file` | Chemin vers le fichier cible | (Obligatoire) |
| `-k`, `--key` | Clé secrète au format hexadécimal (`0x...`) (**16 octets**)| (Obligatoire) |
| `-p`, `--profondeur` | Nombre de rounds de l'algorithme | `11` |

## -- Note --

C'est tarpin long de chiffrer un fichier :O J'imagine que le script est séquentiel c'est pour ça. Pour le moment, j'ai pas la solution, je sais que ça existe du *Multiprocessing* mais je m'y connais malheureusement pas assez en codage :/

Mais c'était un super projet, pour une première en tout cas :)
