import random
from typing import List

TRINARY_CHARS: List[str] = [str(i) for i in range(3)]
LETTERS: str = 'abcdefghijklmnopqrstuvwxyz'

def encode_bytes(data: bytes) -> str:
    result: List[str] = []
    for b in data:
        bits: List[str] = []
        val = b
        for _ in range(6):
            bits.append(str(val % 3))
            val //= 3
        bits.reverse()
        bits_str = ''.join(bits)
        rand_digits = ''.join(random.choice('0123456789') for _ in range(2))
        rand_letter = random.choice(LETTERS)
        result.append(f"{bits_str} {rand_digits}{rand_letter}")
    return ' '.join(result)

def decode_bytes(encoded: str) -> bytes:
    parts: List[str] = encoded.split()
    if len(parts) % 2 != 0:
        raise ValueError("Invalid encoded format")
    decoded_bytes = bytearray()
    for i in range(0, len(parts), 2):
        trinary_str = parts[i]
        rand_part = parts[i + 1]
        if len(trinary_str) != 6 or len(rand_part) != 3:
            raise ValueError("Invalid encoded format")
        val = 0
        for c in trinary_str:
            if c not in TRINARY_CHARS:
                raise ValueError("Invalid trinary character")
            val = val * 3 + int(c)
        decoded_bytes.append(val)
    return bytes(decoded_bytes)
