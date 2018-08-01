from node_recv import CNodeRecv
from node_msgid import CNodeMsgId
from payload import CPayload
from msgid import CMsgId
from encode import CEncode

class generator:
    def __init__(self, cf, name):
        self.cf      = cf
        self.name    = name
        self.typemap = self.cf.get_generator_typemap(self.name)
        self.param   = self.cf.get_generator_cf(self.name)

    def generate_all(self):
        self.generate_payload_header()
        self.generate_msgid_header()
        for name in self.cf.nodes:
            self.generate_source_node_recv_demux(name)
            self.generate_node_msgid_header(name)
        self.generate_encode()

    def generate_source_node_recv_demux(self, node_name):
        gen = CNodeRecv(self, node_name).generate()

    def generate_payload_header(self):
        CPayload(self).generate()

    def generate_msgid_header(self):
        CMsgId(self).generate()

    def generate_node_msgid_header(self, node_name):
        CNodeMsgId(self, node_name).generate()

    def generate_encode(self):
        CEncode(self).generate()
