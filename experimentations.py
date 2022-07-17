from abd import *
import numpy as np
import random
import matplotlib.pyplot as plt
import time



def genere_abs_ord (nb_vars, nb_vals=10000):
    """
    Génère les abcisses/ordonnées des points de la courbe (cf. Figure 9-10) représentant le nombre de noeuds 
    en fonction du nombre de fonctions booléennes selon un nombre de variable fixé.

    Parameters
    ----------
    nb_vars : int
        Le nombre de variables.
    nb_vals : int, optional
        L'échantillon désiré. 10000 par défaut.

    Returns
    -------
    (array of int, array of int)
        Les abcisses et ordonnées de la courbe.

    """
     
    dico = dict()
    x = []
    y = []
    compensation = 1
    nb_feuilles = int (math.pow(2, nb_vars))
    def puissance (x, n):
        """
        Fonction puissance

        Parameters
        ----------
        x : int
            Un entier.
        n : int
            L'exposant.

        Returns
        -------
        int
            La valeur de x^n.

        """
        
        def aux (x, n, acc):
            """
            Fonction récursive (auxiliaire de puissance())

            Parameters
            ----------
            x : int
                Un entier.
            n : int
                L'exposant.
            acc : int
                L'accumulateur.

            Returns
            -------
            int
                La valeur de x^n..

            """
            
            if n == 0:
                return acc
            return aux (x, n - 1, acc * x)
        return aux (x, n, 1)
    
    def generer_entiers_alea (nb_vals, nb_bits):
        """
        Génère des entiers aléatoires

        Parameters
        ----------
        nb_vals : int
            Le nombre de valeur à générer.
        nb_bits : int
            Le nombre de bit maximum des entiers générés.

        Returns
        -------
        res : list of int
            La liste des entiers générés aléatoirement.

        """
        
        res = [0]         
        while nb_vals > 0:
            val = random.getrandbits (nb_bits) 
            if val not in res:
                res.append (val)
                nb_vals -= 1
        return res
    
    if nb_vars > 4:
        borne = puissance (2, nb_feuilles)
        entiers = generer_entiers_alea(nb_vals - 1, nb_feuilles)
        compensation = borne // nb_vals
    else:
        entiers = [i for i in range (0, int(math.pow (2, nb_feuilles)))]
        
    for i in entiers:
        arbre = abd.cons_arbre(table(i,nb_feuilles)) 
        arbre2 = abd.luka(arbre)
        arbre3 = abd.compression_bdd(arbre2)
        n = abd.nb_noeuds (arbre3)
        if n not in dico:
            dico [n] = 1
        else:
            dico [n] += 1
    dico = sorted (dico.items())
    for taille, occurrences in dico:
        x.append (taille)
        y.append (occurrences * compensation)
    x = np.array(x)
    y = np.array(y)
    return (x, y)

def genere_graphe (nb_vars, nb_vals):
    """
    Génère l'histogramme représentant le nombre de noeuds en fonction du nombre de fonctions booléennes
    selon un nombre de variable fixé. 

    Parameters
    ----------
    nb_vars : int
        Nombre de variables.
    nb_vals : int
        L'échantillon désiré.

    Returns
    -------
    function
        L'histogramme (conformément aux figures 9 et 10).

    """
    
    x, y = genere_abs_ord (nb_vars, nb_vals)
    plt.plot (x, y, "b:o")
    plt.title ("Nombre de noeuds des ROBDD pour " + str (nb_vars) + " variables")
    plt.xlabel ("Nombre de noeuds")
    plt.ylabel ("Nombre de fonctions booléennes")
    minx, maxx = plt.xlim()
    plt.xlim (0, maxx)
    return plt.show()

def genere_stats (nb_vars, nb_vals):
    """
    Génère les stats d'une expérimentation (conformément à la figure 10)

    Parameters
    ----------
    nb_vars : int
        Nombre de variables.
    nb_vals : int
        L'échantillon désiré.

    Returns
    -------
    nb_vars : int
        Le nombre de variables.
    nb_vals : int
        L'échantillon.
    int
        Le nombre de tailles uniques de ROBDD.
    temps : float
        Le temps de calcul total.
    temps_par_robdd : float
        Le temps de calcul par ROBDD.

    """
    
    debut = time.time()
    x, _ = genere_abs_ord (nb_vars, nb_vals)
    fin = time.time()
    temps = fin - debut
    temps_par_robdd = temps / nb_vals
    return (nb_vars, nb_vals, len (x), temps, temps_par_robdd)

def genere_stats_et_graphe (nb_vars, nb_vals, fichier):
    """
    Construit le fichier avec les stats et construit l'histogramme de l'experimentation.

    Parameters
    ----------
    nb_vars : int
        Le nombre de variables.
    nb_vals : int
        L'échantillon désiré.
    fichier : string
        Le fichier.

    Returns
    -------
    function
        L'histogramme.

    """
    
    f = open (fichier, "a")
    debut = time.time()
    x, y = genere_abs_ord (nb_vars, nb_vals)
    fin = time.time()
    temps = fin - debut
    temps_par_robdd = temps / nb_vals
    f.write (str (nb_vars) + ";" + str (nb_vals) + ";" + str (len (x)) + ";" + str (temps) + ";" + str (temps_par_robdd) + "\n")
    f.close()
    plt.plot (x, y, "b:o")
    plt.title ("Nombre de noeuds des ROBDD pour " + str (nb_vars) + " variables")
    plt.xlabel ("Nombre de noeuds")
    plt.ylabel ("Nombre de fonctions booléennes")
    minx, maxx = plt.xlim()
    plt.xlim (0, maxx)
    return plt.show()

        

