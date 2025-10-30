import hashlib

class Hasher:
    @staticmethod
    def hash_bytes(data: bytes) -> str:
        sha = hashlib.sha256()
        sha.update(data)
        return sha.hexdigest()

    @staticmethod
    def verify_hash(data: bytes, expected_hash: str) -> bool:
        actual_hash = Hasher.hash_bytes(data)
        return actual_hash == expected_hash
