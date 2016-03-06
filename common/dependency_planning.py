import networkx as nx
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class DependencyResolver(object):
    def __init__(self):
        self.dependencies = {}
    
    def add_task(self, task):
        if task not in self.dependencies:
            self.dependencies[task] = []
    
    def add_dep(self, task, dep):
        self.add_task(dep)
        self.add_task(task)
        self.dependencies[task].append(dep)
    
    def visualize(self):
        G = nx.DiGraph()
        for task in self.dependencies.keys():
            for dep in self.dependencies[task]:
                G.add_edges_from([(dep, task)])
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos, arrows=True, width=2)
        #nx.draw_networkx_edge_labels(G, pos)
        nx.draw(G, pos, node_size=3000)
        plt.savefig('out.png')

    def _dep_resolve(self, node, resolved, unresolved):
        unresolved.append(node)
        for edge in self.dependencies[node]:
            if edge not in resolved:
                if edge in unresolved:
                    raise Exception('Circular reference detected: %s -&gt; %s' % (node.name, edge.name))
                self._dep_resolve(edge, resolved, unresolved)
        resolved.append(node)
        unresolved.remove(node)
        return resolved
        
    def generate_solution(self, goal):
        self.sol = self._dep_resolve(goal, [], [])
        
    def validate_solution(self, path, completed):
        print "Analyzing solution:"
        print path
        print completed
        while len(path) > 0:
            cur = path[0]
            if cur in completed:
                print "Solution suboptimal... repeating task", cur
            del path[0]
            for dep in self.dependencies[cur]:
                if dep == cur:
                    # Circular error
                    return False
                elif dep not in completed:
                    print "Cannot do", cur, "until", dep
                    return False
            completed.append(cur)
        return True

    def visualize_solution(sol=None):
        if sol is None:
            sol = self.sol
        G = nx.DiGraph()
        for task in self.dependencies.keys():
            for dep in self.dependencies[task]:
                G.add_edges_from([(dep, task)])
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos, arrows=True, width=2)
        #nx.draw_networkx_edge_labels(G, pos)
        nx.draw(G, pos, node_size=3000)
        plt.savefig('out.png')

def test_case():
    dr = DependencyResolver()
    dr.add_task('arithmetic mean')
    dr.add_task('geometric mean')
    dr.add_task('median')
    dr.add_task('quartiles')
    dr.add_task('standard deviation')
    dr.add_dep('downside standard deviation', 'arithmetic mean')
    dr.add_dep('MAD', 'arithmetic mean')
    dr.add_dep('sharpe ratio', 'standard deviation')
    dr.add_dep('sortino ratio', 'downside standard deviation')
    dr.visualize()
    dr.generate_solution('MAD')
    print dr.sol
    dr.validate_solution(dr.sol, [])


if __name__ == "__main__":
    test_case()
