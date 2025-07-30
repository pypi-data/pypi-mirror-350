import networkx as nx
import matplotlib.pyplot as mpl_p


def form(n=4, kind="circular"):
    if kind == "linear":
        return linear_graph(n)
    elif kind == "circular":
        return circular_graph(n)
    elif kind == "random":
        return random_graph(n)
    else:
        raise ValueError(f"kind must be 'linear', 'circular' or 'random'; not {kind}.")


def linear_graph(n=4):
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(n)])
    graph.add_edges_from([[i, i+1] for i in range(n-1)])
    return graph


def circular_graph(n=4):
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(n)])
    graph.add_edges_from([[i, (i+1)%n] for i in range(n)])
    return graph


def random_graph(n=4):
    from random import randrange, sample
    graph = nx.Graph()
    verticies = {i for i in range(n)}
    graph.add_nodes_from(verticies)
    edges = []
    for i in range(n):
        vertex_rank = randrange(1, n//2)
        for _ in range(vertex_rank):
            edges.append((i, sample(sorted(verticies-{i}), 1)[0]))
    graph.add_edges_from(set(edges))
    return graph


def draw(graph, with_labels=True):
    nx.draw(graph, with_labels=with_labels)
    mpl_p.show()
