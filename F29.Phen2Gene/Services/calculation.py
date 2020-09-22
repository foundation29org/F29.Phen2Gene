from Phen2Gene.calculation import calc
from Phen2Gene.prioritize import gene_prioritization
from Phen2Gene.weight_assignment import assign

def calculate(kbpath, hpos, weight_model='sk', normalize=True, rows=100):
    hp_weight_dict = {}
    for hp in hpos:
        if hp and hp.find(':') > -1:
            hp = hp.replace(':', '_').strip()
            (weight, replaced_by) = assign(kbpath, hp, weight_model)
            if(weight > 0):
                if(replaced_by != None):
                    hp_weight_dict[replaced_by] = weight
                else:
                    hp_weight_dict[hp] = weight

    gene_dict = calc(kbpath, hp_weight_dict, verbosity=False, gene_weight=None, cutoff=None)
    gene_dict = gene_prioritization(gene_dict)

    dic = {}
    if len(gene_dict) > 0:
        factor = 1
        if normalize:
            first = next(iter(gene_dict.values()))
            factor = first[1]
        for n, key in enumerate(gene_dict):
            if n >= rows: break
            gene, score, status, _, id = gene_dict[key]
            score = score / factor
            item = {
                    'rank': n + 1,
                    'id': id,
                    'score': round(score, 4),
                    'status': status,
                }
            dic[gene] = item
    return dic
