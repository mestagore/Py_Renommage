# Py_Renommage

Un script Python permettant de renommer des fichiers en masse via une interface graphique native Windows.

---

## Fonctionnalités

- Sélection d'un **dossier entier** ou de **fichiers spécifiques** via une fenêtre graphique
- Numérotation automatique avec **padding dynamique** (s'adapte au nombre de fichiers)
- Validation du préfixe (caractères interdits, longueur maximale)
- Gestion des **conflits de noms** (passage par noms temporaires)
- Compatible **Windows / Linux / macOS**

---

## Structure du projet

```
Py_Renommage/
├── main.py          # Point d'entrée — orchestre le programme
├── functions.py     # Logique métier — toutes les fonctions
├── fichiers_test/   # Dossier de test (optionnel)
└── README.md
```

---

## Installation

**Prérequis :** Python 3.8 ou supérieur

`tkinter` est inclus par défaut avec Python. Aucune dépendance externe n'est nécessaire.

Clonez le dépôt :

```bash
git clone https://github.com/votre-utilisateur/Py_Renommage.git
cd Py_Renommage
```

---

## Utilisation

```bash
python main.py
```

Le programme vous propose deux modes :

```
Que voulez-vous renommer ?
1. Un dossier entier
2. Des fichiers spécifiques
Votre choix (1 ou 2) :
```

**Mode 1 — Dossier entier**
> Une fenêtre s'ouvre pour choisir un dossier. Tous ses fichiers seront renommés.

**Mode 2 — Fichiers spécifiques**
> Une fenêtre s'ouvre pour sélectionner des fichiers précis (`Ctrl + clic` pour la multi-sélection).

Ensuite, entrez le préfixe souhaité :

```
Entrez le préfixe souhaité : vacances
Renommé : IMG_4521.jpg  ->  vacances_001.jpg
Renommé : IMG_4522.jpg  ->  vacances_002.jpg
Renommé : IMG_4523.jpg  ->  vacances_003.jpg
Renommage terminé !
```

---

## Validation du préfixe

| Cas | Comportement |
|---|---|
| Champ vide | Redemande |
| Plus de 50 caractères | Redemande avec le compte |
| Caractères interdits (`< > : " / \ \| ? *`) | Redemande avec la liste |
| Préfixe valide | Poursuit le renommage |

---

## Padding dynamique

Le nombre de chiffres s'adapte automatiquement au nombre de fichiers :

| Nombre de fichiers | Exemple |
|---|---|
| 9 fichiers | `photo_1.jpg` … `photo_9.jpg` |
| 42 fichiers | `photo_01.jpg` … `photo_42.jpg` |
| 999 fichiers | `photo_001.jpg` … `photo_999.jpg` |
| 1500 fichiers | `photo_0001.jpg` … `photo_1500.jpg` |

---

## Gestion des conflits

Si un fichier du même nom existe déjà, le programme passe automatiquement par des **noms temporaires** pour éviter tout écrasement :

```
Étape 1 — Noms temporaires
  test_1.pdf  →  __temp_0__.pdf
  test_2.pdf  →  __temp_1__.pdf

Étape 2 — Noms finaux
  __temp_0__.pdf  →  prefixe_001.pdf
  __temp_1__.pdf  →  prefixe_002.pdf
```

---

## Technologies

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![tkinter](https://img.shields.io/badge/tkinter-builtin-green?style=flat)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat)

---

## Licence

Ce projet est sous licence **MIT** — libre d'utilisation, de modification et de distribution.
