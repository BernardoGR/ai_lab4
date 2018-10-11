import fileinput
import pprint as p
import time
from pprint import pprint

debug = False


def format_input_nodes(line):
    # remove white spaces
    line = "".join(line.split())

    b_network = {}
    for node in line.split(","):
        b_network[node] = []
    return b_network


def format_input_probability(b_network, line):
    # remove white spaces
    line = "".join(line.split())
    # split on '=' and on '|' chars
    line_eq_split = line.split("=")
    line_pipe_split = line_eq_split[0].split("|")
    node = line_pipe_split[0].replace("+", "").replace("-", "")
    parents = []
    if len(line_pipe_split) > 1:
        parents = line_pipe_split[1].split(",")
    probability = float(line_eq_split[1])

    b_network[node].append({'parents': parents, 'probability': probability})
    return b_network


def do_query(queries, line):
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

def main():
    # example input
    '''
    Test, Ill
    3
    +Ill = 0.001
    +Test|+Ill=0.9
    +Test|-Ill=0.05
    3
    +Ill
    -Ill|+Test
    +Test|+Ill
    '''
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

    p.pprint(b_network)

    # loop queries input
    queries = []
    for i in range(3+num_probabilities, (3+num_probabilities+num_queries)):
        queries = do_query(queries, line[i])

    pprint(queries)


if __name__ == "__main__":
    main()