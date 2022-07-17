import math 

def decomposition (n):
    """
    Renvoi une liste de bits représentant n en base 2

    Parameters
    ----------
    n : int
        Un entier naturel.

    Returns
    -------
    res : list of boolean
        La liste de bits de n en base 2.

    """
    
    res = []
    while n != 0:
        reste = n % 2
        n = n // 2
        if reste == 0:
            res.append (False)
        else:
            res.append (True)
    return res

def completion (entier, n):
    """
    Tronque la liste si sa taille est plus grande que n, complète la liste avec des False sinon

    Parameters
    ----------
    entier : list of boolean
        La liste représentant les bits.
    n : int
        un entier naturel.

    Returns
    -------
    list
        La liste tronquée ou complétée avec des False.

    """
    
    taille = len (entier)
    if n <= taille:
        return entier[0:n]
    res = entier.copy()
    while taille != n:
        res.append (False)
        taille += 1
    return res

def table (x,n):
    """
    Construit une table de vérité  

    Parameters
    ----------
    x : int
        l'entier à décomposer en base 2.
    n : int
        la taille de la table de vérité.

    Returns
    -------
    list of boolean
        La table de vérité à partir de x et de taille n.

    """
    
    return completion (decomposition(x), n)
    