from base import CGenBase

class CPayload(CGenBase):
    def _payload_type(self, field):
        return self.lookup_type("C.payload."+field['type'])

    """create a field from typespec"""
    def __make_field(self, name, typename):
        typespec = self.lookup_type(typename)
        if 'C.elements' in typespec:
            return typespec['C.type']+" "+name+"["+str(typespec['C.elements'])+"]"
        else:
            return typespec['C.type']+" "+name

    """render header file with payload structs"""
    def __render_header_payload(self):
        typename = self.get_payload_union_typename()
        packed = self.get_attr('c_attr_struct_packed')

        rs = self.get_render_header('payload_h')

        rs.use_type(self.lookup_type('C.os.can_frame_payload'))
        rs.write(typename+" {\n")
        rs.write("    "+self.__make_field('data', 'C.os.can_frame_payload')+";\n")

        for n,m in self.parent.cf.iter_messages():
            rs.write("    struct "+packed+" {\n")

            for f in m.payload:
                t = self._payload_type(f)
                rs.write("         "+t['C.type']+" "+f['name']+":"+str(f['bits'])+";\n")
                rs.use_type(t)

            rs.write("    } "+self.get_payload_union_field(m.name)+";\n")

        rs.write("};\n")
        return str(rs)

    def generate(self):
        self.write_output_file('payload_h', self.__render_header_payload())
