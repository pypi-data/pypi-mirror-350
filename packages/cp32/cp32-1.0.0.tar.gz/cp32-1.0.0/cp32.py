class e32BitCipher:
    def __init__(self, key: int = 0x1AC32B4D):
        self.key = key & 0xFFFFFFFF

    def encrypt(self, s: str) -> str:
        data = s.encode('utf-8')
        result = 0
        for i, b in enumerate(data):
            key_byte = (self.key >> (8 * (i % 4))) & 0xFF
            result ^= (b ^ key_byte) << (8 * (i % 4))
        return f"{result:08x}"

    def decrypt(self, hex_str: str) -> str:
        value = int(hex_str, 16)
        bytes_out = []
        for i in range(4):
            key_byte = (self.key >> (8 * i)) & 0xFF
            b = ((value >> (8 * i)) & 0xFF) ^ key_byte
            if b == 0:
                break
            bytes_out.append(b)
        return bytes(bytes_out).decode('utf-8')