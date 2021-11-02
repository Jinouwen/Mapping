import networkx as nx
import numpy as np
from sir.machine import Machine
from sir.placement import Placement
from utils.evaluator import Evaluator
from algrithms.random_init import RandomInit
import numba as nb
import copy


class ForceDirected(object):
    def __init__(self):
        pass

    @staticmethod
    # @nb.jit(nopython=True, parallel=True)
    def do_mapping_basic(net: nx.DiGraph, machine: Machine, placement=None):
        if placement is None:
            placement = RandomInit.do_mapping(net, machine)
        else:
            placement = copy.deepcopy(placement)
        forces = np.zeros((*machine.size, 4), dtype=float)
        # 0:right 1:left 2:up 3:down
        iteration_condition = True
        swap_list = np.zeros(machine.core_num * 2, dtype=int)
        swap_pos = np.zeros((machine.core_num * 2, 2), dtype=int)
        swap_force = np.zeros(machine.core_num * 2, dtype=float)
        swap_dir = np.zeros(machine.core_num * 2, dtype=int)
        swapped_pos = np.zeros(machine.size, dtype=int)
        iteration_count = 0
        while iteration_condition:
            iteration_count += 1
            swap_num = 0
            swapped_pos.fill(0)
            swap_force.fill(0)
            forces.fill(0)
            for u, v in net.edges:
                # maintain force
                u_pos = tuple(placement.mapping[u])
                v_pos = tuple(placement.mapping[v])
                dx = v_pos[0] - u_pos[0]
                dy = v_pos[1] - u_pos[1]
                if abs(dx) == 1 and dy == 0:
                    forces[u_pos][1 if dx == 1 else 0] -= 1
                    forces[v_pos][0 if dx == 1 else 1] -= 1
                else:
                    forces[u_pos][1] += 1 if dx < 0 else -1
                    forces[v_pos][0] += 1 if dx < 0 else -1
                    forces[u_pos][0] += 1 if dx > 0 else -1
                    forces[v_pos][1] += 1 if dx > 0 else -1
                if abs(dy) == 1 and dx == 0:
                    forces[u_pos][3 if dy == 1 else 2] -= 1
                    forces[v_pos][2 if dy == 1 else 3] -= 1
                else:
                    forces[u_pos][3] += 1 if dy < 0 else -1
                    forces[v_pos][2] += 1 if dy < 0 else -1
                    forces[u_pos][2] += 1 if dy > 0 else -1
                    forces[v_pos][3] += 1 if dy > 0 else -1
            for x in range(machine.size_x - 1):
                for y in range(machine.size_y):
                    force = forces[x][y][0] + forces[x + 1][y][1]
                    if force > 0.5:
                        swap_list[swap_num] = swap_num
                        swap_pos[swap_num] = [x, y]
                        swap_dir[swap_num] = 0
                        swap_force[swap_num] = force
                        swap_num += 1
            for x in range(machine.size_x):
                for y in range(machine.size_y - 1):
                    force = forces[x][y][2] + forces[x][y + 1][3]
                    if force > 0.5:
                        swap_list[swap_num] = swap_num
                        swap_pos[swap_num] = [x, y]
                        swap_dir[swap_num] = 1
                        swap_force[swap_num] = force
                        swap_num += 1
            swap_list_sorted = swap_list[swap_force[:swap_num].argsort()[::-1]]
            for i in swap_list_sorted[:1]:
                u_pos = swap_pos[i]
                v_pos = (u_pos[0] + 1, u_pos[1]) if swap_dir[i] == 0 else (u_pos[0], u_pos[1] + 1)
                if swapped_pos[tuple(u_pos)] == 1 or swapped_pos[tuple(v_pos)] == 1:
                    continue
                # swap
                swapped_pos[tuple(u_pos)] = 1
                swapped_pos[tuple(v_pos)] = 1
                u_id = placement.index[tuple(u_pos)]
                v_id = placement.index[tuple(v_pos)]
                placement.mapping[u_id] = v_pos
                placement.mapping[v_id] = u_pos
                placement.index[tuple(v_pos)] = u_id
                placement.index[tuple(u_pos)] = v_id
            if swap_num == 0:
                iteration_condition = False
            print(iteration_count, Evaluator.evaluate(placement))
            # print(placement.index)
            # print(placement.mapping)
            # input()
        return placement


def main():
    np.random.seed(2)
    from algrithms.hilbert import Hilbert
    from utils.random_net_maker import Net_maker
    net = Net_maker.full_connect(16, 16)
    machine = Machine(16)
    placement_random = RandomInit.do_mapping(net, machine)
    placement_hilbert = Hilbert.do_mapping(net, machine)
    placement_FD = ForceDirected.do_mapping_basic(net, machine, placement_random)
    placement_FD_Hilbert = ForceDirected.do_mapping_basic(net, machine, placement_hilbert)
    from utils.evaluator import Evaluator
    cost_random = Evaluator.evaluate(placement_random)
    cost_hilbert = Evaluator.evaluate(placement_hilbert)
    cost_FD = Evaluator.evaluate(placement_FD)
    cost_FD_Hilbert = Evaluator.evaluate(placement_FD_Hilbert)
    print("random", cost_random)
    print("hilbert", cost_hilbert)
    print("FD_basic", cost_FD)
    print("FD_basic+Hilbert", cost_FD_Hilbert)



if __name__ == '__main__':
    main()
