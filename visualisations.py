import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation

def update(num, edges, line_objects, positions, colors, box_plot_axis, G):
    """
    Update the network graph and the box plot.
    """
    # Reset and update the box plot
    box_plot_axis.clear()
    box_plot_data = create_box_plot_data(edges[:num+1], 25)
    box_plot_axis.boxplot([[v['low'], v['high'], v['low'], v['high']] for v in box_plot_data.values()], patch_artist=True)
    box_plot_axis.set_xticklabels(box_plot_data.keys(), rotation=45, ha='right')
    box_plot_axis.set_title('Box Plot of Low and High Values')
    box_plot_axis.set_xlabel('Students')
    box_plot_axis.set_ylabel('Ranking')
    
    # Reset and update network graph
    G.clear()
    G.add_nodes_from(positions.keys())
    G.add_edges_from(edges[:num+1])
    for i in range(num+1):
        start_pos = positions[edges[i][0]]
        end_pos = positions[edges[i][1]]
        line_objects[i].set_data([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]])
        line_objects[i].set_color(colors[i])

    return tuple(line_objects),


def draw_graph(ranker):
    """
    Draw the network graph and box plot using the ranker object.
    """
    fig = plt.figure()

    graph_axis = fig.add_subplot(121)
    box_plot_axis = fig.add_subplot(122)
    
    # Create node list
    nodes = ranker.students
    
    # Create edge (link) and color lists
    edges = [(rated_pair.higher, rated_pair.lower) for rated_pair in sorted(ranker.data, key=lambda x: x.number)]
    colors = ['blue' if rated_pair.reviewed else 'green' for rated_pair in sorted(ranker.data, key=lambda x: x.number)]
    
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
    ani = FuncAnimation(fig, update, frames=len(edges), fargs=(edges, line_objects, positions, colors, box_plot_axis, G), interval=100, blit=False)
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
