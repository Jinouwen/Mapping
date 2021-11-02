import networkx as nx
from sir.machine import Machine
from sir.placement import Placement


def cost_manhattan(u_pos, v_pos):
    dx = abs(u_pos[0] - v_pos[0])
    dy = abs(u_pos[1] - v_pos[1])
    return dx + dy


def cost_normal(u_pos, v_pos):
    dx = abs(u_pos[0] - v_pos[0])
    dy = abs(u_pos[1] - v_pos[1])
    return ((dx * dx) + (dy * dy)) ** 0.5


class Evaluator(object):
    @staticmethod
    def evaluate(placement: Placement, method='manhattan'):
        net = placement.net
        cost = 0
        cost_fun = eval('cost_'+method)
        for u, v in net.edges:
            u_pos = placement.mapping[u]
            v_pos = placement.mapping[v]
            cost += cost_fun(u_pos, v_pos)
        return cost



