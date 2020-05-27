import copy
from typing import List
import itertools


class Node:

    def __init__(self, data: List[List[List]], row=-1, col=-1, parent=None, g=0, h=0, action_occurred=None):
        self.action_occurred = action_occurred
        self.data = data
        self.parent = parent
        self.h = h
        self.g = g
        if row == -1 or col == -1:
            for d in data:
                if d.__contains__('#'):
                    self.row = data.index(d)
                    self.col = d.index('#')
                    break
        else:
            self.row = row
            self.col = col

    def __repr__(self):
        string = ""
        for row in self.data:
            string += f'{row}\n'
        return string

    def __eq__(self, other):
        return other == self.data.__str__()

    def __hash__(self):
        return hash(self.data.__str__())

    def set_h(self, h):
        # self.cost += h
        self.h = h


class Problem:

    def __init__(self, root: Node, n, m):
        self.root = root
        self.n = n
        self.m = m
        self.goals_generated = self.create_goals(root.data)
        root.set_h(self.h(root))

    def create_goals(self, data):
        classes = dict()
        for row in data:
            for col in row:
                if col != '#':
                    try:
                        classes[col[0]].append(col[1])
                    except:
                        classes[col[0]] = []
                        classes[col[0]].append(col[1])

        goal_generated = []
        for class_name in classes.keys():
            classes[class_name].sort(reverse=True)
            new_row = [[class_name, i] for i in classes[class_name]]
            if len(classes[class_name]) < self.m:
                new_row.insert(0, '#')
            goal_generated.append(new_row)
        goal_permutations = [list(f) for f in list(itertools.permutations(goal_generated))]
        return goal_permutations

    def goal_test(self, node: Node):
        return node.data in self.goals_generated

    def child_node(self, parent, action):
        return self.result(action, parent)

    def _swap(self, state, row, col, new_row, new_col):
        st = copy.deepcopy(state)
        st[row][col], st[new_row][new_col] = st[new_row][new_col], st[row][col]
        return st

    def actions(self, state):
        row = state.row
        col = state.col
        right = {'name': 'right', 'col': col + 1, 'row': row}
        left = {'name': 'left', 'col': col - 1, 'row': row}
        up = {'name': 'up', 'col': col, 'row': row - 1}
        down = {'name': 'down', 'col': col, 'row': row + 1}

        if row == 0 and col == 0:
            return [right, down]
        elif row == self.n - 1 and col == 0:
            return [right, up]
        elif row == 0 and col == self.m - 1:
            return [left, down]
        elif row == self.n - 1 and col == self.m - 1:
            return [left, up]
        elif row == 0:
            return [left, right, down]
        elif col == 0:
            return [right, down, up]
        elif row == self.n - 1:
            return [up, left, right]
        elif col == self.m - 1:
            return [left, up, down]

        return [left, up, down, right]

    def result(self, move, parent):
        row = parent.row
        col = parent.col
        data = parent.data
        new_node = Node(self._swap(data, row, col, move['row'], move['col']), move['row'], move['col'], parent,
                        g=parent.g + 1,
                        action_occurred=move)
        new_node.set_h(self.h(new_node))
        return new_node

    def h(self, state: Node):
        data = state.data
        costs = []
        for goal in self.goals_generated:
            goal_cost = 0
            for row in data:
                for col in row:
                    for row_g in goal:
                        if col in row_g:
                            x = abs(row_g.index(col) - row.index(col))
                            y = abs(goal.index(row_g) - data.index(row))
                            goal_cost += (x + y)*(1+((self.m*self.n)/100))

            costs.append(goal_cost)
        return min(costs)
