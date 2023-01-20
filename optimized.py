from tqdm import tqdm
import time
import csv

all_int = dict()
# On fait x100 pour ne pas avoir de float avec les centimes
MAX_PRICE = 500 * 100
# ROOT_CSV = "csv/bruteforce.csv"
# ROOT_CSV = "csv/file1.csv"
ROOT_CSV = "csv/file2.csv"


def get_action_list():
    all_action_list = []
    with open(ROOT_CSV, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["name"]
            # On ne prend pas en compte les lignes avec des valeurs a 0 ou négative
            if float(row["price"]) <= 0:
                continue
            # Pour éviter les float, on multiplie par 100
            price = int(float(row["price"]) * 100)
            profit = int(float(row["profit"]) * 100)
            gain = round((price * profit) / (100 * 100 * 100), 2)
            action = (name, price, gain)
            all_action_list.append(action)
    return all_action_list


def get_list_action_detail(list_action):
    list_action_name = ""
    list_action_price = 0
    for action in list_action:
        if list_action_name == "":
            list_action_name += action[0]
        else:
            list_action_name += ", " + action[0]
        list_action_price += action[1]
    return list_action_name, list_action_price


def get_best_wallet_by_matrice(prix_max, all_action):
    matrice = [[0 for x in range(prix_max + 1)] for x in range(len(all_action) + 1)]
    for i in tqdm(range(1, len(all_action) + 1)):
        for w in range(1, prix_max + 1):
            if all_action[i - 1][1] <= w:
                # On prend le max entre notre valeur + la valeur du reste ou notre valeur
                matrice[i][w] = max(all_action[i - 1][2] + matrice[i - 1][w - all_action[i - 1][1]], matrice[i - 1][w])
            else:
                matrice[i][w] = matrice[i - 1][w]

    w = prix_max
    n = len(all_action)
    best_wallet = []

    while w >= 0 and n >= 0:
        list_action = all_action[n - 1]
        if matrice[n][w] == matrice[n - 1][w - list_action[1]] + list_action[2]:
            best_wallet.append(list_action)
            w -= list_action[1]
        n -= 1
    return round(matrice[-1][-1], 2), best_wallet


def main():
    start_time = time.time()

    all_action = get_action_list()
    all_int["Recuperation des actions"] = round((time.time() - start_time), 2)

    best_wallet = get_best_wallet_by_matrice(MAX_PRICE, all_action)
    all_int["Recuperation du meilleur wallet"] = round((time.time() - start_time), 2)

    best_wallet_detail = get_list_action_detail(best_wallet[1])

    all_int["La liste des actions est"] = best_wallet_detail[0]
    # On divise par 100 pour récupérer la valeur en €
    all_int["Montant investit"] = best_wallet_detail[1] / 100
    all_int["Gains des actions après 2 ans"] = best_wallet[0]
    all_int["Gains total après 2 ans"] = round(best_wallet[0] + (best_wallet_detail[1] / 100), 2)
    total_execution_time = round((time.time() - start_time), 2)
    all_int["Temps total d'exécution"] = total_execution_time

    for k, v in all_int.items():
        print(f"{k} : {v}")

    # -------------------Bruteforce-------------------
    # 100%|██████████| 20/20 [00:06<00:00,  2.94it/s]
    # Recuperation des actions : 0.0 sec
    # Generation des combinaisons : 0.0 sec
    # Nombre total de combinaison : 1048575
    # Recuperation du meilleur wallet : 6.85 sec
    # Montant investit : 498.1 €
    # Gains après 2 ans : 99.21 €
    # La liste des actions est : Action-4, Action-5, Action-6, Action-8,
    # Action-10, Action-11, Action-13, Action-18, Action-19, Action-20
    # Temps total d'exécution : 6.85 sec

    # Pour 3 elements (en bruteforce sur file1.csv)
    # Recuperation des actions : 0.0 sec
    # Min combinaison : 1
    # Recuperation Min : 0.0 sec
    # Max combinaison : 148
    # Recuperation Max : 0.0 sec
    # Generation des combinaisons : 0.0 sec
    # Nombre total de combinaison : 166666500
    # Recuperation du meilleur wallet : 348.1 (5.48 minutes)
    # Montant investit : 499.85 €
    # Gains après 2 ans : 197.23 €
    # La liste des actions est : Share-JNGS, Share-QQGZ, Share-GRUT
    # Temps total d'exécution : 348.1 sec (5.48 minutes)

    # -------------------Matrice-------------------
    # Fichier bruteforce.csv
    # 100%|██████████| 20/20 [00:00<00:00, 34.57it/s]
    # Recuperation des actions : 0.0 sec
    # Recuperation du meilleur wallet : 0.65 sec
    # La liste des actions est : Action-20, Action-19, Action-18, Action-13,
    # Action-11, Action-10, Action-8, Action-6, Action-5, Action-4
    # Montant investit : 498.1 €
    # Gains des actions après 2 ans : 99.21 €
    # Temps total d'exécution : 0.65 sec

    # Gains total après 2 ans : 597.31 €


    # Fichier file1.csv
    # 100%|██████████| 957/957 [00:23<00:00, 40.65it/s]
    # Recuperation des actions : 0.0 sec
    # Recuperation du meilleur wallet : 25.42 sec
    # La liste des actions est : Share-KMTG, Share-GHIZ, Share-NHWA, Share-UEZB, Share-LPDM, Share-MTLR, Share-USSR,
    # Share-GTQK, Share-FKJW, Share-MLGM, Share-QLMK, Share-WPLI, Share-LGWG, Share-ZSDE, Share-SKKC, Share-QQTU,
    # Share-GIAJ, Share-XJMO, Share-LRBZ, Share-KZBL, Share-EMOV, Share-IFCP
    # Montant investit : 499.95 €                       /////// Sienna : 498.76 €
    # Gains des actions après 2 ans : 198.54 €          /////// Sienna : 196.61 €
    # Gains total après 2 ans : 698.49 €                /////// Sienna : 695,37 €
    # Temps total d'exécution : 25.42 sec

    # Fichier file2.csv
    # 100%|██████████| 541/541 [00:14<00:00, 37.03it/s]
    # Recuperation des actions : 0.0 sec
    # Recuperation du meilleur wallet : 15.95 sec
    # La liste des actions est : Share-ECAQ, Share-IXCI, Share-FWBE, Share-ZOFA, Share-PLLK, Share-LXZU, Share-YFVZ,
    # Share-ANFX, Share-PATS, Share-SCWM, Share-NDKR, Share-ALIY, Share-JWGF, Share-JGTW, Share-FAPS, Share-VCAX,
    # Share-LFXB, Share-DWSK, Share-XQII, Share-ROOM
    # Montant investit : 499.9 €                        /////// Sienna : 489.24 €
    # Gains des actions après 2 ans : 197.95 €          /////// Sienna : 193.78 €
    # Gains total après 2 ans : 697.85 €                /////// Sienna : 683.02 €
    # Temps total d'exécution : 15.95 sec


if __name__ == '__main__':
    main()
