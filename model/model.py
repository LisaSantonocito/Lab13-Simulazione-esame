import copy

from geopy import distance
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapS = {}
        self.path = []
        self.path_edge = []
        self.solBest = 0

    def getAllYear(self):
        return DAO.getAllYear()

    def getAllForme(self, year):
        return DAO.getAllForme(year)

    def buildGraph(self, year, shape):
        self._nodes = DAO.getAllState()
        self._idMapS = {s.id: s for s in self._nodes}
        self._grafo.add_nodes_from(self._nodes)
        edges = DAO.getAllEdge(self._idMapS)

        self._grafo.add_edges_from(edges, weight = 0)

        edges_pesati = DAO.getAllEdgeW(self._idMapS, year, shape)
        for e in edges_pesati:
            if self._grafo.has_edge(e[0],e[1]):
                self._grafo[e[0]][e[1]]["weight"]=e[2]


    def getSumW_node(self):
        result = []
        for n in self._grafo.nodes:
            somma = 0
            for vicino in self._grafo.neighbors(n):
                somma += self._grafo[n][vicino]["weight"]
            result.append((n,somma))
        return result

    def getNodes(self):
        return self._grafo.nodes()

    def getEdges(self):
        return self._grafo.edges()

    def getNumNE(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def computePath(self):
        self.path = []
        self.path_edge = []

        for n in self._grafo.nodes():
            partial = []
            partial.append(n)
            self.ricorsione(partial, [])

    def ricorsione(self, partial, partial_edge):
        n_last = partial[-1]

        neighbors = self.getAdmissibleNeighbs(n_last, partial_edge)

        # stop
        if len(neighbors) == 0:
            weight_path = self.computeWeightPath(partial_edge)
            if weight_path > self.solBest:
                self.solBest = weight_path + 0.0
                self.path = partial[:]
                self.path_edge = partial_edge[:]
            return

        for n in neighbors:
            partial_edge.append((n_last, n, self._grafo.get_edge_data(n_last, n)['weight']))
            partial.append(n)

            self.ricorsione(partial, partial_edge)
            partial.pop()
            partial_edge.pop()

    def getAdmissibleNeighbs(self, n_last, partial_edges):
        all_neigh = self._grafo.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if len(partial_edges) != 0:
                if e[2]["weight"] > partial_edges[-1][2]:
                    result.append(e[1])
            else:
                result.append(e[1])
        return result
    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += distance.geodesic((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km
        return weight

    def get_distance_weight(self, e):
        return distance.geodesic((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km
