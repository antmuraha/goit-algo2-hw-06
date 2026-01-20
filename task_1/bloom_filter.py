import hashlib


class BloomFilter:
    """Simple Bloom filter implementation."""

    def __init__(self, size: int, num_hashes: int):
        """
        Initialize the Bloom filter with a given size and number of hash functions.
        """
        if size <= 0 or num_hashes <= 0:
            raise ValueError("size and num_hashes must be positive")
        self.size = size
        self.num_hashes = num_hashes
        # Use bytearray for memory efficiency (8 bits per byte)
        self.bit_array = bytearray((size + 7) // 8)

    def _hashes(self, item: str) -> list[int]:
        """Generate deterministic hash values using SHA256."""
        hashes = []
        for i in range(self.num_hashes):
            h = hashlib.sha256(f"{item}{i}".encode()).hexdigest()
            hashes.append(int(h, 16) % self.size)
        return hashes

    def _set_bit(self, index: int) -> None:
        # Set the bit at 'index' to 1
        self.bit_array[index // 8] |= 1 << (index % 8)

    def _get_bit(self, index: int) -> bool:
        # Check if the bit at 'index' is set
        return bool(self.bit_array[index // 8] & (1 << (index % 8)))

    def add(self, item: str) -> None:
        """Add an item to the Bloom filter."""
        for hash_value in self._hashes(item):
            self._set_bit(hash_value)

    def check(self, item: str) -> bool:
        """Check if an item might be in the Bloom filter."""
        return all(self._get_bit(h) for h in self._hashes(item))

    def _count_bits_set(self) -> int:
        """Count the number of bits set to 1."""
        count = 0
        for byte in self.bit_array:
            count += bin(byte).count("1")
        return count

    def _false_positive_rate(self, n: int) -> float:
        """Calculate false positive rate for n elements."""
        if n == 0:
            return 0.0
        # Formula: (1 - e^(-k*n/m))^k
        import math

        k = self.num_hashes
        m = self.size
        return (1 - math.exp(-k * n / m)) ** k

    def __repr__(self) -> str:
        bits_set = self._count_bits_set()
        bloom_length = len(self.bit_array)
        # Estimate elements added based on bits set
        import math

        if bits_set == 0:
            estimated_added = 0
        elif bits_set >= self.size:
            estimated_added = self.size
        else:
            estimated_added = int(
                -self.size / self.num_hashes * math.log(1 - bits_set / self.size)
            )

        current_fpr = self._false_positive_rate(estimated_added)

        return (
            f"BloomFilter:\n"
            f"\tbits: {self.size}\n"
            f"\tnumber hashes: {self.num_hashes}\n"
            f"\tbloom length (8 bits): {bloom_length}\n"
            f"\tnumber bits set: {bits_set}\n"
            f"\testimated elements added: {estimated_added}\n"
            f"\tcurrent false positive rate: {current_fpr:.6f}"
        )
