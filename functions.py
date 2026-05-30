# ----------------------------------------------------------------------- * Imports et configuration
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# * Caractères interdits dans les noms de fichiers (Windows + Linux + macOS)
CARACTERES_INTERDITS = r'[<>:"/\\|?*\x00-\x1f]'
LONGUEUR_MAX = 50

# ----------------------------------------------------------------------- * Fonctions utilitaires

# * Retourne la liste des fichiers (pas les dossiers) présents dans `dossier`
def lister_fichiers(dossier):
    fichiers = []
    for f in os.listdir(dossier):
        chemin_complet = os.path.join(dossier, f)

        if os.path.isfile(chemin_complet):                                                      # * os.path.isfile() exclut les sous-dossiers
            fichiers.append(f)
    return fichiers


# * Génère un nom de fichier formaté : prefixe_001.ext, prefixe_002.ext...
def generer_nom(prefixe, numero, extension, nb_total):
    # * Calcule automatiquement le padding selon le nombre de fichiers
    nb_chiffres = len(str(nb_total))
    return f"{prefixe}_{str(numero).zfill(nb_chiffres)}{extension}"                             # * zfill(3) padde le numéro avec des zéros -> 1 devient "001"


# * Boucle jusqu'à obtenir un préfixe valide
def demander_prefixe():
    while True:
        prefixe = input("Entrez le préfixe souhaité : ").strip()

        # ! Refus si le champ est vide
        if not prefixe:
            print("Le préfixe ne peut pas être vide.")
            continue

        # ! Refus si trop long
        if len(prefixe) > LONGUEUR_MAX:
            print(f"Préfixe trop long ({len(prefixe)} caractères). Maximum : {LONGUEUR_MAX}.")
            continue

        # ! Refus si caractères interdits détectés
        if re.search(CARACTERES_INTERDITS, prefixe):
            print(f"Caractères interdits détectés. Évitez : < > : \" / \\ | ? *")
            continue

        # * Préfixe valide
        return prefixe
    

def renommer_fichiers(dossier, prefixe):
    fichiers = lister_fichiers(dossier)
    nb_total = len(fichiers)

    if nb_total == 0:
        print("⚠️ Aucun fichier trouvé dans le dossier.")
        return

    for i, fichier in enumerate(fichiers):
        _, extension = os.path.splitext(fichier)
        nouveau_nom = generer_nom(prefixe, i + 1, extension, nb_total)
        ancien_chemin = os.path.join(dossier, fichier)
        nouveau_chemin = os.path.join(dossier, nouveau_nom)

        # * Vérifie et corrige le nom si un fichier du même nom existe déjà
        nouveau_chemin = generer_nom_unique(nouveau_chemin, prefixe, i + 1, extension, nb_total)

        os.rename(ancien_chemin, nouveau_chemin)
        print(f"Renommé : {fichier} -> {os.path.basename(nouveau_chemin)}")


def renommer_fichiers_specifiques(fichiers, prefixe):
    nb_total = len(fichiers)
    dossier = os.path.dirname(fichiers[0])

    # * Étape 1 : renommer tous les fichiers avec un nom temporaire unique
    # * pour éviter les collisions entre les anciens et nouveaux noms
    fichiers_temp = []
    for i, chemin in enumerate(fichiers):
        _, extension = os.path.splitext(chemin)
        nom_temp = f"__temp_{i}__{extension}"
        chemin_temp = os.path.join(dossier, nom_temp)
        os.rename(chemin, chemin_temp)
        fichiers_temp.append(chemin_temp)
        print(f"Temp : {os.path.basename(chemin)} -> {nom_temp}")

    # * Étape 2 : renommer les fichiers temporaires vers leur nom final
    for i, chemin_temp in enumerate(fichiers_temp):
        _, extension = os.path.splitext(chemin_temp)
        nouveau_nom = generer_nom(prefixe, i + 1, extension, nb_total)
        nouveau_chemin = os.path.join(dossier, nouveau_nom)

        # * Vérifie quand même les collisions avec des fichiers extérieurs au lot
        nouveau_chemin = generer_nom_unique(nouveau_chemin, prefixe, i + 1, extension, nb_total)

        os.rename(chemin_temp, nouveau_chemin)
        print(f"Renommé : {os.path.basename(chemin_temp)} -> {os.path.basename(nouveau_chemin)}")

def choisir_dossier():
    # * Ouvre une fenêtre Windows native de sélection de dossier
    root = tk.Tk()
    root.withdraw()  # * Cache la fenêtre principale tkinter (on veut juste la boîte de dialogue)
    dossier = filedialog.askdirectory(title="Choisissez un dossier à renommer")

    # ! L'utilisateur a fermé la fenêtre sans choisir
    if not dossier:
        print("Aucun dossier sélectionné, abandon.")
        sys.exit(0)

    return dossier


def choisir_fichiers():
    # * Ouvre une fenêtre Windows native de sélection de fichiers (multi-sélection)
    root = tk.Tk()
    root.withdraw()
    fichiers = filedialog.askopenfilenames(title="Choisissez les fichiers à renommer")

    # ! L'utilisateur a fermé la fenêtre sans choisir
    if not fichiers:
        print("Aucun fichier sélectionné, abandon.")
        sys.exit(0)

    return list(fichiers)


def generer_nom_unique(nouveau_chemin, prefixe, numero, extension, nb_total):
    # * Si le fichier n'existe pas encore, on retourne le nom tel quel
    if not os.path.exists(nouveau_chemin):
        return nouveau_chemin

    # * Sinon on ajoute un suffixe _bis, _ter, ou un compteur jusqu'à trouver un nom libre
    suffixes = ["_bis", "_ter", "_quater"]
    for suffixe in suffixes:
        nb_chiffres = len(str(nb_total))
        nom_candidat = f"{prefixe}_{str(numero).zfill(nb_chiffres)}{suffixe}{extension}"
        chemin_candidat = os.path.join(os.path.dirname(nouveau_chemin), nom_candidat)
        if not os.path.exists(chemin_candidat):
            return chemin_candidat

    # * Si _bis, _ter, _quater sont tous pris, on passe à un compteur numérique
    compteur = 2
    while True:
        nb_chiffres = len(str(nb_total))
        nom_candidat = f"{prefixe}_{str(numero).zfill(nb_chiffres)}_{compteur}{extension}"
        chemin_candidat = os.path.join(os.path.dirname(nouveau_chemin), nom_candidat)
        if not os.path.exists(chemin_candidat):
            return chemin_candidat
        compteur += 1


# ----------------------------------------------------------------------- * Point d'entrée du programme

def main():
    print("Que voulez-vous renommer ?")
    print("1. Un dossier entier")
    print("2. Des fichiers spécifiques")
    choix = input("Votre choix (1 ou 2) : ").strip()

    if choix == "1":
        dossier = choisir_dossier()
        print(f"Dossier sélectionné : {dossier}")
        prefixe = demander_prefixe()
        renommer_fichiers(dossier, prefixe)

    elif choix == "2":
        fichiers = choisir_fichiers()
        print(f"{len(fichiers)} fichier(s) sélectionné(s)")
        prefixe = demander_prefixe()
        renommer_fichiers_specifiques(fichiers, prefixe)  # * Voir functions.py ci-dessous

    else:
        print("Choix invalide, abandon.")
        sys.exit(1)

    print("Renommage terminé !")