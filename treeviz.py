from graphviz import Digraph

def show_tree(tree, title='Tree'):
    dot = Digraph()
    dot.graph_attr['rankdir'] = 'TB'
    dot.format = 'png'
    subtree = tree[1:]
    
    ix = 0
    iy = 0


    for t in subtree:
        dot.node(str(ix), t.hex())
        if iy+1 < len(subtree):
            left = iy+1
            right = iy + 2
            dot.edge(str(ix), str(iy+1))
            dot.edge(str(ix), str(iy+2))
            iy +=2
        ix += 1

    dot.node("A", tree[0].hex())
    dot.node("B", "metadata")
    dot.edges(["AB"])
    dot.edges(["A0"])
    dot.render('render/' + title + '.dot', view=False)
    return dot

        
    
