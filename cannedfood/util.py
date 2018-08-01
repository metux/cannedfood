import os

def attr_dict(d, n):
    if n in d:
        return d[n]
    else:
        return {}

def attr_list(d, n):
    if n in d:
        return d[n]
    else:
        return []

def attr_int_def(d, n, df):
    if n in d:
        return d[n]
    else:
        return df

def merge_lists(a, b):
    if a is None:
        a = []
    if b is None:
        b = []
    return list(set(a+b))

def replace_list(s, patterns):
    for p in patterns:
        s = s.replace(p, patterns[p])
    return s

import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def create_file_path(fn):
    return mkdir_p(os.path.dirname(fn))
