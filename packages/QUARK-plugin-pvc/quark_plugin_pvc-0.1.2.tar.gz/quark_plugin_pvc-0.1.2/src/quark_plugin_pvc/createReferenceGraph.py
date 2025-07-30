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

import os
import pickle

import networkx as nx


def create_graph(dir_path: str):
    # Create the original graph as a MultiDiGraph
    graph = nx.MultiDiGraph()

    reference_data_path = os.path.join(dir_path, "reference_data.txt")
    graph_path = os.path.join(dir_path, "reference_graph.gpickle")

    with open(reference_data_path) as infile:
        for line in infile:
            line_elements = line.split()

            # Extract start and end attributes from line elements
            r_start, s_start, n_start, c_start, t_start, l_start = map(
                int, line_elements[1:7]
            )
            r_end, s_end, n_end, c_end, t_end, l_end = map(int, line_elements[9:15])
            duration = float(line_elements[17])

            # Handle missing or invalid data with default values
            if s_start == -1:
                s_start = 0
                t_start = 1  # TODO except of picking a hardcoded value here we should select 1 from the dataset itself
                c_start = 1
            if s_end == -1:
                s_end = 0
                t_end = 1
                c_end = 1
            if n_start == -1:
                n_start = 0
            if n_end == -1:
                n_end = 0

            # Reduce the number of tools and configurations for simplicity
            if c_end < 3 and c_start < 3 and t_start < 2 and t_end < 2:
                graph.add_edge(
                    (s_start, n_start),
                    (s_end, n_end),
                    c_start=c_start,
                    t_start=t_start,
                    c_end=c_end,
                    t_end=t_end,
                    weight=duration,
                )

    # Save the graph to a file in gpickle format
    with open(graph_path, "wb") as file:
        pickle.dump(graph, file, pickle.HIGHEST_PROTOCOL)
