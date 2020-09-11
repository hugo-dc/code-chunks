import hashlib

def sha3_256(data):
    s = hashlib.sha3_256()
    s.update(data)
    return s.digest()
    
def chunkify(program):
    chunks = []
    pos = 0
    this_chunk_start = 0
    this_chunk_code_start = 0
    while pos < len(program):
        pos += (program[pos] - 0x5f) if (0x60 <= program[pos] <= 0x7f) else 1
        if pos >= this_chunk_start + 32:
            hash = sha3_256(
                    program[this_chunk_start:this_chunk_start + 32] +
                    this_chunk_code_start.to_bytes(32, 'big'))
            chunks.append(hash)
            this_chunk_start += 32
            this_chunk_code_start = pos
    return chunks

def next_power_of_2(x):
    return x if x <= 2 else next_power_of_2((x + 1) // 2) * 2

def treefy(chunks, length):
    padded_length = next_power_of_2(len(chunks))
    tree = [None] * padded_length + chunks + [b'\x00'*32] * (padded_length - len(chunks))
    for i in range(padded_length-1, 0, -1):
        tree[i] = sha3_256(tree[i*2] + tree[i*2+1])

    metadata = length.to_bytes(32, 'big')
    hash = sha3_256(tree[1] + metadata)
    tree[0] = hash
    return tree

