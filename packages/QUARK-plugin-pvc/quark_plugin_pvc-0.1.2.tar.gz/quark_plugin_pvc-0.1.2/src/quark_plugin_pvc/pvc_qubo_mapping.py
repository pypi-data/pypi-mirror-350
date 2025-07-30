import itertools
import logging
from dataclasses import dataclass
from typing import DefaultDict, override

import numpy as np
from quark.core import Core, Data, Result
from quark.interface_types import Graph, Qubo
from quark.interface_types.other import Other


@dataclass
class PvcQuboMapping(Core):
    """A module for mapping a graph to a QUBO formalism for the PVC problem."""

    lagrange_factor: float

    @override
    def preprocess(self, data: Graph) -> Result:
        """
        Preprocess the graph data to create a QUBO representation of the PVC problem.

        :param data: Graph data containing the problem to be solved.
        :return: A QUBO representation of the problem.
        """
        # Inspired by https://dnx.readthedocs.io/en/latest/_modules/dwave_networkx/algorithms/tsp.html

        self._graph = data.as_nx_graph()
        problem = self._graph

        # Estimate lagrange if not provided
        n = problem.number_of_nodes()
        timesteps = int((n - 1) / 2 + 1)

        # Get the number of different configs and tools
        config = [x[2]["c_start"] for x in problem.edges(data=True)]
        config = list(set(config + [x[2]["c_end"] for x in problem.edges(data=True)]))

        tool = [x[2]["t_start"] for x in problem.edges(data=True)]
        tool = list(set(tool + [x[2]["t_end"] for x in problem.edges(data=True)]))

        if problem.number_of_edges() > 0:
            weights = [x[2]["weight"] for x in problem.edges(data=True)]
            weights = list(filter(lambda a: a != max(weights), weights))
            lagrange = sum(weights) / len(weights) * timesteps
        else:
            lagrange = 2

        lagrange *= self.lagrange_factor
        logging.info(f"Selected lagrange is: {lagrange}")

        if n in (1, 2) or len(problem.edges) < n * (n - 1) // 2:
            msg = "graph must be a complete graph with at least 3 nodes or empty"
            raise ValueError(msg)

        # Creating the QUBO
        q = DefaultDict(float)

        # We need to implement the following constrains:
        # Only visit 1 node of each seam
        # Don`t visit nodes twice (even if their config/tool is different)
        # Only visit a single node in a single timestep
        # We only need to visit base node once since this path from last node to base node is unique anyway

        # Constraint to only visit a node/seam once
        for node in problem:  # for all nodes in the graph
            for pos_1 in range(timesteps):  # for number of timesteps
                for t_start in tool:
                    for c_start in config:
                        q[
                            (
                                (node, c_start, t_start, pos_1),
                                (node, c_start, t_start, pos_1),
                            )
                        ] -= lagrange
                        for t_end in tool:
                            # For all configs and tools
                            for c_end in config:
                                if c_start != c_end or t_start != t_end:
                                    q[
                                        (
                                            (node, c_start, t_start, pos_1),
                                            (node, c_end, t_end, pos_1),
                                        )
                                    ] += 1.0 * lagrange
                                for pos_2 in range(pos_1 + 1, timesteps):
                                    # Penalize visiting same node again in another timestep
                                    q[
                                        (
                                            (node, c_start, t_start, pos_1),
                                            (node, c_end, t_end, pos_2),
                                        )
                                    ] += 2.0 * lagrange
                                    # Penalize visiting other node of same seam
                                    if node != (0, 0):
                                        # (0,0) is the base node, it is not a seam
                                        # Get the other nodes of the same seam
                                        other_seam_nodes = [
                                            x
                                            for x in problem.nodes
                                            if x[0] == node[0] and x[1] != node
                                        ]
                                        for other_seam_node in other_seam_nodes:
                                            # Penalize visiting other node of same seam
                                            q[
                                                (
                                                    (node, c_start, t_start, pos_1),
                                                    (
                                                        other_seam_node,
                                                        c_end,
                                                        t_end,
                                                        pos_2,
                                                    ),
                                                )
                                            ] += 2.0 * lagrange

        # Constraint to only visit a single node in a single timestep
        for pos in range(timesteps):
            for node_1 in problem:
                for t_start in tool:
                    for c_start in config:
                        q[
                            (
                                (node_1, c_start, t_start, pos),
                                (node_1, c_start, t_start, pos),
                            )
                        ] -= lagrange
                        for t_end in tool:
                            for c_end in config:
                                for node_2 in set(problem) - {
                                    node_1
                                }:  # for all nodes except node1 -> node1
                                    q[
                                        (
                                            (node_1, c_start, t_start, pos),
                                            (node_2, c_end, t_end, pos),
                                        )
                                    ] += lagrange

        # Objective that minimizes distance
        for u, v in itertools.combinations(problem.nodes, 2):
            for pos in range(timesteps):
                for t_start in tool:
                    for t_end in tool:
                        for c_start in config:
                            for c_end in config:
                                nextpos = (pos + 1) % timesteps
                                edge_u_v = next(
                                    item
                                    for item in list(problem[u][v].values())
                                    if item["c_start"] == c_start
                                    and item["t_start"] == t_start
                                    and item["c_end"] == c_end
                                    and item["t_end"] == t_end
                                )
                                # Since it is the other direction we switch start and end of tool and config
                                edge_v_u = next(
                                    item
                                    for item in list(problem[v][u].values())
                                    if item["c_start"] == c_end
                                    and item["t_start"] == t_end
                                    and item["c_end"] == c_start
                                    and item["t_end"] == t_start
                                )
                                # Going from u -> v
                                q[
                                    (
                                        (u, c_start, t_start, pos),
                                        (v, c_end, t_end, nextpos),
                                    )
                                ] += edge_u_v["weight"]
                                # Going from v -> u
                                q[
                                    (
                                        (v, c_end, t_end, pos),
                                        (u, c_start, t_start, nextpos),
                                    )
                                ] += edge_v_u["weight"]

        logging.info("Created Qubo")

        return Data(Qubo.from_dict(q))

    @override
    def postprocess(self, data: Other) -> Result:
        """
        Postprocess the QUBO solution to extract the route.

        :param data: The QUBO solution data.
        :return: The parsed route as a Data object.
        """
        d = data.data

        nodes = list(self._graph.nodes())
        start = ((0, 0), 1, 1)
        route: list = [None] * int((len(self._graph) - 1) / 2 + 1)
        visited_seams = []

        if sum(value == 1 for value in d.values()) > len(route):
            logging.warning("Result is longer than route! This might be problematic!")

        # Prevent duplicate node entries by enforcing only one occurrence per node along route
        for (node, config, tool, timestep), val in d.items():
            if val and (node[0] not in visited_seams):
                if route[timestep] is not None:
                    visited_seams.remove(route[timestep][0][0])
                route[timestep] = (node, config, tool)
                visited_seams.append(node[0])

        # Fill missing values in the route
        if None in route:
            logging.info(f"Route until now is: {route}")
            nodes_unassigned = [
                (node, 1, 1) for node in nodes if node[0] not in visited_seams
            ]
            nodes_unassigned = list(np.random.permutation(nodes_unassigned))
            logging.info(nodes_unassigned)
            logging.info(visited_seams)
            logging.info(nodes)
            for idx, node in enumerate(route):
                if node is None:
                    route[idx] = nodes_unassigned.pop(0)

        # Cycle solution to start at provided start location
        if start is not None and route[0] != start:
            idx = route.index(start)
            route = route[idx:] + route[:idx]

        parsed_route = " ->\n".join(
            [
                f" Node {visit[0][1]} of Seam {visit[0][0]} using config "
                f" {visit[1]} & tool {visit[2]}"
                for visit in route
            ]
        )
        logging.info(f"Route found:\n{parsed_route}")

        return Data(Other(route))
