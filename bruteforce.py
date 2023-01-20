from itertools import combinations
from tqdm import tqdm
import time
import csv

all_int = dict()
MAX_PRICE = 500
ROOT_CSV = "csv/bruteforce.csv"
# ROOT_CSV = "csv/file1.csv"
# ROOT_CSV = "csv/file2.csv"


def get_action_list():
    all_action_list = []
    with open(ROOT_CSV, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["name"]
            price = float(row["price"])
            profit = float(row["profit"])
            gain = (price * profit) / 100
            action = {
                "name": name,
                "price": price,
                "profit": profit,
                "gain": gain,
            }
            all_action_list.append(action)
    return all_action_list


def get_best_wallet_from_all_combination(all_combination):
    best_wallet = {"sum_gain": 0, "sum_wallet": 0, "wallet": ""}
    total_combination = 0
    for wallet_list in tqdm(all_combination):
        for action_list in wallet_list:
            total_combination += 1
            sum_wallet = 0
            sum_gain = 0
            for action in action_list:
                sum_wallet += action.get('price')
                sum_gain += round(action.get('gain'), 2)

            if (best_wallet.get('sum_gain') < sum_gain) and (sum_wallet <= MAX_PRICE):
                best_wallet['sum_gain'] = round(sum_gain, 2)
                best_wallet['sum_wallet'] = sum_wallet
                wallet = get_list_action_name(action_list)
                best_wallet['wallet'] = wallet

    all_int["Nombre total de combinaison"] = total_combination
    return best_wallet


def get_list_action_name(list_action):
    list_action_name = ""
    for action in list_action:
        if list_action_name == "":
            list_action_name += action.get("name")
        else:
            list_action_name += ", " + action.get("name")
    return list_action_name


def main():
    start_time = time.time()
    all_action = get_action_list()
    all_int["Recuperation des actions"] = round((time.time() - start_time), 2)

    all_combination = []
    for compteur in range(1, len(all_action) + 1):
        all_combination.append(combinations(all_action, compteur))
    all_int["Generation des combinaisons"] = round((time.time() - start_time), 2)

    best_wallet = get_best_wallet_from_all_combination(all_combination)

    all_int["Recuperation du meilleur wallet"] = round((time.time() - start_time), 2)
    all_int["Montant investit"] = best_wallet.get('sum_wallet')
    all_int["Gains après 2 ans"] = best_wallet.get('sum_gain')
    all_int["La liste des actions est"] = best_wallet.get('wallet')
    all_int["Temps total d'exécution"] = round((time.time() - start_time), 2)

    for k, v in all_int.items():
        print(f"{k} : {v}")

    # 100%|██████████| 20/20 [00:06<00:00,  2.94it/s]
    # Recuperation des actions : 0.0
    # Generation des combinaisons : 0.0
    # Nombre total de combinaison : 1048575
    # Recuperation du meilleur wallet : 6.85
    # Montant investit : 498.1
    # Gains des actions après 2 ans : 198.54 €
    # Gains après 2 ans : 99.21
    # La liste des actions est : Action-4, Action-5, Action-6, Action-8,
    # Action-10, Action-11, Action-13, Action-18, Action-19, Action-20
    # Temps total d'exécution : 6.85


if __name__ == '__main__':
    main()
