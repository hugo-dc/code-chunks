import json
import merkleize
import treeviz

contracts = ['dai', 'lend', 'link', 'mkr', 'omg', 'usdc', 'usdt', 'wbtc', 'yfi']

for contract in contracts:
    with open('bytecodes/' + contract + '.json', 'r') as json_file:
        rpc_result = json.load(json_file)
    bytecode = bytes.fromhex(rpc_result['result'][2:])
    print('Contract: ', contract.upper())
    chunks = merkleize.chunkify(bytecode)
    print('Total chunks: ', len(chunks))
    tree = merkleize.treefy(chunks, len(bytecode))
    print('Total nodes: ', len(tree))
    print('Generating tree...')
    treeviz.show_tree(tree, contract)
    print('./render/'+contract+'.dot.svg')

