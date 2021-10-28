import networkx as nx
import numpy as np
from sir.machine import Machine
from sir.placement import Placement


def pre_direction(now_d):
    return now_d ^ 3


def next_direction(now_d):
    return now_d ^ 1


def make_curve(x0, y0, x, y, begin_num, direction):
    # 0 right 1 up 2 left 3 down
    # 0,0 in top left
    if x == 1 and y == 1:
        return [(x0, y0)]
    child_x = x / 2
    child_y = y / 2
    matrix_x = [1, 0, -1, 0]
    matrix_y = [0, 1, 0, -1]
    d1 = next_direction(direction)
    d2 = direction
    d3 = direction
    d4 = pre_direction(direction)
    x1, y1 = x0 + matrix_x[d1] * child_x, y0 + matrix_y[d1] * child_y
    x2, y2 = x1 + matrix_x[d2] * child_x, y1 + matrix_y[d2] * child_y
    x3, y3 = x2 + matrix_x[d3] * (child_x - 1) + matrix_x[d4], y2 + matrix_y[d3] * (child_y - 1) + matrix_y[d4]
    begin_num1 = begin_num + child_x * child_y
    begin_num2 = begin_num1 + child_x * child_y
    begin_num3 = begin_num2 + child_x * child_y
    curve0 = make_curve(x0, y0, child_x, child_y, begin_num, d1)
    curve1 = make_curve(x1, y1, child_x, child_y, begin_num1, d2)
    curve2 = make_curve(x2, y2, child_x, child_y, begin_num2, d3)
    curve3 = make_curve(x3, y3, child_x, child_y, begin_num3, d4)
    return curve0 + curve1 + curve2 + curve3


class Hilbert(object):
    def __init__(self):
        pass

    @staticmethod
    def do_mapping(net: nx.DiGraph, machine: Machine):
        placement = Placement(net, machine)
        node_list = list(nx.topological_sort(net))
