import copy
from typing import Dict, List
import itertools


class Node:

    def __init__(self, data: List[List[Dict[str, int]]], row=-1, col=-1, parent=None, g=0, h=0, action_occurred=None):
        self.action_occurred = action_occurred
        self.data = data
        self.parent = parent
        self.h = h
        self.g = g
        self.visited = False
        self.cost = g + h
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
        # return f'Row:{self.row} Col:{self.col}'
        string = ""
        for row in self.data:
            string += f'{row}\n'

        return string

    def __eq__(self, other):
        return other == self.data.__str__()

    def __hash__(self):
        return hash(self.data.__str__())

    def update_cost(self, parent):
        if parent.cost > self.cost:
            self.cost = parent.cost

    def set_h(self, h):
        self.cost += h
        self.h = h


class Problem:

    def __init__(self, root: Node, n, m):
        self.root = root
        self.n = n
        self.m = m
        self.goals_generated = self.create_goals(root.data)
        print(self.goals_generated)
        root.set_h(self.h(root))

    def create_goals(self, data):
        class_count = len(data)
        row_size = len(data[0])
        classes = dict()
        for i in range(class_count):
            classes[chr(ord('a') + i)] = []

        for row in data:
            for col in row:
                if col != '#':
                    classes[list(col.keys())[0]].append(list(col.values())[0])

        print(classes)

        goal_generated = []
        for class_name in classes.keys():
            classes[class_name].sort(reverse=True)

            new_row = [{class_name: i} for i in classes[class_name]]
            if len(classes[class_name]) < row_size:
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

        if row == 0 and col == 0:
            return [
                'right',
                'down'
            ]
        elif row == self.n - 1 and col == 0:
            return [
                'right',
                'up'
            ]
        elif row == 0 and col == self.m - 1:
            return [
                'left',
                'down'
            ]
        elif row == self.n - 1 and col == self.m - 1:
            return [
                'left',
                'up'
            ]
        elif row == 0:
            return [
                'left',
                'right',
                'down'
            ]
        elif col == 0:
            return [
                'right',
                'down',
                'up'
            ]
        elif row == self.n - 1:
            return [
                'up',
                'left',
                'right'
            ]
        elif col == self.m - 1:
            return [
                'left',
                'up',
                'down'
            ]

        return [
            'left',
            'up',
            'down',
            'right'
        ]

    def result(self, move, parent):
        row = parent.row
        col = parent.col
        data = parent.data
        if move == 'right':
            new_node = Node(self._swap(data, row, col, row, col + 1), row, col + 1, parent, g=parent.g + 1,
                            action_occurred=move)
            new_node.set_h(self.h(new_node))
            # new_node.update_cost(parent)
            return new_node
        elif move == 'down':
            new_node = Node(self._swap(data, row, col, row + 1, col), row + 1, col, parent, g=parent.g + 1,
                            action_occurred=move)
            new_node.set_h(self.h(new_node))
            # new_node.update_cost(parent)
            return new_node
        elif move == 'left':
            new_node = Node(self._swap(data, row, col, row, col - 1), row, col - 1, parent, g=parent.g + 1,
                            action_occurred=move)
            new_node.set_h(self.h(new_node))
            # new_node.update_cost(parent)
            return new_node
        else:
            new_node = Node(self._swap(data, row, col, row - 1, col), row - 1, col, parent, g=parent.g + 1,
                            action_occurred=move)
            new_node.set_h(self.h(new_node))
            # new_node.update_cost(parent)
            return new_node

    def h1(self, state: Node):
        data = state.data
        un_sorted = self.n
        for d in data:
            if d.__contains__('#'):
                d = copy.deepcopy(d)
                d.remove('#')

            nums = [list(i.values())[0] for i in d]
            if all(nums[i] >= nums[i + 1] for i in range(len(nums) - 1)):
                un_sorted -= 1

        return un_sorted

    def h2(self, state: Node):
        data = state.data
        class_per_line = 0

        for d in data:
            students = self.m
            if d.__contains__('#'):
                d = copy.deepcopy(d)
                d.remove('#')
                students -= 1

            classes = {list(i.keys())[0] for i in d}
            class_per_line += len(classes) - 1

        return class_per_line

    def h3(self, state: Node):
        data = state.data
        for row in data:
            if not ('#' in row):
                continue
            return row.index('#')




    def h(self, state):
        return self.h1(state) + self.h2(state) + self.h3(state)
