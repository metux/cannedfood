from cannedfood.codegen.C import RenderEnum
from base import CGenBase

"""write header file with can messages"""
class CMsgId(CGenBase):

    def generate(self):
        re = RenderEnum(self.get_attr('all_msg_enum_name'), self.get_attr('all_msg_enum_prefix'))
        for n,m in self.parent.cf.messages.messages.iteritems():
            re.add(m.name, m.canid)

        rs = self.get_render_header('msgid_h')
        rs.write(str(re))

        self.write_output_file('msgid_h', str(rs))
