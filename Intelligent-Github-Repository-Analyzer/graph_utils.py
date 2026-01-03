"""
Graph Utilities Module
Provides functions for graph serialization and deserialization.
"""

import networkx as nx
import streamlit as st


def serialize_graph_data(G):
    """Convert NetworkX graph to serializable format for session state storage"""
    if len(G.nodes()) == 0:
        return None
    
    try:
        # Convert graph to simple data structure
        graph_data = {
            'nodes': [],
            'edges': []
        }
        
        # Store node data
        for node in G.nodes():
            node_data = G.nodes[node] if hasattr(G.nodes[node], 'get') else {}
            graph_data['nodes'].append({
                'id': node,
                'data': dict(node_data)  # Convert to regular dict
            })
        
        # Store edge data
        for edge in G.edges():
            graph_data['edges'].append({
                'source': edge[0],
                'target': edge[1]
            })
        
        return graph_data
    except Exception as e:
        st.warning(f"⚠️ **Graph Serialization Issue**: Could not serialize architecture data - {str(e)}")
        return None


def deserialize_graph_data(graph_data):
    """Convert serialized graph data back to NetworkX graph"""
    if not graph_data:
        return nx.DiGraph()
    
    try:
        G = nx.DiGraph()
        
        # Add nodes with data
        for node_info in graph_data['nodes']:
            G.add_node(node_info['id'], **node_info['data'])
        
        # Add edges
        for edge_info in graph_data['edges']:
            G.add_edge(edge_info['source'], edge_info['target'])
        
        return G
    except Exception as e:
        st.warning(f"⚠️ **Graph Deserialization Issue**: Could not restore architecture data - {str(e)}")
        return nx.DiGraph()
