from problem_formulization import Node, Problem
from _collections import deque

'''
bidirectional search implemented with bfs graph search
problem and goal needed for this algorithm 
'''


def bidirectional_search(problem: Problem, goal: Node):
    nodes_expanded = 2
    nodes_created = 2
    first_state = problem.root
    explored_f = {first_state}
    explored_g = {goal}
    q_f = deque()
    q_g = deque()
    q_f.append(first_state)
    q_g.append(goal)

    while q_g and q_f:
        if q_f:
            nodes_expanded += 1
            visited_state = q_f.popleft()
            if visited_state == goal or visited_state in q_g:
                return info(q_g, visited_state, goal, nodes_expanded, nodes_created)
            for action in problem.actions(visited_state):
                child = problem.child_node(visited_state, action)
                nodes_created += 1
                if not child in explored_f:
                    explored_f.add(child)
                    q_f.append(child)
        if q_g:
            nodes_expanded += 1
            visited_state = q_g.popleft()
            if visited_state == first_state or visited_state in q_f:
                return info(q_f, visited_state, goal, nodes_expanded, nodes_created)
            for action in problem.actions(visited_state):
                child = problem.child_node(visited_state, action)
                nodes_created += 1
                if not child in explored_g:
                    explored_g.add(child)
                    q_g.append(child)

    return 'failure'


# format result(path , depth , ...)
def info(queue, result, goal, nodes_expanded, nodes_created):
    path_to_another = None
    for node in queue:
        if result == node:
            path_to_another = node
            break
    half_way_1 = navigation(result)
    half_way_2 = navigation(path_to_another)
    path = []
    if half_way_1[0] == goal:
        path = half_way_2 + list(reversed(half_way_1))
    else:
        path = half_way_1 + list(reversed(half_way_2))

    return {
        'depth': max(len(actions_occurred(half_way_2)), len(actions_occurred(half_way_1))),
        'path': path,
        'actions': actions_occurred(path),
        'nodes_created': nodes_created,
        'nodes_expanded': nodes_expanded
    }


def navigation(node):
    current = node
    path = []
    while current:
        path.insert(0, current)
        current = current.parent

    return path


def actions_occurred(path):
    actions = []
    for node in path:
        if node.action_occurred:
            actions.append(node.action_occurred)

    return actions
