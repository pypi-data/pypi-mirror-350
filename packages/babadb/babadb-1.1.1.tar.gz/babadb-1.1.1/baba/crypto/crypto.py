import hashlib
import base64

def ternary_to_bytes(ternary_str: str) -> bytes:
    mapping = {'0': 0, '1': 1, '2': 2}
    values = [mapping[c] for c in ternary_str]
    result = 0
    for v in values:
        result = result * 3 + v
    length = (len(ternary_str) * 2 + 7) // 8
    return result.to_bytes(length, 'big')

def hash_and_encode(data: str) -> str:
    b = ternary_to_bytes(data)
    h = hashlib.sha256(b).digest()
    return base64.b64encode(h).decode('ascii')
