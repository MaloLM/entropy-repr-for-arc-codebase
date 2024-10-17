# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import json
import random


def shuffle_list(input_list):
    random.shuffle(input_list)
    return input_list


def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


arc_agi_colormap = {
    0: '#404040',
    1: '#2e67c0',
    2: '#af3827',
    3: '#4f942e',
    4: '#e0c231',
    5: '#6d6d6d',
    6: '#9f3674',
    7: '#b76424',
    8: '#6d9fb6',
    9: '#5f1a23'
}


def manhattan_distance(xa, ya, xb, yb):
    return abs(xa - xb) + abs(ya - yb)


def calculate_center(points):
    x_coordinates = [point[0] for point in points]
    y_coordinates = [point[1] for point in points]

    center_x = sum(x_coordinates) / len(x_coordinates)
    center_y = sum(y_coordinates) / len(y_coordinates)

    return (center_x, center_y)
