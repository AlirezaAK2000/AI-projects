'''
A star search implementation with graph search
first state and fomulized problem needed
cost function implemented in the problem object
and cost while set and update in the creation of
child node.
'''


def a_star_tree_search(first_state, problem):
    current = first_state
    frontier = set()
    explored = set()
    nodes_created = 1
    nodes_expanded = 1
    frontier.add(current)
    # until frontier become empty
    while frontier:
        current = min(frontier, key=lambda s: s.g + s.h)
        if problem.goal_test(current):
            return info(current, nodes_expanded, nodes_created)
        frontier.remove(current)
        explored.add(current)
        children = [problem.child_node(current, action) for action in problem.actions(current)]
        nodes_created += len(children)
        for child in children:
            if child in explored:
                continue

            if child in frontier:
                must_change = False
                t = None
                for f in frontier:
                    if child == f:
                        if not child.g + child.h >= f.h + f.g:
                            must_change = True
                            t = f
                        break
                # nodes that have updated , have n't added to expanded_nodes
                if must_change:
                    frontier.remove(t)
                    frontier.add(child)
            else:
                nodes_expanded += 1
                frontier.add(child)

    return 'Failure'


# format result (find path , depth)
def info(solution, nodes_expanded, nodes_created):
    path = []
    actions = []
    depth = solution.g
    while solution:
        path.append(solution)
        actions.append(solution.action_occurred)
        solution = solution.parent
    path = list(reversed(path))
    actions = list(reversed(actions))
    return {
        'depth': depth,
        'path': path,
        'actions': actions,
        'nodes_created': nodes_created,
        'nodes_expanded': nodes_expanded
    }
