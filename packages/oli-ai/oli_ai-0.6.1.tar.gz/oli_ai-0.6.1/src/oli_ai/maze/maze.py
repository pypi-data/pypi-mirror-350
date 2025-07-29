import random
from collections import deque, namedtuple
import matplotlib
from matplotlib import animation
from IPython.display import HTML, display

matplotlib.use('module://ipykernel.pylab.backend_inline')
random.seed(10)
Edge = tuple
Tree = set

def edge(A, B) -> Edge: return Edge(sorted([A, B]))

def random_tree(nodes, neighbors, pop=deque.pop) -> Tree:
    """Repeat: pop a node and add edge(node, nbr) until all nodes have been added to tree."""
    tree = Tree()
    grid = set(nodes)
    nodes = set(nodes)
    root = nodes.pop()
    frontier = deque([root])
    while nodes:
        node = pop(frontier)
        nbrs = neighbors(node) & nodes
        if nbrs:
            nbr = random.choice(list(nbrs))
            tree.add(edge(node, nbr))
            nodes.remove(nbr)
            frontier.extend([node, nbr])
        nbrs = neighbors(node) & nodes
        #elif random.randint(1,10) == 1:
        #    nbr = random.choice(list(neighbors(node)))
        #    if (nbr in grid):
        #       tree.add(edge(node, nbr))
    return tree




Maze = namedtuple('Maze', 'width, height, edges')

Square = tuple

def neighbors4(square) -> {Square}:
    """The 4 neighbors of an (x, y) square."""
    (x, y) = square
    return {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}

def grid(width, height) -> {Square}: 
    """All squares in a grid of these dimensions."""
    return {(x, y) for x in range(width) for y in range(height)}

def random_maze(width, height, pop=deque.pop) -> Maze:
    """Generate a random maze, using random_tree."""
    tree = random_tree(grid(width, height), neighbors4, pop)
    return Maze(width, height, tree)





####


def neighbors4(square) -> {Square}:
    """The 4 neighbors of an (x, y) square."""
    (x, y) = square
    return {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}

def grid(width, height) -> {Square}: 
    """All squares in a grid of these dimensions."""
    return {(x, y) for x in range(width) for y in range(height)}

def random_maze(width, height, pop=deque.pop) -> Maze:
    """Generate a random maze, using random_tree."""
    tree = random_tree(grid(width, height), neighbors4, pop)
    #tree2 = random_tree(grid(width, height), neighbors4, pop)
    return Maze(width, height, tree)








import matplotlib.pyplot as plt

def plot_maze_fig(maze, figsize=None, path=None):
    """Plot a maze by drawing lines between adjacent squares, except for pairs in maze.edges"""
    w, h  = maze.width, maze.height
    fig = plt.figure(figsize=figsize or (w/5, h/5))
    plt.axis('off')
    plt.gca().invert_yaxis()
    exits = {edge((0, 0), (0, -1)), edge((w-1, h-1), (w-1, h)),  edge((w-1, 0), (w, 0)), edge((0, h-1), (0, h))  }
    edges = maze.edges | exits
    for sq in grid(w, h):
        for nbr in neighbors4(sq):
            if edge(sq, nbr) not in edges:
                plot_wall(sq, nbr)
    if path: # Plot the solution (or any path) as a red line through the maze
        X, Y = transpose((x + 0.5, y + 0.5) for (x, y) in path)
        plt.plot(X, Y, 'r-', linewidth=2)
    #plt.close(fig)
    plt.ioff()
    return fig

def plot_maze(maze, path=None, figsize=(5,5)):
    fig = plot_maze_fig(maze, figsize, path)
    plt.show()
        
def transpose(matrix): return list(zip(*matrix))

def plot_wall(s1, s2):
    """Plot a wall: a black line between squares s1 and s2."""
    (x1, y1), (x2, y2) = s1, s2
    if x1 == x2: # horizontal wall
        y = max(y1, y2)
        X, Y = [x1, x1+1], [y, y]
    else: # vertical wall
        x = max(x1, x2)
        X, Y = [x, x], [y1, y1+1]
    plt.plot(X, Y, 'k-', linewidth=2)





def search_(maze, frontier):
    """Find a shortest sequence of states from start to the goal."""
    start = (0, 0)
    goal = {(maze.width - 1, maze.height - 1), (maze.width - 1, 0),(0, maze.height - 1)}
    frontier.put(start)  # A queue of states to consider
    paths = {start: [start]}   # start has a one-square path
    searched = []
    while frontier:
        s = frontier.pop()
        searched.append(paths[s])
        if s in goal:
            return (paths[s], searched)
        for s2 in neighbors4(s):
            if s2 not in paths and edge(s, s2) in maze.edges and s2 not in frontier:
                frontier.put(s2)
                paths[s2] = paths[s] + [s2]


def search_solution(maze, frontier):
    """Find a shortest sequence of states from start to the goal."""
    start = (0, 0)
    goal = {(maze.width - 1, maze.height - 1), (maze.width - 1, 0),(0, maze.height - 1)}
    frontier.put(start)  # A queue of states to consider
    paths = {start: [start]}   # start has a one-square path
    while frontier:
        s = frontier.pop()
        if s in goal:
            return paths[s]
        for snew in neighbors4(s):
            if snew not in paths and edge(s, snew) in maze.edges and snew not in frontier:
                frontier.put(snew)
                paths[snew] = paths[s] + [snew]




def search_animated(maze,frontier, figsize = (5,5)):
    (solution,searched) = search_(maze,frontier)
    
    plt.rcParams["animation.html"] = "jshtml"
    plt.rcParams['figure.dpi'] = 150 
    fig = plot_maze_fig(maze, figsize)

    def drawframe(n):
        X, Y = transpose((x + 0.5, y + 0.5) for (x, y) in searched[n+1])
        plt.plot(X, Y, 'g-', linewidth=2)

    a = matplotlib.animation.FuncAnimation(fig, drawframe, frames=len(searched)-1)
    #plt.close(fig)
    return a



def search_animated_(maze, frontier, figsize=(5, 5)):
    """
    Visualizzazione animata del percorso di ricerca nel labirinto.

    Args:
        maze: Oggetto labirinto.
        frontier: Struttura dati della frontiera di ricerca.
        figsize: Dimensione della figura.

    Returns:
        HTML object che mostra l'animazione in Google Colab.
    """
    (solution, searched) = search_(maze, frontier)

    plt.rcParams["animation.html"] = "jshtml"
    plt.rcParams['figure.dpi'] = 150

    fig = plot_maze_fig(maze, figsize)

    paths = [transpose((x + 0.5, y + 0.5) for (x, y) in searched[i + 1]) for i in range(len(searched) - 1)]


    def drawframe(n):
        X, Y = transpose((x + 0.5, y + 0.5) for (x, y) in searched[n + 1])
        plt.plot(X, Y, 'g-', linewidth=2)

    animation = matplotlib.animation.FuncAnimation(fig, drawframe, frames=len(paths) - 1, blit=True)

    # Visualizzazione inline per Colab
    plt.close(fig)
    display(HTML(animation.to_jshtml()))
    
    return animation
    
#anim = animation.FuncAnimation(fig, drawframe, frames=10, interval=20)
#matplotlib.animation.FuncAnimation(fig, plot_maze_fig, frames=10)
#drawframe(0)

