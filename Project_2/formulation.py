from _collections import defaultdict
from copy import deepcopy
from typing import List, Tuple
import random

# map components
MUSH_RED, MUSH_BLUE, WALL, PLAIN, MARIO = range(5)


# state structure
class Node:
    def __init__(self, red: List, blue: List, pos: Tuple):
        self.red_mushes = red
        self.blue_mushes = blue
        self.pos = pos

    def __repr__(self):
        return f'pos:{self.pos} - red:{len(self.red_mushes)} - blue:{len(self.blue_mushes)}'

    def __eq__(self, other):
        return other == (self.pos, len(self.red_mushes), len(self.blue_mushes))

    def __hash__(self):
        return hash((self.pos, len(self.red_mushes), len(self.blue_mushes)))


# problem formulation
class Problem:
    def __init__(self, first_state: Node, playground):
        self.playground = playground
        self.first_state = first_state
        self.s = None
        self.a = None
        self.H = dict()
        self.result = defaultdict(lambda: defaultdict(lambda: None))
        self.step = 0

    def set_prev_state_and_get_new(self, s: Node, a):
        self.s = s
        self.a = a
        return self.create_child(a, s)

    # get actions
    @staticmethod
    def actions(state: Node):
        row, col = state.pos
        right = {'name': 'RIGHT', 'col': col + 1, 'row': row}
        left = {'name': 'LEFT', 'col': col - 1, 'row': row}
        up = {'name': 'UP', 'col': col, 'row': row - 1}
        down = {'name': 'DOWN', 'col': col, 'row': row + 1}
        return [left, up, down, right]

    # create new state
    def create_child(self, action, current: Node):
        print(f"action : {action['name']} *** position : {current.pos}")
        row, col = current.pos
        self.step += 1
        child_row, child_col = action['row'], action['col']
        red_mush, blue_mush = current.red_mushes, current.blue_mushes
        unit = self.playground[child_row][child_col]
        if unit != WALL:
            blue_mush = deepcopy(blue_mush)
            red_mush = deepcopy(red_mush)
            if unit == MUSH_BLUE:
                blue_mush.remove((child_row, child_col))
                print('blue mushroom has eaten')
            elif unit == MUSH_RED:
                red_mush.remove((child_row, child_col))
                print('red mushroom has eaten')
            self.playground[row][col] = PLAIN
            self.playground[child_row][child_col] = MARIO
            return Node(red_mush, blue_mush, (child_row, child_col))
        else:
            print('wall!!!!!!!!!!!')
            return deepcopy(current)

    # it checks if current state is the last state or not
    def goal_test(self, state: Node):
        condition = len(state.red_mushes) != len(self.first_state.red_mushes) and len(state.blue_mushes) != len(
            self.first_state.blue_mushes)
        return condition

    # first heuristic that counts remaining mushrooms
    @staticmethod
    def h1(state: Node):
        return len(state.red_mushes) + len(state.blue_mushes)

    # manhattan distance formula
    @staticmethod
    def manhattan(beg, des):
        return abs(beg[0] - des[0]) + abs(beg[1] - des[1])

    #  second heuristic that returns min distance between mario and an existing mushroom
    @staticmethod
    def h2(state: Node):
        pos = state.pos
        mushes = state.blue_mushes + state.red_mushes
        min_man = min([Problem.manhattan(pos, mush) for mush in mushes])
        return min_man

    # third heuristic that returns max distance between two mushroom
    @staticmethod
    def h3(state: Node):
        mushes = state.blue_mushes + state.red_mushes
        return max([max([Problem.manhattan(mushes[i], mushes[j]) for j in range(i + 1, len(mushes))]) for i in
                    range(len(mushes) - 1)])

    @staticmethod
    def h(state: Node):
        return Problem.h1(state)

    # step cost:
    # plain : 1
    # wall : infinity
    # to avoid redundant steps toward walls
    def cost(self, action):
        if self.playground[action['row']][action['col']] == WALL:
            return 10000000000
        return 1


# search algorithms
class Search:
    def __init__(self, problem: Problem):
        self.problem = problem

    # loop for searching last state
    def start_search(self, iter_num=100000):
        s = self.problem.first_state
        for i in range(iter_num):
            s = self.LRTA_agent(s)
            if s == 's':
                print(f'steps : {problem.step}')
                return 's'

    # LRTA* algorithm for search in complex environment
    def LRTA_agent(self, s_hat):
        s, a = self.problem.s, self.problem.a
        # print(f'\ns : {s}')
        # print(f's_hat: {s_hat}')
        # print(f'H : {s in self.problem.H.keys()}\n')

        if self.problem.goal_test(s_hat):
            return 's'
        if s_hat not in self.problem.H:
            self.problem.H[s_hat] = Problem.h(s_hat)
        if self.problem.s:
            self.problem.result[s][a['name']] = s_hat
            prev_h = self.problem.H[s]
            self.problem.H[s] = min(
                [self.LRTA_cost(s, b, self.problem.result[s][b['name']]) for b in Problem.actions(s)])
            print(f'state {s} updated from {prev_h} to {self.problem.H[s]}')
        a = self.get_best_action(s_hat)
        s = s_hat
        return self.problem.set_prev_state_and_get_new(s, a)

    # returns best action and choose random action between actions with minimum cost
    def get_best_action(self, state):
        actions = Problem.actions(state)
        costs = [self.LRTA_cost(state, b, self.problem.result[state][b['name']]) for b in actions]
        min_cost = min(costs)
        best_actions = []
        for i in range(len(actions)):
            if min_cost == costs[i]:
                best_actions.append(actions[i])
        return random.choice(best_actions)

    def LRTA_cost(self, s, a, s_hat):
        if not s_hat:
            return Problem.h(s)
        return self.problem.H[s_hat] + self.problem.cost(a)


if __name__ == '__main__':
    with open('Mario.txt', 'r') as file:
        lines = file.readlines()
    n = int(lines[0])
    m = int(lines[1])
    playground = [[WALL for _ in range(m + 2)]] + [[WALL if i == 0 or i == m + 1 else PLAIN for i in range(m + 2)] for _
                                                   in
                                                   range(n)] + [[WALL for _ in range(m + 2)]]
    mario_pos = tuple(int(j) for j in lines[2].split())
    playground[mario_pos[0]][mario_pos[1]] = MARIO
    k = int(lines[3])
    red, blue = [], []
    pos = None
    for i in range(4, k + 4):
        pos = tuple(int(j) for j in lines[i].split())
        red.append(pos)
        playground[pos[0]][pos[1]] = MUSH_RED
    for i in range(k + 4, 2 * k + 4):
        pos = tuple(int(j) for j in lines[i].split())
        blue.append(pos)
        playground[pos[0]][pos[1]] = MUSH_BLUE

    for line in lines[2 * k + 4:-1]:
        pos = tuple(int(j) for j in line.split())
        playground[pos[0]][pos[1]] = WALL

    print('*** MAP ***')
    print('\n'.join(str(playground).strip('[]').split('], [')))
    first_state = Node(red, blue, mario_pos)
    problem = Problem(first_state, playground)
    search = Search(problem)
    print(search.start_search())
