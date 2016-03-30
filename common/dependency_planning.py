"""Check for any dependencies between a set of tasks or functions"""
from __future__ import print_function
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # nopep8


class DependencyResolver(object):

    """Determines the optimal order to run a set of tasks"""

    def __init__(self):
        self.dependencies = {}
        self.sol = None

    def add_task(self, task):
        """Add a taski (e.g node)"""
        if task not in self.dependencies:
            self.dependencies[task] = []

    def add_dep(self, task, dep):
        """
        Add a dependency (e.g. edge)
            - if the task or dep hasn't been added, they will also be added
        """

        self.add_task(dep)
        self.add_task(task)
        self.dependencies[task].append(dep)

    def visualize(self, out_file='out.png'):
        """Visualize the graph"""
        graph = nx.DiGraph()
        for task in self.dependencies.keys():
            for dep in self.dependencies[task]:
                graph.add_edges_from([(dep, task)])
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos, arrows=True, width=2)
        # nx.draw_networkx_edge_labels(graph, pos)
        nx.draw(graph, pos, node_size=3000)
        plt.savefig(out_file)

    def _dep_resolve(self, node, resolved, unresolved):
        """Solve the problem"""
        unresolved.append(node)
        for edge in self.dependencies[node]:
            if edge not in resolved:
                if edge in unresolved:
                    raise Exception(
                        'Circular reference detected: %s -&gt; %s'
                        % (node.name, edge.name))
                self._dep_resolve(edge, resolved, unresolved)
        resolved.append(node)
        unresolved.remove(node)
        return resolved

    def generate_solution(self, goal):
        """Generates the solution for running goal"""
        self.sol = self._dep_resolve(goal, [], [])

    def validate_solution(self, path, completed=None):
        """Validates that we found a feasible and optimal solution"""
        if completed is None:
            completed = []
        print("Analyzing solution:")
        print(path)
        print(completed)
        while len(path) > 0:
            cur = path[0]
            if cur in completed:
                print("Solution suboptimal... repeating task", cur)
            del path[0]
            for dep in self.dependencies[cur]:
                if dep == cur:
                    # Circular error
                    return False
                elif dep not in completed:
                    print("Cannot do", cur, "until", dep)
                    return False
            completed.append(cur)
        return True
