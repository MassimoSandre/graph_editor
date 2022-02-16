def mst(graph):    
    v = len(graph)

    selected = [False]*v

    n_arcs = 0

    selected[0] = True
    
    to_keep = []

    while (n_arcs<v-1):
        minimun = float("inf")
        x=None
        y=None
        for i in range(v):
            if selected[i]:
                for arc in graph[i].arcs:
                    n,w = arc[:2]
                    if not selected[graph.index(n)]:
                        if minimun > w:
                            minimun = w
                            x = graph[i]
                            y = n
        if y != None:
            to_keep.append((x,y))
            selected[graph.index(y)] = True
        n_arcs+=1
    
        

    for a in graph:
        for b in graph:
            if a != b:
                if (a,b) not in to_keep and (b,a) not in to_keep:
                    a.remove_arc(b,True)



def find_path(starting_node, ending_node,graph):
    distances = [float("inf")]*len(graph)
    compute_distance(starting_node, distances, graph)

    p = [ending_node]
    current_node = ending_node
    while distances[graph.index(current_node)] > 0:
        for arc in current_node.arcs:
            n,w = arc[:2]
            if distances[graph.index(n)] == distances[graph.index(current_node)] - w:
                current_node = n
                p.append(n)
                break # i only consider ONE of the possible shortest paths
    return p



def compute_distance(starting_node, results, graph):

    queue = [(starting_node, 0)]

    while len(queue) > 0:
        current_node, distance = queue.pop(0)
        if results[graph.index(current_node)] > distance:
            results[graph.index(current_node)] = distance
            for n in current_node.arcs:
                if distance + n[1] < results[graph.index(n[0])]:
                    queue.append((n[0], distance + n[1]))
            