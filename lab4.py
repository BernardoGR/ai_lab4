import fileinput
import pprint as p
import time
from pprint import pprint
import itertools
from toposort import toposort, toposort_flatten

debug = False
bn_graph = {}


def format_input_nodes(line):
    # remove white spaces
    line = "".join(line.split())
    
    b_network = {'vars': line.split(",")}
    for node in line.split(","):
        b_network["+"+node] = []
        b_network["-"+node] = []
        # bn_graph[node] = {}
    return b_network


def format_input_probability(b_network, line):
    # remove white spaces
    line = "".join(line.split())
    # split on '=' and on '|' chars
    line_eq_split = line.split("=")
    line_pipe_split = line_eq_split[0].split("|")
    node = line_pipe_split[0]
    # create inverse probability node
    inverse_node = ""
    if "+" in node:
        inverse_node = node.replace("+", "-")
    if "-" in node:
        inverse_node = node.replace("-", "+")
    # get parents probabilities
    parents = []
    if len(line_pipe_split) > 1:
        parents = line_pipe_split[1]
        # append parents to bn_graph
        bn_graph[node[1:]] = set(str(parents).replace("+", "").replace("-", "").split(","))
    else:
        bn_graph[node[1:]] = set()
    probability = float(line_eq_split[1])
    inverse_probability = 1 - probability
    # append new nodes
    b_network[node].append({str(parents): probability})
    if inverse_node != "":
        b_network[inverse_node].append({str(parents): inverse_probability})
    return b_network


def format_input_queries(queries, line):
    # remove white spaces
    line = "".join(line.split())
    # split on '|'
    line_pipe_split = line.rstrip().split('|')
    query = line_pipe_split[0].split(",")
    evidence = []
    if len(line_pipe_split) > 1:
        evidence = line_pipe_split[1].split(',')

    queries.append({'query': query, 'evidence': evidence})

    return queries


def search_probability_by_parents(node, parent_values=None):
    if parent_values:
        for parent in parent_values:
            node = list(filter(lambda x: parent in list(x.keys())[0], node))
    print(node)
    return node


# recieves a list of nodes and return the nodes boolean enumeration:
# in: [A, B]
# out: [[+A, +B], [+A, -B], [-A, +B], [-A, -B]]
def enumerate_nodes(nodes):
    # generate a list of boolean combinations
    combinations = list(map(list, itertools.product([0, 1], repeat=len(nodes))))
    result_combinations = []
    for combination in combinations:
        new_combination = []
        for index, value in enumerate(combination):
            if value:
                sign = '+'
            else:
                sign = '-'
            # start from node index 1 to remove original sign
            new_combination.append(sign + nodes[index][1:])
        result_combinations.append(new_combination)
    return result_combinations

# def get_parents_from_evidence()


def get_probability(node, evidence, b_network):
    # parents_evidence: array in the form: ['+Burglary', '+Earthquake']
    parents_evidence = get_parents_from_evidence(evidence)
    result_probability = search_probability_by_parents(b_network['node'], parents_evidence)
    if len(result_probability) > 1:
        # one parent value was unknown
        print("error: unknown parent")
        return
    else:
        # return probability value queried:
        return


def enumeration_ask(query, evidence, b_network):
    enumerated_list_query_nodes = enumerate_nodes(query)
    Q = []
    print('\n\n combinations of query nodes: ' + str(query))
    print(enumerated_list_query_nodes)
    print('\n for each combination: query + evidence: ')
    for q in enumerated_list_query_nodes:
        evidence_x = q + evidence  # evidence plus the query with values assigned
        print(evidence_x)
        #result = enumerate_all(toposort_flatten(bn_graph), evidence_x, b_network)
        #Q.append(result)
    # after for loop, normalize Q values.


def enumerate_all(b_network_vars, evidence, b_network):
    if len(b_network_vars) == 0:
        return 1
    # get first of b_network_bars
    y = b_network_vars[0]
    # see if the node (y) is contained in the evidence
    if y in str(evidence):
        # get probability of y, given the values assigned to its parents in the evidence
        p_y = get_probability('+'+y, evidence, b_network)
        return p_y * enumerate_all(b_network_vars[1:], (evidence.append('+'+y)), b_network)
    else:
        # remove y multiplying its positive and negative probability:
        # P(y) * enumerate_all(b_network_vars[1:], (evidence + y), b_network)
        # +
        # P(-y) * enumerate_all(b_network_vars[1:], (evidence + -y), b_network)
        p_y = get_probability('+'+y, evidence, b_network)
        p_not_y = get_probability('-'+y, evidence, b_network)
        positive_result = p_y * enumerate_all(b_network_vars[1:], (evidence.append('+'+y)), b_network)
        negative_result = p_not_y * enumerate_all(b_network_vars[1:], (evidence.append('-'+y)), b_network)
        return positive_result + negative_result


def main():
    # example input
    file_input = fileinput.input()
    line = []
    for x in file_input:
        line.append(x)

    b_network = format_input_nodes(line[0])
    num_probabilities = int(line[1])
    num_queries = int(line[2+num_probabilities])

    # loop probabilities input
    for i in range(2, (2+num_probabilities)):
        b_network = format_input_probability(b_network, line[i])

    bn_sorted_nodes = toposort_flatten(bn_graph)

    print("\nb_network")
    p.pprint(b_network)
    print("\n")

    # loop queries input
    queries = []
    for i in range(3+num_probabilities, (3+num_probabilities+num_queries)):
        queries = format_input_queries(queries, line[i])

    print("queries")
    pprint(queries)
    print("\n")

    print("bn_graph")
    p.pprint(bn_graph)
    print("\n")

    print("toposort_bn_grapf")
    p.pprint(bn_sorted_nodes)
    print("\n")

    # print("Test...")
    #for test in queries:
        # enumeration_ask(test['query'], test['evidence'], b_network)

    search_probability_by_parents(b_network['+Alarm'], ['+Burglary'])


if __name__ == "__main__":
    main()