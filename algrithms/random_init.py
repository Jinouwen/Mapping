import networkx as nx
import numpy as np
from sir.machine import Machine
from sir.placement import Placement
from utils.evaluator import Evaluator


class RandomInit(object):

    @staticmethod
    # @nb.jit(nopython=True, parallel=True)
    def do_mapping(net: nx.DiGraph, machine: Machine, placement=None):
        placement = Placement(net, machine)
        permutation = np.random.permutation(machine.core_num)
        i = 0
        for x in range(machine.size_x):
            for y in range(machine.size_y):
                placement.index[x][y] = permutation[i]
                placement.mapping[permutation[i]] = [x, y]
                i += 1
        return placement
