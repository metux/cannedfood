
from cannedfood import util
import logging

payload_types = {
    'uint8':  { 'basetype': 'uint', 'bits':  8, 'min_bits': 1, 'max_bits': 8 },
    'int8':   { 'basetype': 'int',  'bits':  8, 'min_bits': 1, 'max_bits': 8 },
    'int16':  { 'basetype': 'int',  'bits': 16, 'min_bits': 1, 'max_bits': 8 },
    'uint16': { 'basetype': 'int',  'bits': 16, 'min_bits': 1, 'max_bits': 8 },
    'bool':   { 'basetype': 'int',  'bits':  1, 'min_bits': 1, 'max_bits': 8 },
}

class CanMessage:
    def __init__(self, yamlobj):
        self._my_obj  = yamlobj
        self.canid    = yamlobj['id']
        self.priority = util.attr_int_def(yamlobj, 'priority', 0)
        self.name     = yamlobj['message']
        self.payload  = util.attr_list(yamlobj, 'payload')
        self.payload_types = payload_types

        for f in self.payload:
            if 'type' not in f:
                self._payload_err("payload without type")
            if 'name' not in f:
                self._payload_err("payload without name")
            if f['type'] not in payload_types:
                self._payload_err("payload with unknown type: "+f['type'])
            t = payload_types[f['type']]

            if 'bits' in f:
                f['bits'] = int(f['bits'])
                if f['bits'] < t['min_bits']:
                    self._payload_err("payload type "+f['type']+" needs at least "+t['min_bits']+" bits")
                if f['bits'] > t['max_bits']:
                    self._payload_err("payload type "+f['type']+" can at max "+t['max_bits']+" bits")
            else:
                f['bits'] = t['bits']

            # fixme: check types

    def _payload_err(self, text):
        raise Exception("message "+self.name+": "+text)

class CanMessageDB:
    def __init__(self):
        self.messages = {}
        self._my_ids = {}

    def add(self, msg):
        if msg.canid in self._my_ids:
            logging.warning("can id "+str(msg.canid)+" already assigned. make sure they're not on the same bus")
        if msg.name in self.messages:
            Exception("message name \""+msg.name+"\" already assigned")
        self.messages[msg.name] = msg
        self._my_ids[msg.canid] = msg
