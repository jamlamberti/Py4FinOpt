"""Check for any dependencies between a set of tasks or functions"""
from __future__ import print_function
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

    def visualize(self):
        """Visualize the graph"""
        graph = nx.DiGraph()
        for task in self.dependencies.keys():
            for dep in self.dependencies[task]:
                graph.add_edges_from([(dep, task)])
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos, arrows=True, width=2)
        #nx.draw_networkx_edge_labels(graph, pos)
        nx.draw(graph, pos, node_size=3000)
        plt.savefig('out.png')

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

    def validate_solution(self, path, completed):
        """Validates that we found a feasible and optimal solution"""
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

def test_case():
    """A simple smoke test"""
    depr = DependencyResolver()
    depr.add_task('arithmetic mean')
    depr.add_task('geometric mean')
    depr.add_task('median')
    depr.add_task('quartiles')
    depr.add_task('standard deviation')
    depr.add_dep('downside standard deviation', 'arithmetic mean')
    depr.add_dep('MAD', 'arithmetic mean')
    depr.add_dep('sharpe ratio', 'standard deviation')
    depr.add_dep('sortino ratio', 'downside standard deviation')
    depr.visualize()
    depr.generate_solution('MAD')
    print(depr.sol)
    depr.validate_solution(depr.sol, [])


if __name__ == "__main__":
    test_case()
