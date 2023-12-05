import random
import networkx as nx
import DynamicProgramming as dp
import BranchAndBound as bnb
import time
import tracemalloc

TC_PLANS = [["SMALL", 10000, 75], ["MEDIUM", 100000, 100], ["LARGE", 1000000, 125]]

def generateTree(numVerticesDP, numVerticesBnB):
    # Using a graph that will be modified so that it becomes a tree
    t_dp = nx.Graph()
    t_bnb = nx.Graph()

    # Add vertices (nodes)
    t_dp.add_nodes_from(range(1, numVerticesDP + 1))
    t_bnb.add_nodes_from(range(1, numVerticesBnB+ 1))

    # Create a list of vertices and randomly shuffle it
    vertices = list(range(2, numVerticesDP + 1))
    random.shuffle(vertices)

    # Connect each vertex to a random parent to form a tree
    for v in vertices:
        parent = random.choice(range(1, v))
        t_dp.add_edge(parent, v)
        if parent <= numVerticesBnB and v <= numVerticesBnB:
            t_bnb.add_edge(parent, v)

    return t_dp, t_bnb

def generateInput(tcNumber, numVerticesDP, numVerticesBnB):
    t_dp, t_bnb = generateTree(numVerticesDP, numVerticesBnB)

    # Create file input for DP
    f = open("{tcNumber}_dp.in".format(tcNumber=tcNumber), "w")
    f.write("{numVertices}\n".format(numVertices = len(t_dp)))
    tree_dp_arr = nx.to_dict_of_lists(t_dp)
    for _, neighbors in tree_dp_arr.items():
        line = f"{' '.join(map(str, neighbors))}\n"
        f.write(line) 

    # Create file input for BnB
    f = open("{tcNumber}_bnb.in".format(tcNumber=tcNumber), "w")
    f.write("{numVertices}\n".format(numVertices = len(t_bnb)))
    t_bnb_array = nx.to_numpy_array(t_bnb)
    for neighbor in t_bnb_array:
        for i in range(len(neighbor)):
            if (neighbor[i] == 1.0):
                    f.write("{edge} ".format(edge = (i + 1)))
        f.write("\n")

    return t_dp, t_bnb

def computeMVC(G, algo):
    startTime = time.time()
    tracemalloc.start()

    minSize = 0
    if (algo == 'DP'):
        minSize = dp.minSizeVertexCover(G, len(G))
    elif (algo == 'BnB'):
        minSize = bnb.main(G)

    endTime = time.time()
    runningTime = endTime - startTime
    runningMemory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return minSize, runningTime, runningMemory

def generateOutput(tcNumber, numVerticesDP, numVerticesBnB):
    t_dp, t_bnb = generateInput(tcNumber, numVerticesDP, numVerticesBnB)

    # Compute MVC with Dynamic Programming
    minSizeDP, runningTimeDP, runningMemoryDP = computeMVC(t_dp, 'DP')

    # Compute with Branch And Bound
    minSizeBnB, runningTimeBnB, runningMemoryBnB = computeMVC(t_bnb, 'BnB')

    return minSizeDP, runningTimeDP, runningMemoryDP, minSizeBnB, runningTimeBnB, runningMemoryBnB

def main():
    for i in range(len(TC_PLANS)):
        f = open("{variance}.txt".format(variance=TC_PLANS[i][0].lower()), "w")
        minSizeDP, runningTimeDP, runningMemoryDP, minSizeBnB, runningTimeBnB, runningMemoryBnB = generateOutput((i+1), TC_PLANS[i][1], TC_PLANS[i][2])
        f.write('===== {variance} DATASET =====\n'.format(variance=TC_PLANS[i][0]))

        f.write('--- Dynamic Programming ---\n')
        f.write('Min Size: {minSize}\n'.format(minSize = minSizeDP))
        f.write('Running Time: {runningTime} s\n'.format(runningTime=runningTimeDP))
        f.write('Running Memory: {runningMemory} MB\n'.format(runningMemory=(runningMemoryDP[1] / 10**6)))

        f.write('--- Branch And Bound ---\n')
        f.write('Min Size: {minSize}\n'.format(minSize = minSizeBnB))
        f.write('Running Time: {runningTime} s\n'.format(runningTime=runningTimeBnB))
        f.write('Running Memory: {runningMemory} MB\n'.format(runningMemory=(runningMemoryBnB[1] / 10**6)))

        f.write('\n')

if __name__ == '__main__':
    main()