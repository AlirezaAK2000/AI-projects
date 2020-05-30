from problem_formulization import Node, Problem
from iterative_deepening_search import IDS
from a_star_search import a_star_tree_search
from bidirectional_BFS_search import bidirectional_search
import re

'''
getting data and 
deciding to use which algorithm we should use
happens hear. 
'''


# extracting class and height
def find_matches(text):
    if text != '#':
        pattern = '[A-Z]|\d{1,}|[a-z]'
        strs = re.findall(pattern, text)
        return [strs[1], int(strs[0])]
    else:
        return text


def use_a_star(problem):
    result = a_star_tree_search(problem.root, problem)
    print_info(result)


def use_IDS(problem):
    search = IDS(problem)
    result = search.iterative_deeping_search()
    print_info(result)


def use_bs(problem):
    res = bidirectional_search(problem)
    print_info(res)


# print result
def print_info(result):
    if result != 'failure':
        print(result['depth'])
        for action in result['actions']:
            print(action)

        for node in result['path']:
            print(node)

        print(f"Nodes Created: {result['nodes_created']}")
        print(f"Nodes Expanded: {result['nodes_expanded']}")
    else:
        print(result)


# getting first state and create first node
print('________________________________________________________')

n, m = [int(s) for s in input('\tEnter First State:\n').split()]
first_state = []
for _ in range(n): first_state.append(input().split())
first_state = [list(map(find_matches, s)) for s in first_state]
root = Node(first_state)

# getting first state ,n and m to the formulized problem

problem = Problem(root, n, m)

# selecting algorithm
print('________________________________________________________')
tasks = '''Select Algorithm:
1.a*
2.ids
3.bs
'''
algorithm = input(tasks)
algorithms = {
    'a*': use_a_star,
    'ids': use_IDS,
    'bs': use_bs
}
algorithms[algorithm](problem)
