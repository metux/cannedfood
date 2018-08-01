from base import CGenBase

class CEncode(CGenBase):
    def __init__(self, parent):
        CGenBase.__init__(self, parent)
        self.typespec_frame   = self.lookup_type('C.os.can_frame_struct')
        self.typename_frame   = self.typespec_frame['C.type']

    """name of a node's receive handler for message"""
    def __msg_encoder_name(self, msg_name):
        return self.get_attr('all_msg_encoder_name').replace('${MSG_NAME}', msg_name)

    """generate a receive receive handler prototype for a node/message"""
    def __msg_encoder_proto(self, msg, rs):
        union = self.get_payload_union_typename()
        struct = self.get_payload_union_field(msg.name)

        rs.write("static inline void "+self.__msg_encoder_name(msg.name)+"("+self.typename_frame+" *frame")
        for field in msg.payload:
            rs.write(", ")
            self.write_field(field['name'], 'C.payload.'+field['type'], rs)
        rs.writeln(")")
        rs.writeln("{")
        rs.writeln("    memset(frame, 0, sizeof("+self.typename_frame+"));")
        rs.writeln("    frame->"+self.get_attr('can_frame_field_canid')+" = "+self.msg_id_symbol(msg.name)+";");

        if len(msg.payload) > 0:
            rs.writeln("    "+union+"* d = ("+union+"*)&(frame->"+self.get_attr('can_frame_field_data')+");")

            for field in msg.payload:
                rs.writeln("    d->"+struct+"."+field['name']+" = "+field['name']+";")

        rs.writeln("}")
        rs.writeln()

    """generate source code for a node's receive demux"""
    def generate(self):

        rs = self.get_render_header('msg_encode_h')
        rs.use_type(self.typespec_frame)

        for n,m in self.iter_messages():
            self.__msg_encoder_proto(m, rs)

        self.write_output_file('msg_encode_h', str(rs))
