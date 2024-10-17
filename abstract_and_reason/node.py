# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from abstract_and_reason.assets import calculate_center


class Node:
    def __init__(self, value, x, y) -> None:
        """
        Initializes a Node instance.

        Parameters:
        - value: The value associated with the node.
        - x (int): The x-coordinate of the node in the grid.
        - y (int): The y-coordinate of the node in the grid.
        """
        self.value = value
        self.coords = [(x, y)]
        self.connections = []
        self.conn_dists = []
        self.entropies = []
        self.norm_entropies = []

    def get_node_center(self):
        """
        Calculates and returns the center of the node based on its coordinates.

        Returns:
        - tuple: The center coordinates of the node as a tuple (x, y).
        """
        coords = []
        for coord in self.coords:
            coords.append((coord[0], coord[1]))

        return calculate_center(coords)

    def add_connection(self, other_node):
        """
        Adds a connection to another node if it is not already connected.

        Parameters:
        - other_node (Node): The node to connect to this node.
        """
        if other_node not in self.connections:
            self.connections.append(other_node)

    def __hash__(self):
        """
        Returns the hash value of the node based on its value and coordinates.

        Returns:
        - int: The hash value of the node.
        """
        return hash((self.value, tuple(self.coords)))

    def __eq__(self, other):
        """
        Checks if two nodes are equal based on their value and coordinates.

        Parameters:
        - other: The other node to compare with.

        Returns:
        - bool: True if the nodes are equal, False otherwise.
        """
        if isinstance(other, Node):
            return self.value == other.value and self.coords == other.coords
        return False

    def __str__(self) -> str:
        """
        Returns a string representation of the node, including its coordinates and value.

        Returns:
        - str: The string representation of the node.
        """
        coords_str = ";".join([f"({x},{y})" for x, y in self.coords])
        return f"Coords=[{coords_str}], Value={self.value}"
