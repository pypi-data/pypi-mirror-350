#  Copyright 2021 The QUARK Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import itertools
import logging
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import override

import networkx as nx
from quark.core import Core, Data, Result
from quark.interface_types import Graph, Other

from quark_plugin_pvc.createReferenceGraph import create_graph


@dataclass
class PvcGraphProvider(Core):
    """
    In modern vehicle manufacturing, robots take on a significant workload, including performing welding
    jobs, sealing welding joints, or applying paint to the car body. While the robot’s tasks vary widely,
    the objective remains the same: Perform a job with the highest possible quality in the shortest amount
    of time, optimizing efficiency and productivity on the manufacturing line.

    For instance, to protect a car’s underbody from corrosion, exposed welding seams are sealed
    by applying a polyvinyl chloride layer (PVC). The welding seams need to be traversed by a robot to
    apply the material. It is related to TSP, but different and even more complex in some aspects.

    The problem of determining the optimal route for robots to traverse all seams shares similarities
    with Traveling Salesperson Problem (TSP), as it involves finding the shortest possible route to
    visit multiple locations. However, it introduces additional complexities, such as different tool
    and configuration requirements for each seam, making it an even more challenging problem to solve.
    """

    seams: int = 3

    @override
    def preprocess(self, data: None) -> Result:
        """
        Preprocesses the data for the PVC problem.

        :param data: None
        :return: Data object containing the graph
        """
        # Read in the original graph

        data_path = os.path.join(os.path.dirname(__file__), "data")
        graph_path = os.path.join(data_path, "reference_graph.gpickle")

        if not Path(graph_path).is_file():
            create_graph(data_path)

        with open(
            graph_path,
            "rb",
        ) as file:
            graph = pickle.load(file)

        # Get number of seam in graph
        seams_in_graph = list({x[0] for x in graph.nodes})
        seams_in_graph.sort()
        seams_in_graph.remove(0)  # Always need the base node 0 (which is not a seam)

        if len(seams_in_graph) < self.seams:
            logging.info("Too many seams! The original graph has less seams than that!")

        unwanted_seams = seams_in_graph[-len(seams_in_graph) + self.seams :]
        unwanted_nodes = [x for x in graph.nodes if x[0] in unwanted_seams]

        for node in unwanted_nodes:
            graph.remove_node(node)

        if not nx.is_strongly_connected(graph):
            logging.error("Graph is not connected!")
            raise ValueError("Graph is not connected!")

        # Gather unique configurations and tools
        config = [x[2]["c_start"] for x in graph.edges(data=True)]
        config = list(set(config + [x[2]["c_end"] for x in graph.edges(data=True)]))
        tool = [x[2]["t_start"] for x in graph.edges(data=True)]
        tool = list(set(tool + [x[2]["t_end"] for x in graph.edges(data=True)]))

        # Fill the rest of the missing edges with high values
        current_edges = [
            (
                edge[0],
                edge[1],
                edge[2]["t_start"],
                edge[2]["t_end"],
                edge[2]["c_start"],
                edge[2]["c_end"],
            )
            for edge in graph.edges(data=True)
        ]
        all_possible_edges = list(itertools.product(list(graph.nodes), repeat=2))
        all_possible_edges = [
            (edges[0], edges[1], t_start, t_end, c_start, c_end)
            for edges in all_possible_edges
            for c_end in config
            for c_start in config
            for t_end in tool
            for t_start in tool
            if edges[0] != edges[1]
        ]

        missing_edges = [
            item for item in all_possible_edges if item not in current_edges
        ]

        # Add these edges with very high values
        for edge in missing_edges:
            graph.add_edge(
                edge[0],
                edge[1],
                c_start=edge[4],
                t_start=edge[2],
                c_end=edge[5],
                t_end=edge[3],
                weight=100000,
            )

        logging.info("Created PVC problem with the following attributes:")
        logging.info(f" - Number of seams: {self.seams}")
        logging.info(f" - Number of different configs: {len(config)}")
        logging.info(f" - Number of different tools: {len(tool)}")

        self._graph = graph
        return Data(Graph.from_nx_graph(graph.copy()))

    @override
    def postprocess(self, data: Other) -> Result:
        """
        Converts solution dictionary to list of visited seams.

        :param solution: Unprocessed solution
        :return: Processed solution and the time it took to process it
        """

        route = data.data

        # Check if all seams are visited in route
        visited_seams = {seam[0][0] for seam in route if seam is not None}

        if len(visited_seams) == len(route):
            logging.info(
                f"All {len(route) - 1} seams and "
                "the base node got visited (We only need to visit 1 node per seam)"
            )
        else:
            logging.error(f"Only {len(visited_seams) - 1} got visited")
            raise ValueError(f"Only {len(visited_seams) - 1} got visited")

        # Get the total distance
        total_dist = 0
        for idx, _ in enumerate(route[:-1]):
            edge = next(
                item
                for item in list(self._graph[route[idx][0]][route[idx + 1][0]].values())
                if item["c_start"] == route[idx][1]
                and item["t_start"] == route[idx][2]
                and item["c_end"] == route[idx + 1][1]
                and item["t_end"] == route[idx + 1][2]
            )
            dist = edge["weight"]
            total_dist += dist
        logging.info(f"Total distance (without return): {total_dist}")

        # Add distance between start and end point to complete cycle
        return_edge = next(
            item
            for item in list(self._graph[route[0][0]][route[-1][0]].values())
            if item["c_start"] == route[0][1]
            and item["t_start"] == route[0][2]
            and item["c_end"] == route[-1][1]
            and item["t_end"] == route[-1][2]
        )
        return_distance = return_edge["weight"]
        logging.info(f"Distance between start and end: {return_distance}")

        # Get distance for full cycle
        distance = total_dist + return_distance
        logging.info(f"Total distance (including return): {distance}")

        return Data(Other(distance))

    # def visualize_solution(self, path: str):
    #     """
    #     Plot a graph representing the possible locations where seams can start or end, with arrows representing either idle movements or the sealing of a seam

    #     :param processed_solution: The solution already processed by :func:`process_solution`, a list of tuples representing seam start points and the config and tool needed to seal the seam.
    #     :param path: File path for the plot
    #     :returns: None
    #     """
    #     NODE_SIZE = 300  # Default=300
    #     EDGE_WIDTH = 1.0  # Default=1.0
    #     FONT_SIZE = 12  # Default=12

    #     highest_node_id = max(node[1] for node in self._graph.nodes())
    #     G = nx.MultiDiGraph()
    #     G.add_nodes_from(range(highest_node_id + 1))
    #     pos = nx.circular_layout(G)

    #     tools = set()
    #     configs = set()
    #     current_node = 0
    #     for (seam1, node1), config, tool in self._route[1:]:
    #         config = config - 1
    #         tools.add(tool)
    #         configs.add(config)
    #         (seam2, node2) = next(
    #             (seam, node)
    #             for (seam, node) in self._graph.nodes()
    #             if seam == seam1 and not node == node1
    #         )
    #         assert seam1 == seam2, "This is bad"
    #         if not current_node == node1:
    #             G.add_edge(current_node, node1, color=7, width=EDGE_WIDTH, style=-1)
    #         G.add_edge(node1, node2, color=tool, width=2 * EDGE_WIDTH, style=config)
    #         current_node = node2

    #     # The 8 here controls how many edges between the same two nodes are at
    #     # most drawn with spacing between them before drawing them on top of each
    #     # other to avoid cluttering
    #     connectionstyle = [f"arc3,rad={r}" for r in itertools.accumulate([0.15] * 8)]
    #     style_options = ["solid", "dotted", "dashed", "dashdot"]
    #     cmap = plt.cm.Dark2
    #     tools = list(tools)
    #     configs = list(configs)
    #     legend_elements = (
    #         [
    #             Line2D(
    #                 [0],
    #                 [0],
    #                 color=cmap(7),
    #                 lw=EDGE_WIDTH,
    #                 ls=":",
    #                 label="Idle Movement",
    #             )
    #         ]
    #         + [Patch(facecolor=cmap(i), label=f"Tool {i}") for i in tools]
    #         + [
    #             Line2D(
    #                 [0],
    #                 [0],
    #                 color="black",
    #                 lw=2 * EDGE_WIDTH,
    #                 ls=style_options[i % len(style_options)],
    #                 label=f"Config {i + 1}",
    #             )
    #             for i in configs
    #         ]
    #     )
    #     colors = nx.get_edge_attributes(G, "color").values()
    #     widths = nx.get_edge_attributes(G, "width").values()
    #     styles = [
    #         ":" if i == -1 else style_options[i % len(style_options)]
    #         for i in nx.get_edge_attributes(G, "style").values()
    #     ]

    #     nx.draw_networkx(
    #         G,
    #         pos,
    #         node_size=NODE_SIZE,
    #         font_size=FONT_SIZE,
    #         style=list(styles),
    #         edge_color=colors,
    #         edge_cmap=cmap,
    #         width=list(widths),
    #         connectionstyle=connectionstyle,
    #     )

    #     plt.legend(handles=legend_elements)
    #     plt.savefig(path)
    #     plt.close()
