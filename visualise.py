import networkx as nx # pyright: ignore[reportMissingModuleSource]
from crawl import normalize_url
import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]

def build_graph(page_data, base_domain):
    G = nx.DiGraph()

    for normalized_url in page_data:
        G.add_node(normalized_url)

    for normalized_url, data in page_data.items():
        for link in data.get("internal_links", []):
            target = normalize_url(link)
            if target in page_data and target != normalized_url:
                G.add_edge(normalized_url, target)

    return G


def save_graph_image(graph: nx.DiGraph, filename: str = "graph.png") -> None:
    fig, ax = plt.subplots(figsize=(19.2, 10.8))  # 1920x1080 at 100 dpi

    pos = nx.spring_layout(graph, seed=42)

    # Scale node size by number of incoming links
    in_degrees = dict(graph.in_degree())
    node_sizes = [300 + (in_degrees[node] * 200) for node in graph.nodes()]

    # Use page path as label, stripping the domain
    labels = {}
    for node in graph.nodes():
        parts = node.split("/", 1)
        labels[node] = "/" + parts[1] if len(parts) > 1 else "/"

    nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color="steelblue", node_shape="o", alpha=0.8, ax=ax)
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=6, ax=ax)
    nx.draw_networkx_edges(graph, pos, arrows=True, arrowsize=10, edge_color="gray", alpha=0.5, ax=ax)

    ax.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=100, bbox_inches="tight")
    plt.close()
    print(f"Graph saved to {filename}")