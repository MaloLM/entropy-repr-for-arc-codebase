# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from abstract_and_reason.assets import manhattan_distance, calculate_center, shuffle_list, arc_agi_colormap
from .node import Node
from collections import Counter
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, board) -> None:
        """
        Initializes the Graph instance.

        Parameters:
        - board (list): A 2D list representing the grid of nodes. Each element is 
          associated with a node value.
        """
        self.board = board
        self.nodes = []
        self.color_map = arc_agi_colormap
        self._to_nodes()
        self._check_node_integrity()

        self.distribution = None
        self.entropies = None
        self.min_entropy = None
        self.max_entropy = None

        self._compute_distances()
        self._compute_distribution()
        self._compute_entropies()
        self._attach_entropies_to_connections()

    def _compute_distribution(self):
        """
        Computes the distribution of connections within the graph and stores it
        as a probability distribution. The distribution represents the relative
        frequency of each unique connection.
        """
        connections = []
        for node in self.nodes:
            for conn in node.connections:
                connections.append(
                    (node.value, conn.value, node.conn_dists[node.connections.index(conn)]))
                # connections.append((node.value, conn.value)) # enable in case you do not want distance as entropy computation param

        total_connections = len(connections)
        connection_counts = Counter(connections)
        self.distribution = {k: v/total_connections for k,
                             v in connection_counts.items()}

    def _compute_entropies(self):
        """
        Calculates the entropy values for each connection in the graph based on 
        the computed distribution and stores them. Additionally, it identifies 
        the minimum and maximum entropy values.
        """
        self.entropies = {k: -p * np.log2(p)
                          for k, p in self.distribution.items()}

        self.min_entropy = min(self.entropies.values()) if len(
            self.entropies.values()) > 0 else 0
        self.max_entropy = max(self.entropies.values()) if len(
            self.entropies.values()) > 0 else 0

    def _attach_entropies_to_connections(self):
        """
        Attaches the computed entropy and normalized entropy values to each connection 
        of each node. Normalizes entropy values to fall within a range of 0 to 1 
        using the min-max normalization technique.
        """
        if self.entropies is not None:
            for node in self.nodes:
                for i, connection in enumerate(node.connections):
                    res = (node.value, connection.value, node.conn_dists[i])
                    # res = (node.value, connection.value) # enable in case you do not want distance as entropy computation param
                    entropy = self.entropies[res]
                    node.entropies.append(entropy)
                    normalized_entropy = 1 - (
                        entropy - self.min_entropy) / (self.max_entropy - self.min_entropy)
                    node.norm_entropies.append(normalized_entropy)

                assert len(node.entropies) == len(
                    node.connections) and len(node.norm_entropies) == len(
                    node.connections), f"Bizzare... pas autant d'entropies que de connexions? {len(node.norm_entropies)} vs {len(node.connections)} et {len(node.entropies)} vs {len(node.connections)}"

    def _check_node_integrity(self):
        """
        Validates the integrity of the node connections to ensure that the total 
        number of connections matches the expected number for a fully connected 
        graph. Raises an assertion error if the check fails.
        """
        summing = 0
        for node in self.nodes:
            summing += len(node.connections)

            nb_nodes = len(self.nodes)

        assert summing == nb_nodes * \
            (nb_nodes-1), "Bizare ? Il y a un problème entre le nombre de connexions réelles et le nombre de connexions attendues..."

    def _to_nodes(self):
        """
        Converts the 2D grid (board) into nodes and populates the graph with these 
        nodes. Connects nodes based on their position in the grid.
        """
        for x, row in enumerate(self.board):
            for y, _ in enumerate(row):
                new_node = Node(self.board[x][y], x, y)
                self.nodes.append(new_node)
        self._connect_nodes()

    def _compute_distances(self):
        """
        Computes the Manhattan distances between each node and its connected nodes 
        and stores these distances in the nodes.
        """
        for node in self.nodes:
            center = node.get_node_center()
            for conn in node.connections:
                node_center = calculate_center(conn.coords)
                distance = manhattan_distance(
                    center[0], center[1], node_center[0], node_center[1])
                node.conn_dists.append(distance)

    def _connect_nodes(self):
        """
        Establishes connections between each pair of nodes in the graph to make 
        it fully connected, ensuring all nodes have bidirectional connections.
        """
        for current_node in self.nodes:
            for other_node in self.nodes:
                if other_node != current_node:
                    current_node.add_connection(other_node)
                    other_node.add_connection(current_node)

    def get_nodes_coords(self):
        """
        Returns the coordinates of all nodes in the graph.

        Returns:
        - list: A list of coordinates where each element represents the coordinates 
          of a node.
        """
        coords = []
        for node in self.nodes:
            coords.append(node.coords)
        return coords

    def graph_to_board(self):
        """
        Maps the graph's node values back onto the board, filling the 2D array with 
        node indices based on their positions.

        Returns:
        - np.ndarray: A 2D array with node values filled according to the graph's structure.
        """
        nb_nodes = len(self.nodes)
        colors_idx = [node for node in range(nb_nodes)]
        colors_idx = shuffle_list(colors_idx)
        filled_array = np.full(self.board.shape, -1)

        for i, node in enumerate(self.nodes):
            for coord in node.coords:
                x = coord[0]
                y = coord[1]
                filled_array[x][y] = colors_idx[i]

        return filled_array

    def draw(self):
        """
        Visualizes the graph using Matplotlib. Nodes are drawn as colored points, 
        and edges represent connections between nodes with widths proportional to 
        their normalized entropy values.
        """
        G = nx.Graph()

        for node in self.nodes:
            G.add_node(node, label=node.value)

        for node in self.nodes:
            for connected_node in node.connections:
                if not G.has_edge(node, connected_node):
                    entropy = node.norm_entropies[node.connections.index(
                        connected_node)]

                    G.add_edge(
                        node, connected_node, weight=entropy, alpha=entropy)

        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
        edge_alphas = [G[u][v]['alpha'] for u, v in G.edges()]

        max_weight = max(edge_weights) if edge_weights else 1

        edge_widths = [w / max_weight * 1 for w in edge_weights]

        plt.figure(figsize=(16, 12), facecolor="#2b2d31")

        pos = nx.spring_layout(G)

        node_colors = [self.color_map[node.value] for node in G.nodes()]

        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors)

        nx.draw_networkx_edges(G, pos, width=edge_widths,
                               edge_color='#dddddd', label='', alpha=edge_alphas)

        plt.title('Graph Network Visualization', color="#dddddd")
        plt.axis('off')
        plt.show()
