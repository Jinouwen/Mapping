import numpy as np
import networkx as nx
from sir.machine import Machine
from sir.placement import Placement
from algrithms.hilbert import Hilbert
from algrithms.force_directed import ForceDirected
from utils.random_net_maker import Net_maker

def main():
    net = Net_maker.full_connect(4,4)
    machine = Machine(4)

if __name__ == '__main__':
    main()