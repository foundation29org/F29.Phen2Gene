import os

PATH_TESTS_ASSETS = '_tests_assets'
PATH_TESTS_MISMATCH = '_tests_mismatch'

import json
import pickle

def load_object(fn):
    with open(fn, 'rb') as fp:
        return pickle.load(fp)

def save_object(obj, fn, protocol=pickle.HIGHEST_PROTOCOL):
    with open(fn, 'wb') as fp:
        pickle.dump(obj, fp)

def load_object_json(fn):
    with open(fn, 'r') as fp:
        return json.load(fp)

def save_object_json(obj, fn):
    with open(fn, 'w') as fp:
        json.dump(obj, fp, indent=2)

def prettify(obj):
    return json.dumps(obj, indent=2)

def pf(obj): return prettify(obj)

def ppf(obj): print(pf(obj))

def deep_equal(_v1, _v2):
    import operator, types
    def _deep_dict_eq(d1, d2):
        if d1 is None and d2 is None: return True
        if d1 is None and (not d2 is None): return False
        if (not d1 is None) and d2 is None: return False

        k1 = sorted(d1.keys())
        k2 = sorted(d2.keys())
        if k1 != k2: # keys should be exactly equal
            return False
        return sum(deep_equal(d1[k], d2[k]) for k in k1) == len(k1)
    
    def _deep_iter_eq(l1, l2):
        if len(l1) != len(l2):
            return False
        return sum(deep_equal(v1, v2) for v1, v2 in zip(l1, l2)) == len(l1)
    
    op = operator.eq
    c1, c2 = (_v1, _v2)
    
    for t in [str]:
        if isinstance(_v1, t):
            break
    else:
        if isinstance(_v1, dict):
            op = _deep_dict_eq
        else:
            try:
                c1, c2 = (list(iter(_v1)), list(iter(_v2)))
            except TypeError:
                c1, c2 = _v1, _v2
            else:
                op = _deep_iter_eq
    
    return op(c1, c2)

def ensure_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def file_equal(folder, obj, name):
    fn = os.path.join(PATH_TESTS_ASSETS, folder, name)
    ensure_path(os.path.join(PATH_TESTS_ASSETS, folder))
    if not os.path.isfile(fn):
        save_object_json(obj, fn)
    obj1 = json.loads(json.dumps(obj))
    obj2 = load_object_json(fn)
    if not deep_equal(obj1, obj2):
        fn = os.path.join(PATH_TESTS_MISMATCH, folder, name)
        ensure_path(os.path.join(PATH_TESTS_MISMATCH, folder))
        save_object_json(obj, fn)
        return False
    return True
