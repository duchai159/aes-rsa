import base64, hashlib, math

def egcd(a, b):
    """extend euclidean algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
def gcd(a, b):
    """Greatest Common divisor"""
    while a != 0:
      a, b = b % a, a
    return b

def is_coprime(x, y):
        """Return if x is coprime with y"""
        return gcd(x, y) == 1

def find_mod_inverse(a, m):
    """Return mod inverse multiplicative"""
    # obs.: im using pow(a,b,c) instead.
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m

def os2ip(x):
    """
        Octet String to Integer positive
    """
    return int.from_bytes(x, byteorder='big')

def i2osp(x: int, sLen: int):
    """
        Integer-to-Octet-String
        Throw errors: integer too large
    """
    return x.to_bytes(sLen, byteorder='big')

def xor(x: bytes, y: bytes) -> bytes:
    """
        XOR 2 mảng bytes
    """
    return bytes(a ^ b for a, b in zip(x, y))

def tobytes(s, encoding="latin-1"):
        """Transform instances of data types to bytes"""
        if isinstance(s, bytes):
            return s
        elif isinstance(s, bytearray):
            return bytes(s)
        elif isinstance(s,str):
            return s.encode(encoding)
        elif isinstance(s, memoryview):
            return s.tobytes()
        else:
            return bytes([s])

def BASE64Encode(data, key_type):
    """generate string for key exportion with base64"""
    out = "-----BEGIN " + key_type + "-----\n "
    out += toBase64(str(data))+ "\n"
    out += "-----END "+ key_type + "-----" 
    return out

def BASE64Decoding(data, key_type):
    """generate string of pairs from key exportion"""
    data = data.split("\n")
    data = data[1:-1][0]
    return fromBase64(data)

def totuple(text):
    """Convert text into Tuple
        Ex.: "(1,2)" -> (1,2)
    """
    #  remove ( and ):
    text = text[1:-1]
    text = text.split(",")
    return (int(text[0]), int(text[1]))

    
def toBase64(string):
    """Encode String to base64"""
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def fromBase64(string):
    """Decode string from base64 to  normal string"""
    base64_bytes = string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string

def sha256(m):
    """Hasher for our OAEP and Signing function"""
    hasher = hashlib.sha1()
    hasher.update(m)
    return hasher.digest()

def mgf1(seed, emLen, hash=hashlib.sha256):
    """
        MGF1 is a Mask Generation Function based on a hash function.

        Inputs  1. Z - seed from which mask is generated, an octet string
                2. emLen -  intended length in octets of the mask, at most 2^32(hLen)
                Output:
                    1. mask -  an octet string of length l; or "mask too long"
    """
    #    Steps:
    # 1  If emLen > 2^{32}*hLen, output mask too long and stop
    hLen = hash().digest_size
    if emLen > pow(2,32) * hLen:
        raise ValueError("mask too long")

    # 2. Let T be the empty octet string
    T = b""
    # 3. For i = 0 to ceiling(emLen/hLen), do
        # 3.1 Convert i to an octet string C of length 4 with the primitive I2OSP:
        # C = I2OSP(i, 4).
        # 3.2 Concatenate the hash of the seed Z and C to the octet string T:
        # T = T + Hash(Z + C)
    for i in range(math.ceil(emLen / hLen)):
        c = i2osp(i, 4)
        hash().update(seed + c)
        T = T + hash().digest()
    assert(len(T) >= emLen)
    #4. Output the leading l octets of T as the octet string mask.
    return T[:emLen]
