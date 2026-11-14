"""Download source datasets and record checksums in data/manifest.csv."""
import hashlib
from pathlib import Path

def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()

def fetch(url: str, dest: Path) -> Path:
    """TODO (Shela): stream download with retry; write checksum and access date to manifest."""
    raise NotImplementedError("download not implemented yet")
