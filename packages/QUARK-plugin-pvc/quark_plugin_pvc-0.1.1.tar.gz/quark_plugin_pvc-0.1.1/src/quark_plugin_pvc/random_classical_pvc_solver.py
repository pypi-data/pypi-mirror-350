import random
from dataclasses import dataclass

from quark.core import Core, Data, Result
from quark.interface_types import Graph, Other


@dataclass
class RandomClassicalPvcSolver(Core):
    def preprocess(self, data: Graph) -> Result:
        graph = data.as_nx_graph()
        # Deep copy since we are modifying the graph. This ensures that the original graph remains unchanged
        # with a different graph
        mapped_problem = graph.copy()

        # We always start at the base node
        current_node = ((0, 0), 1, 1)
        idx = 1

        tour = {current_node + (0,): 1}  # (0,) is the timestep we visit this node

        # Tour needs to cover all nodes, if there are 2 nodes left we can finish since these 2 nodes belong
        # to the same seam
        while len(mapped_problem.nodes) > 2:
            # Get the random neighbor edge from the current node
            next_node = random.choice(
                [
                    x
                    for x in mapped_problem.edges(current_node[0], data=True)
                    if x[1][0] != current_node[0][0]
                    and x[2]["c_start"] == current_node[1]
                    and x[2]["t_start"] == current_node[2]
                ]
            )
            next_node = (next_node[1], next_node[2]["c_end"], next_node[2]["t_end"])

            # Make the step - add distance to cost, add the best node to tour,
            tour[next_node + (idx,)] = 1

            # Remove all node of that seam
            to_remove = [x for x in mapped_problem.nodes if x[0] == current_node[0][0]]
            for node in to_remove:
                mapped_problem.remove_node(node)

            current_node = next_node
            idx += 1

        # Tour needs to look like {((0, 0), 1, 1, 0): 1,((3, 1), 1, 0, 1): 1,((2, 1), 1, 1, 2): 1,((4, 4), 1, 1, 3): 1}
        # ((0, 0), 1, 1, 0): 1 = ((seam, node), config, tool, timestep): yes we visit this
        self._tour = tour

        return Data(None)

    def postprocess(self, data: None) -> Result:
        filtered_tour = [x[0] for x in self._tour.items() if x[1] == 1]
        filtered_tour.sort(key=lambda x: x[-1])
        filtered_tour = [x[:-1] for x in filtered_tour]

        return Data(Other(filtered_tour))
