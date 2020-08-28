import math
from trie import HexaryTrie
import rlp
import hashlib

CHUNK_SIZE = 32
KEY_LENGTH = 4
METADATA_KEY = bytes.fromhex("ffffffff")
METADATA_VERSION = 0
EMPTY_CODE_ROOT = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
HF_BLOCK_NUMBER = None # TBD

bytecode = bytes.fromhex("00600000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000000")

def get_chunks(bc):
    print('bytecode: ', bc)
    chunks = []

    while len(bc) >= CHUNK_SIZE:
        startOffset = 0
        firstInstructionOffset = 0
        codeChunk = bc[:CHUNK_SIZE]
        chunks.append({'startOffset': startOffset,
                       'firstInstructionOffset': firstInstructionOffset,
                       'codeChunk': codeChunk})
        bc = bc[CHUNK_SIZE:]

    return chunks

def get_immediates(opcode):
    if opcode == bytes.fromhex("60"):
        return 1
    else:
        return 0


def second_pass(chunks): # TODO: Use a better name
    # Scan for instructions with immediates or multi-byte instructions (PUSHN)
    pc = 0
    n = 0
    chunkIdx = 0

    print('chunks: ', chunks)

    for i in range(len(bytecode)):
        pc = i
        print('pc: ', pc)
        opcode = bytecode[pc:pc+1]
        print('opcode: 0x'+opcode.hex())
        n = get_immediates(opcode)
        print('pc + n % CHUNK_SIZE : ', pc + n % CHUNK_SIZE)
        print('pc % CHUNK_SIZE: ', pc % CHUNK_SIZE)
        if ((pc + n) % CHUNK_SIZE) >= (pc % CHUNK_SIZE): # instructions does not cross chunk boundarie
            continue
        else: # compte the index of the chunk after the current instruction:
            chunkIdx = math.floor((pc + n + 1) / CHUNK_SIZE)
            print('chunkIdx: ', chunkIdx)
            print('chunkCount: ', chunkCount)
            if chunkIdx + 1 > chunkCount: #malformed bytecode, or "data section"
                print('breaking...')
                break
            else:
                nextChunk = chunks[chunkIdx]
                print('nextChunk: ', nextChunk)
                nextChunk['firstInstructionOffset'] = (pc + n + 1) - nextChunk['startOffset']
                print('nextChunk: ', nextChunk)
    return(chunks)

def format_key(value):
    byte_array = bytes([value])
    while len(byte_array) < KEY_LENGTH:
        byte_array = bytes.fromhex('00') + byte_array
    return byte_array

def merkleize(chunks): # TODO: Compute codeTrie root according to EIP-2584
    trie = HexaryTrie(db={})
    
    # Process each chunk
    for c in chunks:
        key = format_key(c['startOffset'])
        value = rlp.encode([c['firstInstructionOffset'], c['codeChunk']])

        # insert into codeTrie
        trie.set(key, value)

        # Insert metadata leaf
        s = hashlib.sha3_256()
        s.update(c['codeChunk'])
        codeHash = s.digest()
        codeLength = len(c['codeChunk'])
    
        key = METADATA_KEY
        value = rlp.encode([METADATA_VERSION, codeHash, codeLength])
        trie.set(key, value)

    return trie
    

    
# Divide the bytecode evenly in CHUNK_SIZE parts.
chunks = get_chunks(bytecode)
chunkCount = len(chunks)
chunks = second_pass(chunks)
mpt = merkleize(chunks)

print('mpt: 0x'+ mpt.root_hash.hex())
