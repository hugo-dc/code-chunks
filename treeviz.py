from graphviz import Digraph

def show_tree(tree):
    dot = Digraph()
    subtree = tree[1:]
    
    main_tree = []

    ix = 0
    parent = None
    left = None
    right = None

    toggle = True

    for t in subtree:
        dot.node(str(ix), t.hex())
        if parent is None:
            parent = (str(ix), t.hex())
        elif left is None:
            left = (str(ix), t.hex())
            dot.edges([parent[0]+left[0]])
        elif right is None:
            right = (str(ix), t.hex())
            dot.edges([parent[0]+right[0]])
            if toggle:
                parent = left
                toggle = True
            else:
                parent = right
                toggle = False
                
            left = None
            right = None

        ix += 1
    dot.node("A", tree[0].hex())
    dot.node("B", "metadata")
    dot.edges(["AB"])
    dot.edges(["A0"])
    return dot

        
    
