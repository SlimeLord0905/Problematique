#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random


""" Ce fichier contient la classe TextAn, à utiliser pour résoudre la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes apparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test test_textan.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe TextAn est invoquée par la classe TestTextAn (contenue dans test_textan.py) :

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier test_textan.py)
        - Note : vous pouvez tester votre code en utilisant les commandes :
            + "python test_textan.py"
            + "python test_textan.py -h" (donne la liste des arguments possibles)
            + "python test_textan.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke 
"""

from textan_common import TextAnCommon


class TextAn(TextAnCommon):
    """Classe à utiliser pour coder la solution à la problématique :

        - La classe héritée TextAnCommon contient certaines fonctions de base pour faciliter le travail :
            - recherche des auteurs
            - ouverture des répertoires
            - et autres (voir la classe TextAnCommon pour plus d'information)
            - La classe ParsingClassTextAn est héritée par TextAnCommon et lit la ligne de commande
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes :
            - dot_product_dict (dict1, dict2)
            - dot_product_aut (auteur1, auteur2)
            - doct_product_dict_aut (dict, auteur)
            - find_author (oeuvre)
            - gen_text (auteur, taille, textname)
            - get_nth_element (auteur, n)
            - analyze()

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    # Signes de ponctuation à retirer (compléter cette liste incomplète)
    PONC = ["!", "?", ",", ":", ";", "-", "«", "»", ".", "...", "_", "(", ")", "'"]

    def __init__(self) -> None:
        """Initialize l'objet de type TextAn lorsqu'il est créé

        Args :
            (void) : Utilise simplement les informations fournies dans la classe TextAnCommon

        Returns :
            (void) : Ne fait qu'initialiser l'objet de type TextAn
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        super().__init__()

        self.big = {}
        self.markov = {}
        self.markov_big = {}

        return

    # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    #   la production de textes aléatoires, la détection d'oeuvres inconnues,
    #   l'identification des n-ièmes mots les plus fréquents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelée en premier par test_textan.py
    # Ensuite, selon ce qui est demandé, les fonctions find_author(), gen_text() ou get_nth_element() sont appelées

    @staticmethod
    def dot_product_dict(dict1: dict, dict2: dict) -> float:
        """Calcule le produit scalaire NORMALISÉ de deux vecteurs représentés par des dictionnaires

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé de deux vecteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """
        #print(dict1)
        print("call de dot_product_dict")
        dot_product = 1.0

        len_vec_1 = 0.0
        for key in dict1.keys():
            len_vec_1 += dict1[key]*dict1[key]
        len_vec_2 = 0.0
        for key in dict2.keys():
            len_vec_2 += dict2[key]*dict2[key]

        len_vec_1 = math.sqrt(len_vec_1)
        len_vec_2 = math.sqrt(len_vec_2)

        prod_non_normaliser = 0.0
        for key in dict1.keys():
            if key in dict2:
                prod_non_normaliser += dict1[key] * dict2[key]

        dot_product = prod_non_normaliser/ (len_vec_1*len_vec_2)
        print('prod: ', dot_product)
        return dot_product

    def dot_product_aut(self, auteur1: str, auteur2: str) -> float:
        """Calcule le produit scalaire normalisé entre les oeuvres de deux auteurs, en utilisant dot_product_dict()

        Args :
            auteur1 (str) : le nom du premier auteur
            auteur2 (str) : le nom du deuxième auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """
        print("call de dot_product_aut")
        dot_product = self.dot_product_dict(self.mots_auteurs[auteur1], self.mots_auteurs[auteur2])
        return dot_product

    def dot_product_dict_aut(self, dict_oeuvre: dict, auteur: str) -> float:
        """Calcule le produit scalaire normalisé entre une oeuvre inconnue et les oeuvres d'un auteur,
           en utilisant dot_product_dict()

        Args :
            dict_oeuvre (dict) : la liste des n-grammes d'une oeuvre inconnue
            auteur (str) : le nom d'un auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """
        print("call de dot_product_dict_aut")

        dot_product = self.dot_product_dict(self.mots_auteurs[auteur], dict_oeuvre)
        return dot_product

    def find_author(self, oeuvre: str) -> []:
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue
            avec les écrits de chacun d'entre eux

        Args :
            oeuvre (str) : Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns :
            resultats (Liste[(string, float)]) : Liste de tuples (auteurs, niveau de proximité),
            où la proximité est un nombre entre 0 et 1)
        """
        print(f"Comparaison de {oeuvre}")
        auteur_prob = []
        with open(oeuvre, "r", encoding='utf8') as oeuvre_file:
            oeuvre_content = []
            all_ngram_counts = {}

            for line in oeuvre_file:
                if not self.keep_ponc:
                    for ponct in self.PONC:
                        # la ponctuation est considere comme des espaces
                        line = line.replace(ponct, ' ')

                line_cleaned = line.lower()
                oeuvre_content.extend(line_cleaned.split())

            if self.remove_word_1 and self.remove_word_2:
                words_filtered = [word for word in oeuvre_content if len(word) > 2]
            elif self.remove_word_1:
                words_filtered = [word for word in oeuvre_content if len(word) != 1]
            elif self.remove_word_2:
                words_filtered = [word for word in oeuvre_content if len(word) != 2]
            else:
                words_filtered = [word for word in oeuvre_content]

            # pour generer les ngram
            ngrams = [' '.join(words_filtered[i:i + self.ngram]) for i in
                      range(len(words_filtered) - self.ngram + 1)]

            # dictionnaire pour les frequences
            ngram_counts = {}

            # pour chaque ngram, si il est present dans ngram_counts, il est incremente de 1,
            # sinon il est ajoute dans le dictionnaire avec une frequence de 1
            for ngram in ngrams:

                ngram_counts[ngram] = ngram_counts.get(ngram, 0) + 1

            # pour combiner les ngrams des differentes oeuvres du meme auteur
            for ngram, frequency in ngram_counts.items():
                all_ngram_counts[ngram] = all_ngram_counts.get(ngram, 0) + frequency

        for auteur in self.auteurs:
            auteur_prob.append((auteur, self.dot_product_dict_aut(all_ngram_counts, auteur)))

        resultats = auteur_prob
        return resultats

    '''la generation de texte se fait avec une chaine de markov, les cles du dcitonnaire sont le ngram courant
    tandis que les valeurs sont les ngrams prochains possibles, un de ces derniers est selectionnes et il devient
    par la suite le ngram courant, cela continue jusqu'a taille, pour generer un text avec un n eleve, etant donne qu'une 
    bonne partie des ngrams ont une frequence de 1, il y a souvent un seul ngram prochain possible, 
    par consequent, la chaine de markov ne fait que repeter un bout de texte consecutif'''

    def gen_text_all(self, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques de l'ensemble des auteurs

        Args :
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """
        print("Generation texte tout")

        generated_text = []
        ngram_initial = random.choice(list(self.markov_big.keys()))
        ngram_courant = ngram_initial
        generated_text.append(ngram_courant)
        word_count = self.ngram

        for _ in range(math.floor((taille - 1)/self.ngram)):
            if ngram_courant not in self.markov_big:
                ngram_courant = random.choice(list(self.markov_big.keys()))
            next_word_probs = self.markov_big[ngram_courant]
            next_word = random.choices(list(next_word_probs.keys()), weights=list(next_word_probs.values()))[0]
            generated_text.append(next_word)
            ngram_courant = next_word
            word_count += self.ngram

            if word_count > 15:
                generated_text.append('\n')
                word_count = 0

            with open(textname, "w", encoding='utf8') as text_file:
                for word in generated_text:
                    if word == '\n':
                        text_file.write('\n')

                    else:
                        text_file.write(word + ' ')



    def gen_text_auteur(self, auteur: str, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Ce print ne sert qu'à éliminer un avertissement. Il doit être retiré lorsque le code est complété

        print(f"Generation texte {auteur}")
        if auteur not in self.auteurs:
            print(f"Author '{auteur}' not found.")
            return
        generated_text = []
        ngram_initial = random.choice(list(self.markov[auteur].keys()))
        ngram_courant = ngram_initial
        generated_text.append(ngram_courant)
        word_count = self.ngram
        if word_count > 15:
            generated_text.append('\n')
            word_count = 0

        for _ in range(math.ceil((taille - 1) / self.ngram)):
            if ngram_courant not in self.markov[auteur]:
                ngram_courant = random.choice(list(self.markov[auteur].keys()))
            next_word_probs = self.markov[auteur][ngram_courant]
            next_word = random.choices(list(next_word_probs.keys()), weights=list(next_word_probs.values()))[0]
            generated_text.append(next_word)
            ngram_courant = next_word
            word_count += self.ngram

            if word_count > 15:
                generated_text.append('\n')
                word_count = 0

            with open(textname, "w", encoding='utf8') as text_file:
                for word in generated_text:
                    if word == '\n':
                        text_file.write('\n')

                    else:
                        text_file.write(word + ' ')



    def get_nth_element(self, auteur: str, n: int) -> [[str]]:
        """Après analyse des textes d'auteurs connus, retourner le n-ième plus fréquent n-gramme de l'auteur indiqué

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            n (int) : Indice du n-gramme à retourner

        Returns :
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherché
            (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """
        ngrams = self.mots_auteurs[auteur]
        sorted_ngrams_keys = self.quicksort_descending(list(ngrams.items()))
        frequencies = sorted(set(item[1] for item in sorted_ngrams_keys), reverse=True)

        try:
            target_frequency = frequencies[n - 1]
        except IndexError:
            print("index existe pas, n mit a 1 par defaut")
            target_frequency = frequencies[0]
        ngrams_list = []

        for ngram_key, frequency in sorted_ngrams_keys:
            if frequency == target_frequency:
                try:
                    words = ngram_key.split()
                    ngrams_list.append(words)
                except KeyError:
                    print(f"'{ngram_key}' pas trouve")

        return ngrams_list

    def quicksort_descending(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x[1] > pivot[1]]
        middle = [x for x in arr if x[1] == pivot[1]]
        right = [x for x in arr if x[1] < pivot[1]]
        return self.quicksort_descending(left) + middle + self.quicksort_descending(right)


    def analyze(self) -> None:

        all = {}
        markov_big = {}

        print("Analyse des textes")
        for auteur in self.auteurs:
            markov = {}
            aut_files = self.get_aut_files(auteur)
            all_ngram_counts = {}

            for oeuvre in aut_files:
                with open(oeuvre, "r", encoding='utf8') as oeuvre_file:
                    oeuvre_content = []

                    for line in oeuvre_file:
                        if not self.keep_ponc:
                            for ponct in self.PONC:
                                # la ponctuation est considere comme des espaces
                                line = line.replace(ponct, ' ')

                        line_cleaned = line.lower()
                        oeuvre_content.extend(line_cleaned.split())

                    if self.remove_word_1 and self.remove_word_2:
                        words_filtered = [word for word in oeuvre_content if len(word) > 2]
                    elif self.remove_word_1:
                        words_filtered = [word for word in oeuvre_content if len(word) != 1]
                    elif self.remove_word_2:
                        words_filtered = [word for word in oeuvre_content if len(word) != 2]
                    else:
                        words_filtered = [word for word in oeuvre_content]

                    # pour generer les ngram
                    ngrams = [' '.join(words_filtered[i:i + self.ngram]) for i in
                              range(len(words_filtered) - self.ngram + 1)]

                    ngram_frequencies = {}

                    for ngram in ngrams:
                        ngram_frequencies[ngram] = ngram_frequencies.get(ngram, 0) + 1

                    for ngram, frequency in ngram_frequencies.items():
                        all_ngram_counts[ngram] = all_ngram_counts.get(ngram, 0) + frequency


                    for i in range(len(ngrams) - self.ngram):
                        prefix = ngrams[i]
                        next_ngram = ngrams[i + self.ngram]

                        if prefix not in markov:
                            markov[prefix] = {}
                        if next_ngram not in markov[prefix]:
                            markov[prefix][next_ngram] = 0
                        markov[prefix][next_ngram] += 1

                        if prefix not in markov_big:
                            markov_big[prefix] = {}
                        if next_ngram not in markov_big[prefix]:
                            markov_big[prefix][next_ngram] = 0
                        markov_big[prefix][next_ngram] += 1

            for mot_present, transitions in markov.items():
                sorted_transitions = self.quicksort_descending(list(transitions.items()))
                markov[mot_present] = dict(sorted_transitions)


            self.markov[auteur] = markov


            for ngram, frequency in all_ngram_counts.items():
                all[ngram] = all.get(ngram, 0) + frequency

            # pour stocker toutes les informations de chaque auteur sans mots_auteurs

            self.mots_auteurs[auteur] = all_ngram_counts

            self.big = all


        for mot_present, transitions in markov_big.items():
            sorted_transitions = self.quicksort_descending(list(transitions.items()))
            markov_big[mot_present] = dict(sorted_transitions)

        self.markov_big = markov_big