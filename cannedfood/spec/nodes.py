
from cannedfood import util

class CanNode:
    def __init__(self, yamlobj):
        self._my_obj  = yamlobj
        self.name     = yamlobj['node']
        self.send     = util.attr_list(yamlobj, 'send')
        self.receive  = util.attr_list(yamlobj, 'receive')

    def get_used_messages(self):
        return util.merge_lists(self.send, self.receive)
