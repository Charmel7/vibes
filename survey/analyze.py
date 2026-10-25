"""Compte les réponses d'un export CSV Google Forms. Aucune donnée n'est inventée :
le script affiche seulement n et les effectifs par réponse."""
import csv, sys
from collections import Counter

def main(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        sys.exit("Aucune réponse dans le fichier.")
    head, data = rows[0], rows[1:]
    print(f"n = {len(data)} réponses\n")
    for i, col in enumerate(head):
        if i == 0 and 'horodat' in col.lower():
            continue
        vals = [r[i].strip() for r in data if i < len(r) and r[i].strip()]
        if not vals:
            continue
        print(col[:90])
        free = len(set(vals)) > 0.8 * len(vals) and len(vals) > 8
        if free:
            print(f"  ({len(vals)} réponses libres, à lire à la main)\n")
            continue
        c = Counter()
        for v in vals:
            for part in [p.strip() for p in v.split(', ')]:
                c[part] += 1
        for k, v in c.most_common():
            print(f"  {v:>3}  {100*v/len(vals):4.0f} %  {k}")
        print(f"  (base : {len(vals)} répondants)\n")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage : python3 survey/analyze.py reponses.csv")
    main(sys.argv[1])
