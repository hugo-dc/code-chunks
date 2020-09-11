from graphviz import Digraph

def generate_tree(tree):
    dot = Digraph()
    dot.graph_attr['rankdir'] = 'TB'
    dot.format = 'svg'
    subtree = tree[1:]
    
    ix = 0
    iy = 0
    for t in subtree:
        dot.node(str(ix)+'-'+t.hex(), str(ix))
        if iy+1 < len(subtree):
            left = iy+1
            right = iy + 2
            dot.edge(str(ix)+'-'+t.hex(), str(iy+1)+'-' + subtree[iy+1].hex())
            dot.edge(str(ix)+'-'+t.hex(), str(iy+2)+'-' + subtree[iy+2].hex())
            iy +=2
        ix += 1

    root_id = "root-"+tree[0].hex()
    dot.node(root_id, 'root')
    dot.node("B", "metadata")
    dot.edge(root_id, "B")
    dot.edge(root_id, '0-' + subtree[0].hex())
    return dot
