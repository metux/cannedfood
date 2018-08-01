from cannedfood import util
from cannedfood.codegen.C import RenderSource

class CGenBase:

    def __init__(self, parent, node_name = None):
        self.parent = parent
        self.pattern = {}
        if node_name is not None:
            self.node_name = node_name
            self.node = self.parent.cf.get_node(node_name)
            self.pattern['${NODE_NAME}'] = node_name

    def get_output(self, out_name):
        return self.parent.param['output'][out_name]

    """add includes for an given output into RenderSource"""
    def src_includes(self, out_name, rs, patterns = None):
        if patterns is None:
            patterns = self.pattern
        return rs.add_includes(util.attr_dict(self.get_output(out_name), 'includes'), patterns)

    def msg_id_symbol(self, msg_name):
        return self.get_attr('all_msg_enum_prefix')+msg_name

    def lookup_type(self, name):
        return self.parent.typemap.lookup(name)

    def get_message(self, msg_name):
        return self.parent.cf.get_message(msg_name)

    def iter_messages(self):
        return self.parent.cf.messages.messages.iteritems()

    """write create a field from typespec into an RenderSource"""
    def write_field(self, name, typename, rs):
        typespec = self.lookup_type(typename)
        if 'C.elements' in typespec:
            rs.write(typespec['C.type']+" "+name+"["+str(typespec['C.elements'])+"]")
        else:
            rs.write(typespec['C.type']+" "+name)
        rs.use_type(typespec)

    def get_attr(self, name):
        return self.replace_str(self.parent.param['settings'][name])

    def replace_str(self, text, pattern = None):
        if pattern is None:
            pattern = self.pattern
        return util.replace_list(text, pattern)

    def get_output_file(self, name):
        fn = self.replace_str(self.get_attr('output_dir')+"/"+self.parent.param['output'][name]['file'])
        util.create_file_path(fn)
        return fn

    def write_output_file(self, name, text):
        fn = self.get_output_file(name)
        with open(fn, "w") as text_file:
            text_file.write(text)

    """get the name of the payload struct union"""
    def get_payload_union_typename(self):
        return "union "+self.get_attr('can_frame_payload_union')

    """get the message struct field name in the payload union"""
    def get_payload_union_field(self, msg_name):
        return "payload_"+msg_name

    """create a RenderSource instance for given header output"""
    def get_render_header(self, name):
        rs = RenderSource(self.replace_str(self.parent.param['output'][name]['guard']))
        self.src_includes(name, rs)
        return rs
