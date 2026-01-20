import argparse
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


def is_url(value: str | Path) -> bool:
    parsed = urlparse(str(value))
    return parsed.scheme in {"https"}


def open_log_source(log_source: str | Path):
    """Yield lines from a local file or HTTP(S) URL."""
    if is_url(log_source):
        response = urlopen(str(log_source))
        try:
            for raw in response:
                yield raw.decode("utf-8", errors="ignore")
        finally:
            response.close()
    else:
        with Path(log_source).open("r", encoding="utf-8") as file_handle:
            for raw in file_handle:
                yield raw


class HyperLogLog:
    """HyperLogLog algorithm for approximate cardinality estimation."""

    def __init__(self, precision: int = 5):
        """
        Initialize HyperLogLog with given precision.

        Args:
            precision: Number of bits to use for bucket indexing (4-16).
                      Higher precision = more accuracy but more memory.
                      Default 5 gives ~32 buckets with ~26.3% standard error.
        """
        if not 4 <= precision <= 16:
            raise ValueError("Precision must be between 4 and 16")

        self.precision = precision
        # 2^precision buckets
        self.m = 1 << precision
        self.registers = [0] * self.m

        # Alpha constant for bias correction
        if self.m >= 128:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)
        elif self.m >= 64:
            self.alpha = 0.709
        elif self.m >= 32:
            self.alpha = 0.697
        elif self.m >= 16:
            self.alpha = 0.673
        else:
            self.alpha = 0.5

    def add(self, item: str) -> None:
        """Add an item to the HyperLogLog."""
        # Hash the item using SHA-256
        hash_value = int(hashlib.sha256(item.encode()).hexdigest(), 16)

        # Use first 'precision' bits for bucket index
        bucket_index = hash_value & (self.m - 1)

        # Use remaining bits to find leading zeros
        remaining_bits = hash_value >> self.precision
        leading_zeros = self._count_leading_zeros(remaining_bits) + 1

        # Update register with maximum leading zeros count
        self.registers[bucket_index] = max(self.registers[bucket_index], leading_zeros)

    def _count_leading_zeros(self, bits: int) -> int:
        """Count the number of leading zero bits."""
        if bits == 0:
            return 64 - self.precision  # Maximum possible

        count = 0
        # Check each bit from left to right
        for i in range(64 - self.precision - 1, -1, -1):
            if bits & (1 << i):
                break
            count += 1
        return count

    def count(self) -> int:
        """Estimate the cardinality."""
        # Calculate raw estimate
        raw_estimate = self.alpha * (self.m**2) / sum(2 ** (-x) for x in self.registers)

        # Apply bias correction for small and large ranges
        if raw_estimate <= 2.5 * self.m:
            # Small range correction
            zeros = self.registers.count(0)
            if zeros != 0:
                return int(self.m * math.log(self.m / zeros))

        if raw_estimate <= (1 / 30) * (1 << 32):
            # No correction
            return int(raw_estimate)
        else:
            # Large range correction
            return int(-1 * (1 << 32) * math.log(1 - raw_estimate / (1 << 32)))


def count_unique_ips_set(log_path: str | Path) -> int:
    """Count unique IP addresses in a JSON-lines access log using a set."""
    unique_ips: set[str] = set()

    for line_number, raw_line in enumerate(open_log_source(log_path), start=1):
        line = raw_line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        ip = record.get("remote_addr")
        if isinstance(ip, str):
            stripped_ip = ip.strip()
            if stripped_ip:
                unique_ips.add(stripped_ip)

    return len(unique_ips)


def count_unique_ips_hyperloglog(log_path: str | Path, precision: int = 14) -> int:
    """Count unique IP addresses using HyperLogLog approximate algorithm."""
    hll = HyperLogLog(precision=precision)

    for line_number, raw_line in enumerate(open_log_source(log_path), start=1):
        line = raw_line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        ip = record.get("remote_addr")
        if isinstance(ip, str):
            stripped_ip = ip.strip()
            if stripped_ip:
                hll.add(stripped_ip)

    return hll.count()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count unique IP addresses using set and HyperLogLog."
    )
    parser.add_argument(
        "log_file_or_url",
        type=str,
        help="Path or URL to the JSON-lines access log file.",
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=["set", "hyperloglog", "both"],
        default="both",
        help="Method to use for counting: 'set' (exact), 'hyperloglog' (approximate), or 'both' (default).",
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=5,
        help="HyperLogLog precision (4-16). Default: 5. Higher = more accuracy but more memory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not is_url(args.log_file_or_url):
        print("Reading log from local file...")
        path = Path(args.log_file_or_url)
        if not path.is_file():
            raise FileNotFoundError(f"Log file not found: {args.log_file_or_url}")
        log_source: str | Path = path
    else:
        print("Reading log from URL...")
        log_source = args.log_file_or_url

    print()

    exact_count = None
    if args.method in ["set", "both"]:
        print("=" * 50)
        print("Exact counting using set:")
        print("=" * 50)
        exact_count = count_unique_ips_set(log_source)
        print(f"Unique IP addresses (exact): {exact_count}")
        print()

    if args.method in ["hyperloglog", "both"]:
        print("=" * 50)
        print(f"Approximate counting using HyperLogLog (precision={args.precision}):")
        print("=" * 50)
        approximate_count = count_unique_ips_hyperloglog(
            log_source, precision=args.precision
        )
        print(f"Unique IP addresses (HyperLogLog): {approximate_count}")

        if args.method == "both" and exact_count is not None:
            error = abs(exact_count - approximate_count)
            error_rate = (error / exact_count * 100) if exact_count > 0 else 0
            print()
            print("=" * 50)
            print("Comparison:")
            print("=" * 50)
            print(f"Exact count:        {exact_count}")
            print(f"HyperLogLog count:  {approximate_count}")
            print(f"Absolute error:     {error}")
            print(f"Error rate:         {error_rate:.2f}%")

            # Memory estimation
            # Set: each IP is roughly 15 bytes (average IPv4 string) + overhead
            set_memory = exact_count * 64  # Rough estimate with Python overhead
            # HyperLogLog: precision determines number of registers
            hll_memory = (1 << args.precision) * 1  # 1 byte per register
            memory_ratio = set_memory / hll_memory if hll_memory > 0 else 0

            print()
            print("Memory usage (estimated):")
            print(f"Set:                ~{set_memory:,} bytes")
            print(f"HyperLogLog:        ~{hll_memory:,} bytes")
            print(f"Memory reduction:   {memory_ratio:.1f}x")
        print()


if __name__ == "__main__":
    main()
