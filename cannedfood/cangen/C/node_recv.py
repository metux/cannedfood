from cannedfood.codegen.C import RenderSource
from base import CGenBase

class CNodeRecv(CGenBase):
    def __init__(self, parent, node_name):
        CGenBase.__init__(self, parent, node_name)
        self.typespec_retval  = self.lookup_type('C.msg_handler.retval')
        self.typename_retval  = self.typespec_retval['C.type']
        self.typespec_context = self.lookup_type('C.msg_handler.context')
        self.typename_context = self.typespec_context['C.type']
        self.typespec_frame   = self.lookup_type('C.os.can_frame_struct')
        self.typename_frame   = self.typespec_frame['C.type']

        self.can_handler_proto = self.typename_retval+" "+self.get_attr('node_can_recv_handler')+"("+self.typename_context+" ctx, "+self.typename_frame+"* frame)"

    """name of a node's receive handler for message"""
    def __node_msg_recv_handler_name(self, msg_name):
        return self.get_attr('node_msg_recv_handler').replace('${MSG_NAME}', msg_name)

    """generate a receive receive handler prototype for a node/message"""
    def __node_msg_recv_handler_proto(self, msg, rs):
        rs.use_types([self.typespec_retval, self.typespec_context])

        rs.write(self.typename_retval+" "+self.__node_msg_recv_handler_name(msg.name)+"("+self.typename_context+" ctx")
        for field in msg.payload:
            rs.write(", ")
            self.write_field(field['name'], 'C.payload.'+field['type'], rs)
        rs.write(")")

    """get the message struct field name in the payload union"""
    def __payload_union_field(self, msg_name):
        return "payload_"+msg_name

    """render header file with per-node recv handler prototypes"""
    def render_header_node_recv_prototypes(self):
        rs = self.get_render_header('recv_demux_h')
        rs.use_type(self.typespec_frame)
        rs.comment("Node: %s - CAN message handler prototypes, called by the generated demuxer" % self.node_name)

        for m in self.node.get_used_messages():
            self.__node_msg_recv_handler_proto(self.get_message(m), rs)
            rs.write(";\n")

        rs.comment("Node: %s - generated CAN message receive demuxer" % self.node_name)
        rs.write(self.can_handler_proto+";\n")

        return str(rs)

    """render source code for a node's receive demux"""
    def render_source_node_recv_demux(self):
        union = self.get_payload_union_typename()

        rs = RenderSource(use_types = [self.typespec_frame, self.typespec_retval, self.typespec_retval])
        self.src_includes('recv_demux_c', rs)

        rs.write(self.can_handler_proto+"\n")
        rs.write("{\n")
        rs.write("    "+union+" *__data = ("+union+"*)&(frame->"+self.get_attr('can_frame_field_data')+");\n")
        rs.write("    switch (frame->"+self.get_attr('can_frame_field_canid')+") {\n")

        for m in self.node.get_used_messages():
            msg = self.get_message(m)
            prefix = "__data->"+self.__payload_union_field(m)+"."
            rs.write("        case "+self.msg_id_symbol(m)+":\n")
            rs.write("            return "+self.__node_msg_recv_handler_name(m)+"(ctx")

            for field in msg.payload:
                rs.write(", ")
                rs.write(prefix+field['name'])

            rs.write(");\n")
            rs.write("        break;\n")

        rs.write("    }\n")
        rs.write("    return "+str(self.typespec_retval['C.value.unhandled'])+";\n")
        rs.write("}\n")

        return str(rs)

    def generate(self):
        self.write_output_file('recv_demux_c', self.render_source_node_recv_demux())
        self.write_output_file('recv_demux_h', self.render_header_node_recv_prototypes())
