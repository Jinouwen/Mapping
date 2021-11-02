import networkx as nx
import numpy as np


class Net_maker(object):

    @staticmethod
    def full_connect(layer_num=10, num_per_layer=10):
        net = nx.DiGraph()
        for i in range(layer_num-1):
            # TODO: weight
            edges = [(x,y) for x in range(i * layer_num, i * layer_num + num_per_layer)
                     for y in range((i + 1) * layer_num, (i + 1) * layer_num + num_per_layer)]
            net.add_edges_from(edges)
        return net


def main():
    net = Net_maker.full_connect()
    print(net)

    
if __name__ == '__main__':
    main()
