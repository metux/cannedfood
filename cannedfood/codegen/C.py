from cannedfood import util

"""generate an enum"""
class RenderEnum:
    def __init__(self, enum_name, value_prefix = None):
        self.values = {}
        self.enum_name = enum_name
        self.value_prefix = value_prefix

    def add(self, ident, value):
        self.values[ident] = value

    def _render_key(self, k):
        return self.value_prefix+k

    def _render_val(self, v):
        return str(v)

    def tostr(self):
        s = "enum "+self.enum_name+" {\n"
        for k,v in self.values.iteritems():
            s+="    "+self._render_key(k)+" = "+self._render_val(v)+",\n"
        s+="};\n"
        return s

    def __str__(self):
        return self.tostr()

"""generate a header or source file"""
class RenderSource:
    def __init__(self, guard = None, use_types = []):
        self.t = 0
        self.includes = {}
        self.content = ""
        self.guard = guard
        self.use_types(use_types)

    def add_include(self, inc, patterns = {}):
        if inc is not None:
            i = util.replace_list(inc, patterns)
            self.includes[i] = i

    def add_includes(self, inc, patterns = {}):
        for i in inc:
            self.add_include(i, patterns)

    def write(self, content):
        self.content += content

    def writeln(self, content = ""):
        self.content += content+"\n"

    def __add_guard(self, s):
        if self.guard is None:
            return s

        return "#ifndef "+self.guard+"\n#define "+self.guard+"\n\n"+s+"\n#endif /* "+self.guard+" */\n"

    """ add prerequisites of given typespec"""
    def use_type(self, typespec):
        if typespec is not None:
            if 'C.include' in typespec:
                self.add_include(typespec['C.include'])

    """add a list of types to be used"""
    def use_types(self, types):
        for t in types:
            self.use_type(t)

    """add a comment"""
    def comment(self, text):
        self.write("\n/* "+text+"*/\n")

    """render into a string"""
    def tostr(self):
        s = "/* === AUTO GENERATED === */\n\n"

        for i in self.includes:
            s += "#include "+i+"\n"

        s += "\n"+self.content

        return self.__add_guard(s)

    """convert to string"""
    def __str__(self):
        return self.tostr()
