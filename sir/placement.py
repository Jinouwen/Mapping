import numpy as np
import networkx as nx
from sir.machine import Machine


class Placement(object):
    def __init__(self, net: nx.DiGraph, machine: Machine):
        self.net = net
        self.machine = machine
        self.node_num = net.number_of_nodes()
        self.core_num = machine.core_num
        self.size_x, self.size_y,self.size = machine.size_x, machine.size_y, machine.size
        if self.node_num > self.core_num:
            raise Exception('Cant mapping! [node_num > core_num]')
        self.mapping = np.full((self.node_num, 2), -1, dtype=int)
        self.index = np.full((machine.size_x, machine.size_y), -1, dtype=int)

    def clear(self):
        self.mapping = np.full((self.node_num, 2), -1, dtype=int)
        self.index = np.full((self.size_x, self.size_y), -1, dtype=int)
