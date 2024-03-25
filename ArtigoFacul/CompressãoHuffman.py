import heapq
from collections import defaultdict, Counter
import bitarray

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_huffman_codes(node, prefix="", codes={}):
    if node is not None:
        if node.char is not None:
            codes[node.char] = prefix
        build_huffman_codes(node.left, prefix + "0", codes)
        build_huffman_codes(node.right, prefix + "1", codes)

def compress(text, codes):
    compressed = bitarray.bitarray()
    for char in text:
        compressed.extend(bitarray.bitarray(codes[char]))
    return compressed

def decompress(compressed, root):
    decompressed = []
    current_node = root
    for bit in compressed:
        if bit == 0:
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decompressed.append(current_node.char)
            current_node = root

    return ''.join(decompressed)

def huffman_compress(text):
    root = build_huffman_tree(text)
    codes = {}
    build_huffman_codes(root, codes=codes)
    compressed = compress(text, codes)
    return compressed, root

def huffman_decompress(compressed, root):
    return decompress(compressed, root)

# Exemplo de uso
if __name__ == "__main__":
    # Texto de exemplo
    text = "this is an example for huffman encoding"

    # Comprimir o texto usando o algoritmo de Huffman
    compressed, tree = huffman_compress(text)

    # Descomprimir o texto comprimido
    decompressed = huffman_decompress(compressed, tree)

    print("Texto original:", text)
    print("Texto comprimido:", compressed)
    print("Texto descomprimido:", decompressed)
