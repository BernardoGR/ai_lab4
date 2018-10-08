import fileinput
import time

debug = False


def format_input(line):
    return


def do_query():
    return


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

    print(line)
    nodes = line[0]
    num_probabilities = int(line[1])
    num_queries = int(line[2+num_probabilities])
    print(nodes)
    print(num_probabilities)
    print(num_queries)

    for i in range(2, (2+num_probabilities)):
        # probability = format_input(file_input[i])
        print(line[i])

    for i in range(3+num_probabilities, (3+num_probabilities+num_queries)):
        # query = format_input(file_input[i])
        print(line[i])


if __name__ == "__main__":
    main()
