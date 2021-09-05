"""
Skeleton file for the project 1 of the LINGI2364 course.
Use this as your submission file. Every piece of code that is used in your program should be put inside this file.

This file given to you as a skeleton for your implementation of the Apriori and Depth
First Search algorithms. You are not obligated to use them and are free to write any class or method as long as the
following requirements are respected:

Your apriori and alternativeMiner methods must take as parameters a string corresponding to the path to a valid
dataset file and a double corresponding to the minimum frequency.
You must write on the standard output (use the print() method) all the itemsets that are frequent in the dataset file
according to the minimum frequency given. Each itemset has to be printed on one line following the format:
[<item 1>, <item 2>, ... <item k>] (<frequency>).
Tip: you can use Arrays.toString(int[] a) to print an itemset.

The items in an itemset must be printed in lexicographical order. However, the itemsets themselves can be printed in
any order.

Do not change the signature of the apriori and alternative_miner methods as they will be called by the test script.

__authors__ = "<Antoine Geller and Trudel Nguepi>"
"""

import time

class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()

        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(int, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(item)
        except IOError as e:
            print("Unable to read dataset file!\n" + e)

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return len(self.transactions)

    def items_num(self):
        """Returns the number of different items in the dataset"""
        return len(self.items)

    def get_transaction(self, i):
        """Returns the transaction at index i as an int array"""
        return self.transactions[i]


def apriori(filepath, minFrequency):
    """Runs the apriori algorithm on the specified file with the given minimum frequency"""
    transactions = {}
    dataset = Dataset(filepath)
    for i in range(dataset.trans_num()):  # Create a dictionnary with the transactions
        key = tuple(dataset.get_transaction(i))
        if key in transactions:
            transactions[key] += 1
        else:
            transactions[key] = 1
    number_of_transactions = sum(transactions.values())  # Retrieve the number of transactions
    items = get_items_stage1(dataset,
                             number_of_transactions)  # Retrieve the items sets with one items and their frequencies {[1]: 0.5, [2]: 0.125,...}
    frequent_items = {keys: value for keys, value in items.items() if
                      value >= minFrequency}  # Retrieve the frequent items out of the items above
    for k, v in frequent_items.items():
        print(str(list(k)) + " " + "(" + str(v) + ")")  # Print the frequent items from frequent_items dictionary
    for i in range(1, dataset.items_num()):  # For loop to generate each item set that increase of 1 item each iteration
        items = get_items_stage2(frequent_items, transactions, number_of_transactions,
                                 i + 1)  # Generate the item sets with their frequencies from the frequent items in level i-1
        frequent_items = {keys: value for keys, value in items.items() if
                          value >= minFrequency}  # Retrieve the frequent items for the items generated above and the frequencies.
        for k, v in frequent_items.items():
            print(str(list(k)) + " " + "(" + str(v) + ")")  # Print the frequent items from frequent_items dictionary
    time.sleep(1)


def get_items_stage1(dataset, number_of_transactions):
    """
    Function used only once to return the items and the frequencies at level one where each item set is composed of only
    one item.
    :param dataset: dataset of transactions
    :param number_of_transactions: the number of transactions in the dataset
    :return: A dictionary with the item as key and frequency as values
    """
    items_counts = {}
    for i in range(dataset.trans_num()):
        key = list(dataset.get_transaction(i))
        for j in range(len(key)):  # Retrieve the item
            key_final = tuple(sorted(([key[j]])))
            if key_final in items_counts:  # either initialize the item in dictionary or add one to the count
                items_counts[key_final] += 1
            else:
                items_counts[key_final] = 1
    items_counts = {k: value / number_of_transactions for k, value in items_counts.items()}
    return items_counts


def get_items_stage2(items, transactions, number_of_transactions, i):
    """
    Function used to generate the item sets of size 2 until the maximum size.
    :param items: A dictionary of the item sets of level i-1
    :param transactions: A dictionary of the transactions in the dataset
    :param number_of_transactions: the total number of transactions in the dataset
    :param i: the size of the item sets to generate
    :return: A dictionary of items and their frequencies
    """
    items_returned = {}
    
    return items_returned


def alternative_miner(filepath, minFrequency):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
    data = Dataset(filepath)
    n = data.trans_num()  # calcul du nombre de transaction de la database
    vertical = vertical_rep(data)  # fait une représentation verticale de la database
    # qui sera utilisé par ECLAT
    # on récupère tous les items de la database
    all_items = list(vertical.keys())
    FP = []
    # cette boucle permet de calculer les items les plus fréquents individuellement
    # ie qu'on est au premier niveau de l'arbre. Ces éléments là sont ensuite
    # données à ECLAT qui va continuer à descendre dans l'arbre
    for i in all_items:
        freq = len(vertical[i]) / n
        if freq >= minFrequency:
            print(str([i]) + " " + "(" + str((freq)) + ")")
            FP.append([i])
    ECLAT(FP, minFrequency, n, vertical)


def vertical_rep(data):
    '''permet de donner une représentation vertical de la base de données
    pré: data est une instance de la classe Dataset
    post: retourne un dictionnaire dont les clés sont les items et les valeurs sont transactions
          correspondante stocké dans des listes
    '''
    result = {}
    transaction = []
    for i in range(data.trans_num()):  # pour chaque transaction
        # on l'associe les items correspondants à cette transaction
        for item in data.transactions[i]:
            result.setdefault(item, []).append(i)
    return result


def projection(vertical_data, item_list):
    '''calcul la couverture de d'une liste d'items
      pré:
           vertical_data: représentation verticale de la database retournée par la fonction
           vertical_rep
           item_list: est une liste ordonnée et sans répétitions d'items (ordre croissant)
      post: retourne une liste qui représente la couverture de item_list
    '''

    first = item_list[0]
    # on stock les transactions du premier élément de la liste
    intersec = vertical_data[first]
    # on fait l'intersection avec tous les éléments suivant de item_list
    for i in range(1, len(item_list)):
        succ = item_list[i]
        # permet de faire l'intersection de 2 listes
        intersec = list(set(intersec) & set(vertical_data[succ]))
    return intersec


def ECLAT(FP, minFrequency, n, rep_vertical):
    ''' implémente l'algorithme ECLAT du Depth-First Search
       pré:
           FP: est une liste de liste où seul les derniers éléments de chaque liste diffèrent.
               De plus ces derniers éléments sont ordonnés par ordre croissant.
               Exemple: FP= [[1,3,5],[1,3,6],[1,3,7]]
            minFrequency: float correspondant à la fréquence minimale qu'un itemet doit avoir pour
                          être considéré comme fréquent.
            n: int correspondant au nombre total de transaction dans la database
            rep_vertical: représentation verticale de la database retournée par la fonction
                          vertical_rep
       post: affiche la liste des items fréquents avec leurs fréquences
    '''
    # l'idée consiste à chaque fois prendre une liste d'item et de rajouter
    # les éléments possibles qui peuvent suivre son dernier élément pour rendre
    # la nouvelle liste frequente et ainsi passer à un niveau supérieur

    for Pi in FP:
        # on calcul la couverture de la liste des premiers éléments de Pi losque
        # len(Pi)!=1
        # on retire le dernier élément pour ce calcul. On fait ceci car les
        # les items qui seront ajoutés à la suite auront les mêmes premiers
        # que Pi
        if len(Pi) != 1:
            cover_Pi_1 = set(projection(rep_vertical, Pi[:-1]))  # cover de premier elt sauf le dernier
        else:
            cover_Pi_1 = set(projection(rep_vertical, Pi))
        # calcul de la couverture du dernier élément de Pi
        cover_last_i = set(projection(rep_vertical, [Pi[len(Pi) - 1]]))

        FPi = []
        # pour la liste d'items Pi on va rajouter un item tel que le dernier
        # élément depasse le dernier élément de Pi
        for Pj in FP:
            if Pj[len(Pj) - 1] > Pi[len(Pi) - 1]:  # on prend les items qui suivent Pi
                Pij = list(set(Pi) | set(Pj))  # on fait l'union ce qui permet de passer
                # à un niveau supérieur
                # on calcul la couverture du dernier élément de la liste Pj
                # car on sait que ses premiers éléments sont identiques à ceux
                # de Pi et dont la couverture à déjà été calculé
                cover_last_j = set(projection(rep_vertical, [Pj[len(Pj) - 1]]))
                # ici on calcul la couverture de Pij comme intersection
                # des couvertures de Pi et Pj
                cover_Pij = list(cover_Pi_1 & cover_last_i & cover_last_j)

                supp_Pij = len(cover_Pij)
                freq_Pij = supp_Pij / n  # calcul de la fréquence

                if freq_Pij >= minFrequency:  # détermine la liste d'items est fréquent
                    Pij = sorted(Pij)
                    FPi.append(Pij)  # on rajoute à FPi donc ont est passé à un niveau supérieur
                    print(str(sorted(Pij)) + " " + "(" + str((freq_Pij)) + ")")
            # on recommence le processus
        ECLAT(FPi, minFrequency, n, rep_vertical)
