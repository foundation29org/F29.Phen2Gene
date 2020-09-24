import os

from .calculation import calc
from .prioritize import gene_prioritization
from .weight_assignment import assign

class Phen2Gene():
    def __init__(self, path):
        self.path = path
        self.hpos = self._load_hpos()
        self.obsoletes = self._load_obsoletes()

    '''
        Load
    '''
    def _load_hpos(self):
        hash = set()
        path_weights = os.path.join(self.path, 'weights')
        for fn in os.listdir(path_weights):
            id = fn.strip().upper().replace('_', ':')
            if id.startswith('HP:'):
                hash.add(id)
        return list(hash)

    def _load_obsoletes(self):
        dic = {}
        path_outdated = os.path.join(self.path, 'outdated_HP')
        for fn in os.listdir(path_outdated):
            id = fn.strip().upper().replace('_', ':')
            if id.startswith('HP:'):
                dic[id] = self._read_obsolete(path_outdated, fn)
        return dic

    def _read_obsolete(self, path, fn):
        with open(os.path.join(path, fn), 'r') as fp:
            data = fp.read().split("\n")
        replaced_by = data[1].strip().upper().replace('_', ':')
        consider = [a.strip().upper().replace('_', ':') for a in data[2].split(',') if a]
        return {
                'id': fn.strip().upper().replace('_', ':'),
                'replaced_by': replaced_by,
                'consider': consider
            }

    '''
        Validate
    '''
    def validate(self, hpos):
        dic = {}
        hpos = self._ensure_upper_list(hpos)
        for hpo in hpos:
            if hpo:
                dic[hpo] = self.validate_hpo(hpo)
        return dic
        
    def validate_hpo(self, hpo):
        if hpo:
            hpo = hpo.strip()
            id = hpo.upper().replace('_', ':')
            if len(id) == 10:
                if id.startswith('HP:'):
                    if id in self.hpos:
                        return { 'id': id, 'status': 'ok' }
                    if id in self.obsoletes:
                        obs = self.obsoletes[id]
                        replaced_by = obs['replaced_by']
                        consider = obs['consider']
                        return {
                                'id': id,
                                'status': 'obsolete',
                                'replaced_by': self._replace_hpo(replaced_by),
                                'consider': [hp for hp in [self._replace_hpo(a) for a in consider] if hp]
                            }
                    return  { 'id': id, 'status': 'unknown' }
            return  { 'id': hpo, 'status': 'invalid' }
        return None

    def _replace_hpo(self, hpo):
        if hpo and len(hpo) == 10:
            id = hpo.upper().replace('_', ':')
            if id in self.hpos:
                return id
            if id in self.obsoletes:
                rid = self.obsoletes[id]['replaced_by']
                return self._replace_hpo(rid)
        return None

    '''
        Query
    '''
    def build_query(self, hpos):
        validations = self.validate(hpos)
        for id in validations:
            term = validations[id]
            status = term['status']
            if status == 'invalid': term['target'] = None
            if status == 'unknown': term['target'] = None
            if status == 'ok': term['target'] = [term['id']]
            if status == 'obsolete':
                rep_id = term['replaced_by']
                if rep_id:
                    term['target'] = [rep_id]
                elif len(term['consider']) > 0:
                    cons_ids = term['consider']
                    term['target'] = cons_ids
                else:
                    term['target'] = None
        return validations

    '''
        Calculate
    '''
    def calculate(self, hpos, weight_model='sk', normalize=True, rows=100):
        hpos = self._ensure_upper_list(hpos)
        hp_weight_dict = {}
        for hp in hpos:
            if hp and hp.find(':') > -1:
                hp = hp.replace(':', '_').strip()
                (weight, replaced_by) = assign(self.path, hp, weight_model)
                if(weight > 0):
                    if(replaced_by != None):
                        hp_weight_dict[replaced_by] = weight
                    else:
                        hp_weight_dict[hp] = weight

        gene_dict = calc(self.path, hp_weight_dict, verbosity=False, gene_weight=None, cutoff=None)
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

    '''
        Helpers
    '''
    def _ensure_upper_list(self, ids):
        if not type(ids) is list: ids = [ids]
        ids = [id.upper() for id in ids if id]
        ids = list(dict.fromkeys(ids))
        return ids
