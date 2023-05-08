import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation
import time
import random
import os
import platform

def update(num, edges, line_objects, positions, colors, box_plot_axis, G, blue_edge_counter):
    """
    Update the network graph and the box plot.
    """
    # Reset and update the box plot
    box_plot_axis.clear()
    box_plot_data = create_box_plot_data(edges[:num+1], 50)
    
    # Sort the box plot data based on the midline position
    sorted_box_plot_data = sorted(box_plot_data.items(), key=lambda x: (x[1]['low'] + x[1]['high']) / 2)

    # Update the box plot with the sorted data
    box_plot_axis.boxplot([[v['low'], v['high'], v['low'], v['high']] for _, v in sorted_box_plot_data], patch_artist=True, widths=0.75)
    box_plot_axis.set_xticklabels([k for k, _ in sorted_box_plot_data], rotation=90, ha='right')
    box_plot_axis.set_title('Object Rankings')
    box_plot_axis.set_xlabel('Objects')
    box_plot_axis.set_ylabel('Relative Rank')
    
    # Reset and update network graph
    G.clear()
    G.add_nodes_from(positions.keys())
    G.add_edges_from(edges[:num+1])
    
    for i in range(num+1):
        start_pos = positions[edges[i][0]]
        end_pos = positions[edges[i][1]]
        line_objects[i].set_data([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]])
        line_objects[i].set_color(colors[i])
        
    for i, line in enumerate(line_objects):
        if colors[i] == 'blue':
            line.set_linewidth(2)
        elif colors[i] == 'green':
            line.set_linewidth(1)
            line.set_alpha(0.5)
            
    # Update the blue_edge_counter text
    blue_edge_counter.set_text(f'Input Comparisons: {sum(1 for color in colors[:num+1] if color == "blue")}')

    return tuple(line_objects),

def draw_graph(ranker):
    """
    Draw the network graph and box plot using the ranker object.
    """
    fig = plt.figure()

    graph_axis = fig.add_subplot(121)
    box_plot_axis = fig.add_subplot(122)
    
    # Create node list
    nodes = ranker.comparison_objects
    
    # Create edge (link) and color lists
    edges = [(rated_pair.higher, rated_pair.lower) for rated_pair in sorted(ranker.comparisons.values(), key=lambda x: x.n)]
    colors = ['blue' if not rated_pair.link else 'green' for rated_pair in sorted(ranker.comparisons.values(), key=lambda x: x.n)]
    
    # Create node positions dict, places nodes on a circle
    num_nodes = len(nodes)
    radius = 200
    center_x, center_y = 0, 0
    positions = {student: (center_x + radius * np.cos(i * 2 * np.pi / num_nodes), center_y + radius * np.sin(i * 2 * np.pi / num_nodes)) for i, student in enumerate(nodes)}
    
    # Create a graph
    G = nx.Graph()
    G.add_nodes_from(nodes)
    graph_axis.set_frame_on(False)  # Remove the border around the plot
    nx.draw_networkx_nodes(G, positions, node_color='lightblue', node_size=250, ax=graph_axis)
    nx.draw_networkx_labels(G, positions, font_weight='bold', ax=graph_axis)
    graph_axis.set_aspect('equal')
    line_objects = [graph_axis.plot([], [], color='black', linewidth=1)[0] for _ in range(len(edges))]
    
    # Add a text object for displaying the blue edge count
    blue_edge_count = sum(1 for color in colors if color == 'blue')
    blue_edge_counter = graph_axis.text(0.05, 0.95, f'Blue edges: {blue_edge_count}', transform=graph_axis.transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ani = FuncAnimation(fig, update, frames=len(edges), fargs=(edges, line_objects, positions, colors, box_plot_axis, G, blue_edge_counter), interval=0.1, blit=False)
    fig.set_size_inches(16, 8)

    # Set the axis limits to fit the entire graph
    graph_axis.set_xlim(min(x for x, y in positions.values()) - 50, max(x for x, y in positions.values()) + 50)
    graph_axis.set_ylim(min(y for x, y in positions.values()) - 50, max(y for x, y in positions.values()) + 50)

    # Show
    plt.show()

def create_box_plot_data(edges, num_students):

    box_plot_data = {i: {'low': 0, 'high': num_students} for i in range(num_students)}
    
    for edge in edges:
        box_plot_data[edge[0]]['high'] -= 1
        box_plot_data[edge[1]]['low'] += 1
        
    return box_plot_data

def print_ranking(ranking):
        
    def clear_terminal():
        if platform.system().lower() == "windows":
            os.system('cls')
        else:
            os.system('clear') 
        
    clear_terminal()
    print('<-- Lower Ranked Objects | Higher Ranked Objects -->\n')
    
    for comparion_object, relative_ranking in ranking.items():
        line = []
        
        lower_bottom = [item for item in relative_ranking['lower'] if item[1] > 0.5]
        lower_top = [item for item in relative_ranking['lower'] if item[1] <= 0.5]
        
        higher_bottom = [item for item in relative_ranking['higher'] if item[1] > 0.5]
        higher_top = [item for item in relative_ranking['higher'] if item[1] <= 0.5]
        
        line.append(ConsoleColor.RED)
        for _ in range(len(lower_bottom)):
            line.append('-')
        line.append(ConsoleColor.RESET)
        
        line.append(ConsoleColor.ORANGE)
        for _ in range(len(lower_top)):
            line.append('=')
        line.append(ConsoleColor.RESET)
        
        line.append(ConsoleColor.GREEN)
        for _ in range(((len(ranking.keys()) - len(relative_ranking['higher'])) - len(relative_ranking['lower'])) + 2):
            line.append('#')
        line.append(ConsoleColor.RESET)
        
        line.append(ConsoleColor.ORANGE)
        for _ in range(len(higher_top)):
            line.append('=')
        line.append(ConsoleColor.RESET)
        
        line.append(ConsoleColor.RED)
        for _ in range(len(higher_bottom)):
            line.append('-')
        line.append(ConsoleColor.RESET)
        
        gap = ''
        if comparion_object < 10:
            gap = ' '
            
        print(f'{comparion_object} {gap}: {"".join(line)}')  

class ConsoleColor:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;214m'
    RESET = '\033[0m'  