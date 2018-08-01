
class TypeMap:
    def __init__(self, spec = {}):
        self.spec = spec

    def lookup(self, typename):
        if typename not in self.spec:
            raise Exception("type \""+typename+"\" not defined in typemap")
        return self.spec[typename]

    def add(self, name, ent):
        ent['name'] = name
        self.spec[name] = ent

    def add_dict(self, yamlobj):
        for n in yamlobj:
            self.add(n, yamlobj[n])
