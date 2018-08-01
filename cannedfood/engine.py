
import spec

from cangen import C

def run_all(fn):
    cf = spec.load_config(fn)
    errs = cf.check_node_messages()
    if (errs > 0):
        return errs
    gen = C.generator(cf, "c.default")
    gen.generate_all()
    return 0
