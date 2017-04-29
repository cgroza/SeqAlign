import binarytree as bt

# known ultrametric matrix
test_matrix = [[0, 8, 8, 5, 3],
               [8, 0, 3, 8, 8],
               [8, 3, 0, 8, 8],
               [5, 8, 8, 0, 5],
               [3, 8, 8, 5, 0]]

def is_ultrametric(D):
    # For every i, j, k rows: max { D(i, j), D(j, k), D(i, k) } is not unique
    r = range(0, len(D))
    # Generate all possible i, j, k triplets were i != j != k
    distances = [[D[i][k], D[j][k], D[i][j]] for i in r for j in r for k in r
              if i != k and i != j and j != k]
    # Check the conditions against all triplets
    for d in distances:
        if d.count(max(d)) == 1:
            # unique max => nonultrametrich
            return False
    return True

def make_tree(D):
    r = range(0, len(D))
    pairs = [(i, j) for i in r for j in r if i < j]
    nodes = []
    while len(pairs) != 0:
        # look for the pair with the smallest distance
        for (i, j) in pairs:
            if D[i][j] == min([D[h][k] for (h,k) in pairs]):
                j_node = None
                i_node = None
                # check if the pair members are already in nodes
                for n in nodes:
                    # traverse node and see if it connects to either i or j
                    # choose the largest node (placed in front of the nodes list)
                    # and do not overwrite a newer large node with an older smaller one
                    # the tree is converted to a list for easy search
                    values = bt.convert(n)
                    if i in values:
                        i_node = n
                    if j in values:
                        j_node = n

                # if not, assign them to nodes
                if not j_node:
                    j_node = bt.Node(j)

                if not i_node:
                    i_node = bt.Node(i)

                # finally, join the created or found nodes by the root
                # NOTE: make node values -1 to avoid distance and coordinate conflict
                # this could be solved by mapping the (i,j) coordinates to alphabetic names
                root = bt.Node("D({},{})={}".format(i, j, str(D[i][j])))
                root.left = j_node
                root.right = i_node
                # place the node in front of the list
                # this naturally ensures that complete nodes are in front and incomplete nodes in the tail
                nodes.insert(0, root)
                pairs.remove((i, j))

    return nodes[0]

if __name__ == "__main__":
    bt.pprint(make_tree(test_matrix))
