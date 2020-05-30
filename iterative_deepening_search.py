'''
iterative deeping search algorithm
using dfs tree search for implementing
we should pass formulized problem to this class
'''


class IDS:

    def __init__(self, problem):
        self.problem = problem
        self.nodes_expanded = 0
        self.nodes_created = 0

    def _deep_limited_search(self, depth):
        return self._recursive_search(self.problem.root, self.problem, depth)

    def _recursive_search(self, root, problem, limit):
        if problem.goal_test(root):
            return root
        elif limit == 0:
            return 'cutoff'
        else:
            cut_off_occurred = False
            actions = problem.actions(root)
            self.nodes_created += len(actions)
            self.nodes_expanded += 1
            for action in actions:
                child = problem.result(action, root)
                result = self._recursive_search(child, problem, limit - 1)
                if result == 'cutoff':
                    cut_off_occurred = True
                elif result != 'failure':
                    return result

            return 'cutoff' if cut_off_occurred else 'failure'

    #
    def iterative_deeping_search(self, first_deep=0):
        self.nodes_created = 0
        self.nodes_expanded = 0
        for depth in range(first_deep, 1000000000):
            print(f'depth: {depth}')
            result = self._deep_limited_search(depth)
            if result != 'cutoff' and result != 'failure':
                return self.info(result)
            elif result != 'cutoff':
                return result

    # format result
    def info(self, solution):
        path = []
        actions = []
        depth = solution.g
        while solution:
            path.insert(0, solution)
            actions.insert(0, (solution.action_occurred)['name'])
            solution = solution.parent

        return {
            'depth': depth,
            'path': path,
            'actions': actions,
            'nodes_created': self.nodes_created,
            'nodes_expanded': self.nodes_expanded
        }
