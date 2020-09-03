import hashlib

def generate_code_root(program):
    tree = treefy(chunkify(program), len(program))
    return tree[0]

def chunkify(program):
    chunks = []
    pos = 0
    this_chunk_start = 0
    this_chunk_code_start = 0
    while pos < len(program):
        pos += (program[pos] - 0x5f) if (0x60 <= program[pos] <= 0x7f) else 1
        if pos >= this_chunk_start + 32:
            s = hashlib.sha3_256()
            s.update(program[this_chunk_start:this_chunk_start + 32] + this_chunk_code_start.to_bytes(32, 'big'))
            digest = s.digest()
            s = hashlib.sha3_256()
            s.update(program[this_chunk_start:this_chunk_start + 32] + this_chunk_code_start.to_bytes(32, 'big'))
            digest = s.digest()
            chunks.append(digest)
            this_chunk_start += 32
            this_chunk_code_start = pos
    return chunks

def next_power_of_2(x):
    return x if x <= 2 else next_power_of_2((x + 1) // 2) * 2

def treefy(chunks, length):
    padded_length = next_power_of_2(len(chunks))
    tree = [None] * padded_length + chunks + [b'\x00'*32] * (padded_length - len(chunks))
    for i in range(padded_length-1, 0, -1):
        s = hashlib.sha3_256()
        s.update(tree[i*2] + tree[i*2+1])
        digest=s.digest()
        tree[i] = digest
    metadata = length.to_bytes(32, 'big')
    s = hashlib.sha3_256()
    s.update(tree[1] + metadata)
    digest = s.digest()
    tree[0] = digest
    return tree

