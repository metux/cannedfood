from cannedfood.codegen.C import RenderEnum
from base import CGenBase

"""generate a C enum with messages IDs for an individual node"""
class CNodeMsgId(CGenBase):
    def __render_enum(self):
        re = RenderEnum(self.get_attr('node_msg_enum_name'), '')
        sym = self.get_attr('node_msg_enum_symbol')
        for m in self.node.get_used_messages():
            re.add(sym.replace('${MSG_NAME}', m) , self.get_message(m).canid)
        return str(re)

    def generate(self):
        rs = self.get_render_header('node_msgid_h')
        rs.write(self.__render_enum())
        self.write_output_file('node_msgid_h', str(rs))
