import math
from echauffement import *
from graphviz import Graph


class abd:
    def __init__ (self, etiquette=None, faux=None, vrai=None):
        """
        Définition d'un arbre binaire de décision'

        Parameters
        ----------
        etiquette : string, optional
            l'étiquette du noeud. None par défaut
        faux : abd, optional
            Fils correspondant à l'évaluation False de l'étiquette. None par défaut
        vrai : abd, optional
            Fils correspondant à l'évaluation True de l'étiquette. None par défaut

        Returns
        -------
        None.

        """
        
        self.etiquette = etiquette
        self.faux = faux
        self.vrai = vrai
     
    @staticmethod
    def affiche (arbre):
        """
        Affiche un arbre binaire de décision / ROBDD (avec le module graphviz)

        Parameters
        ----------
        arbre : abd
            L'arbre à afficher.

        Returns
        -------
        graphviz.dot.Graph
            Le graphique correspondant à l'arbre.

        """
        
        dot = Graph()
        def chercher_noeud (noeud, noeuds):
            """
            Cherche un noeud dans une liste

            Parameters
            ----------
            noeud : abd
                Le noeud à chercher.
            noeuds : list
                La liste de noeuds.

            Returns
            -------
            string
                Le code du noeud trouvé (utile pour l'affichage), False sinon .
            abd
                Le noeud trouvé, False sinon.

            """
            
            for (c, n) in noeuds:
                if noeud == n:
                    return (c, n)
            return (False, False)
        
        def ajouter_liens (edges, dot):
            """
            Ajoute les liens dans le graphe 

            Parameters
            ----------
            edges : method
                Contient les liens à ajouter.
            dot : graphviz.dot.Graph
                le graphe.

            Returns
            -------
            dot : graphviz.dot.Graph
                Le graphe contenant ses nouveaux liens.

            """
            
            for edge in edges:
                if len (edge) == 3:
                    etiquette, faux, _ = edge
                    dot.edge(etiquette, faux, style="dotted")
                else:
                    etiquette, vrai = edge
                    dot.edge(etiquette, vrai)
            return dot
        
        def aux (noeud, dot, edges, noeuds, nom):
            """
            Fonction récursive (auxiliaire de affiche())

            Parameters
            ----------
            noeud : abd
                DESCRIPTION.
            dot : graphviz.dot.Graph
                Le graphe.
            edges : method
                Contient les liens entre les noeuds dans le graphe.
            noeuds : list
                La liste des noeuds présent dans l'arbre.
            nom : string
                Le code du noeud.

            Returns
            -------
            dot : graphviz.dot.Graph
                Le graphique correspondant à l'arbre.

            """
            
            if noeud == None or (noeud.faux == None and noeud.vrai == None):
                return dot
            code_faux, faux = chercher_noeud (noeud.faux, noeuds)        
            if faux:
                edges.add ((nom, code_faux, "d"))
            else:
                code_faux = "f" + nom
                dot.node(code_faux, noeud.faux.etiquette)
                edges.add ((nom, code_faux, "d"))
                noeuds.add ((code_faux, noeud.faux))
                dot = aux (noeud.faux, dot, edges, noeuds, code_faux)
            code_vrai, vrai = chercher_noeud (noeud.vrai, noeuds)
            if vrai: 
                edges.add ((nom, code_vrai))
            else:
                code_vrai = "v" + nom
                dot.node(code_vrai, noeud.vrai.etiquette)
                edges.add ((nom, code_vrai))
                noeuds.add ((code_vrai, noeud.vrai))
                dot = aux (noeud.vrai, dot, edges, noeuds, code_vrai)
            
            return dot
        
        edges = set()
        noeuds = set()
        dot.node("r", arbre.etiquette)
        dot = aux (arbre, dot, edges, noeuds, "r")
        ajouter_liens (edges, dot)
        return dot
     
    @staticmethod
    def cons_arbre (table_verite):
        """
        Construit l'arbre binaire de décision associé à la table de vérité

        Parameters
        ----------
        table_verite : list of boolean
            Une table de vérité.

        Returns
        -------
        abd
            L'arbre binaire de décision.

        """
        
        def aux (table_verite, i):
            """
            Fonction récursive (auxiliaire de cons_arbre())

            Parameters
            ----------
            table_verite : list of boolean
                Une table de vérité.
            i : int
                Compteur de la hauteur dans l'arbre.

            Returns
            -------
            abd
                L'arbre binaire de décision.

            """
            
            if i == 0:
                return abd (str(table_verite[0]))
            longueur = len (table_verite)
            faux = table_verite [0:(longueur//2)]
            vrai = table_verite [(longueur//2):]
            noeud = abd ("x" + str(int(i)), aux (faux, i-1), aux (vrai, i-1))
            return noeud
        i = math.log2(len(table_verite))
        return aux (table_verite, i)
    
    @staticmethod
    def luka (arbre):
        """
        Construit un arbre binaire de décision enrichi par les mots de Lukasiewicz

        Parameters
        ----------
        arbre : abd
            Un arbre binaire de décision.

        Returns
        -------
        abd
            L'arbre binaire de décision enrichi.

        """
        
        if arbre.faux == None and arbre.vrai == None:
            return arbre
        faux = abd.luka (arbre.faux)
        vrai = abd.luka (arbre.vrai)
        etiquette = "(" + arbre.etiquette + "(" + faux.etiquette + ")" + "(" + vrai.etiquette + "))"
        return abd (etiquette, faux, vrai)
    
    @staticmethod
    def compression (arbre):
        """
        Construit un arbre binaire de décision compressé

        Parameters
        ----------
        arbre : abd
            Un arbre binaire de décision enrichi par les mots de Lukasiewicz.

        Returns
        -------
        abd
            L'arbre compressé.

        """
        
        
        def trouver (etiquette, noeuds):
            """
            Cherche une étiquette dans une liste de noeuds 

            Parameters
            ----------
            etiquette : string
                La variable qu'on cherche.
            noeuds : list of abd
                La liste de noeuds de l'arbre.

            Returns
            -------
            abd
                Le noeud qui contient l'étiquette recherchée, False sinon.

            """
            
            for noeud in noeuds:
                if noeud.etiquette == etiquette:
                    return noeud
            return False
        
        def extraire_etiquette (etiquette_luka):
            """
            Extrait le nom de la variable d'un noeud à partir de son mot de Lukasiewicz

            Parameters
            ----------
            etiquette_luka : string
                Le mot de Lukasiewicz.

            Returns
            -------
            string
                Le nom de la variable.

            """
            
            if etiquette_luka [0] == '(':
                i = 1
                while etiquette_luka [i] != '(':
                    i += 1
                return etiquette_luka [1:i]
            return etiquette_luka
        
        def renommer (arbre):
            """
            Renomme chaque noeud de l'arbre par leur variable (modifie l'arbre reçu en paramètre)

            Parameters
            ----------
            arbre : abd
                L'arbre à renommer.

            Returns
            -------
            None.

            """
            
            if arbre == None:
                return 
            arbre.etiquette = extraire_etiquette (arbre.etiquette)
            renommer (arbre.faux)
            renommer (arbre.vrai)
                           
        def aux (arbre, noeuds):
            """
            Fonction récursive (auxiliaire de compression())

            Parameters
            ----------
            arbre : abd
                L'arbre à compresser.
            noeuds : list of abd
                La liste des noeuds de l'arbre.

            Returns
            -------
            abd
                L'arbre binaire de décision compressé.

            """
            
            if arbre == None:
                return None
            if arbre.faux == None and arbre.vrai == None:
                feuille = trouver (arbre.etiquette, noeuds)
                if not feuille:
                    nouv_feuille = abd (arbre.etiquette)
                    noeuds.append (nouv_feuille)
                    return nouv_feuille 
                return feuille
            noeud = trouver (arbre.etiquette, noeuds)
            if not noeud:
                faux = aux (arbre.faux, noeuds)
                vrai = aux (arbre.vrai, noeuds)
                nouv_arbre = abd (arbre.etiquette, faux, vrai)
                noeuds.append (nouv_arbre)
                return nouv_arbre
            return noeud
        
        res = aux (arbre, [])
        renommer (res)
        return res
   
    @staticmethod
    def dot (arbre, fichier):
        """
        Construit un fichier représentant le graphe de l'arbre en langage dot

        Parameters
        ----------
        arbre : abd
            L'arbre à transformer en graphe.
        fichier : string
            Nom du fichier.

        Returns
        -------
        None.

        """
        
        f = open (fichier, "a")
        f.write (str(abd.affiche (arbre)))
        f.close()
    
    @staticmethod
    def compression_bdd (arbre):
        """
        Construit le ROBDD obtenu par compression de l'arbre

        Parameters
        ----------
        arbre : abd
            L'arbre binaire de décision à compresser.

        Returns
        -------
        abd
            Le ROBDD.

        """
        
        
        def trouver (etiquette, noeuds):
            """
            Cherche une étiquette dans une liste de noeuds 

            Parameters
            ----------
            etiquette : string
                La variable qu'on cherche.
            noeuds : list of abd
                La liste de noeuds de l'arbre.

            Returns
            -------
            abd
                Le noeud qui contient l'étiquette recherchée, False sinon.

            """
            
            for noeud in noeuds:
                if noeud.etiquette == etiquette:
                    return noeud
            return False
        
        def extraire_etiquette (etiquette_luka):
            """
            Extrait le nom de la variable d'un noeud à partir de son mot de Lukasiewicz

            Parameters
            ----------
            etiquette_luka : string
                Le mot de Lukasiewicz.

            Returns
            -------
            string
                Le nom de la variable.

            """
            if etiquette_luka [0] == '(':
                i = 1
                while etiquette_luka [i] != '(':
                    i += 1
                return etiquette_luka [1:i]
            return etiquette_luka
        
        def renommer (arbre):
            """
            Renomme chaque noeud de l'arbre par leur variable (modifie l'arbre reçu en paramètre)

            Parameters
            ----------
            arbre : abd
                L'arbre à renommer.

            Returns
            -------
            None.

            """
            if arbre == None:
                return 
            arbre.etiquette = extraire_etiquette (arbre.etiquette)
            renommer (arbre.faux)
            renommer (arbre.vrai)
            
        def est_inutile (fils):
            """
            Retourne le fils unique du noeud s'il existe, False sinon

            Parameters
            ----------
            fils : abd
                Un noeud de l'arbre.

            Returns
            -------
            abd
                Le fils du noeud s'il est unique, False sinon.

            """
            
            if fils.faux == None and fils.vrai == None:
                return False
            if fils.faux == fils.vrai:
                return fils.faux
            return False
                           
        def aux (arbre, noeuds, racine=False):
            """
            Fonction récursive (auxiliaire de compression_bdd())

            Parameters
            ----------
            arbre : abd
                L'arbre binaire de décision à compresser.
            noeuds : list of abd
                La liste des noeuds de l'arbre.
            racine : boolean, optional
                Active le cas particulier de la racine. False par défaut.

            Returns
            -------
            abd
                Le ROBDD.

            """
            
            if arbre == None:
                return None
            if arbre.faux == None and arbre.vrai == None:
                feuille = trouver (arbre.etiquette, noeuds)
                if not feuille:
                    nouv_feuille = abd (arbre.etiquette)
                    noeuds.append (nouv_feuille)
                    return nouv_feuille 
                return feuille
            noeud = trouver (arbre.etiquette, noeuds)
            if not noeud:
                faux = aux (arbre.faux, noeuds)
                vrai = aux (arbre.vrai, noeuds)
                nouv_faux = est_inutile (faux)
                nouv_vrai = est_inutile (vrai)
                if nouv_faux:
                    faux = nouv_faux
                if nouv_vrai:
                    vrai = nouv_vrai                           
                nouv_arbre = abd (arbre.etiquette, faux, vrai)
                if racine and est_inutile(nouv_arbre):
                    return faux 
                noeuds.append (nouv_arbre)
                return nouv_arbre
            return noeud
        
        res = aux (arbre, [], True)
        renommer (res)
        return res
     
    @staticmethod   
    def nb_noeuds (arbre):
        """
        Retourne le nombre de noeuds dans un arbre

        Parameters
        ----------
        arbre : abd
            L'arbre dont il faut compter les noeuds.

        Returns
        -------
        int
            Le nombre de noeuds.

        """
        
        def aux (arbre, noeuds):
            """
            Fonction récursive (auxiliaire de nb_noeuds())

            Parameters
            ----------
            arbre : abd
                L'arbre.
            noeuds : list of abd
                La liste des noeuds de l'arbre déjà rencontrés.

            Returns
            -------
            int
                Le nombre de noeuds.

            """
            
            if arbre == None:
                return 0
            res = 1
            noeuds.add(arbre)
            if not arbre.faux in noeuds:
                res += aux (arbre.faux, noeuds)
            if not arbre.vrai in noeuds:
                res += aux (arbre.vrai, noeuds)
            return res
        return aux (arbre, set())
    
    
    @staticmethod
    def fusion_ROBDD (arbre1, arbre2):
        """
        Fusionne deux ROBDD

        Parameters
        ----------
        arbre1 : abd
            1er ROBDD.
        arbre2 : abd
            2ème ROBDD.

        Returns
        -------
        abd
            la fusion des deux ROBDD.

        """
        
        diamant = u"\u25C7" 
        
        def comparer_arbres (arbre1, arbre2):
            """
            Test d'égalité de deux arbres selon l'étiquette et les enfants 

            Parameters
            ----------
            arbre1 : abd
                1er arbre.
            arbre2 : abd
                2ème arbre.

            Returns
            -------
            bool
                True si les deux arbres sont égaux, False sinon.

            """
            
            if arbre1.etiquette == arbre2.etiquette and arbre1.faux == arbre2.faux and arbre1.vrai == arbre1.vrai:
                return True
            return False
        
        def arbre_deja_present (arbre, noeuds):
            """
            Détermine si un noeud a déjà été traité lors du parcours d'une autre branche

            Parameters
            ----------
            arbre : abd
                arbre.
            noeuds : list of abd
                La liste des noeuds déjà traités.

            Returns
            -------
            abd
                Le noeud trouvé dans la liste, False sinon.

            """
            
            for noeud in noeuds:
                if comparer_arbres (arbre, noeud):
                    return noeud
            return False
        
        def comparer_etiquettes (etiquette1, etiquette2):
            """
            Compare la longueur de deux étiquettes

            Parameters
            ----------
            etiquette1 : string
                la 1ère étiquette.
            etiquette2 : string
                La 2ème étiquette.

            Returns
            -------
            int
                0 si les deux étiquettes ont la même longueur,
                1 si l'étiquette 1 est plus grande que l'étiquette 2,
                -1 sinon
                

            """
            
            e1 = etiquette1.split (diamant) [0]
            e2 = etiquette2.split (diamant) [0]
            if e1 == e2:
                return 0
            if e1 > e2:
                return 1
            return -1
        
        def equilibrer_etiquettes (etiquette1, etiquette2):
            """
            Equilibre la taille des étiquettes. 
            Hyp : etiquette1 > etiquette2

            Parameters
            ----------
            etiquette1 : string
                1ère étiquette.
            etiquette2 : string
                2ème étiquette.

            Returns
            -------
            etiquette2 : string
                L'étiquette2 remontée à une taille égale à celle d'étiquette1.

            """
            
            taille = len (etiquette1)
            
            while len (etiquette2) < taille:
                etiquette2 += etiquette2
            return etiquette2
        
        def table_feuille (feuille):
            """
            Renomme une feuille True/False en "1"/"0"

            Parameters
            ----------
            feuille : abd
                une feuille.

            Returns
            -------
            string
                "0" si False, "1" sinon.
            string
                "0" si False, "1" sinon.

            """
            
            if feuille.etiquette [0] == "0" or feuille.etiquette [0] == "1":
                valeurs = feuille.etiquette.split ("\n")
                return (valeurs [0], valeurs[1])
            valeurs = feuille.etiquette.split (diamant)
            if valeurs [0] == "True":
                v0 = "1"
            else:
                v0 = "0"
            if valeurs [1] == "True":
                v1 = "1"
            else:
                v1 = "0"
            return (v0, v1)
        
        def renommer_binaire (arbre):
            """
            Renomme les noeuds de l'arbre en binaire.
            (Modifie l'arbre reçu en argument)

            Parameters
            ----------
            arbre : abd
                ROBDD.

            Returns
            -------
            v0 : string
                le nombre binaire issu du sous-arbre faux.
            v1 : string
                Le nombre binaire remonté du sous-arbre vrai.

            """
            
            arbreestFeuille = (arbre.faux == None and arbre.vrai == None)
            if arbreestFeuille:
                v0, v1 = table_feuille (arbre)
                arbre.etiquette = v0 + "\n" + v1
                return (v0, v1)
            else:
                v00, v01 = renommer_binaire (arbre.faux) 
                v10, v11 = renommer_binaire (arbre.vrai)
                taille_v00 = len (v00)
                taille_v10 = len (v10)
                if taille_v00 > taille_v10:
                    v10 = equilibrer_etiquettes (v00, v10)
                    v11 = equilibrer_etiquettes (v01, v11)
                if taille_v00 < taille_v10:
                    v00 = equilibrer_etiquettes (v10, v00)
                    v01 = equilibrer_etiquettes (v11, v01)       
                v0 = v00 + v10
                v1 = v01 + v11
                arbre.etiquette = v0 + "\n" + v1
                return (v0, v1)
        
        def aux (arbre1, arbre2, noeuds):
            """
            Fonction récursive (auxiliaire de fusion_ROBDD())

            Parameters
            ----------
            arbre1 : abd
                1er ROBDD.
            arbre2 : abd
                2ème ROBDD.
            noeuds : list of abd
                La liste des noeuds déjà rencontrés.

            Returns
            -------
            abd
                L'arbre fusion de arbre1 et arbre2.

            """
             
            arbre1estFeuille = arbre1.faux == None and arbre1.vrai == None
            arbre2estFeuille = arbre2.faux == None and arbre2.vrai == None
            
            comparaison = comparer_etiquettes (arbre1.etiquette, arbre2.etiquette)
            
            if  arbre1estFeuille and arbre2estFeuille :
                etiquette = arbre1.etiquette + diamant + arbre2.etiquette
                arbre = abd (etiquette)
                
            
            elif arbre1estFeuille:
                etiquette = arbre1.etiquette + diamant + arbre2.etiquette
                arbre = abd(etiquette, aux(arbre1, arbre2.faux, noeuds), aux (arbre1, arbre2.vrai, noeuds))
                
            
            elif arbre2estFeuille:
                etiquette = arbre1.etiquette + diamant + arbre2.etiquette
                arbre =  abd(etiquette, aux(arbre1.faux, arbre2, noeuds), aux(arbre1.vrai, arbre2, noeuds))
            
            elif comparaison == 0:
                etiquette = arbre1.etiquette
                arbre = abd (etiquette, aux (arbre1.faux, arbre2.faux, noeuds), aux (arbre1.vrai, arbre2.vrai, noeuds))
            
            elif comparaison == 1:
                etiquette = arbre1.etiquette
                arbre = abd (etiquette, aux (arbre1.faux, arbre2, noeuds), aux (arbre1.vrai, arbre2, noeuds))
            else:
                etiquette = arbre2.etiquette
                arbre = abd (etiquette, aux (arbre1, arbre2.faux, noeuds), aux (arbre1, arbre2.vrai, noeuds))
            
            noeud = arbre_deja_present (arbre, noeuds)
            if not noeud:
                noeuds.add (arbre)
                return arbre
            return noeud
            
           
        res = aux (arbre1, arbre2, set())
        renommer_binaire(res)
        return res
    
    @staticmethod
    def simplification_et_reduction_ROBDD (arbre, op):
        """
        Phases de simplification et réduction de ROBDD

        Parameters
        ----------
        arbre : abd
            ROBDD.
        op : fonction
            L'opérateur (prenant deux binaires sous forme de string).

        Returns
        -------
        abd
            Le ROBDD final.

        """
        
        diamant = u"\u25C7" 
        

        
        def renommer_variables (arbre, noeuds=set()):
            """
            Renomme les noeuds de l'arbre avec les variables.
            (Modifie l'arbre reçu en argument)

            Parameters
            ----------
            arbre : abd
                ROBDD.
            noeuds : list of abd, optional
                La liste des noeuds déjà traités. set() par défaut.

            Returns
            -------
            None.

            """
            
            if arbre == None or arbre in noeuds:
                return
            taille_etiquette = len (arbre.etiquette)
            if taille_etiquette == 1:
                if arbre.etiquette == "0":
                    arbre.etiquette = "False"
                else:
                    arbre.etiquette = "True"
                noeuds.add (arbre)
                return 
            i = int (math.log2 (taille_etiquette))
            arbre.etiquette = "x" + str (i)
            noeuds.add (arbre)
            renommer_variables (arbre.faux, noeuds)
            renommer_variables (arbre.vrai, noeuds)
            return
            
        def trouver (etiquette, noeuds):
            """
            Cherche une étiquette dans une liste de noeuds 

            Parameters
            ----------
            etiquette : string
                La variable qu'on cherche.
            noeuds : list of abd
                La liste de noeuds de l'arbre.

            Returns
            -------
            abd
                Le noeud qui contient l'étiquette recherchée, False sinon.

            """
            
            for noeud in noeuds:
                if noeud.etiquette == etiquette:
                    return noeud
            return False
        
        def est_inutile (fils):
            """
            Retourne le fils unique du noeud s'il existe, False sinon

            Parameters
            ----------
            fils : abd
                Un noeud de l'arbre.

            Returns
            -------
            abd
                Le fils du noeud s'il est unique, False sinon.

            """
            
            if fils.faux == None and fils.vrai == None:
                return False
            if fils.faux == fils.vrai:
                return fils.faux
            return False
        
        def aux (arbre, noeuds, racine=False):
            """
            Fonction récursive (auxiliaire de simplification_et_reduction_ROBDD())

            Parameters
            ----------
            arbre : abd
                ROBDD.
            noeuds : list of abd
                La liste des noeuds déjà traités.
            racine : bool, optional
                Indique si on traite la racine. False par défaut.

            Returns
            -------
            TYPE
                Retourne le ROBDD final ayant été fusionné simplifié et réduit.

            """
            
            arbreestFeuille = arbre.faux == None and arbre.vrai == None
            operandes = arbre.etiquette.split ("\n")
            etiquette = op (operandes [0], operandes [1])
            if arbreestFeuille:
                noeud = trouver (etiquette, noeuds)
                if not noeud:
                    arbre = abd (etiquette)
                    noeuds.add (arbre)
                    return arbre
                return noeud
            
            noeud = trouver (etiquette, noeuds)
            if not noeud:
                faux = aux (arbre.faux, noeuds)
                vrai = aux (arbre.vrai, noeuds)
                nouv_faux = est_inutile (faux)
                nouv_vrai = est_inutile (vrai)
                if nouv_faux:
                    faux = nouv_faux
                if nouv_vrai:
                    vrai = nouv_vrai
                arbre = abd (etiquette, faux, vrai)
                if racine and est_inutile(arbre):
                    return faux 
                noeuds.add (arbre)
                return arbre
            return noeud
            
        res = aux (arbre, set(), True)
        renommer_variables (res)
        return res
        
def et (table1, table2):
    """
    Opérateur booléen.

    Parameters
    ----------
    table1 : string
        la 1ère table.
    table2 : string
        La 2ème table.

    Returns
    -------
    res : string
        La table résultat.

    """
    
    res = ""
    for i in range (len(table1)):
        if table1 [i] == "1" and table2 [i] == "1":
            res += "1"
        else:
            res += "0"
    return res
        
arbre = abd.cons_arbre(table(61152,16))  
arbre2 = abd.luka(arbre)
arbre3 = abd.compression_bdd(arbre2)  

arbre4 = abd.cons_arbre(table(28662,16))  
arbre5 = abd.luka(arbre4)
arbre6 = abd.compression_bdd(arbre5)  

fusion3_6 = abd.fusion_ROBDD (arbre3, arbre6)
fusion3_6_bdd = abd.simplification_et_reduction_ROBDD(fusion3_6, et)
        
         

                
"""arbre = abd.cons_arbre(table(38,8))  
arbre2 = abd.luka(arbre)
arbre3 = abd.compression(arbre2)
arbre4 = abd.compression_bdd(arbre2)"""


        