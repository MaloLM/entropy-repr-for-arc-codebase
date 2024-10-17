# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import matplotlib.pyplot as plt
from matplotlib import colors


class Graphics:
    def __init__(self) -> None:
        self.cmap = colors.ListedColormap(
            ['#404040', '#2e67c0', '#af3827', '#4f942e', '#e0c231',
             '#6d6d6d', '#9f3674', '#b76424', '#6d9fb6', '#5f1a23'])
        self.text_color = '#dddddd'
        self.bg_color = '#2b2d31'
        self.fontweight = 'bold'
        self.grid_color = 'white'
        self.grid_linewidth = 0.5
        self.title_size = 10

    def plot_one(self, ax, board, text, pad=15, cmap=None):
        current_cmap = cmap if cmap is not None else self.cmap
        vmax = cmap.N if cmap is not None else 10

        norm = colors.Normalize(vmin=0, vmax=vmax)

        ax.imshow(board, cmap=current_cmap, norm=norm)
        ax.grid(True, which='both', color=self.grid_color,
                linewidth=self.grid_linewidth)

        plt.setp(plt.gcf().get_axes(), xticklabels=[], yticklabels=[])

        ax.set_xticks([x-0.5 for x in range(1 + len(board[0]))])
        ax.set_yticks([x-0.5 for x in range(1 + len(board))])

        ax.set_title(text, color=self.text_color,
                     fontweight=self.fontweight, pad=pad)

    def plot_board(self, text, board):
        fig, axs = plt.subplots(1, 1, figsize=(5, 5))
        plt.suptitle(f'{text}', fontsize=self.title_size,
                     color=self.text_color, fontweight=self.fontweight, y=1)

        self.plot_one(axs, board, 'Board')

        fig.patch.set_linewidth(5)
        fig.patch.set_edgecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)

        plt.tight_layout()
        plt.show()

    def plot_side_to_side_boards(self, board_right, board_left, title,  text_right, text_left, b1_cmap, b2_cmap):
        fig, axs = plt.subplots(1, 2, figsize=(5*2, 4*1))
        plt.suptitle(f'{title}', fontsize=self.title_size,
                     color=self.text_color, fontweight=self.fontweight, y=1)

        self.plot_one(axs[0], board_right, f'{text_right}', cmap=b1_cmap)
        self.plot_one(axs[1], board_left, f'{text_left}', cmap=b2_cmap)

        fig.patch.set_linewidth(5)
        fig.patch.set_edgecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)

        plt.tight_layout()
        plt.show()

    def plot_task(self, text, puzzle_inps, puzzle_outs):
        plot_width = len(puzzle_inps)

        fig, axs = plt.subplots(2, plot_width, figsize=(3*plot_width, 3*2))
        plt.suptitle(f'{text}', fontsize=self.title_size,
                     color=self.text_color, fontweight=self.fontweight, y=1)

        for j in range(plot_width):
            if plot_width > 1:
                x = (0, j)
                y = (1, j)
            else:
                x = 0
                y = 1
            self.plot_one(axs[x], puzzle_inps[j], 'Input')
            self.plot_one(axs[y], puzzle_outs[j], 'Output')

        fig.patch.set_linewidth(5)
        fig.patch.set_edgecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)

        plt.tight_layout()
        plt.show()

    def plot_solution_only(self, text, puzzle_outs):
        plot_width = len(puzzle_outs)

        fig, axs = plt.subplots(1, plot_width, figsize=(5*plot_width, 5*1))
        plt.suptitle(f'{text}', fontsize=self.title_size,
                     color=self.text_color, fontweight=self.fontweight, y=1)

        for j in range(plot_width):
            self.plot_one(axs, puzzle_outs[j], 'Output')

        fig.patch.set_linewidth(5)
        fig.patch.set_edgecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)

        plt.tight_layout()
        plt.show()

    def plot_full_task(self, title, puzzle_inps_train, puzzle_outs_train, puzzle_inps_test, puzzle_outs_test=None):

        num_train = len(puzzle_inps_train)
        num_test = len(puzzle_inps_test)

        w = num_train + num_test
        fig, axs = plt.subplots(2, w, figsize=(3.5*w, 3*2))
        plt.suptitle(f'{title}', fontsize=self.title_size,
                     color=self.text_color, fontweight=self.fontweight, y=1)

        for i in range(num_train):
            self.plot_one(axs[0, i], puzzle_inps_train[i], 'Train input')
            self.plot_one(axs[1, i], puzzle_outs_train[i], 'Train output')

        for j in range(num_train, w):
            index = j-num_train

            self.plot_one(axs[0, j], puzzle_inps_test[index], 'Test input')

            if puzzle_outs_test != None:
                self.plot_one(
                    axs[1, j], puzzle_outs_test[index], 'Test output')
            else:
                axs[1, j].axis('off')

        fig.patch.set_linewidth(10)
        fig.patch.set_edgecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)

        plt.tight_layout()
        plt.show()
