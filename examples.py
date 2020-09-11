import json
import merkleize
import treeviz

contracts = ['bat', 'link', 'mkr', 'omg', 'usdc', 'dai', 'lend', 'wbtc', 'yfi', 'usdt']

for contract in contracts:
    with open('bytecodes/' + contract + '.json', 'r') as json_file:
        rpc_result = json.load(json_file)
    bytecode = bytes.fromhex(rpc_result['result'][2:])
    print('Contract: ', contract.upper())
    chunks = merkleize.chunkify(bytecode)
    print('Total chunks: ', len(chunks))
    total_leafs = merkleize.next_power_of_2(len(chunks))
    print('Total leafs: ', total_leafs)
    tree = merkleize.treefy(chunks, len(bytecode))
    print('Total nodes: ', len(tree))
    print('Generating tree...')
    tviz = treeviz.generate_tree(tree)
    tviz.render('render/'+contract+'.dot', view=False)
    print('./render/'+contract+'.dot.svg')

