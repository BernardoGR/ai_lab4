import fileinput
import pprint as p
import time
from pprint import pprint
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
        bn_graph[node] = set(str(parents).split(","))
    else:
        bn_graph[node] = set()
    probability = float(line_eq_split[1])
    inverse_probability = 1 - probability
    # append new nodes
    b_network[node].append({str(parents): probability})
    if inverse_node != "":
        b_network[inverse_node].append({str(parents): inverse_probability})
    return b_network


def search_probability_by_parents(node, parent_values=None):
    if parent_values:
        for parent in parent_values:
            node = list(filter(lambda x: parent in list(x.keys())[0], node))
    print(node)


def do_query(queries, line):
    # remove white spaces
    line = "".join(line.split())
    # split on '|'
    line_pipe_split = line.rstrip().split('|')
    query = line_pipe_split[0]
    evidence = []
    if len(line_pipe_split) > 1:
        evidence = line_pipe_split[1].split(',')

    queries.append({str(query) : evidence})

    return queries

'''
def conditional_prob(query, evidence):
   
    return cond_prob_res


def chain_rule(query, evidence):

    return chain_rule_res


def total_probability (query, evidence):

    return total_probability_res
'''


def enumeration_ask(query, evidence, b_network):
    cpt = []
    list_query = list(query.keys())[0].split(',')
    for q in list_query:
        enumerate_all(b_network['vars'], q, b_network, evidence)


def enumerate_all(b_network_vars, q, evidence, b_network):
    if len(b_network_vars):
        return 1
    y = b_network_vars[0]
    if y in evidence:
        # sacar parents de y
        y_parents = list(b_network["+"+y].keys())[0].replace("+", "").replace("-", "").split(',')
        # lista de parents no contenidos en la evidencia
        parents_not_evidence = list(filter(lambda parent: parent not in str(evidence), y_parents))
        return enumerate_all(parents_not_evidence,  q, evidence, b_network) * enumerate_all(b_network_vars[1:],  q, evidence, b_network)
    else:

        return


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
        queries = do_query(queries, line[i])

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
    # search_probability_by_parents(b_network['+Alarm'], ['+Earthquake','+Burglary'])


if __name__ == "__main__":
    main()