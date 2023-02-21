import sys

input_file = sys.argv[1];
output_file = sys.argv[2];

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        self.vertices[vertex] = []

    def add_edge(self, vertex1, vertex2):
        self.vertices[vertex1].append(vertex2)
        self.vertices[vertex2].append(vertex1)

    def edges(self):
        return [(u, v) for u in self.vertices
                       for v in self.vertices[u] if u < v]

    def len(self):
        return len(self.vertices)


def create_graph(filename):
    with open(filename, 'r') as input:
        graph_info = input.readline().split(" ")

        v = int(graph_info[0])
        k = int(graph_info[1])
        
        edges = []
        vertex_number = 1

        for line in input:
            vertices = map(int, line.split(" "))
            edges.append((vertex_number, vertices))
            vertex_number += 1

        g = Graph()

        for i in range(1, v + 1):
            g.add_vertex(i)

        for u, vertices in edges:
            for v in vertices:
                g.add_edge(u, v)

    return g, k


def reduce_kclique_to_sat(g, k):
    clauses = []

    for i in range(1, k + 1):
        clauses.append([(i-1) * g.len() + j + 1 for j in range(g.len())])

    for i in range(1, k):
        for j in range(i + 1, k + 1):
            for l in range(g.len()):
                clauses.append([-(i - 1) * g.len() - l -1, -(j - 1) * g.len() - l - 1])

    for i in range(1, k):
        for j in range(i + 1, k + 1):
            for u in range(g.len()):
                for v in range(g.len()):
                    vertices = list(g.vertices.keys())
                    if ((vertices[u], vertices[v]) not in g.edges()
                        and (vertices[v], vertices[u]) not in g.edges()
                        and u != v):
                        clauses.append(
                            [-(i - 1) * g.len() - u - 1, (j - 1) * g.len() - v - 1])

    final_format = ""
    final_format += "p cnf " + str(k * g.len()) + " " + str(len(clauses)) + "\n"
    for clause in clauses:
        final_format += " ".join(map(str, clause)) + " 0\n"

    return final_format


def write_to_file(filename, result):
    with open(filename, 'w') as output:
        output.write(result)


graph_info = create_graph(input_file)
write_to_file(output_file, reduce_kclique_to_sat(*graph_info))
