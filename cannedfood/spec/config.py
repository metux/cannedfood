
import yaml
from messages import CanMessageDB, CanMessage
from nodes import CanNode
from types import TypeMap
import logging
import os
from cannedfood import util

class CanSpecConfig:
    def __init__(self, configfile):
        self.messages = CanMessageDB()
        self.nodes = {}
        self.typemap = TypeMap()
        self.__load_config_yaml(configfile)

    """add a node object -- check for duplicate name"""
    def add_node(self, node):
        if node.name in self.nodes:
            raise Exception("node name \""+node.name+"\" already defined")
        self.nodes[node.name] = node

    """load messages from a yaml file"""
    def load_messages_yaml(self, fn):
        for ent in self.load_yaml(fn):
            self.messages.add(CanMessage(ent))

    """load nodes from a yaml file"""
    def load_nodes_yaml(self, fn):
        for ent in self.load_yaml(fn):
            self.add_node(CanNode(ent))

    """load nodes from a yaml file"""
    def load_typemap_yaml(self, fn):
        self.typemap.add_dict(self.load_yaml(fn))

    """consistency check between nodes and messages"""
    def check_node_messages(self):
        errs = 0
        for n, node in self.nodes.iteritems():
            errs += self.__check_node_msg(node)

    def __check_node_msg(self, node):
        errs = 0
        if node.receive is not None:
            for msg in node.receive:
                if msg not in self.messages.messages:
                    logging.error("node "+node.name+" wanna receive undefined message "+msg)
                    errs = errs + 1

        if node.send is not None:
            for msg in node.send:
                if msg not in self.messages.messages:
                    logging.error("node "+node.name+" wanna send undefined message "+msg)
                    errs = errs + 1

        return errs

    def load_yaml(self, fn):
        fn = util.replace_list(fn, {'${CONF_DIR}': self.confdir, '%': self.confdir})
        with open(fn) as stream:
            return yaml.safe_load(stream)

    def __load_config_yaml(self, fn):
        self.confdir = os.path.dirname(os.path.abspath(fn))
        self.config = self.load_yaml(fn)

        for ent in self.config['sources']:
            if 'messages' in ent:
                self.load_messages_yaml(ent['messages'])
            if 'typemap' in ent:
                self.load_typemap_yaml(ent['typemap'])
            if 'nodes' in ent:
                self.load_nodes_yaml(ent['nodes'])

    def get_generator_param(self, name):
        return self.config['generator'][name]['settings']

    def get_generator_cf(self, name):
        return self.config['generator'][name]

    def get_generator_typemap(self, name):
        return self.typemap

    # fixme: automatically pass through message objects
    def get_message(self, name):
        return self.messages.messages[name]

    # fixme: automatically pass through node objects
    def get_node(self, name):
        return self.nodes[name]

    def iter_messages(self):
        return self.messages.messages.iteritems()

def load_yaml(fn):
    return CanSpecConfig(fn)
